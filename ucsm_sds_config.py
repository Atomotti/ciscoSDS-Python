"""
ucsm_sds_config.py

Purpose:
    Complete Setup of a Scale-Out Object Storage Solution with S-Series and C220

Author:
    Olli Walsdorf (owalsdor@cisco.com)
    Cisco Systems, Inc.
"""
import sys
import json
from colorama import init
from time import sleep
from itertools import chain
from ucsmsdk import ucshandle

# use Colorama to make Termcolor work on Windows too
init()


from ucsmsdk.mometa.adaptor.AdaptorEthAdvFilterProfile import AdaptorEthAdvFilterProfile
from ucsmsdk.mometa.adaptor.AdaptorEthArfsProfile import AdaptorEthArfsProfile
from ucsmsdk.mometa.adaptor.AdaptorEthCompQueueProfile import AdaptorEthCompQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorEthFailoverProfile import AdaptorEthFailoverProfile
from ucsmsdk.mometa.adaptor.AdaptorEthInterruptProfile import AdaptorEthInterruptProfile
from ucsmsdk.mometa.adaptor.AdaptorEthInterruptScalingProfile import AdaptorEthInterruptScalingProfile
from ucsmsdk.mometa.adaptor.AdaptorEthNVGREProfile import AdaptorEthNVGREProfile
from ucsmsdk.mometa.adaptor.AdaptorEthOffloadProfile import AdaptorEthOffloadProfile
from ucsmsdk.mometa.adaptor.AdaptorEthRecvQueueProfile import AdaptorEthRecvQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorEthRoCEProfile import AdaptorEthRoCEProfile
from ucsmsdk.mometa.adaptor.AdaptorEthVxLANProfile import AdaptorEthVxLANProfile
from ucsmsdk.mometa.adaptor.AdaptorEthWorkQueueProfile import AdaptorEthWorkQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorHostEthIfProfile import AdaptorHostEthIfProfile
from ucsmsdk.mometa.adaptor.AdaptorRssProfile import AdaptorRssProfile
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider
from ucsmsdk.mometa.compute.ComputeChassisConnPolicy import ComputeChassisConnPolicy
from ucsmsdk.mometa.compute.ComputeChassisDiscPolicy import ComputeChassisDiscPolicy
from ucsmsdk.mometa.compute.ComputePowerSyncPolicy import ComputePowerSyncPolicy
from ucsmsdk.mometa.cpmaint.CpmaintMaintPolicy import CpmaintMaintPolicy
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac
from ucsmsdk.mometa.epqos.EpqosDefinition import EpqosDefinition
from ucsmsdk.mometa.epqos.EpqosEgress import EpqosEgress
from ucsmsdk.mometa.equipment.EquipmentBinding import EquipmentBinding
from ucsmsdk.mometa.equipment.EquipmentChassisProfile import EquipmentChassisProfile
from ucsmsdk.mometa.equipment.EquipmentComputeConn import EquipmentComputeConn
from ucsmsdk.mometa.equipment.EquipmentComputeConnPolicy import EquipmentComputeConnPolicy
from ucsmsdk.mometa.fabric.FabricEthLanEp import FabricEthLanEp
from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
from ucsmsdk.mometa.fabric.FabricEthVlanPc import FabricEthVlanPc
from ucsmsdk.mometa.fabric.FabricEthVlanPortEp import FabricEthVlanPortEp
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.firmware.FirmwareAutoSyncPolicy import FirmwareAutoSyncPolicy
from ucsmsdk.mometa.firmware.FirmwareCatalogPack import FirmwareCatalogPack
from ucsmsdk.mometa.firmware.FirmwareChassisPack import FirmwareChassisPack
from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import FirmwareComputeHostPack
from ucsmsdk.mometa.firmware.FirmwareExcludeChassisComponent import FirmwareExcludeChassisComponent
from ucsmsdk.mometa.firmware.FirmwareExcludeServerComponent import FirmwareExcludeServerComponent
from ucsmsdk.mometa.firmware.FirmwarePackItem import FirmwarePackItem
from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock
from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
from ucsmsdk.mometa.ls.LsBinding import LsBinding
from ucsmsdk.mometa.ls.LsPower import LsPower
from ucsmsdk.mometa.ls.LsPower import LsPower
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.ls.LsServerExtension import LsServerExtension
from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
from ucsmsdk.mometa.ls.LsVersionBeh import LsVersionBeh
from ucsmsdk.mometa.lsboot.LsbootDef import LsbootDef
from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage
from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy
from ucsmsdk.mometa.lstorage.LstorageControllerRef import LstorageControllerRef
from ucsmsdk.mometa.lstorage.LstorageControllerRef import LstorageControllerRef
from ucsmsdk.mometa.lstorage.LstorageDasScsiLun import LstorageDasScsiLun
from ucsmsdk.mometa.lstorage.LstorageDiskGroupConfigPolicy import LstorageDiskGroupConfigPolicy
from ucsmsdk.mometa.lstorage.LstorageDiskGroupConfigPolicy import LstorageDiskGroupConfigPolicy
from ucsmsdk.mometa.lstorage.LstorageDiskGroupQualifier import LstorageDiskGroupQualifier
from ucsmsdk.mometa.lstorage.LstorageDiskGroupQualifier import LstorageDiskGroupQualifier
from ucsmsdk.mometa.lstorage.LstorageDiskSlot import LstorageDiskSlot
from ucsmsdk.mometa.lstorage.LstorageDiskSlot import LstorageDiskSlot
from ucsmsdk.mometa.lstorage.LstorageDiskZoningPolicy import LstorageDiskZoningPolicy
from ucsmsdk.mometa.lstorage.LstorageDiskZoningPolicy import LstorageDiskZoningPolicy
from ucsmsdk.mometa.lstorage.LstorageLocalDiskConfigRef import LstorageLocalDiskConfigRef
from ucsmsdk.mometa.lstorage.LstorageProfile import LstorageProfile
from ucsmsdk.mometa.lstorage.LstorageProfileBinding import LstorageProfileBinding
from ucsmsdk.mometa.lstorage.LstorageVirtualDriveDef import LstorageVirtualDriveDef
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock
from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.power.PowerMgmtPolicy import PowerMgmtPolicy
from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy
from ucsmsdk.mometa.qosclass.QosclassDefinition import QosclassDefinition
from ucsmsdk.mometa.qosclass.QosclassEthBE import QosclassEthBE
from ucsmsdk.mometa.qosclass.QosclassEthClassified import QosclassEthClassified
from ucsmsdk.mometa.qosclass.QosclassFc import QosclassFc
from ucsmsdk.mometa.storage.StorageLocalDisk import StorageLocalDisk
from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef
from ucsmsdk.mometa.vnic.VnicDefBeh import VnicDefBeh
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy
from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicVnicBehPolicy import VnicVnicBehPolicy

filename = "C:\Users\Administrator\Box Sync\PythonSDS\ucsm.json"
txtname = "C:\Users\Administrator\Box Sync\PythonSDS\ucsm_sds_config.txt"
#filename = "/root/python_sds/ucsm.json"

# Write results into txt file
filetxt = open(txtname, "w")

#Read JSON data into the settings_file variable
print "Reading JSON File"
file = open(filename, "r")
settings_file = json.load(file)
file.close()

# Login to UCS Manager
print "\nLogging into UCSM"
handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=settings_file['secure'])
handle.login()
ucsm_login = handle.login()
if ucsm_login == True:
	print 'Login successful'.format()
	filetxt.write("Login successful\n")
else:
	print 'Please check your credentials'.format()

# Set NTP Server
mo = handle.query_dn("sys/svc-ext/datetime-svc")
mo.timezone = settings_file['timezone']
mo.policy_owner = "local"
mo.admin_state = "enabled"
mo.port = "0"
mo_ntp = CommNtpProvider(parent_mo_or_dn=mo, name=settings_file['ntp'])
handle.set_mo(mo)
print "\nSet Timezone to " + "\033[33m" + settings_file['timezone'] + "\033[0m" + " and NTP Server to " + "\033[33m" + settings_file['ntp'] + "\033[0m"
filetxt.write("\nSet Timezone to " + settings_file['timezone'] + " and NTP Server to " + settings_file['ntp'])
handle.commit()

# Set Global Chassis Discovery Policies
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-discovery")
mo.multicast_hw_hash = "disabled"
mo.backplane_speed_pref = "40G"
mo.policy_owner = "local"
mo.action = "platform-max"
mo.rebalance = "user-acknowledged"
mo.link_aggregation_pref = "none"
handle.set_mo(mo)
print "\nSet Backplane to 40G, Platform-Max and No-Link-Group-Preference"
filetxt.write("\nSet Backplane to 40G, Platform-Max and No-Link-Group-Preference")
handle.commit()

# Set Server Discovery Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/server-discovery")
mo.action = "immediate"
mo.policy_owner = "local"
mo.name = "default"
handle.set_mo(mo)
print "Set Server Discovery Policy to Immediate"
filetxt.write("Set Server Discovery Policy to Immediate")
handle.commit()

# Set Rack Server Discovery Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/server-mgmt-policy")
mo.action = "auto-acknowledged"
mo.policy_owner = "local"
mo.name = "default"
handle.set_mo(mo)
print "Set Rack Server Discovery Policy to Auto-Acknowledged"
filetxt.write("Set Rack Server Discovery Policy to Auto-Acknowledged")
handle.commit()

# Set Power Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/psu-policy")
mo.policy_owner = "local"
mo.redundancy = "n+1"
handle.set_mo(mo)
print "Set Power Policy to N+1"
filetxt.write("Set Power Policy to N+1")
handle.commit()

# Set Global Power Allocation Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/pwr-mgmt-policy")
mo.style = "intelligent-policy-driven"
mo.profiling = "no"
mo.name = "default"
mo.skip_power_deploy_check = "no"
mo.policy_owner = "local"
mo.skip_power_check = "no"
handle.set_mo(mo)
print "Set Global Power Allocation Policy to Policy Driven"
filetxt.write("Set Global Power Allocation Policy to Policy Driven")
handle.commit()

# Set Port Discovery Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/port-discovery")
print "Set Server Port Auto Configure Policy"
filetxt.write("Set Server Port Auto Configure Policy")
handle.commit()

# Set Hardware Change Discovery Policy
obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/hw-change-disc-policy")
print "Set HW Change Discovery Policy"
filetxt.write("Set HW Change Discovery Policy")
handle.commit()

# Set IP Pool
obj = handle.query_dn("org-root")
mo = IppoolPool(parent_mo_or_dn=obj, is_net_bios_enabled="disabled", name="ext-mgmt", policy_owner="local", ext_managed="internal", supports_dhcp="disabled", guid="00000000-0000-0000-0000-000000000000", assignment_order="sequential")
mo_1 = IppoolBlock(parent_mo_or_dn=mo, subnet=settings_file['ippool_subnet'], sec_dns=settings_file['ippool_sec_dns'], r_from=settings_file['ippool_start_from'], def_gw=settings_file['ippool_gw'], to=settings_file['ippool_end_to'], prim_dns=settings_file['ippool_prim_dns'])
handle.add_mo(mo, True)
print "\nCreated IP Pool with Subnet " + "\033[33m" + settings_file['ippool_subnet'] + "\033[0m" + ", IP Range " + "\033[33m" + settings_file['ippool_start_from'] + " - " + settings_file['ippool_end_to'] + "\033[0m" + ", Gateway " + "\033[33m" + settings_file['ippool_gw'] + "\033[0m" + " and DNS " + "\033[33m" + settings_file['ippool_prim_dns'] + "\033[0m"
filetxt.write("\nCreated IP Pool with Subnet " + settings_file['ippool_subnet'] + ", IP Range " + settings_file['ippool_start_from'] + " - " + settings_file['ippool_end_to'] + ", Gateway " + settings_file['ippool_gw'] + " and DNS " + settings_file['ippool_prim_dns'])
handle.commit()

# Set MAC Pool
obj = handle.query_dn("org-root")
mo = MacpoolPool(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['macpool_name'], assignment_order="sequential")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to=settings_file['macpool_end_to'], r_from=settings_file['macpool_start_from'])
handle.add_mo(mo, True)
print "\nCreated MAC Pool with Name " + "\033[33m" + settings_file['macpool_name'] + "\033[0m" + " and Range " + "\033[33m" + settings_file['macpool_start_from'] + " - " + settings_file['macpool_end_to'] + "\033[0m"
filetxt.write("\nCreated MAC Pool with Name " + settings_file['macpool_name'] + " and Range " + settings_file['macpool_start_from'] + " - " + settings_file['macpool_end_to'])
handle.commit()

# Set UUID Pool
obj = handle.query_dn("org-root")
obj_1 = handle.query_classid("uuidpoolPool")
for uuid in obj_1[:1]:
	uuidprefix = str(uuid.prefix)
mo = UuidpoolPool(parent_mo_or_dn=obj, prefix=uuidprefix, policy_owner="local", assignment_order="sequential", name=settings_file['uuidpool_name'])
mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to=settings_file['uuidpool_end_to'], r_from=settings_file['uuidpool_start_from'])
handle.add_mo(mo, True)
print "\nCreated UUID Pool with Name " + "\033[33m" + settings_file['uuidpool_name'] + "\033[0m" + " and Range " + "\033[33m" + settings_file['uuidpool_start_from'] + " - " + settings_file['uuidpool_end_to'] + "\033[0m"
filetxt.write("\nCreated UUID Pool with Name " + settings_file['uuidpool_name'] + " and Range " + settings_file['uuidpool_start_from'] + " - " + settings_file['uuidpool_end_to'])
handle.commit()

# Set Network Control Policy
obj = handle.query_dn("org-root")
mo = NwctrlDefinition(parent_mo_or_dn=obj, lldp_transmit="disabled", name=settings_file['cdp_name'], lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="enabled", uplink_fail_action="link-down")
mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local")
handle.add_mo(mo, True)
print "\nCreated Network Control Policy with Name " + "\033[33m" + settings_file['cdp_name'] + "\033[0m"
filetxt.write("\nCreated Network Control Policy with Name " + settings_file['cdp_name'])
handle.commit()

# Set Boot Policy
obj = handle.query_dn("org-root")
mo = LsbootPolicy(parent_mo_or_dn=obj, enforce_vnic_name="yes", policy_owner="local", boot_mode="legacy", name=settings_file['bootpolicy_name'], reboot_on_update="no")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-local", lun_id="0", order="2")
mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
mo_3 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
mo_4 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_3, order="1")
handle.add_mo(mo, True)
print "\nCreated Boot Policy with name " + "\033[33m" + settings_file['bootpolicy_name'] + "\033[0m"
filetxt.write("\nCreated Boot Policy with name " + settings_file['bootpolicy_name'])
handle.commit()

# Set Server Maintenance Policy
obj = handle.query_dn("org-root")
mo = LsmaintMaintPolicy(parent_mo_or_dn=obj, soft_shutdown_timer="150-secs", policy_owner="local", uptime_disr="user-ack", name=settings_file['servermaintpolicy_name'])
handle.add_mo(mo, True)
print "\nCreated Server Maintenance Policy with name " + "\033[33m" + settings_file['servermaintpolicy_name'] + "\033[0m"
filetxt.write("\nCreated Server Maintenance Policy with name " + settings_file['servermaintpolicy_name'])
handle.commit()

# Set Power Control Policy
obj = handle.query_dn("org-root")
mo = PowerPolicy(parent_mo_or_dn=obj, fan_speed="any", policy_owner="local", prio="no-cap", name=settings_file['powercontrolpolicy_name'])
handle.add_mo(mo, True)
print "\nSet Power Control Policy with name " + "\033[33m" + settings_file['powercontrolpolicy_name'] + "\033[0m"
filetxt.write("\nSet Power Control Policy with name " + settings_file['powercontrolpolicy_name'])
handle.commit()

# Set FI Uplink Ports
mo = handle.query_dn("fabric/lan/A")
for i in settings_file['uplinkport']:
	mo_1 = FabricEthLanEp(parent_mo_or_dn=mo, eth_link_profile_name="default", flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="no", slot_id="1", admin_state="enabled", port_id=i)
	handle.add_mo(mo_1, True)
mo_2 = handle.query_dn("fabric/lan/B")
for i in settings_file['uplinkport']:
	mo_3 = FabricEthLanEp(parent_mo_or_dn=mo_2, eth_link_profile_name="default", flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="no", slot_id="1", admin_state="enabled", port_id=i)
	handle.add_mo(mo_3, True)
print "\nSet Uplink Ports on both FI to " + "\033[33m" + ', '.join(settings_file['uplinkport']) + "\033[0m"
filetxt.write("\nSet Uplink Ports on both FI to " + ', '.join(settings_file['uplinkport']))
handle.commit()

# Set FI vPC
mo = handle.query_dn("fabric/lan/A")
mo_1 = FabricEthLanPc(parent_mo_or_dn=mo, name=settings_file['vpc_name'][0], flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="40gbps", port_id=settings_file['vpc_id'][0], lacp_policy_name="default")
for i in settings_file['uplinkport']:
	mo_2 = FabricEthLanPcEp(parent_mo_or_dn=mo_1, admin_state="enabled", auto_negotiate="no", slot_id="1", port_id=i, eth_link_profile_name="default")
	handle.add_mo(mo_1, True)
mo_3 = handle.query_dn("fabric/lan/B")
mo_4 = FabricEthLanPc(parent_mo_or_dn=mo_3, name=settings_file['vpc_name'][1], flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="40gbps", port_id=settings_file['vpc_id'][1], lacp_policy_name="default")
for i in settings_file['uplinkport']:
	mo_5 = FabricEthLanPcEp(parent_mo_or_dn=mo_4, admin_state="enabled", auto_negotiate="no", slot_id="1", port_id=i, eth_link_profile_name="default")
	handle.add_mo(mo_4, True)
print "\nCreated vPC " + "\033[33m" + ', '.join(settings_file['vpc_name']) + "\033[0m" + " with ID " + "\033[33m" + ', '.join(settings_file['vpc_id']) + "\033[0m" + " on Uplink Ports"
filetxt.write("\nCreated vPC " + ', '.join(settings_file['vpc_name']) + " with ID " + ', '.join(settings_file['vpc_id']) + " on Uplink Ports")
handle.commit()

# Create VLANs and set native VLAN
mo = handle.query_dn("fabric/lan")
for i,j in zip(settings_file['vlan_name'], settings_file['vlan_id']):
	mo_1 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name=i, compression_type="included", policy_owner="local", default_net="no", id=j)
	handle.add_mo(mo_1, True)
mo_2 = settings_file['vlan_name'].index(settings_file['vlan_native'])	
mo_3 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name=settings_file['vlan_native'], compression_type="included", policy_owner="local", default_net="yes", id=settings_file['vlan_id'][mo_2])
handle.add_mo(mo_3, True)
print "\nCreated VLANs with Name " + "\033[33m" + ', '.join(settings_file['vlan_name']) + "\033[0m" + " and ID " + "\033[33m" + ', '.join(settings_file['vlan_id']) + "\033[0m" + " and set Native VLAN to " + "\033[33m" + settings_file['vlan_native'] + "\033[0m"
filetxt.write("\nCreated VLANs with Name " + ', '.join(settings_file['vlan_name']) + " and ID " + ', '.join(settings_file['vlan_id']) + " and set Native VLAN to " + settings_file['vlan_native'])
handle.commit()

# Create QoS System Class
mo = QosclassDefinition(parent_mo_or_dn=mo, policy_owner="local")
mo_1 = QosclassEthBE(parent_mo_or_dn=mo, multicast_optimize="no", weight=settings_file['qos_besteffort'][0], mtu=settings_file['qos_besteffort'][1])
handle.add_mo(mo_1, True)
mo_2 = QosclassFc(parent_mo_or_dn=mo, cos=settings_file['qos_fc'][0], weight=settings_file['qos_fc'][1])
handle.add_mo(mo_2, True)
if settings_file['qos_class'] == 'yes':
	for i,j,k,m,n in zip(settings_file['qos_priority'], settings_file['qos_cos'], settings_file['qos_packet_drop'], settings_file['qos_weight'], settings_file['qos_mtu']):
		mo_3 = QosclassEthClassified(parent_mo_or_dn=mo, cos=j, weight=m, drop=k, multicast_optimize="no", mtu=n, priority=i, admin_state="enabled")
		handle.add_mo(mo_3, True)
	print "\nCreated QoS System Class with Priority " + "\033[33m" + ', '.join(settings_file['qos_priority']) + "\033[0m"
	filetxt.write("\nCreated QoS System Class with Priority " + ', '.join(settings_file['qos_priority']))
handle.set_mo(mo)
handle.commit()

# Create QoS Policies
obj = handle.query_dn("org-root")
if settings_file['qos_class'] == 'yes':
	for i,j in zip(settings_file['qos_name'], settings_file['qos_priority']):
		mo = EpqosDefinition(parent_mo_or_dn=obj, policy_owner="local", name=i)
		mo_1 = EpqosEgress(parent_mo_or_dn=mo, rate="line-rate", host_control="none", prio=j, burst="10240")
		handle.add_mo(mo, True)
	print "\nCreated QoS Policies " + "\033[33m" + ', '.join(settings_file['qos_name']) + "\033[0m"
	filetxt.write("\nCreated QoS Policies " + ', '.join(settings_file['qos_name']))
handle.commit()

# Create Adapter Policy for Linux
obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['adapterpolicy_name'])
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_3 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_4 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_5 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="8", ring_size="4096")
mo_6 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="16")
mo_7 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="8", ring_size="4096")
mo_8 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_9 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_10 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_11 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_12 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="32", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_13 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
print "\nCreated Adapter Policy " + "\033[33m" + settings_file['adapterpolicy_name'] + "\033[0m"
filetxt.write("\nCreated Adapter Policy " + settings_file['adapterpolicy_name'])
handle.commit()

# Create VNIC Adapter
vnic_number = input("\nHow many vNIC would you like to create?: ")
obj = handle.query_dn("org-root")
for i in range(1, vnic_number + 1):
	vnic_name = raw_input("What is the name of vNIC " + str(i) + "?: ")
	vnic_switch = raw_input("What is the Fabric ID? [A-B, B-A, A, B]: ")
	vnic_mtu = raw_input("What is the MTU size? [default, 9000]: ")
	if settings_file['qos_policy'] == 'yes':
		vnic_qos = raw_input("What is the QoS Policy to use? [" + ', '.join(settings_file['qos_name']) + "]: ")
	vnic_vlan = raw_input("What is the VLAN to use? [" + ', '.join(settings_file['vlan_name']) + "]: ")
	vnic_vlannative = raw_input("Native VLAN? [yes, no]: ")
	mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name=vnic_name, stats_policy_name="default", switch_id=vnic_switch, mtu=vnic_mtu, policy_owner="local", templ_type="updating-template", qos_policy_name=vnic_qos, target="adaptor", ident_pool_name=settings_file['macpool_name'], cdn_source="vnic-name", nw_ctrl_policy_name=settings_file['cdp_name'])
	if vnic_vlan == 'yes':
		mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name=vnic_vlan)
	else:
		mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name=vnic_vlan)
	handle.add_mo(mo, True)
	print "\nCreated vNIC with name " + "\033[33m" + vnic_name + "\033[0m"
	filetxt.write("\nCreated vNIC with name " + vnic_name)
handle.commit()

# Create LAN Connectivity Policy
lanconn = raw_input("\nDo you wish to create a LAN Connectivity Policy? [yes, no]: ")
if lanconn == 'yes':
	lanconn_number = input("\nHow many LAN Connectivity Policies would you like to create?: ")
	obj = handle.query_dn("org-root")
	vnic = handle.query_classid("vniclanConnTempl")
	vnic_1 = []
	for j in range(1, lanconn_number + 1):
		lanconn_policyname = raw_input("What is the name of Policy " + str(j) + "?: ")
		mo = VnicLanConnPolicy(parent_mo_or_dn=obj, policy_owner="local", name=lanconn_policyname)
		for i in vnic:
			vnic_1.append(i.name)
		lanconn_vnic = raw_input("What vNICs would you like to add to the Policy? Please list in the right order. [" + ", ".join(vnic_1) + "]: ")
		lanconn_vnic = lanconn_vnic.split(", ")
		lanconn_vnicname = raw_input("What are the names of the vNICs? Please list in the same order: ")
		lanconn_vnicname = lanconn_vnicname.split(", ")
		lanconn_vnicorder = range(1, len(lanconn_vnic) + 1)
		lanconn_vnicid = range(0, len(lanconn_vnic))
		for k, l, m, n in zip(lanconn_vnic, lanconn_vnicname, lanconn_vnicorder, lanconn_vnicid):
			vnic = handle.query_classid("vniclanConnTempl", filter_str="(name, " + k + ", type='eq')")
			for o in vnic:
				vnic_2 = []
				vnic_2.extend([o.switch_id, o.qos_policy_name, o.mtu, o.name])
				mo_1 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name=settings_file['cdp_name'], admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id=str(vnic_2[0]), name=lanconn_vnicname[n], order=str(m), qos_policy_name=str(vnic_2[1]), adaptor_profile_name=settings_file['adapterpolicy_name'], ident_pool_name=settings_file['macpool_name'], cdn_source="vnic-name", mtu=str(vnic_2[2]), nw_templ_name=str(vnic_2[3]), addr="derived")
				handle.add_mo(mo, True)
		print "\nCreated LAN Connectivity Policy with name " + "\033[33m" + lanconn_policyname + "\033[0m" + " and vNICs " + "\033[33m" + ", ".join(lanconn_vnicname) + "\033[0m"
		filetxt.write("\nCreated LAN Connectivity Policy with name " + lanconn_policyname + " and vNICs " + ", ".join(lanconn_vnicname))
handle.commit()

# Set Host FW Package
obj = handle.query_dn("org-root")
mo = FirmwareComputeHostPack(parent_mo_or_dn=obj, ignore_comp_check="yes", name=settings_file['hostfw_name'], stage_size="0", rack_bundle_version=settings_file['hostfw_package'], update_trigger="immediate", policy_owner="local", mode="staged", override_default_exclusion="yes")
mo_1 = FirmwareExcludeServerComponent(parent_mo_or_dn=mo, server_component="local-disk")
handle.add_mo(mo, True)
print "\nCreated Host FW Policy with Package " + "\033[33m" + settings_file['hostfw_package'] + "\033[0m"
filetxt.write("\nCreated Host FW Policy with Package " + settings_file['hostfw_package'])
handle.commit()

# Set Chassis FW Package
obj = handle.query_dn("org-root")
mo = FirmwareChassisPack(parent_mo_or_dn=obj, chassis_bundle_version=settings_file['chassisfw_package'], name=settings_file['chassisfw_name'], stage_size="0", update_trigger="immediate", force_deploy="no", policy_owner="local", mode="staged", override_default_exclusion="yes")
mo_1 = FirmwareExcludeChassisComponent(parent_mo_or_dn=mo, chassis_component="local-disk")
handle.add_mo(mo, True)
print "\nCreated Chassis FW Policy with Package " + "\033[33m" + settings_file['chassisfw_package'] + "\033[0m"
filetxt.write("\nCreated Chassis FW Policy with Package " + settings_file['chassisfw_package'])
handle.commit()

# Set Chassis Maintenance Policy
obj = handle.query_dn("org-root")
mo = CpmaintMaintPolicy(parent_mo_or_dn=obj, policy_owner="local", uptime_disr="user-ack", name=settings_file['chassismaint_name'])
handle.add_mo(mo, True)
print "\nCreated Chassis Maintenance Policy with Name " + "\033[33m" + settings_file['chassismaint_name'] + "\033[0m" + " and User_Ack"
filetxt.write("\nCreated Chassis Maintenance Policy with Name " + settings_file['chassismaint_name'] + " and User_Ack")
handle.commit()

# Set Compute Connection Policy
obj = handle.query_dn("org-root")
if settings_file['computeconn_policy'] == 'Single':
	mo = EquipmentComputeConnPolicy(parent_mo_or_dn=obj, policy_owner="local", server_sioc_connectivity="single-server-single-sioc" , name=settings_file['computeconn_name'])
else:
	mo = EquipmentComputeConnPolicy(parent_mo_or_dn=obj, policy_owner="local", server_sioc_connectivity="single-server-dual-sioc" , name=settings_file['computeconn_name'])
handle.add_mo(mo, True)
print "\nCreated Chassis Connection Policy with Name " + "\033[33m" + settings_file['computeconn_name'] + "\033[0m" + " and Single Server " + "\033[33m" + settings_file['computeconn_policy'] + "\033[0m" + " SIOC"
filetxt.write("\nCreated Chassis Connection Policy with Name " + settings_file['computeconn_name'] + " and Single Server " + settings_file['computeconn_policy'] + " SIOC")
handle.commit()

# Set Disk Zoning Policy
def parse_range(rng):
    parts = rng.split('-')
    if 1 > len(parts) > 2:
        raise ValueError("Bad range: '%s'" % (rng,))
    parts = [int(i) for i in parts]
    start = parts[0]
    end = start if len(parts) == 1 else parts[1]
    if start > end:
        end, start = start, end
    return range(start, end + 1)
	
def parse_range_list(rngs):
    return sorted(set(chain(*[parse_range(rng) for rng in rngs.split(',')])))
	
disks_server1 = list(parse_range_list(settings_file['disknumber_server1']))
disks_server2 = list(parse_range_list(settings_file['disknumber_server2']))
obj = handle.query_dn("org-root")
mo = LstorageDiskZoningPolicy(parent_mo_or_dn=obj, preserve_config="no", policy_owner="local", name=settings_file['diskzone_name'])
if settings_file['disknumber_server2'] == '0':
	for i in disks_server1:
		mo_1 = LstorageDiskSlot(parent_mo_or_dn=mo, id=str(i), ownership="dedicated")
		mo_2 = LstorageControllerRef(parent_mo_or_dn=mo_1, controller_type="SAS", server_id="1", controller_id="1")
	handle.add_mo(mo, True)
	print "\nCreated Chassis Disk Zoning Policy with Name " + "\033[33m" + settings_file['diskzone_name'] + "\033[0m" + " and disks " + "\033[33m" + str(disks_server1) + "\033[0m"
	filetxt.write("\nCreated Chassis Disk Zoning Policy with Name " + settings_file['diskzone_name'] + " and disks " + str(disks_server1))
else:
	for i,j in zip(disks_server1, disks_server2):
		mo_1 = LstorageDiskSlot(parent_mo_or_dn=mo, id=str(i), ownership="dedicated")
		mo_2 = LstorageControllerRef(parent_mo_or_dn=mo_1, controller_type="SAS", server_id="1", controller_id="1")
		mo_3 = LstorageDiskSlot(parent_mo_or_dn=mo, id=str(j), ownership="dedicated")
		mo_4 = LstorageControllerRef(parent_mo_or_dn=mo_3, controller_type="SAS", server_id="2", controller_id="1")
	handle.add_mo(mo, True)
	print "\nCreated Chassis Disk Zoning Policy with Name " + "\033[33m" + settings_file['diskzone_name'] + "\033[0m" + " and disks " + "\033[33m" + str(disks_server1) + str(disks_server2) + "\033[0m"
	filetxt.write("\nCreated Chassis Disk Zoning Policy with Name " + settings_file['diskzone_name'] + " and disks " + str(disks_server1) + str(disks_server2))
handle.commit()

# Create and bind Chassis Profile
obj = handle.query_dn("org-root")
for i,j in zip(settings_file['chassisprofile_name'], settings_file['chassisdn']):
	mo = EquipmentChassisProfile(parent_mo_or_dn=obj, name=i, compute_conn_policy_name=settings_file['computeconn_name'], maint_policy_name=settings_file['chassismaint_name'], policy_owner="local", chassis_fw_policy_name=settings_file['chassisfw_name'], resolve_remote="yes", type="instance", disk_zoning_policy_name=settings_file['diskzone_name'])
	mo_1 = EquipmentBinding(parent_mo_or_dn=mo, chassis_dn="sys/" + j, restrict_migration="no")
	handle.add_mo(mo, True)
print "\nWaiting until Chassis Profile(s) is/are associated"
handle.commit()
sleep(40)
print "\nCreated Chassis Profile " + "\033[33m" + ', '.join(settings_file['chassisprofile_name']) + "\033[0m" + " for " + "\033[33m" + ', '.join(settings_file['chassisdn']) + "\033[0m"
filetxt.write("\nCreated Chassis Profile " + ', '.join(settings_file['chassisprofile_name']) + " for " + ', '.join(settings_file['chassisdn']))

# Set Boot Disks to Unconfigured Good
print "\nSetting Boot Disks to Unconfigured Good. This can take up to 5 minutes"
filter = '(variant_type,"C3000_BOOT",type="eq") and (disk_state,"jbod",type="eq")'
filter_1 = '(variant_type,"default",type="eq") and (disk_state,"jbod",type="eq")'
obj_1 = handle.query_classid("StorageLocalDisk", filter_str=filter)
obj_2 = handle.query_classid("StorageLocalDisk", filter_str=filter_1)
for i in obj_1:
	disk = i.dn
	disk_1 = disk.split('/disk-')[0]
	mo = StorageLocalDisk(parent_mo_or_dn=disk_1, admin_action="unconfigured-good", id=i.id, admin_action_trigger="triggered")
	handle.add_mo(mo, True)
for j in obj_2:
	disk_2 = j.dn
	disk_3 = disk_2.split('/disk-')[0]
	mo_1 = StorageLocalDisk(parent_mo_or_dn=disk_3, admin_action="unconfigured-good", id=j.id, admin_action_trigger="triggered")
	handle.add_mo(mo_1, True)
print "Set Boot Disks of all C220 and S3260 to Unconfigured Good"
filetxt.write("Set Boot Disks of all C220 and S3260 to Unconfigured Good")
handle.commit()

# Configure S3260 Top Loaded Disks
print "\nSetting S3260 Top Loaded Disks to Unconfigured Good and/or JBOD. This can take up to 5 minutes"
disksgood = list(parse_range_list(settings_file['disk_good']))
disksjbod = list(parse_range_list(settings_file['disk_jbod']))
filter_enclosure = '(num_slots,"56",type="eq")'
obj = handle.query_classid("storageEnclosure", filter_str=filter_enclosure)
for i in obj:
	filter_diskgood = '(variant_type,"C3000_TOP",type="eq") and (disk_state,"unconfigured-good",type="eq")'
	obj_1 = handle.query_children(in_mo=i, class_id="StorageLocalDisk", filter_str=filter_diskgood)
	disksgood_1 = []
	for j in obj_1:
		disksgood_1.append(j.id)
	disksgood_2 = map(int,disksgood_1)
	disksgood_3 =[]
	for k in disksgood:
		if k not in disksgood_2:
			disksgood_3.append(k)
	for l in disksgood_3:
		mo = StorageLocalDisk(parent_mo_or_dn=i.dn, admin_action="unconfigured-good", id=str(l), admin_action_trigger="triggered")
		handle.add_mo(mo, True)	
for m in obj:
	filter_diskjbod = '(variant_type,"C3000_TOP",type="eq") and (disk_state,"jbod",type="eq")'
	obj_2 = handle.query_children(in_mo=m, class_id="StorageLocalDisk", filter_str=filter_diskjbod)
	disksjbod_1 = []
	for n in obj_2:
		disksjbod_1.append(n.id)
	disksjbod_2 = map(int,disksjbod_1)
	disksjbod_3 = []
	for o in disksjbod:
		if o not in disksjbod_2:
			disksjbod_3.append(o)
	for p in disksjbod_3:
		mo = StorageLocalDisk(parent_mo_or_dn=m.dn, admin_action="jbod", id=str(p), admin_action_trigger="triggered")
		handle.add_mo(mo, True)	
print "Converted Disks "  + "\033[33m" + str(disksgood) + "\033[0m" + " to Unconfigured Good and Disks "  + "\033[33m" + str(disksjbod) + "\033[0m" + " to JBOD"
filetxt.write("Converted S3260 Top Loaded Disks "  + str(disksgood) + " to Unconfigured Good and Disks "  + str(disksjbod) + " to JBOD")
handle.commit()

# Create S3260 Disk Group Boot Policy
disk_raid0 = raw_input("\nDo you wish to create RAID 0 disk groups per top loaded HDD? [yes, no]: ")
if disk_raid0 == 'yes':
	disk_raid0name = raw_input("What should be the starting name of the Disk Group Policy?: ")
	disk_accesspolicy = raw_input("What should be the Access Policy? [platform-default, read-write, read-only, blocked]: ")
	disk_readpolicy = raw_input("What should be the Read Policy? [platform-default, read-ahead, normal]: ")
	disk_writepolicy = raw_input("What should be the Write Cache Policy? [platform-default, write-through, write-back-good-bbu, always-write-back]: ")
	disk_iopolicy = raw_input("What should be the IO Policy? [platform-default, direct, cached]: ")
	disk_cachepolicy = raw_input("What should be the Drive Cache Policy? [platform-default, no-change, enable, disable]: ")
	for i in disksgood:
		obj = handle.query_dn("org-root")
		mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", name=disk_raid0name + str(i))
		mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy=disk_readpolicy, drive_cache=disk_cachepolicy, strip_size="platform-default", io_policy=disk_iopolicy, write_cache_policy=disk_writepolicy, security="no", access_policy=disk_accesspolicy)
		mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num=str(i), span_id="unspecified")
		handle.add_mo(mo, True)
obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="mirror", name=settings_file['s3260_diskgroupbootpolicy'])
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", security="no", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="202", span_id="unspecified")
mo_3 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="201", span_id="unspecified")
handle.add_mo(mo, True)
if disk_raid0 == 'yes':
	print "\nCreated Disk Group Boot Policy " + "\033[33m" + settings_file['s3260_diskgroupbootpolicy'] + "\033[0m" + " and individual RAID0 Disk Group Policies for S3260"
	filetxt.write("\nCreated Disk Group Boot Policy " + settings_file['s3260_diskgroupbootpolicy'] + " and individual RAID0 Disk Group Policies for S3260")
else:
	print "\nCreated Disk Group Boot Policy " + "\033[33m" + settings_file['s3260_diskgroupbootpolicy'] + "\033[0m" + " for S3260"
	filetxt.write("\nCreated Disk Group Boot Policy " + settings_file['s3260_diskgroupbootpolicy'] + " for S3260")
handle.commit()

# Create C220 Disk Group Boot Policy
obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="mirror", name=settings_file['c220_diskgroupbootpolicy'])
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", security="no", access_policy="platform-default")
mo_2 = LstorageDiskGroupQualifier(parent_mo_or_dn=mo, use_jbod_disks="no", use_remaining_disks="yes", num_ded_hot_spares="unspecified", drive_type="HDD", num_drives="2", min_drive_size="unspecified", num_glob_hot_spares="unspecified")
handle.add_mo(mo, True)
print "\nCreated Disk Group Boot Policy " + "\033[33m" + settings_file['c220_diskgroupbootpolicy'] + "\033[0m" + " for C220"
filetxt.write("\nCreated Disk Group Boot Policy " + settings_file['c220_diskgroupbootpolicy'] + " for C220")
handle.commit()

# Create C220 Storage Profile
obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['c220_storageprofilepolicy'])
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=settings_file['c220_diskgroupbootpolicy'], auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['c220_storageprofilelun'])
handle.add_mo(mo, True)
print "\nCreated C220 Storage Profile " + "\033[33m" + settings_file['c220_storageprofilepolicy'] + "\033[0m"
filetxt.write("\nCreated C220 Storage Profile " + settings_file['c220_storageprofilepolicy'])
handle.commit()

# Create S3260 Storage Profile
disks_server1 = list(parse_range_list(settings_file['disknumber_server1']))
disks_server2 = list(parse_range_list(settings_file['disknumber_server2']))
disksgood = list(parse_range_list(settings_file['disk_good']))
s3260_blade = raw_input("How many S3260 Blades do you have per Chassis?: ")
if s3260_blade == '1':
	if disk_raid0 == 'yes':
		obj = handle.query_dn("org-root")
		mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['s32601_storageprofilepolicy'])
		mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=settings_file['s3260_diskgroupbootpolicy'], auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32601_storageprofilebootlun'])
		for i in disksgood:
			mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=disk_raid0name + str(i), auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32601_storageprofileraidlun'] + str(i))
			handle.add_mo(mo, True)
	else:
		obj = handle.query_dn("org-root")
		mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['s32601_storageprofilepolicy'])
		mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=settings_file['s3260_diskgroupbootpolicy'], auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32601_storageprofilebootlun'])
		handle.add_mo(mo, True)
	print "\nCreated S3260 Storage Profile " + "\033[33m" + settings_file['s32601_storageprofilepolicy'] + "\033[0m"
	filetxt.write("\nCreated S3260 Storage Profile " + settings_file['s32601_storageprofilepolicy'])
else:
	if disk_raid0 == 'yes':
		obj = handle.query_dn("org-root")
		mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['s32601_storageprofilepolicy'])
		mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=settings_file['s3260_diskgroupbootpolicy'], auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32601_storageprofilebootlun'])
		disks1_server1 = []
		disks1_server2 = []
		for j in disks_server1:
			if j in disksgood:
				disks1_server1.append(j)
		for k in disks1_server1:
			mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name=disk_raid0name + str(k), auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32601_storageprofileraidlun'] + str(k))
			handle.add_mo(mo, True)
		mo_3 = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name=settings_file['s32602_storageprofilepolicy'])
		mo_4 = LstorageDasScsiLun(parent_mo_or_dn=mo_3, local_disk_policy_name=settings_file['s3260_diskgroupbootpolicy'], auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32602_storageprofilebootlun'])
		for l in disks_server2:
			if l in disksgood:
				disks1_server2.append(l)
		for n in disks1_server2:
			mo_5 = LstorageDasScsiLun(parent_mo_or_dn=mo_3, local_disk_policy_name=disk_raid0name + str(n), auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name=settings_file['s32602_storageprofileraidlun'] + str(n))
			handle.add_mo(mo_3, True)
handle.commit()


# Create C220 Service Profile Template
sp_number = input("\nHow many Service Profiles for C220 would you like to create?: ")
obj = handle.query_dn("org-root")
for i in range(1, sp_number + 1):
	sp220_name = raw_input("\nWhat is the name of the C220 Service Profile " + str(i) + "?: ")
	obj = handle.query_dn("org-root")
	mo = LsServer(parent_mo_or_dn=obj, uuid="derived", name=sp220_name, maint_policy_name=settings_file['servermaintpolicy_name'], stats_policy_name="default", ext_ip_state="none", power_policy_name=settings_file['powercontrolpolicy_name'], boot_policy_name=settings_file['bootpolicy_name'], policy_owner="local", host_fw_policy_name=settings_file['hostfw_name'], scrub_policy_name="default", ident_pool_name=settings_file['uuidpool_name'], resolve_remote="yes", type="instance")
	sp220_lanconn = raw_input("Would you like to use a LAN Connectivity Policy? [yes, no]: ")
	if sp220_lanconn == 'yes':
		sp_lanconn = handle.query_classid("vniclanConnPolicy")
		sp_lanconn_1 = []
		for i in sp_lanconn:
			sp_lanconn_1.append(i.name)
		lanconn_vnic = raw_input("What LAN Connectivity Policy would you like to use? [" + ", ".join(sp_lanconn_1) + "]: ")
		mo_1 = VnicConnDef(parent_mo_or_dn=mo, lan_conn_policy_name=lanconn_vnic)
		handle.add_mo(mo, True)
	else:
		vnic = handle.query_classid("vniclanConnTempl")
		vnic_1 = []
		for i in vnic:
			vnic_1.append(i.name)
		lanconn_vnic = raw_input("What vNICs would you like to add to the Service Profile? Please list in the right order. [" + ", ".join(vnic_1) + "]: ")
		lanconn_vnic = lanconn_vnic.split(", ")
		for i, j in enumerate(lanconn_vnic, 1):
			mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", vnic_name=j, order=str(i), transport="ethernet", admin_host_port="ANY")
			vnic = handle.query_classid("vniclanConnTempl", filter_str="(name, " + j + ", type='eq')")
			for k in vnic:
				vnic_2 = []
				vnic_2.extend([k.switch_id, k.qos_policy_name, k.mtu, k.name])
				mo_2 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name=settings_file['cdp_name'], admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id=str(vnic_2[0]), name=str(j), order=str(i), qos_policy_name=str(vnic_2[1]), adaptor_profile_name=settings_file['adapterpolicy_name'], ident_pool_name=settings_file['macpool_name'], cdn_source="vnic-name", mtu=str(vnic_2[2]), nw_templ_name=str(vnic_2[3]), addr="derived")
			handle.add_mo(mo, True)
	mo_2 = handle.query_classid("lstorageProfile")
	storage = []
	for j in mo_2:
		storage.append(j.name)
	sp_storage = raw_input("What Storage Profile would you like to use? [" + ", ".join(storage) + "]: ")
	mo_3 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name=sp_storage)
	mo_4 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
	mo_5 = LsPower(parent_mo_or_dn=mo, state="up")
	handle.add_mo(mo, True)
	c220_bind = raw_input("Would you like to bind the service profile to a C220 Rack Server?  [yes, no]: ")
	if c220_bind == 'yes':
		rack = '(model,"UCSC-C220-M4S",type="eq") and (oper_state,"unassociated",type="eq")'
		obj_1 = handle.query_classid("computeRackUnit", filter_str=rack)
		rack_1 = []
		for k in obj_1:
			rack_1.append(k.dn)
		rack_2 = raw_input("What C220 Rack Server would you like to use? [" + ", ".join(rack_1) + "]: ")
		mo_6 = LsBinding(parent_mo_or_dn=mo, pn_dn=rack_2, restrict_migration="no", admin_action="unspecified", admin_action_trigger="idle")
	handle.add_mo(mo, True)
	if c220_bind == 'yes':
		print "\nCreated C220 Service Profile Template " + "\033[33m" + sp220_name + "\033[0m" + " and bound it to server " + "\033[33m" + rack_2 + "\033[0m"
		filetxt.write("\nCreated C220 Service Profile Template " + sp220_name + " and bound it to server " + rack_2)
	else:
		print "\nCreated C220 Service Profile Template " + "\033[33m" + sp220_name + "\033[0m"
		filetxt.write("\nCreated C220 Service Profile Template " + sp220_name)
handle.commit()

# Create S3260 Service Profile Template
sp_number = input("\nHow many Service Profiles for S3260 would you like to create?: ")
obj = handle.query_dn("org-root")
for i in range(1, sp_number + 1):
	sp3260_name = raw_input("\nWhat is the name of the S3260 Service Profile " + str(i) + "?: ")
	obj = handle.query_dn("org-root")
	mo = LsServer(parent_mo_or_dn=obj, uuid="derived", name=sp3260_name, maint_policy_name=settings_file['servermaintpolicy_name'], stats_policy_name="default", ext_ip_state="none", power_policy_name=settings_file['powercontrolpolicy_name'], boot_policy_name=settings_file['bootpolicy_name'], policy_owner="local", host_fw_policy_name=settings_file['hostfw_name'], scrub_policy_name="default", ident_pool_name=settings_file['uuidpool_name'], resolve_remote="yes", type="instance")
	sp3260_lanconn = raw_input("Would you like to use a LAN Connectivity Policy? [yes, no]: ")
	if sp3260_lanconn == 'yes':
		sp_lanconn = handle.query_classid("vniclanConnPolicy")
		sp_lanconn_1 = []
		for i in sp_lanconn:
			sp_lanconn_1.append(i.name)
		lanconn_vnic = raw_input("What LAN Connectivity Policy would you like to use? [" + ", ".join(sp_lanconn_1) + "]: ")
		mo_1 = VnicConnDef(parent_mo_or_dn=mo, lan_conn_policy_name=lanconn_vnic)
		handle.add_mo(mo, True)
	else:
		vnic = handle.query_classid("vniclanConnTempl")
		vnic_1 = []
		for i in vnic:
			vnic_1.append(i.name)
		lanconn_vnic = raw_input("What vNICs would you like to add to the Service Profile? Please list in the right order. [" + ", ".join(vnic_1) + "]: ")
		lanconn_vnic = lanconn_vnic.split(", ")
		for i, j in enumerate(lanconn_vnic, 1):
			mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", vnic_name=j, order=str(i), transport="ethernet", admin_host_port="ANY")
			vnic = handle.query_classid("vniclanConnTempl", filter_str="(name, " + j + ", type='eq')")
			for k in vnic:
				vnic_2 = []
				vnic_2.extend([k.switch_id, k.qos_policy_name, k.mtu, k.name])
				mo_2 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name=settings_file['cdp_name'], admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id=str(vnic_2[0]), name=str(j), order=str(i), qos_policy_name=str(vnic_2[1]), adaptor_profile_name=settings_file['adapterpolicy_name'], ident_pool_name=settings_file['macpool_name'], cdn_source="vnic-name", mtu=str(vnic_2[2]), nw_templ_name=str(vnic_2[3]), addr="derived")
			handle.add_mo(mo, True)
	mo_2 = handle.query_classid("lstorageProfile")
	storage = []
	for j in mo_2:
		storage.append(j.name)
	sp_storage = raw_input("What Storage Profile would you like to use? [" + ", ".join(storage) + "]: ")
	mo_3 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name=sp_storage)
	mo_4 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
	mo_5 = LsPower(parent_mo_or_dn=mo, state="up")
	handle.add_mo(mo, True)
	s3260_bind = raw_input("Would you like to bind the service profile to a S3260 blade?  [yes, no]: ")
	if s3260_bind == 'yes':
		blade = '(model,"UCSC-C3K-M4SRB",type="eq") and (oper_state,"unassociated",type="eq")'
		obj_1 = handle.query_classid("computeBlade", filter_str=blade)
		blade_1 = []
		for k in obj_1:
			blade_1.append(k.dn)
		blade_2 = raw_input("What S3260 Blade would you like to use? [" + ", ".join(blade_1) + "]: ")
		mo_6 = LsBinding(parent_mo_or_dn=mo, pn_dn=blade_2, restrict_migration="no", admin_action="unspecified", admin_action_trigger="idle")
	handle.add_mo(mo, True)
	if s3260_bind == 'yes':
		print "\nCreated S32600 Service Profile Template " + "\033[33m" + sp3260_name + "\033[0m" + " and bound it to server " + "\033[33m" + blade_2 + "\033[0m"
		filetxt.write("\nCreated S32600 Service Profile Template " + sp3260_name + " and bound it to server " + blade_2)
	else:
		print "\nCreated S32600 Service Profile Template " + "\033[33m" + sp3260_name + "\033[0m"
		filetxt.write("\nCreated S32600 Service Profile Template " + sp3260_name)
handle.commit()

handle.logout()
