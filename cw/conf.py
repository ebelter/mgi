import jinja2, os, sys, yaml

class CromwellConf(object):
    def __init__(self, attrs):
        self._attrs = attrs
        self.is_validated = False

    ## ATTRIBUTES
    def getattr(self, name):
        if name not in self.attribute_names():
            raise Exception(f"Unknown attribute <{name}>")
        if name in self._attrs:
            return self._attrs[name]
        return None

    def setattr(self, name, value):
        if name not in self.attribute_names():
            raise Exception(f"Unknown attribute <{name}>")
        self._attrs[name] = value
        return value

    @staticmethod
    def known_attributes():
        return {
                # ATTR: [value, required]
                "CROMWELL_DIR": [os.getcwd, True],
                "CROMWELL_PORT": ["8888", True],
                "LSF_DOCKER_VOLUMES": ["/scratch1/fs1/hprc:/scratch1/fs1/hprc /storage1/fs1/hprc:/storage1/fs1/hprc", True],
                "LSF_JOB_GROUP": [None, True],
                "LSF_QUEUE": [None, True],
                "LSF_USER_GROUP": [None, True],
                "CROMWELL_JOB_ID": [None, False],
                "CROMWELL_HOST": [None, False],
                "CROMWELL_URL": [None, False],
                }

    @staticmethod
    def attribute_names():
        return CromwellConf.known_attributes().keys()

    def required_attribute_names():
        names = set()
        known_attrs = CromwellConf.known_attributes()
        for name, (value, isrequired) in known_attrs.items():
            if isrequired:
                names.add(name)
        return names

    def default_attributes():
        attrs = {}
        known_attrs = CromwellConf.known_attributes()
        #for name, (value, isrequired) in known_attrs.items():
        for name, (value, isrequired) in known_attrs.items():
            if callable(value):
                value = value()
            attrs[name] = value
        return attrs

    def validate_attributes(self):
        e = []
        for name in CromwellConf.required_attribute_names():
            value = self.getattr(name)
            if value is None:#if a not in attrs or attrs[a] is None or attrs[a] == "null":
                e.append(name)
        if len(e):
            raise Exception(f"Missing or undefined attributes: {' | '.join(e)}")
        self.is_validated = True
    ##-

    ## SAVE / LOAD
    @staticmethod
    def yaml_fn():
        return "cw.yaml"

    def save(self):
        yaml_fn = CromwellConf.yaml_fn()
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(self._attrs))

    def safe_load():
        yaml_fn = CromwellConf.yaml_fn()
        if os.path.exists(yaml_fn):
            return CromwellConf.load(yaml_fn)
        return CromwellConf(CromwellConf.default_attributes())

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
    ##--

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

    ## RESOURCES
    @staticmethod
    def resources_dn():
        return os.path.join(os.path.dirname(__file__), "resources")

    @staticmethod
    def template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.conf.jinja")
    ##-

    ### conf
    def server_conf_fn(self):
        return os.path.join(self.dir_for("server"), "conf")

    def server_conf_content(self):
        with open(CromwellConf.template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        attrs = self._attrs.copy()
        attrs.update(self.dir_attrs())
        return template.render(attrs)

    ### db
    @staticmethod
    def server_db_fn():
        return os.path.join("server", "db")

    ### run
    def server_run_fn(self):
        return os.path.join(self.dir_for("server"), "run")

    @staticmethod
    def server_run_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.run.jinja")

    def server_run_content(self):
        return self._generate_content(template_fn=CromwellConf.server_run_template_fn(), attrs={"CROMWELL_CONF_FN": self.server_conf_fn()})

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
