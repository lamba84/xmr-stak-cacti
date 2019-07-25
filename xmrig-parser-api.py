#!/usr/bin/python
'''
Cacti parser for xmrig-amd https://github.com/xmrig/xmrig-amd
This version parse api/json request  
@author: lamba84
REV: 0.1
fixed timeout issue in production
'''

import requests
import re
import argparse
import json 

mytoken="change this to your token"
parser = argparse.ArgumentParser(description='XMR-stack hash rates parser')
parser.add_argument('url', metavar='url', type=str,
                    help='xmrig-api <url and port>. Eg. 127.0.0.1:8081 ')


args = parser.parse_args()

port=re.search(r'\:([0-9]*)', args.url).group(1)
if (port==""):
    print "missing port"
    exit()
elif (args.url.find('http://')<>-1):
    hash_url=args.url
else:
    hash_url='http://'+args.url+'/1/summary'
    
def get_rate_api(h_url):
    try:
        page= requests.get(h_url, headers={"Authorization":mytoken}, timeout=2).json()
        #print json.dumps(page, sort_keys=True, indent=2, separators=(',', ': '))
        total=page['hashrate']['total']
        th=" "
        i=0
        for t in page['hashrate']['threads']:
            th=th+"th%s:%s "%(i,t[0])
            i=i+1
        #rtn_str= "total_2.5s:%s total_1m:%s total_15m:%s" %(t_rates[0],t_rates[1],t_rates[2])
        res=th+"tot60s:%s"%(total[1])
        return res
    except:
        return "th0:0.0 tot60s:0.0"

print get_rate_api(hash_url)