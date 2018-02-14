import sys
import json
import csv
from colorama import init
from itertools import chain
from ucsmsdk import ucshandle

# use Colorama to make Termcolor work on Windows too
init()

filename = "C:\Users\Administrator\Box Sync\PythonSDS\ucsm.json"
txtname = "C:\Users\Administrator\Box Sync\PythonSDS\ucsm_query.txt"
#filename = "/root/python_sds/ucsm.json"

# Read JSON data into the settings_file variable
print "Reading JSON File"
file = open(filename, "r")
settings_file = json.load(file)
file.close()

# Write results into txt file
filetxt = open(txtname, "w")

# Login to UCS Manager
print "\nLogging into UCSM"
handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=settings_file['secure'])
handle.login()
ucsm_login = handle.login()
if ucsm_login == True:
	print 'Login successful'.format()
else:
	print 'Please check your credentials'.format()
	
# Query available Blades and server
obj = handle.query_dn("org-root")
blade = '(model,"UCSC-C3K-M4SRB",type="eq")'
rack = '(model,"UCSC-C220-M4S",type="eq")'
chassis = '(model,"UCSC-C3X60-BASE",type="eq")'
obj_1 = handle.query_classid("computeBlade", filter_str=blade)
obj_2 = handle.query_classid("computeRackUnit", filter_str=rack)
obj_3 = handle.query_classid("equipmentchassis", filter_str=chassis)
print obj_3
print ("These are the discovered S3260 chassis with DN, PID: \n")
filetxt.write("These are the discovered S3260 chassis with DN, PID: \n")
for k in obj_3:
	print "\033[33m" + k.dn, k.model + "\033[0m"
	filetxt.write(k.dn + " " + k.model + "\n")
print ("\nThese are the discovered S3260 blades with DN, PID, Cores, Memory: \n")
filetxt.write("\nThese are the discovered S3260 blades with DN, PID, Cores, Memory: \n")
for i in obj_1:
	print "\033[33m" + i.dn, i.model, i.num_of_cores, i.total_memory + "\033[0m"
	filetxt.write(i.dn + " " + i.model + " " + i.num_of_cores + " " + i.total_memory + "\n")
print ("\nThese are the discovered C220 Rack Server with DN, PID, Cores, Memory: \n")
filetxt.write("\nThese are the discovered C220 Rack Server with DN, PID, Cores, Memory: \n")
for j in obj_2:
	print "\033[33m" + j.dn, j.model, j.num_of_cores, j.total_memory + "\033[0m"
	filetxt.write(j.dn + " " + j.model + " " + j.num_of_cores + " " + j.total_memory + "\n")
	
# Query available Firmware Packages
obj = handle.query_dn("org-root")
firmware = '(type,"c-series-bundle",type="eq")'
obj_1 = handle.query_classid("firmwareDistributable", filter_str=firmware)
print ("\nThese are the avalaible C-Series Firmware Packages: \n")
filetxt.write("\nThese are the avalaible C-Series Firmware Packages: \n")
for i in sorted(obj_1):
	print "\033[33m" + i.name, i.version + "\033[0m"	
	filetxt.write(i.name + " " + i.version + "\n")
	
# Query available Disks
obj = handle.query_dn("org-root")
ssd = '(variant_type,"C3000_TOP",type="eq") and (device_type,"SSD",type="eq")'
obj_1 = handle.query_classid("StorageLocalDisk", filter_str=ssd)
print ("\nThese are the avalaible S3260 SSDs: \n")
filetxt.write("\nThese are the avalaible S3260 SSDs: \n")
for i in obj_1:
	print "\033[33m" + i.dn, i.device_type, i.model, i.vendor, i.disk_state + "\033[0m"
	filetxt.write(i.dn + " " + i.device_type + " " + i.model + " " + i.vendor + " " + i.disk_state + "\n")
hdd = '(variant_type,"C3000_TOP",type="eq") and (device_type,"HDD",type="eq")'
obj_2 = handle.query_classid("StorageLocalDisk", filter_str=hdd)
print ("\nThese are the avalaible S3260 HDDs: \n")
filetxt.write("\nThese are the avalaible S3260 HDDs: \n")
for j in obj_2:
	print "\033[33m" + j.dn, j.device_type, j.model, j.vendor, j.disk_state + "\033[0m"
	filetxt.write(j.dn + " " + j.device_type + " " + j.model + " " + j.vendor + " " + j.disk_state + "\n")
ssdboot = '(variant_type,"C3000_BOOT",type="eq")'
obj_3 = handle.query_classid("StorageLocalDisk", filter_str=ssdboot)
print ("\nThese are the avalaible S3260 Boot SSDs: \n")
filetxt.write("\nThese are the avalaible S3260 Boot SSDs: \n")
for k in obj_3:
	print "\033[33m" + k.dn, k.device_type, k.model, k.vendor, k.disk_state + "\033[0m"
	filetxt.write(k.dn + " " + k.device_type + " " + k.model + " " + k.vendor + " " + k.disk_state + "\n")
obj_4 = handle.query_classid("computeBoard", filter_str=rack)
print ("\nThese are the avalaible C220 Boot disks: \n")
filetxt.write("\nThese are the avalaible C220 Boot disks: \n")
for l in obj_4:
	controller = '(rn,"storage-SAS-1",type="eq")'
	obj_5 = handle.query_children(in_mo=l, class_id="StorageController", filter_str=controller)
	for m in obj_5:
		disk = '(enc_association,"direct-attached",type="eq")'
		obj_6 = handle.query_children(in_mo=m, class_id="StorageLocalDisk", filter_str=disk)
		for n in obj_6:
			print "\033[33m" + n.dn, n.device_type, n.model, n.vendor, n.disk_state + "\033[0m"
			filetxt.write(n.dn + " " + n.device_type + " " + n.model + " " + n.vendor + " " + n.disk_state + "\n")
filetxt.close()
handle.logout()