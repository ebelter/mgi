import click, os, tempfile, unittest
from io import StringIO

class MetricsSeqlendistReportsTest(unittest.TestCase):

    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_plot_bins_length_report(self):
        from cig.metrics.seqlendist.reports import write_plot_bins_length_report as report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_fn = os.path.join(self.temp_d.name, "seqlengthdists.bins.png")
        #out_fn = "p.png"
        with open(out_fn, "wb") as out_h:
            report(out_h, sld)
        self.assertTrue(os.path.exists(out_fn))

    def test_plot_bins_number_report(self):
        from cig.metrics.seqlendist.reports import write_plot_bins_number_report as report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_fn = os.path.join(self.temp_d.name, "seqlengthdists.bins.png")
        #out_fn = "p.png"
        with open(out_fn, "wb") as out_h:
            report(out_h, sld)
        self.assertTrue(os.path.exists(out_fn))

    def test_plot_dist_report(self):
        from cig.metrics.seqlendist.reports import write_plot_dist_report as report
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, label="test")
        sld.complete()
        out_fn = os.path.join(self.temp_d.name, "seqlengthdists.dist.png")
        #out_fn = "p.png"
        with open(out_fn, "wb") as out_h:
            report(out_h, sld)
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
        LOWER -- UPPER         COUNT          BASES      PCT
BIN         1 -- 200               0 (            0 bp ) 0.00%
BIN       201 -- 500              14 (         5402 bp ) 42.05%
BIN       501 -- 1000             11 (         7444 bp ) 57.95%
BIN      1001 -- 2000              0 (            0 bp ) 0.00%
BIN      2001 -- 5000              0 (            0 bp ) 0.00%
BIN      5001 -- 10000             0 (            0 bp ) 0.00%
BIN     10001 -- 20000             0 (            0 bp ) 0.00%
BIN     20001 -- +                 0 (            0 bp ) 0.00%
"""
        out_h.seek(0)
        #print(f"{out_h.read()}")
        #out_h.seek(0)
        self.maxDiff = 10000
        self.assertEqual(out_h.read(), expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
