import scapy.all as scapy
import argparse
import os
from re import findall, search
from threading import Thread, Event
from time import sleep
from tqdm import tqdm
from subprocess import call


ip_patt = b"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

ips = []

class Timer(Thread):


    def __init__(self, time_sec):
        super().__init__()
        self.time_sec = time_sec

    def stopped(self):
        print('Time is over.\n')
        print(ips)
        input('Enter for exit')
        os.abort()
        
    def run(self):
        
        for i in tqdm(range(self.time_sec)):
            sleep(1)
        else:
            self.stopped()




def procces_sniffed_package(package):
    mask_ip = scapy.conf.route.route("0.0.0.0")[2][:-1]
    

    if package.haslayer(scapy.IP):
        ip_lay = package['IP']
        src = ip_lay.src

        if mask_ip in src:
            if not src in ips:
                ips.append(src)

def sniff(interface):
    scapy.sniff(
        iface=interface,
        store=False,
        prn=procces_sniffed_package,
    )


argparser = argparse.ArgumentParser()
argparser.add_argument('-i', type=str, dest='i', help='Interface name')
argparser.add_argument('-s', type=int, dest='secs', help='Interface name')
args = argparser.parse_args()


try:
    call('clear')
    print(f"\nSniffing interface {args.i} is running\n")
    times = Timer(args.secs).start()

    sniff(args.i)
except KeyboardInterrupt:
    print("Aborted by keyboard")
    