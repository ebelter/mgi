import click, os, tempfile, unittest
from io import StringIO

class MetricsCollateReportsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_sv_report(self):
        from cig.metrics.collate.reports import write_csv_report, write_tsv_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_csv_report(out_h, sld)
        expected_output = """metric,test
min,214
max,922
mean,513.84
median,496
length,12846
count,25
n50,593
"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

        out_h = StringIO()
        expected_output.replace(",", "\t")
        write_csv_report(out_h, sld)
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_json_report(self):
        from cig.metrics.collate.reports import write_json_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """[
  {
    "min": 214.0,
    "max": 922.0,
    "mean": 513.84,
    "median": 496.0,
    "length": 12846.0,
    "count": 25.0,
    "n50": 593.0,
    "label": "test"
  }
]"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_table_report(self):
        from cig.metrics.collate.reports import write_table_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """            test
------  --------
min       214
max       922
mean      513.84
median    496
length  12846
count      25
n50       593"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_mw_report(self):
        from cig.metrics.collate.reports import write_mw_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """{| class="wikitable" style="text-align: left;"
|+ <!-- caption -->
|-
!        !! align="right"|     test
|-
| min    || align="right"|   214
|-
| max    || align="right"|   922
|-
| mean   || align="right"|   513.84
|-
| median || align="right"|   496
|-
| length || align="right"| 12846
|-
| count  || align="right"|    25
|-
| n50    || align="right"|   593
|}"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_yaml_report(self):
        from cig.metrics.collate.reports import write_yaml_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """- count: 25.0
  label: test
  length: 12846.0
  max: 922.0
  mean: 513.84
  median: 496.0
  min: 214.0
  n50: 593.0
"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
