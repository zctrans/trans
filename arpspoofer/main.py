import scapy.all as scapy

def create_packet(ip):
    packet = scapy.ARP(
        op=2,
        pdst=ip
    )
