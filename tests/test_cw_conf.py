import os, re, tempfile, unittest, yaml
from jinja2 import Template

from cw.conf import CromwellConf

class CwCconfTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.cc_attrs = {}
        for name in CromwellConf.attribute_names():
            self.cc_attrs[name] = "MINE"
        self.cc_attrs["CROMWELL_DIR"] = self.temp_d.name
        self.yaml_fn = os.path.join(self.temp_d.name, CromwellConf.yaml_fn())
        with open(self.yaml_fn, "w") as f:
            f.write(yaml.dump(self.cc_attrs))

    def tearDown(self):
        self.temp_d.cleanup()

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

    def test_load(self):
        attrs_n = CromwellConf.attribute_names()
        self.assertEqual(len(attrs_n), 6)

        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        self.assertTrue(cc._attrs)
        self.assertTrue(cc.is_validated)

        dir_names = CromwellConf.known_dir_names()
        self.assertEqual(len(dir_names), 5)
        for name in dir_names:
            self.assertEqual(cc.dir_for(name), os.path.join(self.temp_d.name, name))

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
        pass

    def test_validate_attributes(self):
        cc = CromwellConf({})
        self.assertTrue(bool(cc))
        with self.assertRaisesRegex(Exception, "Missing or undefined attributes"):
            cc.validate_attributes()
        for name in CromwellConf.attribute_names():
            cc._attrs[name] = "MINE"
        CromwellConf.validate_attributes(cc)

    def test_resources(self):
        resources_dn = CromwellConf.resources_dn()
        expected_dn = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "cw", "resources")
        self.assertEqual(resources_dn, expected_dn)

        got = CromwellConf.template_fn()
        expected = os.path.join(expected_dn, "server.conf.jinja")
        self.assertEqual(got, expected)

        got = CromwellConf.server_run_template_fn()
        expected = os.path.join(expected_dn, "server.run.jinja")
        self.assertEqual(got, expected)

        got = CromwellConf.server_start_template_fn()
        expected = os.path.join(expected_dn, "server.start.jinja")
        self.assertEqual(got, expected)

    def test_makedirs(self):
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()
        cc.makedirs()
        for name in CromwellConf.known_dir_names():
            self.assertTrue(os.path.exists(cc.dir_for(name)))

    def test_server_conf(self):
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()

        server_conf_fn = cc.server_conf_fn()
        self.assertEqual(server_conf_fn, os.path.join(self.temp_d.name,"server", "conf"))
        server_conf = cc.server_conf_content()
        self.assertRegex(server_conf, f"root = \"{cc.dir_for('runs')}\"")
        self.assertRegex(server_conf, "LSF_DOCKER_VOLUMES='\$\{cwd\}:\$\{docker_cwd\} MINE'")
        m = re.findall(f"\-oo {cc.dir_for('lsf_logs')}", server_conf)
        self.assertEqual(len(m), 1)
        self.assertRegex(server_conf, f"workflow-log-dir = \"{cc.dir_for('wf_logs')}\"")
        self.assertRegex(server_conf, f"file:{cc.dir_for('db')}")

    def test_server_run(self):
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()

        template_fn = cc.server_run_template_fn()
        self.assertEqual(template_fn, os.path.join(CromwellConf.resources_dn(), "server.run.jinja"))
        content = cc.server_run_content()
        self.assertRegex(content, f"file={cc.server_conf_fn}")

    def test_server_start(self):
        os.chdir(self.temp_d.name)
        cc = CromwellConf.load()

        template_fn = cc.server_start_template_fn()
        self.assertEqual(template_fn, os.path.join(CromwellConf.resources_dn(), "server.start.jinja"))
        content = cc.server_start_content()
        self.assertRegex(content, f"LSF_DOCKER_VOLUMES='MINE")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
