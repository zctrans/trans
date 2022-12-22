from ui.gui_scanner import *
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

def gen_ips(target):
    
    ips = []
    target_root = match(r'\d+\.\d+\.\d+\.', target).group()
    for i in range(0, 256):
        ips.append(target_root+str(i))
    return ips



class Root(QtWidgets.QMainWindow ,Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        Root.show(self)

        self.model = QtGui.QStandardItemModel()

        self.gateway_edit.setText("192.168.1.1")
        self.floor_edit.setText("64")
        self.ceil_edit.setText("75")
        self.scan_button.setText("S\nC\nA\nN")
        
        self.scan_button.clicked.connect(lambda: self.scan_event())

    def get(self, ip, begin, end):
        goods = []
        ips = gen_ips(ip)[int(begin):int(end)]
        step = 100 / len(ips)

        for ip in ips:
            result = scan(ip)
            if result:
                goods.append(result[0])
            self.scan_pb.setValue(int(self.scan_pb.value()) + int(step))
        if not int(self.scan_pb.value()) == 100:
            self.scan_pb.setValue(100)
        return goods

    def scan_event(self):

        self.scan_pb.setValue(0)
        self.model.clear()
        gateway_ip = self.gateway_edit.text()
        begin = self.floor_edit.text()
        end = self.ceil_edit.text()
        result = self.get(gateway_ip, begin, end)
        
        
        self.victims_list.setModel(self.model)

        for victim in result:
            item = QtGui.QStandardItem(victim['ip'])
            self.model.appendRow(item)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Root()
    sys.exit(app.exec_())