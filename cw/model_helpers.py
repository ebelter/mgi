import os
from cw import Pipeline, Workflow

def resolve_features(given_features, known_features):
    features = {}
    for f in given_features:
        k, v = f.split("=", 1)
        if k not in known_features:
            raise Exception(f"Unknown feature: {k}")
        if v == "":
            raise Exception(f"No value given for feature: {k}")
        if known_features[k]["type"] is bool:
            if v in [None, "false", "False", "n", "N"]:
                v = False
            else:
                v = True
        if known_features[k]["type"] == "file" and not os.path.exists(v):
            raise Exception(f"Feature <{k}> is a file, but given value <{v}> does not exist")
        features[k] = v
    return features
#-- resolve_features

# Pipeline
def pipeline_features():
    return {
            "name": {"desc": "name for the pipeline", "type": str, "required": True},
            "wdl": { "desc": "pipeline wdl file", "type": "file", "required": True},
            "imports": { "desc": "imports zip file of imports used by WDL", "type": "file", "requried": False},
            "outputs": { "desc": "yaml file of pipeline steps and outputs", "type": "file", "requried": False},
        }
def get_pipeline(identifier):
    if type(identifier) is int or identifier.isnumeric():
        pipeline = Pipeline.query.get(identifier)
    else:
        pipeline = Pipeline.query.filter(Pipeline.name == identifier).one_or_none()
    #if pipeline is None: ...
    return pipeline
#-- get_pipeline

# Workflow
def wf_features():
    return {
            "wf_id": {"desc": "cromwell workflow id", "type": str, "required": True},
            "name": {"desc": "name for the workflow", "type": str, "required": True},
            "pipeline": {"desc": "pipeline id or name", "type": int, "required": True},
            "status": {"desc": "workflow status", "type": str, "required": False},
        }

def wf_features_help():
    known_features = wf_features()
    return list(map(lambda k: [k, known_features[k]["desc"]], known_features.keys()))
#-- wf_features_help

def get_wf(identifier):
    if type(identifier) is int or identifier.isnumeric():
        wf = Workflow.query.get(identifier)
    else:
        wf = Workflow.query.filter(Workflow.wf_id == identifier).one_or_none()
        if wf is None:
            wf = Workflow.query.filter(Workflow.name == identifier).one_or_none()
    #if wf is None: ...
    return wf
#-- get_wf
