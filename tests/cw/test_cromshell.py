import os, tempfile, unittest
from unittest.mock import patch

from cw.cromshell import config_dn, server_fn, update_server

class CwCromshellTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_cromshell_dirs_and_files(self ):
        self.assertEqual(config_dn(), os.path.join(os.sep, "apps", "cromshell", ".cromshell"))
        self.assertEqual(server_fn(), os.path.join(os.sep, "apps", "cromshell", ".cromshell", "cromwell_server.config"))

    @patch("cw.cromshell.config_dn")
    def test_update_server(self, p):
        url = "http://server:0000"
        p.return_value = "/blah"

        rv, msg = update_server(url)
        self.assertEqual(rv, None)
        self.assertEqual(msg, "No cromshell directory at </blah> detected, not updating url\n")

        p.return_value = self.temp_d.name
        rv, msg = update_server(url)
        self.assertEqual(rv, True)
        self.assertEqual(msg, f"Updated cromshell url <{url}> in <{server_fn()}>\n")
        with open(server_fn(), "r") as f:
            got = f.readline().rstrip()
        self.assertEqual(got, url)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
