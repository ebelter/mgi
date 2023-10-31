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
        self.assertEqual(len(SeqLenDist.lengths_for("lr")), 8)

    def test_init(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        self.assertEqual(sld.lengths, [])
        self.assertEqual(len(sld.distbins), 8)

    def test_load(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn)
        self.assertEqual(sld.lengths[0], ["test", 214, 1])
        self.assertEqual(sld.lengths[1], ["test", 237, 1])
        self.assertEqual(sld.lengths[2], ["test", 261, 1])

    def test_complete(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn)
        sld.complete()
        self.assertEqual(len(sld.lengths_df), 25)
        self.assertFalse(sld.summary_df.empty)
        expected = """min         214.00
max         922.00
mean        513.84
length    12846.00
count        25.00
n50         593.00
Name: test, dtype: float64"""
        #print(f"{sld.summary_df.loc['test']}")
        #print(f"||{sld.bins_df.xs('test')}||")
        self.assertEqual(f"{sld.summary_df.loc['test']}", expected)
        expected = """     min  max        mean  length  count
bin                                     
1    214  500  385.857143    5402     14
2    554  922  676.727273    7444     11"""
        self.assertEqual(f"{sld.bins_df.xs('test')}", expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
