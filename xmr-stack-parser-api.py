#!/usr/bin/python
'''
Cacti parser for xmr-stak  by fireice-uk.
This version parse api/json web page, so it works only with xmr-stak-cpu for now  
@author: lamba84
REV: 0.2
return results by thread
added try except in case of lost connection
REV: 0.1
intial release

TO-DO:
this parser will become the only mantained once all XMR-stak versions will use api/json output. expected by end of 2017

@author: lamba84
'''

import requests
import re
import argparse
import json 

parser = argparse.ArgumentParser(description='XMR-stack hash rates parser')
parser.add_argument('url', metavar='url', type=str,
                    help='xmr-stack-api <url and port>. Eg. 127.0.0.1:8081 ')


args = parser.parse_args()

port=re.search(r'\:([0-9]*)', args.url).group(1)
if (port==""):
    print "missing port"
    exit()
elif (args.url.find('http://')<>-1):
    hash_url=args.url
else:
    hash_url='http://'+args.url+'/api.json'
    
def get_rate_api(h_url):
    try:
        page= requests.get(h_url).json()
        #print json.dumps(page, sort_keys=True, indent=2, separators=(',', ': '))
        t_rates=page['hashrate']['total']
        total=" "
        i=0
        for t in page['hashrate']['threads']:
            total=total+"tot%s:%s "%(i,t[0])
            i=i+1
        #rtn_str= "total_2.5s:%s total_1m:%s total_15m:%s" %(t_rates[0],t_rates[1],t_rates[2])
        return total
    except:
        return "tot0:0.0"

print get_rate_api(hash_url)