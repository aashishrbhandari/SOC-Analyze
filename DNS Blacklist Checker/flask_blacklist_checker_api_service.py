from flask import Flask
from flask import request

from dns.asyncresolver import Resolver
import dns.resolver
import dns.rrset
import ipaddress

import asyncio

from typing import Tuple

import re

'''
API Infos

/check_blacklist?ip=10.10.10.10


Checks:
1. Valid IP

If blacklisted  Result:
------- 
{
    "success": true,
    "b": true,
    "ip": 1.1.1.1,
    "bs" : [
        { "b_service_domain": "torserver.tor.dnsbl.sectoor.de.", "type": "127.0.0.1" }
        ...
    ]
}

If Not Blacklisted
-------
{
    "success": false,
    "b": false,
    "ip": 1.1.1.1,
    "bs" : []
}

2. Invalid IP, Wrong
{
    "success": false,
    "error": {"type": , "desc": ""}
}


Types:
------
Invalid IP
String Not an IP
No Param Provided

# Internet Down cannot Connect to DNS Blacklist Service
'''

USE_TCP = True

USE_DNSSERVERS = ['1.1.1.1', '8.8.8.8']


blacklist_services = [
    "b.barracudacentral.org",
    "bl.spamcop.net",
    "blacklist.woody.ch",
    "cbl.abuseat.org",
    "combined.abuse.ch",
    "combined.rbl.msrbl.net",
    "db.wpbl.info",
    "dnsbl.cyberlogic.net",
    "dnsbl.sorbs.net",
    "drone.abuse.ch",
    "drone.abuse.ch",
    "duinv.aupads.org",
    "dul.dnsbl.sorbs.net", "dul.ru",
    "dynip.rothen.com",
    "http.dnsbl.sorbs.net",
    "images.rbl.msrbl.net",
    "ips.backscatterer.org",
    "ix.dnsbl.manitu.net",
    "korea.services.net",
    "misc.dnsbl.sorbs.net",
    "noptr.spamrats.com",
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
    "smtp.dnsbl.sorbs.net",
    "socks.dnsbl.sorbs.net",
    "spam.abuse.ch",
    "spam.dnsbl.sorbs.net",
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
    "web.dnsbl.sorbs.net",
    "wormrbl.imp.ch",
    "xbl.spamhaus.org",
    "zen.spamhaus.org",
    "zombie.dnsbl.sorbs.net"
]

app = Flask(__name__)


async def dns_query(domain: str, rtype: str = 'A', **kwargs) -> dns.rrset.RRset:
    kwargs, res_cfg = dict(kwargs), {}
    if 'filename' in kwargs:
        res_cfg['filename'] = kwargs.pop('filename')
    if 'configure' in kwargs:
        res_cfg['configure'] = kwargs.pop('configure')
    rs = Resolver(**res_cfg)
    rs.nameservers = USE_DNSSERVERS
    rs.timeout = 1
    rs.lifetime = 1
    res: dns.resolver.Answer = await rs.resolve(domain, rdtype=rtype, tcp=USE_TCP, **kwargs)
    return res.rrset


async def dns_bulk(*queries: Tuple[str, str], **kwargs):
    ret_ex = kwargs.pop('return_exceptions', True)
    coros = [dns_query(dom, rt, **kwargs) for dom, rt in list(queries)]
    return await asyncio.gather(*coros, return_exceptions=ret_ex)


def is_ip(given_ip):
    try:
        ipaddress.ip_address(given_ip)
        return True
    except ValueError as except_me:
        return False


def generate_queries(bad_ip):
    bad_queries = []
    for one_blacklister in blacklist_services:
        dns_bad_ip_req = query = '.'.join(
            reversed(str(bad_ip).split("."))) + "." + one_blacklister
        bad_queries.append((dns_bad_ip_req, 'A'))
    return bad_queries


def get_bname_dict(one_dns_result):
    dns_blacklist_data = str(one_dns_result).split(" ")
    b_name = None
    b_type = dns_blacklist_data[-1]
    if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', dns_blacklist_data[0]):
        b_name = ".".join(dns_blacklist_data[0].split(".")[4:])
    else:
        b_name = dns_blacklist_data[0]
    return {"b_service_domain": b_name, "type": b_type}


async def do_bulk_query(badip):

    blacklisted = False

    if is_ip(badip):

        queries = generate_queries(badip)

        res = await dns_bulk(*queries)

        blacklist_db = []
        for index, one_dns_result in enumerate(res):
            if isinstance(one_dns_result, Exception):
                continue
            bname_dict = get_bname_dict(one_dns_result)
            blacklist_db.append(bname_dict)

        if len(blacklist_db) > 0:
            blacklisted = True

        return {
            "success": True,
            "b": blacklisted,
            "ip": badip,
            "bs": blacklist_db
        }

    else:
        return {
            "success": False,
            "error": {"type": "Not IP", "desc": "Not a Valid IP Address"}
        }


@app.route("/")
def route_slash():
    return {"info": "Hello, I am Blacklist API Service!, For URL Blacklist send Request as /check_blacklist?ip=1.1.1.1"}


@app.route("/check_blacklist")
def check_blacklist():
    badip = request.args.get('ip', None)
    if badip:
        result = asyncio.run(do_bulk_query(badip))
        return result, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}
    else:
        return {
            "success": False,
            "error": {"type": "No Param Provided", "desc": "To check IP DNS Blacklist, the API req requires url Param 'ip'"}
        }, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return {"info": f"You Requested Path: {path}, For URL Blacklist send Request as /check_blacklist?ip=1.1.1.1"}, {"Access-Control-Allow-Origin": "*", "X-Backend": "Py DNS Blacklist API"}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
