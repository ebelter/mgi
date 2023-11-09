import click, os, tempfile, unittest
from io import StringIO

class MetricsSeqlendistReportsTest(unittest.TestCase):

    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_csv_report(self):
        from cig.metrics.seqlendist.reports import write_csv_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_csv_report(out_h, sld)
        expected_output = """label,count,length,min,max,mean,median,n50
test,25,12846,214,922,513,496,593
"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_json_report(self):
        from cig.metrics.seqlendist.reports import write_json_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """{"label": "test", "min": 214, "max": 922, "mean": 513, "median": 496, "length": 12846, "count": 25, "n50": 593}"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)

    def test_png_report(self):
        from cig.metrics.seqlendist.reports import write_png_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_fn = os.path.join(self.temp_d.name, "seqlengthdists.png")
        #out_fn = "p.png"
        with open(out_fn, "wb") as out_h:
            write_png_report(out_h, sld)
        self.assertTrue(os.path.exists(out_fn))

    def test_text_report(self):
        from cig.metrics.seqlendist.reports import write_text_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_text_report(out_h, sld)
        expected_output = """SAMPLE    test
COUNT     25
BASES     12846 bp
MEAN      513 bp
MEDIAN    496 bp
N50       593 bp
LARGEST   922 bp
SEQS        1 -- 200      (            0 bp ) 0.00%
SEQS      201 -- 500      (         5402 bp ) 42.05%
SEQS      501 -- 1000     (         7444 bp ) 57.95%
SEQS     1001 -- 2000     (            0 bp ) 0.00%
SEQS     2001 -- 5000     (            0 bp ) 0.00%
SEQS     5001 -- 10000    (            0 bp ) 0.00%
SEQS    10001 -- 20000    (            0 bp ) 0.00%
SEQS    20001 -- +        (            0 bp ) 0.00%
"""
        out_h.seek(0)
        self.maxDiff = 10000
        self.assertEqual(out_h.read(), expected_output)

    def test_yaml_report(self):
        from cig.metrics.seqlendist.reports import write_yaml_report as write_report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_h = StringIO()
        write_report(out_h, sld)
        expected_output = """count: 25
label: test
length: 12846
max: 922
mean: 513
median: 496
min: 214
n50: 593
"""
        out_h.seek(0)
        self.assertEqual(out_h.read(), expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
