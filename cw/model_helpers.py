from cw import Pipeline

def resolve_features(given_features, known_features):
    features = {}
    for f in given_features:
        k, v = f.split("=", 1)
        if k not in known_features:
            raise Exception(f"Unknown feature: {k}")
        if v == "":
            raise Exception(f"No value given for feature: {k}")
        if known_features[k]["type"] is bool:
            if v in [None, "", "false", "False", "n", "N"]:
                v = False
            else:
                v = True
        features[k] = v
    return features
#-- resolve_features

# Pipeline
def pipeline_features():
    return {
            "name": {"desc": "name for the pipeline", "type": str, "required": True},
            "wdl": { "desc": "pipeline wdl file", "type": str, "required": True},
            "imports": { "desc": "imports zip file of imports used by WDL", "type": str, "requried": False},
            "outputs": { "desc": "yaml file of pipeline steps and outputs", "type": str, "requried": False},
        }
def get_pipeline(identifier):
    q = None
    if type(identifier) is int or identifier.isnumeric():
        pipeline = Pipeline.query.get(identifier)
    else:
        pipeline = Pipeline.query.filter(Pipeline.name == identifier).one_or_none()
    #if pipeline is None: ...
    return pipeline
#-- get_pipeline
