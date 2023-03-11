import click, json, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import Mock, patch

from tests.cw.test_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def _setUpClass(self):
        self.wf_id = "67c1c73d-9b92-408e-9f7a-5ad0c9df2a36"
        self.metadata_fn = os.path.join(self.data_dn, "wf", f"{self.wf_id}.md")

    @patch("cw.server.server_factory")
    def test_status_cmd(self, server_p):
        from cw.wf_status import status_cmd as cmd
        from cw import db, Workflow
        runner = CliRunner()

        wf = Workflow.query.get(1)
        self.assertTrue(wf)
        self.assertEqual(wf.status, "succeeded")

        server = Mock()
        server_p.return_value = server
        server.configure_mock(**{"status_for_workflow.return_value": None})

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [str(wf.id)], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"""Failed to get status for workflow {self.wf_id} ... see above errors.
"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(server_p.call_count, 1)

        server.configure_mock(**{"status_for_workflow.return_value": "failed"})
        result = runner.invoke(cmd, [wf.wf_id], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""failed
"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(server_p.call_count, 2)
        db.session.refresh(wf)
        self.assertEqual(wf.status, "failed")

    @patch("cw.server.server_factory")
    def test_status_detailed_cmd(self, server_p):
        from cw.wf_status import status_cmd as cmd
        from cw import db, Workflow
        runner = CliRunner()

        wf = Workflow.query.get(1)
        self.assertTrue(wf)
        self.assertEqual(wf.status, "failed") # set in previous test

        server = Mock()
        server_p.return_value = server

        with open(self.metadata_fn, "r") as f:
            md = json.load(f)

        server.configure_mock(**{"metadata_for_workflow.return_value": md})
        result = runner.invoke(cmd, [wf.wf_id, "--detailed"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.maxDiff = 10000
        expected_output = f"""Workflow ID:      67c1c73d-9b92-408e-9f7a-5ad0c9df2a36
Status:           Running
Workflow name:    test.hello-world
Workflow inputs:  /home/ebelter/dev/mgi/tests/cw/data/wf/homer.hello-world.inputs.json
Workflow name:
Tasks:
name                                         time                 aborted    done    running    preempted    failed
long_read_rna_pipeline.clean_reference       0:01:17                    0       1          0            0         0
long_read_rna_pipeline.get_splice_junctions  0:00:29                    0       1          0            0         0
long_read_rna_pipeline.minimap2              4:15:26                    0       1          0            0         0
long_read_rna_pipeline.init_talon_db         1:15:19                    0       1          0            0         0
long_read_rna_pipeline.combined_fastq        0:00:53                    0       1          0            0         0
long_read_rna_pipeline.decompressed_gtf      0:00:06                    0       1          0            0         0
long_read_rna_pipeline.transcriptclean"""
        self.assertRegex(result.output, expected_output)
        self.assertEqual(server_p.call_count, 1)
        db.session.refresh(wf)
        self.assertEqual(wf.status, "running")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
