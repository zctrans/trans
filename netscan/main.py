import scapy.all as scapy
from tabulate import tabulate
import argparse


class Caught:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac

    def show(self):
        print(f"\n------------------------\nIP: {self.ip}\nMAC: {self.mac}\n------------------------\n")


def scan(ip):

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    caughts = []

    for el in answered:
        for answer in el:
            caughts.append(Caught(answer.pdst, answer.hwsrc))
    
    
    return caughts
        
def show_tabled(list_of_caught):
    print(tabulate(
        [[caught.ip, caught.mac] for caught in list_of_caught],
        headers=['IP', 'MAC']
    ))    

argparser = argparse.ArgumentParser()
argparser.add_argument('-t', type=str, dest='target', help='IP of victim')
args = argparser.parse_args()

show_tabled(scan(args.target))