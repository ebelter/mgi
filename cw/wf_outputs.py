import click, json, os, re, shutil, sys, yaml
from cw.model_helpers import get_wf
import cw.server

known_pipelines = {
        "encode_hic": {
            "hic.merge_replicates": ["bam"], # merged bam
            "hic.calculate_stats": ["stats", "stats_json"],
            "hic.add_norm": ["output_hic"],
            "hic.create_eigenvector": ["eigenvector_bigwig", "eigenvector_wig"],
            "hic.create_eigenvector_10kb": ["eigenvector_bigwig", "eigenvector_wig"],
            "hic.arrowhead": ["out_file"],
            "hic.hiccups": ["merged_loops"],
        },
        "encode_rna": {
            "rna.align": ["anno_flagstat", "anno_flagstat_json", "annobam", "genome_flagstat", "genome_flagstat_json", "genomebam", "log", "log_json"],
            "rna.bam_to_signals": ["unique_minus", "unique_plus", "unique_unstranded", "all_minus", "all_plus", "all_unstranded" ], # "all_" not generated maybe because one replicate?
            "rna.kallisto": [ "quants" ],
            "rna.mad_qc": ["madQCmetrics", "madQCplot"], # if replicates == 2
            "rna.rna_qc": ["rnaQC"],
            "rna.rsem_quant": ["genes_results", "isoforms_results", "number_of_genes"],
        }
}

@click.group(short_help="commands for wf outputs")
def cli():
    "Command for Workflow Outputs"
    pass

@click.command(short_help="gather outputs from a cromwell run")
@click.argument("workflow-identifier", type=str, required=True, nargs=1)
@click.argument("destination", type=str, required=True, nargs=1)
@click.option("--tasks_and_outputs", "-t", type=str, required=True)
@click.option("--list-outputs", "-l", is_flag=True, default=False, help="List, do not copy, the outputs found in the workflow")
def gather_cmd(workflow_identifier, destination, tasks_and_outputs, list_outputs):
    """
    Gather Outputs from a Cromwell Run

    Give the metadata file, destination path, and the outputs to gather

    Make sure the destination exists

    Generate metadata file with `cromshell metadata <WORKFLOW_ID>`

    For tasks and outputs, give a known pipeline or yaml formatted file of tasks and outputs to gather

    Ex:

    pipeline.task1:
    - output_file1
    pipeline.task2:
    - output_file1
    - output_file2

    Outputs will be copied into the destination into task subdirectories. If the task has multiple shards, files will be copied into the shard subdirectory.
    """
    wf = get_wf(workflow_identifier)
    if wf is None:
        raise Exception(f"Failed to get workflow for <{workflow_identifier}>")
    metadata = get_metadata(wf)
    if metadata is None:
        raise Exception(f"Failed to get workflow metadata for <{workflow_identifier}>")
    calls = metadata.get("calls", None)
    if calls is None:
        raise Exception(f"Failed to find <calls> in workflow metadata!")

    if not os.path.exists(destination):
        raise Exception(f"Destination directory <{destination}> does not exist!")

    tasks_and_outputs = resolve_tasks_and_outputs(tasks_and_outputs)
    rm_wf_name_re = re.compile(rf"^{metadata['workflowName']}\.")
    for task_name, file_keys in tasks_and_outputs.items():
        sys.stdout.write(f"[INFO] Task <{task_name}> files: <{' '.join(file_keys)}>\n")
        task = calls.get(task_name, None)
        if task is None:
            sys.stderr.write(f"[WARN] No task found for <{task_name}> ... skipping\n")
            continue

        shards, shard_idxs = collect_shards_outputs(task, file_keys)
        sys.stdout.write(f"[INFO] Found {len(shards)} of {len(shard_idxs)} tasks DONE\n")

        if list_outputs:
            # List the outputs found in the workflow
            sys.stdout.write(f"[INFO] Listing files for {task_name}\n")
            list_shards_outputs(task_name, shards)
        else:
            # Copy shards files, use separate directory if multiple shards
            dest_dn = os.path.join(destination, re.sub(rm_wf_name_re, "", task_name))
            copy_shards_outputs(shards, dest_dn)
    sys.stdout.write(f"[INFO] Done\n")
cli.add_command(gather_cmd, name="gather")

def get_metadata(wf):
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{wf.wf_id}/metadata?excludeKey=submittedFiles&expandSubWorkflows=true"
    response = server.query(url)
    if not response or not response.ok:
        #sys.stderr.write(f"Failed to get response from server at {url}\n")
        return None
    return json.loads(response.content.decode())
#-- get_metadata

def resolve_tasks_and_outputs(tasks_and_outputs):
    if os.path.exists(tasks_and_outputs):
        with open(tasks_and_outputs, "r") as f:
            tasks_and_outputs = yaml.safe_load(f)
    elif tasks_and_outputs in known_pipelines:
        tasks_and_outputs = known_pipelines[tasks_and_outputs]
    else:
        raise Exception(f"No such known pipeline <{tasks_and_outputs}>.")
    return tasks_and_outputs
#-- tasks_and_outputs

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
