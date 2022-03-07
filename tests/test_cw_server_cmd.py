import click, os, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf
#from cw.server_cmd import server_cmd as cmd, start_server, wait_for_host
import cw.server_cmd

class CwServerCmdTest(unittest.TestCase):
    def setUp(self):
        from cw.setup_cmd import setup_cmd as cmd
        self.temp_d = tempfile.TemporaryDirectory()
        cw_attrs = dict.fromkeys(CromwellConf.attribute_names(), "NULL")
        cw_attrs["CROMWELL_DIR"] = self.temp_d.name
        cw_attrs["CROMWELL_PORT"] = "8888"
        cw_attrs["LSF_QUEUE"] = "general"
        cw_attrs["LSF_JOB_GROUP"] = "job"
        cw_attrs["LSF_USER_GROUP"] = "user"
        self.cw_attrs = cw_attrs
        self.cw_yaml_fn = os.path.join(self.temp_d.name, "cw.yaml")
        with open(self.cw_yaml_fn, "w") as f:
            f.write(yaml.dump(cw_attrs))
        self.cc = CromwellConf(self.cw_attrs)

        runner = CliRunner()
        result = runner.invoke(cmd, ["--yaml-file", self.cw_yaml_fn], catch_exceptions=False)

    def tearDown(self):
        self.temp_d.cleanup()

    @patch("subprocess.check_output")
    def test_start_server(self, co_p):
        from cw.server_cmd import start_server as fun
        co_p.return_value = b"Job <1234> is submitted to queue <general>.\n"
        job_id = fun(self.cc)
        self.assertEqual(job_id, "1234")
        co_p.return_value = b"Job not submitted"
        with self.assertRaisesRegex(Exception, "Failed to parse LSF bsub command output to get job id: "):
            fun(self.cc)

    @patch("subprocess.check_output")
    @patch("time.sleep")
    def test_wait_on_host(self, sleep_p, co_p):
        from cw.server_cmd import wait_for_host as fun
        job_id = "1234"
        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user RUN   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        host = fun(job_id)
        self.assertEqual(host, "compute1-exec-225.ris.wustl.edu")

        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user PEND   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        with self.assertRaisesRegex(Exception, "Seems server job is not starting. Fix and try again."):
            fun(job_id)

        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user EXIT   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        with self.assertRaisesRegex(Exception, f"Seems server <{job_id}> IS DONE/EXIT. Fix and try again!"):
            fun(job_id)

    @patch("cw.server_cmd.start_server")
    @patch("cw.server_cmd.wait_for_host")
    def test_server_cmd(self, wait_p, start_p):
        from cw.server_cmd import server_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        job_id = "1234"
        start_p.return_value = job_id
        host = "compute1-exec-225.ris.wustl.edu"
        wait_p.return_value = host

        result = runner.invoke(cmd, [self.cw_yaml_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Waiting for job <{job_id}> to start to obtain HOST...
Server running on <{host}> port <8888>
Updating YAML file <{self.cw_yaml_fn}>
Server ready!
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
