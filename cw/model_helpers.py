from cw import Pipeline

def get_pipeline(identifier):
    q = None
    if type(identifier) is int or identifier.isnumeric():
        pipeline = Pipeline.query.get(identifier)
    else:
        pipeline = Pipeline.query.filter(Pipeline.name == identifier).one_or_none()
    #if pipeline is None: ...
    return pipeline
