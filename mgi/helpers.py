def resolve_features(given_featues, known_features=None, boolean_features=[]):
    features = {}
    for f in given_featues:
        k, v = f.split("=", 1)
        if known_features and k not in known_features:
            raise Exception(f"Unknown feature: {k}")
        if v == "":
            raise Exception(f"No value given for feature: {k}")
        if k in boolean_features:
            if v in [None, "", "false", "False", "n", "N"]:
                v = False
            else:
                v = True
        features[k] = v
    return features
#-- resolve_features
