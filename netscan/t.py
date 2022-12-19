import scapy.all as scapy


    def scan(ip):
        packet1 = scapy.ARP(pdst=ip)
        etherpacket = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')

        broadcast_packet = etherpacket/packet1
        ans, unans = scapy.srp(broadcast_packet, timeout=10)

        print(ans.summary())





    scan("192.168.1.1/24")
