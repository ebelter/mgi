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
        self.root_dn = self._attrs["CROMWELL_DIR"]
        for bn in self.dir_names():
            setattr(self, "_".join([bn, "dn"]), os.path.join(self.root_dn, bn))
        self._attrs["CROMWELL_ROOT_DIR"] = self.runs_dn

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
            raise Exception("Failed to get sever script content! No server conf file found at {self.server_conf_fn}!")
        with open(CromwellConf.server_script_template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        return template.render(CROMWELL_CONF_FN=server_conf_fn)

    def server_conf(self):
        with open(CromwellConf.template_fn(), "r") as f:
            template = jinja2.Template(f.read())
        return template.render(self._attrs)
    #-- SERVER_CONF
#-- CromwellConf
