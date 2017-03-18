#!/usr/bin/python
import urllib2
from urllib2 import urlopen, HTTPError
import json

RR_URL = "https://reverse.report/commonapi/v1/name/%s.json?page=0"

def rr_search(domain):
    domains = []
    ips = []
    both = []
    url = RR_URL % domain
    is_next_page = True

    while is_next_page:
        try:
            headers = {'User-Agent': 'Lynx/2.8.3.rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.5a'}
            request = urllib2.Request(url, headers=headers)
            response = urlopen(request)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
            if "next_page_url" in json_obj:
                is_next_page = True
                url = json_obj['next_page_url']
            else:
                is_next_page = False
            raw_d_list = json_obj['records']
            for ip, domain in raw_d_list.iteritems():
                ips.append(ip)
                domains.append(domain)
                both.append((ip,domain))

        except HTTPError as e:
            print("Something broke: %s", e)

    return domains, ips, both

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("[*] No domain provided. Syntax: reverse_report.py <domain> [*]")
    else:
        print('[*] Searching reverse.report for domain [*]')
        domain = sys.argv[1]
        domains, ips, both = rr_search(domain)
        for domain in domains:
            print(domain)
