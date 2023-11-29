import click, os, tempfile, unittest
from click.testing import CliRunner

class MetricsAlignemntCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.samtools_statsfile = os.path.join(self.data_dn, "samtools.stat")
        self.vg_statsfile = os.path.join(self.data_dn, "vgstat.stat")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_resolve_reports(self):
        from cig.metrics.alignment.cmd import resolve_reports as fun
        from cig.metrics.alignment.reports import write_summary_report_table, write_summary_report_csv

        got = fun(["summary", "summary:csv"])
        self.assertEqual(got, [["summary", "table", write_summary_report_table], ["summary", "csv", write_summary_report_csv]])
        with self.assertRaisesRegex(Exception, f"Unknown report type \(unknown\) in given report: unknown"):
            fun(["unknown"])
        with self.assertRaisesRegex(Exception, f"Unknown report format \(unknown\) in given report: summary:unknown"):
            fun(["summary:unknown"])

    def test1_cmd(self):
        from cig.metrics.alignment.cmd import alignment_cmd as cmd
        #from cig.metrics.alignment.reports import available_reports_types, available_report_formats
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "SAMPLE001")
        result = runner.invoke(cmd, ["-r", "summary:table", "-l", "SAMPLE001,SAMPLE001", "-o", out_n, self.samtools_statsfile, self.vg_statsfile], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(out_n+".table"))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
