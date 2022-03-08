import jinja2, os, sys, yaml

class CromwellConf(object):
    def __init__(self, attrs):
        self._attrs = attrs
        CromwellConf.validate_attributes(attrs)
        self._setpaths()

    def dir_names(self):
        return ("db", "lsf_logs", "runs", "server", "wf_logs")

    def _setpaths(self):
        self._attrs["CROMWELL_DIR"] = os.path.abspath(self._attrs["CROMWELL_DIR"])
        self.cromwell_dn = self._attrs["CROMWELL_DIR"]
        self._dir_attrs = {}
        for bn in self.dir_names():
            dn = os.path.join(self.cromwell_dn, bn)
            self._dir_attrs["_".join(["CROMWELL", bn.upper(), "DIR"])] = dn
            setattr(self, "_".join([bn, "dn"]), dn)
        self.server_conf_fn = os.path.join(self.server_dn, "conf")
        self.server_run_fn = os.path.join(self.server_dn, "run")
        self.server_start_fn = os.path.join(self.server_dn, "start")

    def from_yaml(yaml_file):
        with open(yaml_file, "r") as f:
            attrs = yaml.safe_load(f)
        self = CromwellConf(attrs)
        return self

    def setup(self):
        self.makedirs()
        self.write_server_files()

    def write_server_files(self):
        for ft in ("conf", "run", "start"):
            fun = getattr(self, f"server_{ft}_content")
            with open(getattr(self, f"server_{ft}_fn"), "w") as f:
                f.write(fun())

    def makedirs(self):
        for bn in self.dir_names():
            os.makedirs(getattr(self, "_".join([bn, "dn"])), exist_ok=True)

    ##--

    ## ATTRS
    @staticmethod
    def attribute_names():
        return [ "CROMWELL_DIR", "CROMWELL_PORT", "LSF_DOCKER_VOLUMES",
                "LSF_JOB_GROUP", "LSF_QUEUE", "LSF_USER_GROUP",]

    def validate_attributes(attrs):
        e = []
        for a in CromwellConf.attribute_names():
            if a not in attrs or attrs[a] is None or attrs[a] == "null":
                e.append(a)
        if len(e):
            raise Exception(f"Missing or undefined attributes: {' | '.join(e)}")
    ##-

    @staticmethod
    def resources_dn():
        return os.path.join(os.path.dirname(__file__), "resources")
    #-- resources_dn

    @staticmethod
    def template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.conf.jinja")
    #-- template_fn

    # SERVER
    def server_conf_content(self):
        with open(CromwellConf.template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        attrs = self._attrs.copy()
        attrs.update(self._dir_attrs)
        return template.render(attrs)

    @staticmethod
    def server_run_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.run.jinja")

    def server_run_content(self):
        return self._generate_content(template_fn=CromwellConf.server_run_template_fn(), attrs={"CROMWELL_CONF_FN": self.server_conf_fn})

    @staticmethod
    def server_start_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.start.jinja")

    def server_start_content(self):
        return self._generate_content(template_fn=CromwellConf.server_start_template_fn())

    def _generate_content(self, template_fn, attrs={}):
        if not os.path.exists(template_fn):
            raise Exception(f"Template file {template_fn} does not exist!")
        attrs.update(self._attrs.copy())
        attrs.update(self._dir_attrs)
        with open(template_fn, "r") as f:
            template = jinja2.Template(f.read())
        return template.render(**attrs)
    ##-
#-- CromwellConf
