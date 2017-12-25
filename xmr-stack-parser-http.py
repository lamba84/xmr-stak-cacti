#!/usr/bin/python
'''
Cacti parser for xmr-stak  by fireice-uk.
This version parse http web page, so it works with any version of xmr-stak once HTML report is configured open  
@author: lamba84

REV: 0.1
intial release
REV: 0.2
added try statment and fixed output when miner is stuck
TO-DO:
this parser will be discontinued once all XMR-stak version will use api/json output. expected by end of 2017
'''

import requests
import re
import argparse

parser = argparse.ArgumentParser(description='XMR-stack hash rates parser')
parser.add_argument('url', metavar='url', type=str,
                    help='xmr-stack http url and port. Eg. 127.0.0.1:8081 ')


args = parser.parse_args()

port=re.search(r'\:([0-9]*)', args.url).group(1)
if (port==""):
    print "missing port"
    exit()
elif (args.url.find('http://')<>-1):
    hash_url=args.url
else:
    hash_url='http://'+args.url+'/h'
    
def get_rate(h_url): #get data for web interface version of xmr-stack miner, basic function
    try: 
        page = requests.get(h_url)
        matchObj = re.findall(r'<th>Totals:</th><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>', page.content, re.M|re.I|re.S)
    except:
        print "Zero"
        exit()
    
    return matchObj[0][1]

def get_rate_dev(h_url): #get data for web interface version of xmr-stack miner, dev version and return in format suitable for Cacti
    try: 
        page = requests.get(h_url)
        matchObj = re.findall(r'<th>(total.*?)</th><td> (.*?)</td><td> (.*?)</td><td> (.*?)</td></tr>', page.content, re.M|re.I|re.S)
        rtn_str= "total_2.5s:"+matchObj[0][1]+" "+"total_1m:"+matchObj[0][2]+" "+"total_15m:"+matchObj[0][3]
    except:
        rtn_str="total_2.5s:0.0 total_1m:0.0 total_15m:0.0"
    
    return rtn_str

#print get_rate(hash_url)
print get_rate_dev(hash_url)