# CW - MGI Cromwell CLI

A command line interface to run and manage cromwelll workflows.

## Directory Structure and Files

db
logs
runs
server

Upcoming

## Tutorial [MGI LSF]

This tutorial is targeted for running on MGI's LSF platform.

**In the commands below, use your preferred options!**

### Setup and Start the Cromwell Server
#### Start an interactive job with MGI Cromwell(cw) CLI
**use your preferred LSF_DOCKER_VOLUMES and LSF_USER_GROUP**
**the $USER environment variable may not be set - use your username**
From a compute client, run the *ebelter/mgi:cromwell' docker interactively:
```
LSF_DOCKER_VOLUMES="/home/${USER}:/home/${USER} /scratch1/fs1/hprc:/scratch1/fs1/hprc /storage1/fs1/hprc:/storage1/fs1/hprc" bsub -q general-interactive -g /${USER}/default -G compute-hprc -Is -R 'span[hosts=1] select[mem>4G] rusage[mem=4G]' -M 4G -a 'docker(ebelter/mgi:cromwell)' /bin/bash
```

#### Setup the Cromwell Configuration
Create a directory for running the cromwell service. Here we are using our ${USER} directory in the HPRC scratch space, but can be in a different location.
```
cd /scratch1/fs1/hprc/${USER}
mkdir cromwell
cd cromwell
```

Now run the setup command providing *your* LSF options to use when running pipelines. Optionally, use `--env` to attempt to get some configs from the environment.
```
cw setup job_group=/$USER/default queue=general user_group=compute-hprc docker_volumes='/scratch1/fs1/hprc:/scratch1/fs1/hprc /storage1/fs1/hprc:/storage1/fs1/hprc' --env

-- OUTPUT --
Setup cromwell: making directories, scripts, and configuration.
```

#### Start the Cromwell Server
The server start command finishes once server has been assigned an LSF ID, and started running. The cromwell server will still take a minute or to to download the docker image and start the server. There will be a line in the *server/log* like "Cromwell 81 service started on 0.0.0.0:8888" indicating the server is ready.
```
cw server start

-- OUTPUT --
Waiting for job <560377> to start to obtain HOST...
Server running on <compute1-exec-118.ris.wustl.edu> port <8888>
Updating application configuration...
Server ready!
```

#### Verify the Server is Running
```
cw server heartbeat

-- OUTPUT --
Checking host <compute1-exec-118.ris.wustl.edu> listening on <8888> ...
URL: http://compute1-exec-118.ris.wustl.edu:8888/engine/v1/version
Cromwell server is up and running! Response: b'{"cromwell":"81"}'
```

### Run a Workflow
Run the _hello world_ test worlfow.

#### Add a pipeline
```
WDL_PATH=/apps/wdl/hello-world
cw pipelines add name=hello_world wdl=${WDL_PATH}/hello_world.wdl inputs=${WDL_PATH}/hello_world.inputs.json outputs=${WDL_PATH}/hello_world.outputs.yaml

-- OUTPUT --
Add pipeline hello_world /apps/wdl/hello-world/hello_world.wdl None /apps/wdl/hello-world/hello_world.outputs.yaml
```

#### Create the Inputs
MGI managed WDL pipelines have inputs templates. These have place holders in them in order to fill from the comand line and save a copy. Here is the *hello-world* inputs file:
```
cat /apps/wdl/hello-world/hello_world.inputs.json 

-- OUTPUT --
{
  "hw.name": "{{NAME}}"
}
```

The **ipelines inputs** command will fill in these place holders for you. Add the NAME parameter to the inputs and output a file for the workflow using `cw` CLI. The inputs can also be copied and manually edited.
```
cw pipelines inputs hello_world NAME=MGI -o hello_world_1.inputs.json

-- OUTPUT --
Wrote pipeline <hello_world> inputs to hello_world_1.inputs.json
```
_Inputs file we just created:_
```
cat hello_world_1.inputs.json
{
  "hello_world.name": "MGI",
}
```
#### Submit a workflow
Using the inputs json file just created.
```
cw wf submit hello_world_1 hello_world hello_world_1.inputs.json

-- OUTPUT --
Pipeline:    hello_world
Inputs json: hello_world_1.inputs.json
[2023-01-13 10:01:12,21] [info] Slf4jLogger started
[2023-01-13 10:01:13,45] [info] Workflow 73efbd74-cdb2-465a-a414-0125e1f33ced submitted to http://compute1-exec-118.ris.wustl.edu:8888
Workflow 73efbd74-cdb2-465a-a414-0125e1f33ced submitted, waiting for it to start...
```

### Listing, Status and Outputs for Workflows
#### List workflows
```
cw wf list

-- OUTPUT --
$ cw wf list
WF_ID                                 NAME        STATUS     PIPELINE    INPUTS
------------------------------------  ----------  ---------  ----------  ----------------------
e6dcb226-4178-45ff-a7fc-467604bc63f4  hello_world4         succeeded  hello_world          test_run_1.inputs.json
```
#### Check the status of a workflow
Get the workflow id from the submit oputput or by listing workflows. Set the WF_ID for convenience.
```
WF_ID=e6dcb226-4178-45ff-a7fc-467604bc63f4
cw wf status $WF_ID

-- OUTPUT --
succeeded
```

#### Show the detailed view of a workflow
```
cw wf detail 12c27c14-bc57-4be9-b17d-45d551d16e20

-- OUTPUT --
Workflow ID:      12c27c14-bc57-4be9-b17d-45d551d16e20
Status:           Succeeded
Workflow name:    hello_world_1
Workflow inputs:  hello_world_1.inputs.json
Workflow name:
Tasks:
name                time       aborted    done    running    preempted    failed
hw.run_hello_world  0:01:15          0       1          0            0         0
```

#### List the outputs of a workflow
```
cw wf outputs list $WF_ID

-- OUTPUT --
cw wf outputs list e6dcb226-4178-45ff-a7fc-467604bc63f4
[INFO] Task <hello_world.run_hello_world> files: <output_file>
[INFO] Found 1 of 1 tasks DONE
[INFO] Listing files for hello_world.run_hello_world
hello_world.run_hello_world
 shard -1
  /scratch1/fs1/hprc/test/runs/hello_world/e6dcb226-4178-45ff-a7fc-467604bc63f4/call-run_hello_world/execution/hello_world.txt
```

#### Copy the outputs of a workflow to a new location
```
$ cw wf outputs gather e6dcb226-4178-45ff-a7fc-467604bc63f4 dest/

-- OUTPUT --
[INFO] Task <hello_world.run_hello_world> files: <output_file>
[INFO] Found 1 of 1 tasks DONE
[INFO] Copy /scratch1/fs1/hprc/test/runs/hello_world/e6dcb226-4178-45ff-a7fc-467604bc63f4/call-run_hello_world/execution/hello_world.txt to dest/run_hello_world
[INFO] Done
```

_List the output the destination (dest)_
```
ll dest/
total 3.0K
drwx--S---. 3 ebelter compute-hprc 4.0K Jan 13 11:34 ./
drwx-wS---. 8 ebelter compute-hprc 4.0K Jan 17 11:58 ../
drwx--S---. 3 ebelter compute-hprc 4.0K Jan 17 12:05 run_hello_world/

ll dest/run_hello_world/
total 3.5K
drwx--S---. 3 ebelter compute-hprc 4.0K Jan 17 12:05 ./
drwx--S---. 3 ebelter compute-hprc 4.0K Jan 13 11:34 ../
-rw-------. 1 ebelter compute-hprc   85 Jan 17 12:05 hello_world.txt
drwx--S---. 2 ebelter compute-hprc 4.0K Jan 17 11:55 run_hello_world/
```


### Stop the Server
When done running, stop the server using the command below. The LSF can just be killed, but the command updates the local DB it uses.

```
cw server stop

-- OUTPUT --
Server URL: <http://compute1-exec-36.ris.wustl.edu:8888>
Stopping job <441696>
Job <441696> is being terminated
Updating application configuration...
```

### Error Investgation
Look in the _server/log_ file. Most errors will be there. They may also reference errors in the starting workflow tasks, which STDOUT/ERR are in the individual workflow/task paths.


```
Failed to start workflow
Failed to get response from server at http://compute1-exec-118.ris.wustl.edu:8888/api/workflows/v1/73efbd74-cdb2-465a-a414-0125e1f33ced/status
Workflow failed to start. Please verify by checking server logs in <server/log>. Typically failures are due to misconfiguration of inputs or missing files.
```
