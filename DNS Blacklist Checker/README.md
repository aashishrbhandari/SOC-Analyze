DNS Blacklist Service
--------------------------
`I tried a way to get it done as i can`


A Simple DNS Blacklist Service API & CLI to get Blacklist details for IP addresses.

### Note
In Simple words, the Code is taken from  [IsThisIPBad](https://github.com/jgamblin/isthisipbad) and then rewamped and applied AsyncIO.

For Effecient Result Try Changing the Timeout from 5 to 9

<strong> Recommended : </strong> Timeout 8

`Ignore the Exception Mostly`

### Further References:
 - To Further Optimize it I used Code from here [AsyncIO DNSPython Example](https://stackoverflow.com/questions/30675026/sending-dns-queries-asynchronously-with-asyncio-and-dnspython)

# Requirements
1. Python 3.7+
2. Download Req `python3 -m pip install flask dnspython`


# How It works


## CLI

<strong> Quick Check: </strong>

```cmd & bash
Z:\Projects\SOC-analyze>python "DNS Blacklist Checker\blacklist_check_cli_v2.py" 5.2.69.50 | bash -c 'jq'
{
  "success": true,
  "blacklisted": true,
  "ip": "5.2.69.50",
  "bl_list": [
    {
      "dnsbl_name": "bl.spamcop.net.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "https://www.spamcop.net/bl.shtml?5.2.69.50"
    },
    {
      "dnsbl_name": "cbl.abuseat.org.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50"
    },
    {
      "dnsbl_name": "rbl.interserver.net.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "http://sigs.interserver.net/ip?ip=5.2.69.50"
    },
    {
      "dnsbl_name": "spamrbl.imp.ch.",
      "dnsbl_type": "127.0.0.8",
      "dnsbl_link": "50.69.2.5.spamrbl.imp.ch. 49 IN TXT \"1636807434: 13.11.2021 13:43: HELO sent to a spamtrap for blacklist.imp.ch on 157.161.9.64:587\""
    },
    {
      "dnsbl_name": "torserver.tor.dnsbl.sectoor.de.",
      "dnsbl_type": "127.0.0.1",
      "dnsbl_link": "http://www.sectoor.de/tor.php"
    },
    {
      "dnsbl_name": "xbl.spamhaus.org.",
      "dnsbl_type": "127.0.0.4",
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50"
    },
    {
      "dnsbl_name": "zen.spamhaus.org.",
      "dnsbl_type": "127.0.0.4,127.0.0.3",
      "dnsbl_link": "https://www.spamhaus.org/sbl/query/SBLCSS"
    }
  ],
  "bl_timedout": [
    {
      "dnsbl_name": "noptr.spamrats.com",
      "dnsbl_error": "The DNS operation timed out after 1.1181519031524658 seconds"
    },
    {
      "dnsbl_name": "spam.spamrats.com",
      "dnsbl_error": "The DNS operation timed out after 1.1025300025939941 seconds"
    }
  ],
  "bl_exception": [],
  "bl_count": 57
}

```

##### Run with DNS Timeout set to Recommended: 8 


```
J:\Projects\SOC-analyze>python "DNS Blacklist Checker\blacklist_check_cli_v2.py" 5.2.69.50 8 | bash -c 'jq'
{
  "success": true,
  "blacklisted": true,
  "ip": "5.2.69.50",
  "bl_list": [
    {
      "dnsbl_name": "bl.spamcop.net.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "https://www.spamcop.net/bl.shtml?5.2.69.50"
    },
    {
      "dnsbl_name": "cbl.abuseat.org.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50"
    },
    {
      "dnsbl_name": "rbl.interserver.net.",
      "dnsbl_type": "127.0.0.2",
      "dnsbl_link": "http://sigs.interserver.net/ip?ip=5.2.69.50"
    },
    {
      "dnsbl_name": "spamrbl.imp.ch.",
      "dnsbl_type": "127.0.0.8",
      "dnsbl_link": "50.69.2.5.spamrbl.imp.ch. 300 IN TXT \"1636807434: 13.11.2021 13:43: HELO sent to a spamtrap for blacklist.imp.ch on 157.161.9.64:587\""
    },
    {
      "dnsbl_name": "torserver.tor.dnsbl.sectoor.de.",
      "dnsbl_type": "127.0.0.1",
      "dnsbl_link": "http://www.sectoor.de/tor.php"
    },
    {
      "dnsbl_name": "xbl.spamhaus.org.",
      "dnsbl_type": "127.0.0.4",
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50"
    },
    {
      "dnsbl_name": "zen.spamhaus.org.",
      "dnsbl_type": "127.0.0.3,127.0.0.4",
      "dnsbl_link": "https://www.spamhaus.org/sbl/query/SBLCSS"
    }
  ],
  "bl_timedout": [],
  "bl_exception": [
    {
      "dnsbl_name": "noptr.spamrats.com",
      "dnsbl_error": "All nameservers failed to answer the query 50.69.2.5.noptr.spamrats.com. IN A: Server 1.1.1.1 UDP port 53 answered SERVFAIL"
    },
    {
      "dnsbl_name": "spam.spamrats.com",
      "dnsbl_error": "All nameservers failed to answer the query 50.69.2.5.spam.spamrats.com. IN A: Server 1.1.1.1 UDP port 53 answered SERVFAIL"
    }
  ],
  "bl_count": 57
}
```



## API

<strong> Command to Run: </strong>

```bash
Z:\Projects\SOC-analyze>python "DNS Blacklist Checker\flask_blacklist_checker_api_service_v2.py" 
```
<strong> Example Run: </strong>

```cmd
Z:\Projects\SOC-analyze>python "DNS Blacklist Checker\flask_blacklist_checker_api_service_v2.py" 
 * Serving Flask app 'flask_blacklist_checker_api_service_v2' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 117-719-022
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.1.6:5000/ (Press CTRL+C to quit)
```



<strong> Example Curl Request: </strong>

##### Quick Curl Check for 1 IP
Same can be done by providing additional URL Param [rtimeout]

```
Example Request: curl -vk "http://192.168.1.6:5000/check_blacklist?ip=5.2.69.50&rtimeout=8"
```

```cmd

Z:\Projects\SOC-analyze>curl -vk "http://192.168.1.6:5000/check_blacklist?ip=5.2.69.50"
*   Trying 192.168.1.6...
* TCP_NODELAY set
* Connected to 192.168.1.6 (192.168.1.6) port 5000 (#0)
> GET /check_blacklist?ip=5.2.69.50 HTTP/1.1
> Host: 192.168.1.6:5000 
> User-Agent: curl/7.55.1
> Accept: */*
>
* HTTP 1.0, assume close after body  
< HTTP/1.0 200 OK
< Content-Type: application/json     
< Content-Length: 2045
< Access-Control-Allow-Origin: *     
< X-Backend: Py DNS Blacklist API    
< Server: Werkzeug/2.0.2 Python/3.7.4
< Date: Sun, 14 Nov 2021 11:08:36 GMT
<
{
  "bl_count": 57,
  "bl_exception": [],
  "bl_list": [
    {
      "dnsbl_link": "https://www.spamcop.net/bl.shtml?5.2.69.50",  
      "dnsbl_name": "bl.spamcop.net.",
      "dnsbl_type": "127.0.0.2"
    },
    {
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50", 
      "dnsbl_name": "cbl.abuseat.org.",
      "dnsbl_type": "127.0.0.2"
    },
    {
      "dnsbl_link": "http://sigs.interserver.net/ip?ip=5.2.69.50",
      "dnsbl_name": "rbl.interserver.net.",
      "dnsbl_type": "127.0.0.2"
    },
    {
      "dnsbl_link": "50.69.2.5.spamrbl.imp.ch. 100 IN TXT \"1636807434: 13.11.2021 13:43: HELO sent to a spamtrap for blacklist.imp.ch on 157.161.9.64:587\"",
      "dnsbl_name": "spamrbl.imp.ch.",
      "dnsbl_type": "127.0.0.8"
    },
    {
      "dnsbl_link": "http://www.sectoor.de/tor.php",
      "dnsbl_name": "torserver.tor.dnsbl.sectoor.de.",
      "dnsbl_type": "127.0.0.1"
    },
    {
      "dnsbl_link": "https://www.spamhaus.org/query/ip/5.2.69.50",
      "dnsbl_name": "xbl.spamhaus.org.",
      "dnsbl_type": "127.0.0.4"
    },
    {
      "dnsbl_link": "https://www.spamhaus.org/sbl/query/SBLCSS",
      "dnsbl_name": "zen.spamhaus.org.",
      "dnsbl_type": "127.0.0.3,127.0.0.4"
    }
  ],
  "bl_timedout": [
    {
      "dnsbl_error": "The DNS operation timed out after 1.10371732711792 seconds",
      "dnsbl_name": "smtp.dnsbl.sorbs.net"
    },
    {
      "dnsbl_error": "The DNS operation timed out after 1.0917298793792725 seconds",
      "dnsbl_name": "http.dnsbl.sorbs.net"
    },
    {
      "dnsbl_error": "The DNS operation timed out after 1.089717149734497 seconds",
      "dnsbl_name": "noptr.spamrats.com"
    },
    {
      "dnsbl_error": "The DNS operation timed out after 1.129404067993164 seconds",
      "dnsbl_name": "korea.services.net"
    },
    {
      "dnsbl_error": "The DNS operation timed out after 1.1238045692443848 seconds",
      "dnsbl_name": "spam.spamrats.com"
    }
  ],
  "blacklisted": true,
  "ip": "5.2.69.50",
  "success": true
}
* Closing connection 0

```
