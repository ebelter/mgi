import click, json, os, re, shutil, sys, yaml

from cw.conf import CromwellConf
known_pipelines = {
        "encode_hic": {
            "hic.merge_replicates": ["bam"], # merged bam
            "hic.calculate_stats": ["stats", "stats_json"],
            "hic.add_norm": ["output_hic"],
            "hic.create_eigenvector": ["eigenvector_bigwig", "eigenvector_wig"],
            "hic.create_eigenvector_10kb": ["eigenvector_bigwig", "eigenvector_wig"],
            "hic.arrowhead": ["out_file"],
            "hic.hiccups": ["merged_loops"],
        }
}

@click.command(short_help="Start a cromwell server")
@click.argument("metadata-file", type=str, required=True, nargs=1)
@click.argument("destination", type=str, required=True, nargs=1)
@click.argument("tasks_and_outputs", type=str, required=True, nargs=1)
def outputs_cmd(metadata_file, destination, tasks_and_outputs):
    """
    Gather Outputs from a Cromwell Run

    Give the metadata file, destination path, and the outputs to gather

    Make sure the destination exists

    Generate metadata file with `cromshell metadata <WORKFLOW_ID>`

    For tasks and outputs, give a known pipeline or json formatted file of tasks and oiutputs to gather

    """
    if not os.path.exists(metadata_file):
        raise Exception(f"Metadata file <{metadata_file}> does not exist!")
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    calls = metadata.get("calls", None)
    if calls is None:
        raise Exception(f"Failed to find <calls> in workflow metadata!")

    if not os.path.exists(destination):
        raise Exception(f"Destination directory <{destination}> does not exist!")

    tasks_and_outputs = resolve_tasks_and_outputs(tasks_and_outputs)
    rm_wf_name_re = re.compile(f"^{metadata['workflowName']}\.")
    for task_name, file_keys in tasks_and_outputs.items():
        sys.stdout.write(f"[INFO] Task <{task_name}> files: <{' '.join(file_keys)}>\n")
        task = calls.get(task_name, None)
        if task is None:
            sys.stderr.write(f"[WARN] No task found for <{task_name}> ... skipping\n")
            continue
        succeeded_calls = 0
        files_and_dests = []
        for call in task:
            if call["executionStatus"] != "Done":
                continue
            succeeded_calls += 1
            dest = os.path.join(destination, re.sub(rm_wf_name_re, "", task_name))
            for file_key in file_keys:
                files = call["outputs"][file_key]
                if type(files) is str:
                    files = [files]
                files_and_dests.append([files, dest])
        sys.stdout.write(f"[INFO] Calls {succeeded_calls} of {len(task)} DONE\n")
        files_missing = 0
        for files, dest in files_and_dests:
            os.makedirs(dest, exist_ok=1)
            for fn in files:
                if not os.path.exists(fn):
                    sys.stdout.write(f"[INFO] File <{fn}> not found ... skipping\n")
                    files_missing += 1
                    continue
                sys.stdout.write(f"[INFO] Copy {fn} to {dest}\n")
                shutil.copy(fn, dest)
        sys.stdout.write(f"[INFO] Copied {len(files_and_dests)} skipped {files_missing} missing files\n")
    sys.stdout.write(f"[INFO] Done\n")
#-- outputs_cmd

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
