import sys
import json

FOG_COUNT = int()
EDGE_COUNT_PPART = int()
FOG_SUBNET = str()
EDGE_SUBNET = str()

def initializeComposeFile(fileName):
    file = open(fileName,'w+')
    ttext = "version: '2.2'\n\nnetworks:\n  default:\n    external:\n      name: elfstore-network\n\nservices:\n"
    file.write(ttext)
    file.close()

def writeFog(id, ip, port, fogFileName):
    file = open(fogFileName,'a',encoding='utf-8')
    fogCommand  = "java -Xms80m -Xmx800m -cp edgefs/cli/target/edgefilesystem-0.1-jar-with-dependencies.jar com.dreamlab.edgefs.controlplane.FogServer {} {} 1 1 0.25 0".format(ip,str(port))
    ttext = "  fog{}:\n    container_name: fog{}\n    image: elfstorenojson\n    mem_limit: 4096m\n    cpus: 2\n    volumes:\n      - ./Logs/serverLogs/:/log.dir_IS_UNDEFINED/\n    networks:\n      default:\n        ipv4_address: {}\n    expose:\n      - \"{}\"\n    command: {}\n\n".format(str(id),str(id),ip,port,fogCommand)
    file.write(ttext)
    #print(ttext)
    file.close()

def writeEdge(edgeId,edgeIp,edgePort,fogIp,fogPort,edgeFileName):
    file  = open(edgeFileName,'a',encoding='utf-8')
    edgeCommand = "java -Xms40m -Xmx200m -cp edgefs/cli/target/edgefilesystem-0.1-jar-with-dependencies.jar com.dreamlab.edgefs.edge.server.EdgeServer {} {} {} 88 {} {}  /edgedatatemp  /edgefs/logs".format(edgeId,edgeIp,edgePort,fogIp,fogPort)
    ttext  = "  edge{}:\n    container_name: edge{}\n    image: elfstorenojson\n    mem_limit: 4096m\n    cpus: 1\n    volumes:\n      - ./Logs/edgeClientLogs/:/edgefs/logs/\n      - ./Logs/edgeServerLogs/:/log.dir_IS_UNDEFINED/\n    networks:\n      default:\n       ipv4_address: {}\n    expose:\n      - \"{}\"\n    command: {}\n\n".format(str(edgeId),str(edgeId),edgeIp,str(edgePort),edgeCommand)
    file.write(ttext)
    #print(ttext)
    file.close()

    ## Generate the edge config file at the same time
    configFile = open("edge-config-files/edge"+str(edgeId)+"_config.json",'w',encoding = 'utf-8')
    configDict = dict()
    configDict.update({"edgeId":edgeId, "edgeIp":edgeIp, "edgePort":edgePort, "reliability":85, "fogIp":fogIp, "fogPort":fogPort, "logsFolder": "/edgefs/logs", "baseLog":"/edgefs/baseLog", "compFormat":"NA"})
    json.dump(configDict, configFile, indent = 4)
    configFile.close()

if __name__ == "__main__":
    FOG_COUNT = int(sys.argv[1])
    EDGE_COUNT_PPART = int(sys.argv[2])
    FOG_SUBNET = sys.argv[3]
    EDGE_SUBNET = sys.argv[4]
    FOG_PORT = 9000
    EDGE_PORT = 7000

    fogFileName = "fogs-docker-compose.yml"
    edgeFileName = "edges-docker-compose.yml"
    #initializeComposeFile(fogFileName)
    initializeComposeFile(edgeFileName)

    globalEdgeCount = 0;

    for i in range(0,FOG_COUNT):
        fogIp = FOG_SUBNET + str(i)
        fogPort = FOG_PORT + i
        #writeFog(i+1,fogIp,fogPort,fogFileName)
        for j in range(0,EDGE_COUNT_PPART):
            edgeIp = EDGE_SUBNET + str(globalEdgeCount)
            edgePort = EDGE_PORT + globalEdgeCount
            writeEdge(globalEdgeCount+1,edgeIp,edgePort,fogIp,fogPort,edgeFileName)
            globalEdgeCount = globalEdgeCount + 1
