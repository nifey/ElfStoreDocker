### Overview
* The Cmd module is used to create the shell and the argparse module is used for parsing the command.
* elfs_cli.py is the driver file, rest of the python files are modules(one for each command in the CLI) that implement the necessary thrift APIs for that particular command.
* The CLI and the client files are written in python3.
* The directory ./DataAndLogs (cli/DataAndLogs) will be created in runtime. It will contain one directory for each edge, wherein the data and metadata of microbatches is stored. It will also contain a logs.txt file.

### Suported Commands
* `join`
* `regstream`
* `get`
* `put`
* `find`
* `ls`

### Prerequisites
* The fogs must must be active in their respective terminals.
* Put the edgefilesystem-0.1-jar-with-dependencies.jar file, after compilation, in cli/target/ folder.
    * The above step has to be done manually.
    * The jar file is only required for `join`.

### Usage
1. Open a new terminal.
2. Start the elfs_cli.py,
	2.1 The -W ignore option supresses the warnings.
	2.2 You to specify the edge config file when starting the CLI. This file is used to maintain a session for that particular edge.
3. (optional) You can spin up edges from the CLI using `join` . If you need to add more edges, then add a new config file in the edge-config-files directory.
4. Execute required CLI commands.
5. Use `help`  for more information about a specific command.

* Use `help` to view list of available commands.
* Use `help` 'commandxyz' to view usage and all parameters of 'commandxyz'.
* The arguments of a CLI command can be given in any order
* The values for arguments can be specified in the following two ways
	* --argument1=value
	* --argument2 value

### Examples

* Start CLI with session maintained for edge1
    ```
    python -W ignore elfs_cli.py edge-config-files\edge1_config.json
    ```

* Start another CLI in a new terminal with session maintained for edge7
    ```
    python -W ignore elfs_cli.py edge-config-files\edge7_config.json
    ```
* Start all the edges (i.e it will start the edges in background whose config files are present in the edge-config-file directory)
    ```
    join --configFiles edge-config-files
    ```
* Register stream_id_test
    ```
    regstream --id stream_id_test --reli .99
    ```
* Register stream_id_test2, set minReplica, set maxReplica, verbose enabled
    ```
    regstream --id stream_id_test2 --reli .90 --minReplica 6 --maxReplica 8 --v
    ```
* Put 'n' files ('n' is the number of files in the D:/Lab/DataAndLogs/Files directory) , setLease is true
    ```
    put --path=D:/Lab/DataAndLogs/Files --streamId=stream_id_test --start=100 --setLease
    ```
* Put 'n' files ('n' is the number of files in the specified directory), each file as one block, verbose enabled
    ```
    put --path=D:/Lab/DataAndLogs/Files --streamId=stream_id_test --start=200 --singleBlock --v
    ```
* Put a single file, as single block
    ```
    put --path=D:/Lab/DataAndLogs/microbatch_single_file_test.txt --streamId=stream_id_test2 --start=300 --singleBlock
    ```
* Put a single file (splitting done based on default block size of 10MB) with additional metadata (in a json file)
    ```
    put --path=D:/Lab/DataAndLogs/microbatch_single_file_test.txt --streamId=stream_id_test2 --start=300 --metadata=additional-block-metadata/block_metadata_sample.json
    ```
* Get microbatches/blocks in the range [100,104] (all inclusive)
    ```
    get --start=100 --end=104
    ```
* Get a single block
    ```
    get --start 200
    ```
* List blocks in the whole system, groupBy  edge (default)
    ```
    ls --all
    ```
* List blocks in the buddy pool, groupBy  edge (default)
    ```
    ls --buddies
    ```
* List blocks in the neighbors of the current fog, groupBy  mbids
    ```
    ls --neighbors --groupBy mbids
    ```
* List blocks in the buddy pool and the neighbors, groupBy mbids, verbose enabled
    ```
    ls --neighbors --buddies --groupBy=mbids --v
    ```
* Find the edge locations of mictobatch 200
    ```
    find --mbid 200
    ```
* Find block(s) using metadata
    ```
    find --metadata additional-block-metadata/block_metadata_sample.json
    ```
