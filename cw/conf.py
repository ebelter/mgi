import jinja2, os, sys, yaml

class CromwellConf(object):
    def __init__(self, attrs):
        self._attrs = attrs
        self.is_validated = False

    def save(self):
        yaml_fn = CromwellConf.yaml_fn()
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(self._attrs))

    def safe_load():
        yaml_fn = CromwellConf.yaml_fn()
        if os.path.exists(yaml_fn):
            return CromwellConf.load(yaml_fn)
        return CromwellConf(dict.fromkeys(CromwellConf.attribute_names()))

    def load(yaml_fn="cw.yaml"):
        yaml_file = CromwellConf.yaml_fn()
        if not os.path.exists(yaml_file):
            raise Exception(f"Cannot create config object, given YAML file <{yaml_file}> does not exist!")
        with open(yaml_fn, "r") as f:
            attrs = yaml.safe_load(f)
        self = CromwellConf(attrs)
        self.validate_attributes()
        self._attrs["CROMWELL_DIR"] = os.path.abspath(self._attrs["CROMWELL_DIR"])
        return self

    @staticmethod
    def yaml_fn():
        return "cw.yaml"

    @staticmethod
    def known_dir_names():
        return set(["db", "lsf_logs", "runs", "server", "wf_logs"])

    def dir_for(self, name):
        cw_dn = self._attrs.get("CROMWELL_DIR", None)
        if cw_dn is None:
            raise Exception("No CROMWELL_DIR set in cromwell conf attributes!")
        if name not in CromwellConf.known_dir_names():
            raise Exception(f"Dir name <name> is not in the known directory names!")
        return os.path.join(cw_dn, name)

    def dir_attrs(self):
        dir_attrs = {}
        for name in CromwellConf.known_dir_names():
            dir_attrs["_".join(["CROMWELL", name.upper(), "DIR"])] = self.dir_for(name)
        return dir_attrs

    def makedirs(self):
        for name in CromwellConf.known_dir_names():
            os.makedirs(self.dir_for(name), exist_ok=True)

    ##--

    ## SETUP
    def setup(self):
        self.makedirs()
        self.write_server_files()

    def write_server_files(self):
        server_dn = self.dir_for("server")
        for name in ("conf", "run", "start"):
            fn =  getattr(self, f"server_{name}_fn")
            fun = getattr(self, f"server_{name}_content")
            with open(fn(), "w") as f:
                f.write(fun())
    ##--

    ## ATTRS
    @staticmethod
    def attribute_names():
        return [ "CROMWELL_DIR", "CROMWELL_PORT", "LSF_DOCKER_VOLUMES",
                "LSF_JOB_GROUP", "LSF_QUEUE", "LSF_USER_GROUP",]

    def validate_attributes(self):
        attrs = self._attrs
        e = []
        for a in CromwellConf.attribute_names():
            if a not in attrs or attrs[a] is None or attrs[a] == "null":
                e.append(a)
        if len(e):
            raise Exception(f"Missing or undefined attributes: {' | '.join(e)}")
        self.is_validated = True
    ##-

    @staticmethod
    def resources_dn():
        return os.path.join(os.path.dirname(__file__), "resources")
    #-- resources_dn

    @staticmethod
    def template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.conf.jinja")
    #-- template_fn

    ## SERVER
    ### conf
    def server_conf_fn(self):
        return os.path.join(self.dir_for("server"), "conf")

    def server_conf_content(self):
        with open(CromwellConf.template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        attrs = self._attrs.copy()
        attrs.update(self.dir_attrs())
        return template.render(attrs)

    ### run
    def server_run_fn(self):
        return os.path.join(self.dir_for("server"), "run")

    @staticmethod
    def server_run_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.run.jinja")

    def server_run_content(self):
        return self._generate_content(template_fn=CromwellConf.server_run_template_fn(), attrs={"CROMWELL_CONF_FN": self.server_conf_fn})

    ### start
    @staticmethod
    def server_start_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.start.jinja")

    def server_start_fn(self):
        return os.path.join(self.dir_for("server"), "start")

    def server_start_content(self):
        return self._generate_content(template_fn=CromwellConf.server_start_template_fn())

    ###
    def _generate_content(self, template_fn, attrs={}):
        if not os.path.exists(template_fn):
            raise Exception(f"Template file {template_fn} does not exist!")
        attrs.update(self._attrs.copy())
        attrs.update(self.dir_attrs())
        with open(template_fn, "r") as f:
            template = jinja2.Template(f.read())
        return template.render(**attrs)
    ##-
#-- CromwellConf
