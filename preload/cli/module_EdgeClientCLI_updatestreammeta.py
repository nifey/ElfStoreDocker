import sys
sys.path.append('./gen-py')
import math
import random
import time
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from fogclient import FogService
from fogclient.ttypes import *
from EdgeServices import EdgeService
from EdgeServices.ttypes import *
import time
import os
import collections
import json
import multiprocessing
from pprint import pprint
import hashlib
import contextlib

#if os.path.isdir("/edgefs/logs") == False:
#    os.mkdir("/edgefs/logs")

## the file logs.txt will be created later
BASE_LOG = str() #"/edgefs/logs/"
FOG_SERVICE = 0


STREAM_ID = str()
FOG_IP = str()
FOG_PORT = int()
START = int()
NUM = int()

## Used when the --v (i.e verbose) is set to false
## The output of the python file of the correspoding command is written here
## so that it does not show up in the CLI
class DummyFile(object):
    def write(self, x):
        pass
    def flush(self):
        pass

@contextlib.contextmanager
def nostdout():
    #save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
## end of --v context

class EdgeClient:
    def __init__(self):
        self.log = {}

    def getStreamMetadata(self, sid):
        client,transport = self.openSocketConnection(FOG_IP, FOG_PORT, FOG_SERVICE)
        streamMetadataInfo = client.getStreamMetadata(sid, True, True, True)
        self.closeSocket(transport)
        return streamMetadataInfo.streamMetadata

    # Return the fog client instance to talk to the fog
    def openSocketConnection(self,ip,port, choice):
        print("ip ",ip," port",port," choice ", "open socket connection")
        # Make socket
        transport = TSocket.TSocket(ip, port)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TFramedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        if(choice == FOG_SERVICE):
            client = FogService.Client(protocol)
        else:
            print("In the edge service call ")
            client = EdgeService.Client(protocol)

        # Connect!
        transport.open()

        print("came here")

        return client,transport

    #Close connection
    def closeSocket(self,transport):

        print("closing connection")
        transport.close()


    #stream metadata update has an id of 300
    def updateStreamMD(self):
        print("Going to update stream metadata, first get the latest stream metadata")

        timestamp_record = "-1, 300,"+ str(-1)  + ",stream md update,starttime = "+repr(time.time())+","
        global STREAM_ID
        metadata = self.getStreamMetadata(STREAM_ID)
        #type of ownerFog is NodeInfoPrimary
        ownerFog = metadata.owner.value
        ownerFog_ip = ownerFog.NodeIP
        ownerFog_port = ownerFog.port
        print("Owner of ", STREAM_ID, " is ", ownerFog_ip, " : ", ownerFog_port)

        print("============ VERSION IS ============" , metadata.version.value)
        current_value = int(metadata.otherProperties["update_prop"].value)
        next_value = current_value + 1
        metadata.otherProperties["update_prop"] = DynamicTypeStreamMetadata(str(next_value), "Integer", True)

        client,transport = self.openSocketConnection(ownerFog_ip, ownerFog_port, FOG_SERVICE)

        #result type is StreamMetadataUpdateResponse
        result = client.updateStreamMetadata(metadata)
        #lets add the status as well as the last field in the log
        if result.code > 0:
            #success case
            timestamp_record = timestamp_record +"endtime = " + repr(time.time()) + ",1" + '\n'
        else:
            #failure case
            timestamp_record = timestamp_record +"endtime = " + repr(time.time()) + ",0" + '\n'

        self.closeSocket(transport)

        myLogs = open(BASE_LOG+ "logs.txt",'a')
        myLogs.write(timestamp_record)
        myLogs.close()

        return result.code


def updateMeta(streamId,fogIp,fogPort,num,baseLogPath,verbose = False):
    global STREAM_ID
    STREAM_ID = streamId
    global FOG_IP
    FOG_IP = fogIp
    global FOG_PORT
    FOG_PORT = int(fogPort)
    global NUM
    NUM = int(num)
    global START
    START = 700

    ## create the directory for edge client logs if it does not exist
    global BASE_LOG
    BASE_LOG = baseLogPath

    if os.path.isdir(BASE_LOG) == False:
        os.mkdir(BASE_LOG)

    myEdge = EdgeClient()

    if verbose == True:
        for i in range(NUM):
            response = myEdge.updateStreamMD()
            #return myEdge.formulateJsonResponse(STREAM_ID)
    else:
        for i in range(NUM):
            responseCode = 0
            with nostdout():
                responseCode = myEdge.updateStreamMD()
            #jsonResponse = myEdge.formulateJsonResponse(STREAM_ID)
            sys.stdout = sys.__stdout__
            if responseCode > 0: print("success; Code = "+str(responseCode))
            else: print("failure; Code = "+str(responseCode))
            #return jsonResponse
