import os, re, tempfile, unittest, yaml
from jinja2 import Template

from cw.conf import CromwellConf

class CwCconfTest(unittest.TestCase):
    
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def get_cc(self):
        attrs = dict.fromkeys(CromwellConf.attribute_names(), "MINE")
        attrs["CROMWELL_DIR"] = self.temp_d.name
        cc = CromwellConf(attrs=attrs)
        self.assertTrue(bool(cc))
        self.assertDictEqual(cc._attrs, attrs)
        return cc

    def test_cromwell_conf(self):
        cc = self.get_cc()

        attrs_n = CromwellConf.attribute_names()
        self.assertEqual(len(attrs_n), 6)
        self.assertTrue(cc._attrs)

        dir_names = cc.known_dir_names()
        self.assertEqual(len(dir_names), 5)
        for name in dir_names:
            self.assertEqual(cc.dir_for(name), os.path.join(self.temp_d.name, name))

    def test_validate_attributes(self):
        with self.assertRaisesRegex(Exception, "Missing or undefined attributes"):
            CromwellConf.validate_attributes({})
        CromwellConf.validate_attributes(self.get_cc()._attrs)

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
        cc = self.get_cc()
        cc.makedirs()
        for name in cc.known_dir_names():
            self.assertTrue(os.path.exists(cc.dir_for(name)))

    def test_server_conf(self):
        cc = self.get_cc()
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
        cc = self.get_cc()
        template_fn = cc.server_run_template_fn()
        self.assertEqual(template_fn, os.path.join(CromwellConf.resources_dn(), "server.run.jinja"))
        content = cc.server_run_content()
        self.assertRegex(content, f"file={cc.server_conf_fn}")

    def test_server_start(self):
        cc = self.get_cc()
        template_fn = cc.server_start_template_fn()
        self.assertEqual(template_fn, os.path.join(CromwellConf.resources_dn(), "server.start.jinja"))
        content = cc.server_start_content()
        self.assertRegex(content, f"LSF_DOCKER_VOLUMES='MINE")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
