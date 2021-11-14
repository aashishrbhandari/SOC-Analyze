from flask import Flask
from flask import request

from dns.asyncresolver import Resolver
import dns.resolver as dns_resolver
import dns.rrset
import dns.exception as dns_exception
import asyncio
from typing import Tuple
import ipaddress

import re

USE_TCP = False

USE_DNSSERVERS = ['1.1.1.1']

# Slow DNS BL Services Removed from Blacklist Service List
blacklist_services = [
    "dnsbl.sorbs.net",
    "misc.dnsbl.sorbs.net",
    "smtp.dnsbl.sorbs.net",
    "socks.dnsbl.sorbs.net",
    "spam.dnsbl.sorbs.net",
    "web.dnsbl.sorbs.net",
    "zombie.dnsbl.sorbs.net",
    "dul.dnsbl.sorbs.net",
    "http.dnsbl.sorbs.net",
    "noptr.spamrats.com"
]

blacklist_services += [
    "b.barracudacentral.org",
    "bl.spamcop.net",
    "blacklist.woody.ch",
    "cbl.abuseat.org",
    "combined.abuse.ch",
    "combined.rbl.msrbl.net",
    "db.wpbl.info",
    "dnsbl.cyberlogic.net",
    "drone.abuse.ch",
    "drone.abuse.ch",
    "duinv.aupads.org",
    "dul.ru",
    "dynip.rothen.com",
    "images.rbl.msrbl.net",
    "ips.backscatterer.org",
    "ix.dnsbl.manitu.net",
    "korea.services.net",
    "ohps.dnsbl.net.au",
    "omrs.dnsbl.net.au",
    "osps.dnsbl.net.au",
    "osrs.dnsbl.net.au",
    "owfs.dnsbl.net.au",
    "pbl.spamhaus.org",
    "phishing.rbl.msrbl.net",
    "probes.dnsbl.net.au",
    "proxy.bl.gweep.ca",
    "rbl.interserver.net",
    "rdts.dnsbl.net.au",
    "relays.bl.gweep.ca",
    "relays.nether.net",
    "residential.block.transip.nl",
    "ricn.dnsbl.net.au",
    "rmst.dnsbl.net.au",
    "spam.abuse.ch",
    "spam.rbl.msrbl.net",
    "spam.spamrats.com",
    "spamrbl.imp.ch",
    "t3direct.dnsbl.net.au",
    "tor.dnsbl.sectoor.de",
    "torserver.tor.dnsbl.sectoor.de",
    "ubl.lashback.com",
    "ubl.unsubscore.com",
    "virus.rbl.jp",
    "virus.rbl.msrbl.net",
    "wormrbl.imp.ch",
    "xbl.spamhaus.org",
    "zen.spamhaus.org"
]

app = Flask(__name__)


"""
Single DNS BL can report BL for Multiple Times... it is also added
"""


def format_dnsbl_response(dnsbl_response, dnsbl_response_details):

    dnsbl_str_list = dnsbl_response.rrset.to_text().replace("\n", " ").split(" ")
    dnsbl_details_str = dnsbl_response_details.rrset.to_text()

    dnsbl_name = get_dnsbl_name(dnsbl_str_list[0])
    dnsbl_type = dnsbl_str_list[4]

    if len(dnsbl_str_list) > 6:
        dnsbl_type = dnsbl_type + "," + dnsbl_str_list[9]

    dnsbl_link = get_dnsbl_link(dnsbl_details_str)
    dnsbl_data = {"dnsbl_name": dnsbl_name,
                  "dnsbl_type": dnsbl_type, "dnsbl_link": dnsbl_link}

    return dnsbl_data


def get_dnsbl_link(dnsbl_details_str):
    url_str = re.search("(?P<url>https?://[^\s]+)", dnsbl_details_str)
    if url_str:
        return url_str.group("url").strip('"')
    else:
        return dnsbl_details_str


def get_dnsbl_name(dnsbl_query):
    if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', dnsbl_query):
        return ".".join(dnsbl_query.split(".")[4:])
    else:
        return dnsbl_query


async def query_dns(domain_name: str, rdtype: str = 'A', rtime: int = 1):

    our_resolver = Resolver()
    our_resolver.nameservers = USE_DNSSERVERS
    our_resolver.timeout = int(rtime)
    our_resolver.lifetime = int(rtime)

    try:
        dnsbl_response: dns.resolver.Answer = await our_resolver.resolve(domain_name, rdtype=rdtype, tcp=USE_TCP)
        dnsbl_response_details: dns.resolver.Answer = await our_resolver.resolve(domain_name, rdtype="TXT", tcp=USE_TCP)
        dnsbl_dict = format_dnsbl_response(
            dnsbl_response, dnsbl_response_details)
        return {"status": True, "timeout": False, "unknown": False, "dnsbl_response": dnsbl_dict}
    except dns_resolver.NXDOMAIN as no_dns_query:
        return {"status": False, "timeout": False, "unknown": False, "dnsbl_response": {}}
    except dns_exception.Timeout as dns_query_timedout:
        return {"status": False, "timeout": True, "unknown": False, "dnsbl_response": {"dnsbl_name": get_dnsbl_name(domain_name), "dnsbl_error": str(dns_query_timedout)}}
    except Exception as except_me:
        #print("Unexpected Exception: ", except_me)
        return {"status": False, "timeout": False, "unknown": True, "dnsbl_response": {"dnsbl_name": get_dnsbl_name(domain_name), "dnsbl_error": str(except_me)}}


async def query_dns_bulk(*dns_queries: Tuple[str, str], rtime):
    query_dns_bunch = [query_dns(domain_name, rdtype, rtime)
                       for domain_name, rdtype in list(dns_queries)]
    return await asyncio.gather(*query_dns_bunch)


def is_ip(given_ip):
    try:
        ipaddress.ip_address(given_ip)
        return True
    except ValueError:
        return False


def generate_dns_queries(check_ip):
    dns_queries = []
    for one_blacklister in blacklist_services:
        dns_query = f'{".".join(reversed(str(check_ip).split(".")))}.{one_blacklister}'
        dns_queries.append((dns_query, 'A'))
    return dns_queries


def get_bname_dict(one_dns_result):
    dns_blacklist_data = str(one_dns_result).split(" ")
    b_name = None
    b_type = dns_blacklist_data[-1]
    if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', dns_blacklist_data[0]):
        b_name = ".".join(dns_blacklist_data[0].split(".")[4:])
    else:
        b_name = dns_blacklist_data[0]
    return {"b_service_domain": b_name, "type": b_type}


async def process_bulk_query(check_ip, rtime):

    blacklisted = False

    if is_ip(check_ip):

        queries = generate_dns_queries(check_ip)

        result_set = await query_dns_bulk(*queries, rtime=rtime)

        dnsbl_timeout = []
        dnsbl_exception = []
        dnsbl_found = []

        for dnsq_result in result_set:
            if dnsq_result["status"]:
                dnsbl_found.append(dnsq_result["dnsbl_response"])
                blacklisted = True
            else:
                if dnsq_result["timeout"]:
                    dnsbl_timeout.append(dnsq_result["dnsbl_response"])
                if dnsq_result["unknown"]:
                    dnsbl_exception.append(dnsq_result["dnsbl_response"])

        query_result = {
            "success": True,
            "blacklisted": blacklisted,
            "ip": check_ip,
            "bl_list": dnsbl_found,
            "bl_timedout": dnsbl_timeout,
            "bl_exception": dnsbl_exception,
            "bl_count": len(blacklist_services)
        }

        # print(query_result)
        return query_result

    else:
        return {
            "success": False,
            "error": {"type": "Not IP", "desc": "Not a Valid IP Address", "bl_count": len(blacklist_services)}
        }


@app.route("/")
def route_slash():
    return {"info": "Hello, I am Blacklist API Service!, For URL Blacklist send Request as /check_blacklist?ip=1.1.1.1 \n Also Check 'http://192.168.1.6:5000/check_blacklist?ip=5.2.69.50'"}


@app.route("/check_blacklist")
def check_blacklist():
    badip = request.args.get('ip', None)
    rtimeout = request.args.get('rtimeout', 1)

    if badip:
        result = asyncio.run(process_bulk_query(badip, rtimeout))
        return result, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}
    else:
        return {
            "success": False,
            "error": {"type": "No Param Provided", "desc": "To check IP DNS Blacklist, the API req requires url Param 'ip'"}
        }, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return {"info": f"You Requested Path: {path}, For URL Blacklist send Request as /check_blacklist?ip=1.1.1.1\n Also Check 'http://192.168.1.6:5000/check_blacklist?ip=5.2.69.50'"}, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
