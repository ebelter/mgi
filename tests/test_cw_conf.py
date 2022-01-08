import os, tempfile, unittest, yaml
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
        self.assertEqual(cc.root_dn, self.temp_d.name)
        self.assertDictEqual(cc._attrs, attrs)
        return cc

    def test_cromwell_conf(self):
        attrs_n = CromwellConf.attribute_names()
        self.assertTrue(bool(attrs_n))
        self.assertEqual(len(attrs_n), 6)

        cc = self.get_cc()
        self.assertEqual(cc.root_dn, cc._attrs["CROMWELL_DIR"])
        self.assertEqual(cc._attrs["CROMWELL_ROOT_DIR"], os.path.join(cc._attrs["CROMWELL_DIR"], "runs"))
        for bn in cc.dir_names():
            attr_n = "_".join([bn, "dn"])
            self.assertEqual(getattr(cc, attr_n), os.path.join(cc.root_dn, bn))
        self.assertEqual(cc.server_script_fn, os.path.join(cc.server_dn, "run"))

    def test_validate_attributes(self):
        with self.assertRaisesRegex(Exception, "Missing or undefined attributes"):
            CromwellConf.validate_attributes({})
        CromwellConf.validate_attributes(self.get_cc()._attrs)

    def test_resources(self):
        resources_dn = CromwellConf.resources_dn()
        expected_dn = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "cw", "resources")
        self.assertEqual(resources_dn, expected_dn)

        got = CromwellConf.template_fn()
        expected = os.path.join(expected_dn, "compute1.conf.jinja")
        self.assertEqual(got, expected)

        got = CromwellConf.server_script_template_fn()
        expected = os.path.join(expected_dn, "server.sh.jinja")
        self.assertEqual(got, expected)

    def test_makedirs(self):
        cc = self.get_cc()
        cc.makedirs()
        for bn in cc.dir_names():
            self.assertTrue(os.path.exists(getattr(cc, "_".join([bn, "dn"]))))

    def test_server_conf(self):
        cc = self.get_cc()
        server_conf_fn = cc.server_conf_fn
        self.assertEqual(server_conf_fn, os.path.join(self.temp_d.name,"server", "conf"))
        server_conf = cc.server_conf()
        self.assertRegex(server_conf, f"root = \"{self.temp_d.name}/runs\"")

        os.makedirs(os.path.dirname(server_conf_fn))
        with open(server_conf_fn, "w") as f:
            f.write(server_conf)
        server_script = cc.server_script_content()
        self.assertRegex(server_script, server_conf_fn)
        
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
