import scapy.all as scapy
from scapy.layers import http
from scapy.layers.http import *

def procces_sniffed_package(package):
    if package.haslayer(http.HTTPRequest):
        print(package.summary())

def sniff(interface):
    scapy.sniff(
        iface=interface,
        store=False,
        prn=procces_sniffed_package,
    )

sniff('wlp2s0b1')