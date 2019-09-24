import json
import os
import numpy
import paramiko

deployment_output = json.load(open("deployment_output.json"))

copy_done_vm = {}
key_path = "/home/violetadmin1/.ssh/id_rsa"
copy_file = "jar/"


fog_to_privateip = {}
privateip_to_fog = {}
edgeip_to_vm = {}
fogno_to_globalpublicip ={}
vm_copy_status = {}

for key in deployment_output :
    if "Fog" in key:
        vm_ip = deployment_output[key]["host_vm_ip"]
        fog_to_privateip[key] = deployment_output[key]["private_networks"]
        fogno_to_globalpublicip[int(key[6])] = deployment_output[key]["public_global_network"]


    elif "Edge" in key:
        edge_to_privateip = deployment_output[key]["private_networks"]
        vm_ip = deployment_output[key]["host_vm_ip"]
        vm_no = deployment_output[key]["host_vm_name"].split("-")[1]

        for key2 in edge_to_privateip:
            edgeip_to_vm[key]=(vm_ip,key2,edge_to_privateip[key2],vm_no)


#to get fogid to privteip and private network
for key in fog_to_privateip:
    violet_private = fog_to_privateip
    for key2 in violet_private:
        for key3 in violet_private[key2]:
            privateip_to_fog[key3] = (key2,violet_private[key2][key3],)

docker_copy_command = "sudo docker cp {0} {1}:/edgefs/{0}"

for key in edgeip_to_vm:
    vm_ip = edgeip_to_vm[key][0]
    # Add your custom username of vm here
    vm_username = "vm"+edgeip_to_vm[key][3]
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # vm_username is the username of the vm
    c.connect( hostname = vm_ip, username = vm_username, pkey = k)

    os.system("sudo scp -i {0} -r {1} {3}@{2}:~".format(key_path, copy_file, vm_ip,vm_username))
    vm_copy_status[vm_ip] = 1

    c.exec_command(docker_copy_command.format(copy_file, key))
    c.close()

