import click, os, tempfile, unittest
from io import StringIO

class MetricsSeqlendistObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_lengths_for(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        with self.assertRaisesRegex(Exception, "Unknown binning type: foo"):
            SeqLenDist.lengths_for("foo")
        self.assertEqual(len(SeqLenDist.lengths_for("asm")), 7)
        self.assertEqual(len(SeqLenDist.lengths_for("lr")), 8)
        self.assertEqual(SeqLenDist.lengths_for("501,1001,1501,2001"), [1, 501, 1001, 1501, 2001])
        self.assertEqual(SeqLenDist.lengths_for("2000:500"), [1, 501, 1001, 1501, 2001])

    def test_init(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        self.assertEqual(sld.lengths, [])
        self.assertEqual(len(sld.distbins), 8)

    def test_load(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, "test")
        self.assertEqual(sld.lengths[0], ["test", 214, 1])
        self.assertEqual(sld.lengths[1], ["test", 237, 1])
        self.assertEqual(sld.lengths[2], ["test", 261, 1])

    def test_complete(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, "test")
        sld.complete()
        self.assertEqual(len(sld.lengths_df), 25)
        self.assertFalse(sld.summary_df.empty)
        expected = """min         214.00
max         922.00
mean        513.84
median      496.00
length    12846.00
count        25.00
n50         593.00
Name: test, dtype: float64"""
        #print(f"{sld.summary_df.loc['test']}")
        self.assertEqual(f"{sld.summary_df.loc['test']}", expected)
        self.maxDiff = 10000
        #import re
        #s = re.sub('\n', '|\n', f"{sld.bins_df.xs('test')}")
        #print(f"{s}")
        expected = """       min    max        mean  median  length  count
bin                                                 
0      0.0    0.0    0.000000     0.0     0.0    0.0
1    214.0  500.0  385.857143   407.0  5402.0   14.0
2    554.0  922.0  676.727273   617.0  7444.0   11.0
3      0.0    0.0    0.000000     0.0     0.0    0.0
4      0.0    0.0    0.000000     0.0     0.0    0.0
5      0.0    0.0    0.000000     0.0     0.0    0.0
6      0.0    0.0    0.000000     0.0     0.0    0.0
7      0.0    0.0    0.000000     0.0     0.0    0.0"""
        self.assertEqual(f"{sld.bins_df.xs('test')}", expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
