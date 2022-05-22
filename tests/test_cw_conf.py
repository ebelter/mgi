import os, re, unittest, yaml
from jinja2 import Template

from cw.conf import CromwellConf
from tests.test_cw_base import BaseWithDb

class CwCconfTest(BaseWithDb):
    def setUp(self):
        self.cc_attrs = {}
        for name in CromwellConf.attribute_names():
            self.cc_attrs[name] = "MINE"
        self.cc_attrs["CROMWELL_DIR"] = self.temp_d.name
        self.yaml_fn = os.path.join(self.temp_d.name, CromwellConf.yaml_fn())
        with open(self.yaml_fn, "w") as f:
            f.write(yaml.dump(self.cc_attrs))

    def test_init(self):
        cc = CromwellConf({})
        self.assertTrue(bool(cc))
        self.assertFalse(cc.is_validated)

    def test_attributes(self):
        known_attributes = CromwellConf.known_attributes()
        self.assertTrue(bool(known_attributes))
        self.assertEqual(type(known_attributes), dict)
        default_attributes = CromwellConf.default_attributes()
        self.assertTrue(bool(default_attributes))
        self.assertEqual(type(default_attributes), dict)
        self.assertEqual(default_attributes.keys(), known_attributes.keys())
        required_attribute_names = CromwellConf.required_attribute_names()
        self.assertTrue(bool(required_attribute_names))
        self.assertEqual(type(required_attribute_names), set)

        cc = CromwellConf(default_attributes)
        self.assertDictEqual(cc._attrs, default_attributes)
        self.assertEqual(cc.getattr("CROMWELL_PORT"), default_attributes["CROMWELL_PORT"])
        self.assertEqual(cc.getattr("CROMWELL_PORT"), cc._attrs["CROMWELL_PORT"])
        cc.CROMWELL_PORT = "9999"
        self.assertEqual(cc.setattr("CROMWELL_PORT", "9999"), "9999")
        self.assertEqual(cc.getattr("CROMWELL_PORT"), cc._attrs["CROMWELL_PORT"])
        self.assertEqual(cc.getattr("CROMWELL_PORT"), "9999")

        self.assertEqual(cc.get("CROMWELL_PORT"), default_attributes["CROMWELL_PORT"])
        self.assertEqual(cc.get("CROMWELL_PORT"), cc._attrs["CROMWELL_PORT"])
        cc.CROMWELL_PORT = "9999"
        self.assertEqual(cc.set("CROMWELL_PORT", "9999"), "9999")
        self.assertEqual(cc.get("CROMWELL_PORT"), cc._attrs["CROMWELL_PORT"])
        self.assertEqual(cc.get("CROMWELL_PORT"), "9999")

    def test_load(self):
        attrs_n = CromwellConf.attribute_names()
        self.assertEqual(len(attrs_n), 9)

        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        self.assertTrue(cc._attrs)
        self.assertTrue(cc.is_validated)

    def test_save(self):
        cc = CromwellConf(self.cc_attrs)
        os.chdir(self.temp_d.name)
        os.makedirs("test_save")
        os.chdir("test_save")
        cc.save()
        yaml_fn = CromwellConf.yaml_fn()
        self.assertTrue(os.path.exists("cw.yaml"))
        with open(yaml_fn, "r") as f:
            got = yaml.safe_load(f)
        self.assertDictEqual(got, self.cc_attrs)

    def test_safe_load(self):
        dn = os.path.join(self.temp_d.name, "noyaml")
        os.makedirs(dn)
        os.chdir(dn)
        cc = CromwellConf.safe_load()
        self.assertTrue(cc)
        self.assertDictEqual(cc._attrs, CromwellConf.default_attributes())
        self.assertTrue(not cc.is_validated)

        os.chdir(self.temp_d.name)
        cc = CromwellConf.safe_load()
        self.assertTrue(cc._attrs)
        self.assertTrue(cc.is_validated)

    def test_validate_attributes(self):
        cc = CromwellConf({})
        self.assertTrue(bool(cc))
        with self.assertRaisesRegex(Exception, "Missing or undefined attributes"):
            cc.validate_attributes()
        for name in CromwellConf.attribute_names():
            cc._attrs[name] = "MINE"
        CromwellConf.validate_attributes(cc)

    def test_server_conf(self):
        from cw import appcon
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        configs = ["docker_volumes=MINE", "job_group=MINE", "queue=MINE", "user_group=MINE"]
        for c in configs:
            n, v = c.split("=")
            appcon.set(group="lsf", name=n, value=v)
        server_conf = cc.server_conf_content()
        self.assertRegex(server_conf, f"root = \"{appcon.get('runs_dn')}\"")
        self.assertRegex(server_conf, "LSF_DOCKER_VOLUMES='\$\{cwd\}:\$\{docker_cwd\} MINE'")
        m = re.findall(f"\-oo {appcon.get('logs_dn')}", server_conf)
        self.assertEqual(len(m), 1)
        self.assertRegex(server_conf, f"workflow-log-dir = \"{appcon.get('runs_dn')}\"")
        self.assertRegex(server_conf, f"file:{appcon.get('db_dn')}/db")

    def test_server_run(self):
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        content = cc.server_run_content()
        self.assertRegex(content, f"LSF_DOCKER_VOLUMES='MINE")

    def test_server_start(self):
        from cw import appcon
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        content = cc.server_start_content()
        self.assertRegex(content, f"file={appcon.get(group='server', name='conf_fn')}")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
