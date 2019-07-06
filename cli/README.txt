Overview : 
* elfs_cli.py is the driver file, rest of the python files are modules(one for each command in the cli) that implement the necessary thrift APIs for that particular command.
* The cli and the modules are written in python3
* The directory DataAndLogs will be created in runtime. It will contain one directory for each edge, wherein the data and metadata of microbatches is stored. It will also contain a logs.txt file.

Suported Commands : 
* join
* regstream
* get
* put
* find
* ls

Prerequisites: 
* The fogs must must be active in other terminals
* Put the edgefilesystem-0.1-jar-with-dependencies.jar file, after compilation, in cli/target/ folder
	** The above step has to be done manually.
	** The jar file is only required for the join command

Usage : 
1. Open a new terminal.
2. start the elfs_cli.py,
	2.1 The -W ignore option supresses the warnings.
	2.2 You to specify the edge config file when starting the cli. This file is used to maintain a session for that particular edge.
3. (optional) You can spin up edges from the cli using the join command. If you need to add more edges, then add a new config file in the edge-config-files directory.
4. Execute required cli commands.
5. use 'help' command for more information about a specific command.

* use 'help' to view list of available commands.
* use 'help' 'commandx' to view usage and all parameters of 'commandx'.
* the parameters can be given in any order
* the values for parameters can be specified in the following two ways
	* --param1=value
	* --param1 value

Examples :

## Start cli with session maintained for edge1
python -W ignore elfs_cli.py edge-config-files\edge1_config.json

## Start another cli in a new terminal with session maintained for edge7
python -W ignore elfs_cli.py edge-config-files\edge7_config.json

## Start all the edges (i.e it will start the edges in background whose config files are present in the edge-config-file directory)
join --configFiles edge-config-files

## register stream_id_test
regstream --id stream_id_test --reli .99 

## register stream_id_test2, set minReplica, set maxReplica, verbose enabled
regstream --id stream_id_test2 --reli .90 --minReplica 6 --maxReplica 8 --v

## put 'n' files ('n' is the number of files in the D:/Lab/DataAndLogs/Files directory) , setLease is true
put --path=D:/Lab/DataAndLogs/Files --streamId=stream_id_test --start=100 --setLease

## put 'n' files ('n' is the number of files in the D:/Lab/DataAndLogs/Files directory), each file as one block, verbose enabled
put --path=D:/Lab/DataAndLogs/Files --streamId=stream_id_test --start=200 --singleBlock --v

## put a single file, as single block
put --path=D:/Lab/DataAndLogs/microbatch_single_file_test.txt --streamId=stream_id_test2 --start=300 --singleBlock

## get microbatches/blocks in the range [100,104] (all inclusive)
get --start=100 --end=104

## get a single block
get --start 200

##list blocks in the whole system, groupBy  edge (default)
ls --all

## list blocks in the buddy pool, groupBy  edge (default)
ls --buddies 

## list blocks in the neighbors of the current fog, groupBy  mbids
ls --neighbors --groupBy mbids

## list blocks in the buddy pool and the neighbors, groupBy mbids, verbose enabled
ls --neighbors --buddies --groupBy=mbids --v

##find the edge locations of mictobatch 200
find --mbid 200 

