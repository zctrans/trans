from subprocess import call, check_output, CalledProcessError
from random import randint as ri
from re import search, findall
from socket import if_nameindex

def generate_random_mac_adress():
    new_mac = f'{ri(10, 99)}:{ri(10, 99)}:{ri(10, 99)}:{ri(10, 99)}:{ri(10, 99)}:{ri(10, 99)}'
    return new_mac

def call_shell(command):
    call(command, shell=True)

def check_changed(interface):
    while True:
        try:
            result = check_output(['ifconfig', interface, 'hw', 'ether', generate_random_mac_adress()])
        except CalledProcessError:
            continue
        break


def change_mac(interface, new_mac=''):
    call_shell(f'ifconfig {interface} down')

    if new_mac:
        call_shell(f'ifconfig {interface} hw ether {new_mac}')
        call_shell(f'ifconfig {interface} up')
        return

    check_changed(interface)
    call_shell(f'ifconfig {interface} up')

def get_mac():
    result = check_output(['ifconfig']).decode()
    return search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', result).group()

def user_interface():
    interfaces = dict(if_nameindex())
    
    for index, inter in interfaces.items():
        print(f"{index}: {inter}")
    
    try:
        interface = interfaces[int(input("Select interface(don't use ): "))]
    except KeyError:
        print("Wrong key of interface. Abort.")
        return
    except ValueError:
        print("Wrong key of interface. Abort.")
        return

    mac = input("Enter new mac-address or leave blank for generate random: ")
    if mac:
        change_mac(interface, mac)
    else:
        change_mac(interface)
    
    print("mac-adress if changed.")




