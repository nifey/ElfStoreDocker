import json
import sys
import random
import hashlib

import module_EdgeClientCLI_get

EDGE_ID = int()
EDGE_IP = str()
EDGE_PORT = int()
EDGE_RELI = float()
FOG_IP = str()
FOG_PORT = int()
LOGS_FOLDER = str()
BASE_LOG = str()
CLIENT_ID = str()
COMP_FORMAT = str()

def do_get(start, end, edgeId, edgeIp, edgePort, edgeReli, fogIp, fogPort, erausureCode):
    module_EdgeClientCLI_get.get(start, end, edgeId, edgeIp, edgePort, edgeReli, fogIp, fogPort, erasureCode, True)

if __name__ == '__main__':
    if(len(sys.argv) < 5):
        print("usage: python get_test.py edge_config_file start end no_of_times_to_get erasureCode")
        sys.exit(0)
    CONFIG_FILE = sys.argv[1]
    edgeConfig = json.load(open(CONFIG_FILE,'r'))
    EDGE_ID = edgeConfig['edgeId']
    EDGE_IP = edgeConfig['edgeIp']
    EDGE_PORT = edgeConfig['edgePort']
    EDGE_RELI = edgeConfig['reliability']
    FOG_IP = edgeConfig['fogIp']
    FOG_PORT = edgeConfig['fogPort']
    LOGS_FOLDER = edgeConfig['logsFolder']
    BASE_LOG = edgeConfig['baseLog']
    CLIENT_ID = hashlib.md5(str(EDGE_ID).encode('utf-8')).hexdigest()
    COMP_FORMAT = edgeConfig['compFormat']

    ##Printing the session information.
    print("Session Information")
    print("Edge ID : " + str(EDGE_ID))
    print("Edge IP : " + EDGE_IP)
    print("Edge Port : " + str(EDGE_PORT))
    print("Edge Reliability : " + str(EDGE_RELI))
    print("Fog IP : " + FOG_IP)
    print("Fog Port : " + str(FOG_PORT))
    print("Storage Location : " + "./DataAndLogs/edge"+str(EDGE_ID)+"_data")
    print("Client ID : " + CLIENT_ID)

    start = int(sys.argv[2])
    end = int(sys.argv[3])
    get_times = int(sys.argv[4])
    erasureCode = False
    if sys.argv[5] == "1":
        erasureCode = True
    for i in range(get_times):
        randMbId = random.randint(start, end)
        do_get(randMbId, randMbId, EDGE_ID, EDGE_IP, EDGE_PORT, EDGE_RELI, FOG_IP, FOG_PORT, erasureCode);
