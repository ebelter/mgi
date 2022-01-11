import jinja2, os, sys

class CromwellConf(object):
    def __init__(self, attrs):
        self._attrs = attrs
        CromwellConf.validate_attributes(attrs)
        self._setdirs()
        self.server_conf_fn = os.path.join(self.server_dn, "conf")
        self.server_script_fn = os.path.join(self.server_dn, "run")
    #-- __init__

    # DIRS
    def dir_names(self):
        return ("cromshell", "db", "lsf_logs", "runs", "server", "wf_logs")

    def _setdirs(self):
        root_dn = self._attrs["CROMWELL_DIR"]
        self._dir_attrs = {}
        for bn in self.dir_names():
            dn = os.path.join(root_dn, bn)
            self._dir_attrs["_".join(["CROMWELL", bn.upper(), "DIR"])] = dn
            setattr(self, "_".join([bn, "dn"]), dn)

    def makedirs(self):
        for bn in self.dir_names():
            os.makedirs(getattr(self, "_".join([bn, "dn"])))
    #-- DIRS

    @staticmethod
    def attribute_names():
        return [ "CROMWELL_DIR", "LSF_DEFAULT_DOCKER", "LSF_DOCKER_VOLUMES",
                "LSF_JOB_GROUP", "LSF_QUEUE", "LSF_USER_GROUP",]
    #-- required_attributes

    def validate_attributes(attrs):
        e = []
        for a in CromwellConf.attribute_names():
            if a not in attrs or attrs[a] is None or attrs[a] == "null":
                e.append(a)
        if len(e):
            raise Exception(f"Missing or undefined attributes: {' | '.join(e)}")
    #-- validate_attributes

    @staticmethod
    def resources_dn():
        return os.path.join(os.path.dirname(__file__), "resources")
    #-- resources_dn

    @staticmethod
    def template_fn():
        return os.path.join(CromwellConf.resources_dn(), "compute1.conf.jinja")
    #-- template_fn

    # SERVER
    @staticmethod
    def server_script_template_fn():
        return os.path.join(CromwellConf.resources_dn(), "server.sh.jinja")

    def server_script_content(self):
        server_conf_fn = self.server_conf_fn
        if not os.path.exists(server_conf_fn):
            raise Exception("Failed to generate the sever script content! Requied server conf file found at {self.server_conf_fn} does not exist!")
        return self._generate_content(CromwellConf.server_script_template_fn(), {"CROMWELL_CONF_FN": server_conf_fn})

    def server_conf(self):
        with open(CromwellConf.template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        attrs = self._attrs.copy()
        attrs.update(self._dir_attrs)
        return template.render(attrs)

    def _generate_content(self, template_fn, attrs=None):
        if not os.path.exists(template_fn):
            raise Exception(f"Template file {template_fn} does not exist!")
        if attrs is None:
            attrs = self._attrs.copy()
            attrs.update(self._dir_attrs)
        with open(template_fn, "r") as f:
            template = jinja2.Template(f.read())
        return template.render(attrs)
#-- CromwellConf
