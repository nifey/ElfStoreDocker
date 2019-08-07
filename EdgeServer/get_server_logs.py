import json
import os
import numpy
import paramiko

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
        ##
        k = paramiko.RSAKey.from_private_key_file(key_path)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect( hostname = vm_ip, username = "dreamlab", pkey = k)
        ##mkdir
        c.exec_command("mkdir -p /home/dreamlab/FogServerLogs/"+key+"/")
        os.system("mkdir -p /home/dreamlab/FogServerLogs/"+key+"/")
        c.exec_command("sudo docker cp "+key+":/log.dir_IS_UNDEFINED/log.file_IS_UNDEFINED.log /home/dreamlab/FogServerLogs/"+key+"/")
        os.system("sudo scp -i {0} -r dreamlab@{1}:/home/dreamlab/FogServerLogs/{2}/ /home/dreamlab/FogServerLogs/{2}".format(key_path, vm_ip, key))

    elif "Edge" in key:
        edge_to_privateip = deployment_output[key]["private_networks"]
        vm_ip = deployment_output[key]["host_vm_ip"]
        k = paramiko.RSAKey.from_private_key_file(key_path)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect( hostname = vm_ip, username = "dreamlab", pkey = k)
        c.exec_command("mkdir -p /home/dreamlab/EdgeServerLogs/"+key+"/")
        os.system("mkdir -p /home/dreamlab/EdgeServerLogs/"+key+"/")
        c.exec_command("sudo docker cp "+key+":/log.dir_IS_UNDEFINED/log.file_IS_UNDEFINED.log /home/dreamlab/EdgeServerLogs/"+key+"/")
        os.system("sudo scp -i {0} -r dreamlab@{1}:/home/dreamlab/EdgeServerLogs/{2}/ /home/dreamlab/EdgeServerLogs/{2}".format(key_path, vm_ip, key))

        for key2 in edge_to_privateip:
            edgeip_to_vm[key]=(vm_ip,key2,edge_to_privateip[key2])


#to get fogid to privteip and private network
for key in fog_to_privateip:
    violet_private = fog_to_privateip
    for key2 in violet_private:
        for key3 in violet_private[key2]:
            privateip_to_fog[key3] = (key2,violet_private[key2][key3],)


print "Done"

