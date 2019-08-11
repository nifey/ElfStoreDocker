import json
import os
import numpy

deployment_output = json.load(open("deployment_output.json"))

copy_done_vm = {}
key_path = "/home/dreamlab/.ssh/id_rsa"


fog_to_privateip = {}
privateip_to_fog = {}
edgeip_to_vm = {}
fogno_to_globalpublicip ={}

for key in deployment_output :
    if "Fog" in key:
        vm_ip = deployment_output[key]["host_vm_ip"]
        fog_to_privateip[key] = deployment_output[key]["private_networks"]
        fogno_to_globalpublicip[int(key[6])] = deployment_output[key]["public_global_network"]


    elif "Edge" in key:
        edge_to_privateip = deployment_output[key]["private_networks"]
        vm_ip = deployment_output[key]["host_vm_ip"]

        for key2 in edge_to_privateip:
            edgeip_to_vm[key]=(vm_ip,key2,edge_to_privateip[key2])


#to get fogid to privteip and private network
for key in fog_to_privateip:
    violet_private = fog_to_privateip
    for key2 in violet_private:
        for key3 in violet_private[key2]:
            privateip_to_fog[key3] = (key2,violet_private[key2][key3],)


vm_set = set()
for key in edgeip_to_vm:
    vm_ip = edgeip_to_vm[key][0]
    vm_set.add(vm_ip)


for vm_ip in vm_set:
    os.system("sudo scp -i {0} -r dreamlab@{1}:/home/dreamlab/Logs/ /home/dreamlab/packemLogs/".format(key_path, vm_ip))

print "Fetched edge client logs from all vms successfully"

