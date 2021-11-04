DNS Blacklist Service
--------------------------
`I tried a way to get it done as i can`


A Simple DNS Blacklist Service API & CLI to get Blacklist details for IP addresses.

### Note
In Simple words, the Code is taken from  [IsThisIPBad](https://github.com/jgamblin/isthisipbad) and then rewamped and Async IO is applied.

### Further References:
 - To Further Optimize it I used Code from here [AsyncIO DNSPython Example](https://stackoverflow.com/questions/30675026/sending-dns-queries-asynchronously-with-asyncio-and-dnspython)

### Requirements
1. Python 3.7+
2. Download Req `python3 -m pip install flask dnspython`


### How It works



#### CLI

<strong> Quick Check: </strong>

```bash
root@test-u-18:/# python3 blacklist_checker_cli.py 1.1.1.1
[['1.1.1.1.cbl.abuseat.org.', '127.0.0.2'], ['1.1.1.1.xbl.spamhaus.org.', '127.0.0.4'], ['1.1.1.1.zen.spamhaus.org.', '127.0.0.4']]
```

#### API

<strong> Command to Run: </strong>

```bash
root@test-u-18:/# python3 flask_blacklist_checker_api_service.py
```
<strong> Example Run: </strong>

```bash
root@test-u-18:/# python3 flask_blacklist_checker_api_service.py
 * Serving Flask app 'flask_blacklist_checker_api_service' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.25.209.85:5000/ (Press CTRL+C to quit)
```

<strong> Example Curl Request: </strong>

Quick Curl Check for 1 IP

```bash

root@test-u-18:/# curl -vk "http://172.25.209.85:5000/check_blacklist?ip=5.2.69.50"
*   Trying 172.25.209.85:5000...
* TCP_NODELAY set
* Connected to 172.25.209.85 (172.25.209.85) port 5000 (#0)
> GET /check_blacklist?ip=5.2.69.50 HTTP/1.1
> Host: 172.25.209.85:5000
> User-Agent: curl/7.68.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 487
< Access-Control-Allow-Origin: *
< X-Backend: Py DNS Blacklist API
< Server: Werkzeug/2.0.2 Python/3.9.2
< Date: Thu, 04 Nov 2021 10:00:12 GMT
<
{"b":true,"bs":[{"b_service_domain":"bl.spamcop.net.","type":"127.0.0.2"},{"b_service_domain":"blacklist.woody.ch.","type":"127.0.0.10"},{"b_service_domain":"cbl.abuseat.org.","type":"127.0.0.2"},{"b_service_domain":"rbl.interserver.net.","type":"127.0.0.2"},{"b_service_domain":"torserver.tor.dnsbl.sectoor.de.","type":"127.0.0.1"},{"b_service_domain":"xbl.spamhaus.org.","type":"127.0.0.4"},{"b_service_domain":"zen.spamhaus.org.","type":"127.0.0.4"}],"ip":"5.2.69.50","success":true}
* Closing connection 0

```

Quick Check API with `jq`

```bash

root@test-u-18:/# curl -sk "http://172.25.209.85:5000/check_blacklist?ip=5.2.69.50" | jq
{
  "b": true,
  "bs": [
    {
      "b_service_domain": "bl.spamcop.net.",
      "type": "127.0.0.2"
    },
    {
      "b_service_domain": "blacklist.woody.ch.",
      "type": "127.0.0.10"
    },
    {
      "b_service_domain": "cbl.abuseat.org.",
      "type": "127.0.0.2"
    },
    {
      "b_service_domain": "rbl.interserver.net.",
      "type": "127.0.0.2"
    },
    {
      "b_service_domain": "xbl.spamhaus.org.",
      "type": "127.0.0.4"
    },
    {
      "b_service_domain": "zen.spamhaus.org.",
      "type": "127.0.0.4"
    }
  ],
  "ip": "5.2.69.50",
  "success": true
}

```