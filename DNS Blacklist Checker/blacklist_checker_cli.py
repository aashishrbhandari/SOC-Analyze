from dns.asyncresolver import Resolver
import dns.resolver
import dns.rrset
import asyncio
from typing import Tuple
import sys
import ipaddress

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


async def process_req():

    badip = None

    if len(sys.argv) > 1:
        badip = sys.argv[1]
    else:
        sys.exit("Please Provide IP as Argument")

    if not is_ip(badip):
        sys.exit("IP Address is InValid")

    queries = generate_queries(badip)

    res = await dns_bulk(*queries)

    blacklist_db = []
    for i, a in enumerate(res):
        if isinstance(a, Exception):
            continue
        dns_blk_ip = str(a).split(" ")
        blacklist_db.append([dns_blk_ip[0], dns_blk_ip[-1]])

    return blacklist_db


def run_program():
    val = asyncio.run(process_req())
    print(val)


run_program()
