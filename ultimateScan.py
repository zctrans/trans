from lib import *
from re import match
import argparse

def get_v_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--victim', dest='victim', help='Victim IP')
    parser.add_argument('-b', '--begin', dest='begin', help='Begin of slice')
    parser.add_argument('-e', '--end', dest='end', help='End of slice')
    parser.add_argument('-gi', '--gateway_ip', dest='gi', help='Optional: IP of gateway')
    options = parser.parse_args()

    return options

def gen_ips(target):
    ips = []
    target_root = match(r'\d+\.\d+\.\d+\.', target).group()
    for i in range(0, 256):
        ips.append(target_root+str(i))

    return ips            
        

def show():
    for ip in gen_ips(get_v_args().victim)[int(get_v_args().begin):int(get_v_args().end)]:
        result = scan(ip)        
        display_result(result, ip, True)

show()


