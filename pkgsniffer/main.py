import scapy.all as scapy

def procces_sniffed_package(package):
    print(package)

def sniff(interface):
    scapy.sniff(
        iface=interface,
        store=False,
        prn=procces_sniffed_package,
    )


sniff("")