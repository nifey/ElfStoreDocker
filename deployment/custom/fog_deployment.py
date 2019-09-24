import json
import os
import paramiko


deployment_output = json.load(open("deployment_output.json"))
#copy cluster.conf to each of the fog containers

copy_done_vm = {}
key_path = "/home/violetadmin1/.ssh/id_rsa"
copy_file = "cluster.conf"

#we need to start the server process within each container and we will read the ip of the fogs from cluster.conf
#From container ip, we should be able to get both the container name and vm ip to start the process

#storing tuple of container name and vm ip here with key being the fog ip


fog_ip_to_info = {}

# this dict maps fog ip to vm number
ip_to_vm_no = {}
for key in deployment_output:
    if "Fog" in key:
        fog_ip = deployment_output[key]["public_global_network"]
        print fog_ip
        vm_ip = deployment_output[key]["host_vm_ip"]
        vm_no = deployment_output[key]["host_vm_name"].split('-')[1]
        ip_to_vm_no[str(fog_ip)] = str(vm_no)
        print vm_ip
        fog_ip_to_info[fog_ip] = (key, vm_ip)
        if vm_ip not in copy_done_vm:
            print("scp -i {0} {1} vm{3}@{2}:~".format(key_path, copy_file, vm_ip, vm_no))
            with open(copy_file, 'r') as printfile:
                print(printfile.read())
            os.system("scp -i {0} {1} vm{3}@{2}:~".format(key_path, copy_file, vm_ip, vm_no))
            copy_done_vm[vm_ip] = 1



#copy file from VM to container
#copying the cluster.conf to the root path
copy_command = "sudo docker cp {0} {1}:/{0}"

#starting the Fog server
server_start_command = "sudo docker exec -i {0} java -Xms80m -Xmx800m -cp /randomscheme.jar com.dreamlab.edgefs.controlplane.FogServer {1} {2} {3} {4} {5} 0"

with open(copy_file) as f:
        content = f.readlines()

content = [x.strip() for x in content]

for elem in content:
    arr = elem.split(',')
    print arr
    fog_ip = arr[0]
    fog_port = arr[1]
    pool_id = arr[2]
    node_id = arr[3]
    fog_rel = arr[4]
    container_name = fog_ip_to_info[fog_ip][0]
    vm_ip = fog_ip_to_info[fog_ip][1]
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Change the user name to your vm username
    c.connect( hostname = vm_ip, username = "vm"+ip_to_vm_no[fog_ip], pkey = k)
    c.exec_command(copy_command.format(copy_file, container_name))
    start_server = server_start_command.format(container_name, fog_ip, fog_port, pool_id, node_id, fog_rel)
    c.exec_command('nohup ' + start_server + ' >/dev/null 2>&1 &')
    c.close()

print "done copying config and starting Fog servers"
