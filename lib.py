import scapy.all as scapy
from termcolor import colored

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
  
def display_result(result, target, once=False):
    if not result:
        print(colored(f"[-] {target} is not found", 'red'))
        return
    if once:
        print(colored(f"[+] {result[0]['ip']}\t\t\t{result[0]['mac']}", "green"))
        return
