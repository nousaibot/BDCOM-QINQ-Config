out_tag = input("Номер верхнего тега: ")
VlanName = input("Имя  верхнего тега: ")
tag = 3000
Epon = int(input("Количество Epon портов: "))
Ether = int(input("Количество Ethernet портов: "))
tEther = int(input("Количество 10G Ethernet портов (если нет ввести 0): "))

open("config.txt", "w")
file = open("config.txt", "a")

Conf = """
 conf
 vlan {0}
 name {1}
 !
 system mtu 2025

 epon onu-config-template ACCESS
 cmd-sequence 001 epon onu all-port ctc vlan mode tag %1
 cmd-sequence 002 epon onu all-port storm-control mode 1 threshold 256
 cmd-sequence 003 epon onu all-port ctc loopback detect
 cmd-sequence 004 epon onu all-port ctc notify loopback
 cmd-sequence 005 switchport port-security mode dynamic
 cmd-sequence 006 switchport port-security dynamic maximum 10
 !
 """.format(out_tag, VlanName)
file.write(Conf)

for i in range(1, (Ether + 1)):
    iEther = """interface GigaEthernet0/{0}
 switchport trunk vlan-allowed add {1}
 switchport mode dot1q-tunnel-uplink
 no switchport trunk vlan-untagged
 no shutdown
 !
""".format(i, out_tag)
    file.write(iEther)

if tEther > 0:
    for i in range(1, (tEther + 1)):
        teEther = """ interface TGigaEthernet0/{0}
 switchport trunk vlan-allowed add {1}
 switchport mode dot1q-tunnel-uplink
 no shutdown
 !
""".format(i, out_tag)
        file.write(teEther)

for i in range(1, Epon + 1):
    epon = """
    default interface ePON 0/{0}
    interface EPON0/{0}
    no switchport trunk vlan-allowed
    no switchport trunk vlan-untagged
    no switchport mode
    no switchport pvid
    switchport mode dot1q-translating-tunnel
    switchport pvid {1}
    switchport protected 1
    """.format(i, out_tag)
    file.write("\n" + epon)

    for j in range(1, 65):
        j = str(j)
        tag += 1
        interface = """epon pre-config-template ACCESS binded-onu-llid {0} param {1}
    """.format(j, tag)
        file.write(interface)
    file.write("no shutdown\n    !\n")

Other = """dot1q-tunnel
 """
file.write(Other)

file.close()


print("\nФайл конфигурации сгенерирован!")