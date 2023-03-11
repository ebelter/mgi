import click, json, os, re, shutil, sys, yaml
from cw.model_helpers import get_wf
import cw.server

@click.group(short_help="commands for wf outputs")
def cli():
    """
    Command for Workflow Outputs

    If giving YAML file of outputs, format tasks and outputs as so:

    pipeline.task1:
    - output_file1
    pipeline.task2:
    - output_file1
    - output_file2
"""
    pass

@click.command(short_help="gather outputs from a cromwell run")
@click.argument("workflow-identifier", type=str, required=True, nargs=1)
@click.argument("destination", type=str, required=True, nargs=1)
@click.option("--tasks_and_outputs", "-t", type=str, required=False)
def gather_cmd(workflow_identifier, destination, tasks_and_outputs):
    """
    Gather Outputs from a Cromwell Run

    Give the workflow cromwell id, name, or local db id and  the existing destination path.

    Optionally, give the tasks and outputs as a YAML file, see man outputs help for formatting.

    Outputs will be copied into the destination into task subdirectories. If the task has multiple shards, files will be copied into the shard subdirectory.
    """
    wf = get_wf(workflow_identifier)
    if wf is None:
        raise Exception(f"Failed to get workflow for <{workflow_identifier}>")
    tasks_and_outputs = resolve_tasks_and_outputs(wf.pipeline, tasks_and_outputs)
    metadata = cw.server.server_factory().metadata_for_workflow(wf.wf_id)
    if metadata is None:
        raise Exception(f"Failed to get workflow metadata for <{workflow_identifier}>")
    calls = metadata.get("calls", None)
    if calls is None:
        raise Exception(f"Failed to find <calls> in workflow metadata!")
    if not os.path.exists(destination):
        raise Exception(f"Destination directory <{destination}> does not exist!")

    rm_wf_name_re = re.compile(rf"^{metadata['workflowName']}\.")
    for task_name, file_keys in tasks_and_outputs.items():
        sys.stdout.write(f"[INFO] Task <{task_name}> files: <{' '.join(file_keys)}>\n")
        task = calls.get(task_name, None)
        if task is None:
            sys.stderr.write(f"[WARN] No task found for <{task_name}> ... skipping\n")
            continue

        shards, shard_idxs = collect_shards_outputs(task, file_keys)
        sys.stdout.write(f"[INFO] Found {len(shards)} of {len(shard_idxs)} tasks DONE\n")
        dest_dn = os.path.join(destination, re.sub(rm_wf_name_re, "", task_name))
        copy_shards_outputs(shards, dest_dn)
    sys.stdout.write(f"[INFO] Done\n")
cli.add_command(gather_cmd, name="gather")

@click.command(short_help="list outputs from a cromwell run")
@click.argument("workflow-identifier", type=str, required=True, nargs=1)
@click.option("--tasks_and_outputs", "-t", type=str, required=False)
def list_cmd(workflow_identifier, tasks_and_outputs):
    """
    List Outputs from a Cromwell Run

    Give the workflow cromwell id, name, or local db id.

    Optionally, give the tasks and outputs as a YAML file, see man outputs help for formatting.
"""
    wf = get_wf(workflow_identifier)
    if wf is None:
        raise Exception(f"Failed to get workflow for <{workflow_identifier}>")
    tasks_and_outputs = resolve_tasks_and_outputs(wf.pipeline, tasks_and_outputs)
    metadata = cw.server.server_factory().metadata_for_workflow(wf.wf_id)
    if metadata is None:
        raise Exception(f"Failed to get workflow metadata for <{workflow_identifier}>")
    calls = metadata.get("calls", None)
    if calls is None:
        raise Exception(f"Failed to find <calls> in workflow metadata!")

    rm_wf_name_re = re.compile(rf"^{metadata['workflowName']}\.")
    for task_name, file_keys in tasks_and_outputs.items():
        sys.stdout.write(f"[INFO] Task <{task_name}> files: <{' '.join(file_keys)}>\n")
        task = calls.get(task_name, None)
        if task is None:
            sys.stderr.write(f"[WARN] No task found for <{task_name}> ... skipping\n")
            continue

        shards, shard_idxs = collect_shards_outputs(task, file_keys)
        sys.stdout.write(f"[INFO] Found {len(shards)} of {len(shard_idxs)} tasks DONE\n")
        sys.stdout.write(f"[INFO] Listing files for {task_name}\n")
        list_shards_outputs(task_name, shards)
cli.add_command(list_cmd, name="list")

def resolve_tasks_and_outputs(pipeline, tasks_and_outputs):
    if tasks_and_outputs is not None and os.path.exists(tasks_and_outputs):
        fn = tasks_and_outputs
    elif pipeline.outputs is not None:
        fn = pipeline.outputs
    else:
        raise Exception(f"No outputs found for pipeline <{wf.pipeline.name}>\nAdd outputs with the 'cw pipelines update' command or provide them with tasks_and_outputs option")
    with open(fn, "r") as f:
        tasks_and_outputs = yaml.safe_load(f)
    return tasks_and_outputs
#-- resolve_tasks_and_outputs

def collect_shards_outputs(task, output_keys):
    shards = []
    shard_idxs = set()
    for call in task:
        shard_idxs.add(call["shardIndex"])
        if call["executionStatus"] != "Done":
            continue
        files_to_copy = []
        for k in output_keys:
            files = call["outputs"].get(k, None)
            if files is None:
                continue
            if type(files) is str:
                files = [files]
            files_to_copy += files
        shards.append([call["shardIndex"], files_to_copy])
    return shards, shard_idxs
#-- collect_shards_outputs

def copy_shards_outputs(shards, dest_dn):
    if len(shards) > 1:
        dest_dn = os.path.join(dest_dn, "shard{}")
    for idx, files in shards:
        if files is None:
            continue
        dest = dest_dn.format(str(idx))
        os.makedirs(dest, exist_ok=1)
        for fn in files:
            if not os.path.exists(fn):
                sys.stdout.write(f"[INFO] File <{fn}> not found ... skipping\n")
                continue
            sys.stdout.write(f"[INFO] Copy {fn} to {dest}\n")
            shutil.copy(fn, dest)
#-- copy_shards_outputs

def list_shards_outputs(task_name, shards):
    print(f"{task_name}")
    for idx, files in shards:
        print(f" shard {idx}")
        print("\n".join(list(map(lambda f: f"  {f}", files))))
#-- list_shards_outputs
