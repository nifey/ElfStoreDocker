import json
import os
import numpy
import paramiko

deployment_output = json.load(open("deployment_output.json"))

copy_done_vm = {}
key_path = "/home/violetadmin1/.ssh/id_rsa"
copy_file = "edge-config-files/"


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


#print "here",privateip_to_fog
#print edgeip_to_vm

# python EdgeServer.py 1 127.0.0.1 8000 8 127.0.0.1 9090 /home/swamiji/
numpy.random.seed(1234)
reliability = numpy.random.normal(90,3,len(edgeip_to_vm.keys()))
edgeDocker_name = []
edgeId_list = []
edgeIP_list = []
edgePort_list = []
edge_vm = []
fogIp_list = []
fogPort_list = []
DATA_PATH = "/edgefs/data/"
BASE_LOG = "/edgefs/logs/"

## create the directory if note present
## delete any old edge config files if the directory is present
if os.path.isdir("./edge-config-files") == False:
    os.mkdir("./edge-config-files")
else:
    os.system("sudo rm -rvf edge-config-files/")
    os.mkdir("./edge-config-files")

i = 0
edge_command = "java -Xms40m -Xmx200m -cp edgefs/cli/target/edgefilesystem-0.1-jar-with-dependencies.jar com.dreamlab.edgefs.edge.server.EdgeServer"
for key in edgeip_to_vm:
    fogPort = 6000 + int(key[5]) - 1
    edgePort = 5000 + i
    # print "edge vm is ",edgeip_to_vm[key][2]
    edgeIP_list.append(edgeip_to_vm[key][2])
    edgeDocker_name.append(key)
    edgePort_list.append(edgePort) #hard coded port
    pvt_ip = edgeip_to_vm[key][1]
    fogIp_list.append(fogno_to_globalpublicip[int(key[5])])
    fogPort_list.append(fogPort)
    vm_ip = edgeip_to_vm[key][0]
    vm_copy_status.update({vm_ip:0})
    # Add your custom username of vm here
    vm_username = "vm"+edgeip_to_vm[key][3]
    edge_vm.append(edgeip_to_vm[key][0])
    part_eid = key.split("-")[1].split(".")
    part_eid = int(part_eid[0] + part_eid[1])
    edgeId_list.append(part_eid)

    ## Generate the edge config file


    configFile = open("edge-config-files/edge"+str(edgeId_list[i])+"_config.json",'w')
    configDict = dict()
    configDict.update({
        "edgeId":edgeId_list[i],
        "edgeIp":edgeIP_list[i],
        "edgePort":edgePort_list[i],
        "reliability":int(reliability[i]),
        "fogIp":fogIp_list[i],
        "fogPort":fogPort_list[i],
        "logsFolder": "/edgefs/logs",
        "baseLog":BASE_LOG+str(edgeId_list[i])+"/",
        "compFormat":"NA"
        })
    json.dump(configDict, configFile, indent = 4)
    configFile.close()



    ## generate the edge sever command and execute it
    #print "python EdgeServer.py ",edgeId_list[i],edgeIP_list[i], edgePort_list[i],int(reliability[i]),fogIp_list[i],fogPort_list[i],DATA_PATH+str(i+1)
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ## vm_username is the username of the vm
    c.connect( hostname = vm_ip, username = vm_username, pkey = k)

    ## now generate the edge server command and execut it
    start_edge_server = "sudo docker exec -i "+ key+" "+edge_command+" "+str(edgeId_list[i])+" "+str(edgeIP_list[i])+" "+ str(edgePort_list[i])+" "+str(int(reliability[i]))+" "+str(fogIp_list[i])+" "+str(fogPort_list[i])+" "+DATA_PATH+str(edgeId_list[i])+" "+BASE_LOG+str(edgeId_list[i])+"/ 262144000"
    print str(key)
    c.exec_command('nohup ' + start_edge_server + ' >/dev/null 2>&1 &')
    c.close()
    i = i + 1

#print edgeIP_list, edgePort_list, fogIp_list, fogPort_list,edgeId_list
print "edge devices deployed succesfully"
print "Now copying generated edge-config-files to all the edge containers ..."

docker_copy_command = "sudo docker cp {0} {1}:/edgefs/cli/{0}"

for key in edgeip_to_vm:
    vm_ip = edgeip_to_vm[key][0]
    # Add your custom username of vm here
    vm_username = "vm"+edgeip_to_vm[key][3]
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # vm_username is the username of the vm
    c.connect( hostname = vm_ip, username = vm_username, pkey = k)

    ## clean up the existing edge-config-files
    #c.exec_command('sudo docker exec -i '+key+' rm -rvf /edgefs/cli/edge-config-files/')
    ## copy the new config files to the vm
    #if vm_copy_status[vm_ip] == 0:
    ## i.e this is the first time the files are being copied to this vm.
    os.system("sudo scp -i {0} -r {1} {3}@{2}:~".format(key_path, copy_file, vm_ip,vm_username))
    vm_copy_status[vm_ip] = 1

    ## copy the new config files from the vm to the container
    c.exec_command(docker_copy_command.format(copy_file, key))
    ## remove the edge-config-files from the vm
    #c.exec_command("sudo rm -rvf edge-config-files/")
    c.close()

print "Copied edge-config-files successfully"
