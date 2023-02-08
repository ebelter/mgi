import os, tempfile, unittest

from tests.test_base_classes import TestBaseWithDb

class EntityPathFactory(TestBaseWithDb):
    def test_resolve_entity_and_kind_from_value(self):
        from mgi.entity.helpers import resolve_entity_and_kind_from_value

        for ek in ("cram", "cram crai", "cram md5"):
            fn = os.path.join(os.sep, "mnt", "data", ".".join(["__TEST__"] + ek.split(" ")))
            e, k, e2 = resolve_entity_and_kind_from_value(fn)
            self.assertEqual(e, "__TEST__")
            self.assertEqual(k, ek)
            self.assertEqual(e2, "__TEST__")

        for ek in ("vcf", "vcf tbi"):
            fn = os.path.join(os.sep, "mnt", "data", ".".join(["__TEST__", "*", "g"] + ek.split(" ")))
            e, k, e2 = resolve_entity_and_kind_from_value(fn)
            self.assertEqual(e, "__TEST__")
            self.assertEqual(k, "g "+ek)
            self.assertEqual(e2, "__TEST__")

        e, k, e2 = resolve_entity_and_kind_from_value("__TEST__.dunno.whatever.fastq")
        self.assertEqual(e, "__TEST__")
        self.assertEqual(k, "fastq")
        self.assertEqual(e2, "__TEST__.dunno.whatever")

        e, k, e2 = resolve_entity_and_kind_from_value("__TEST__.fastq.gz")
        self.assertEqual(e, "__TEST__")
        self.assertEqual(k, "fastq")
        self.assertEqual(e2, "__TEST__")

        e, k, e2 = resolve_entity_and_kind_from_value("__TEST__.dunno.whatever")
        self.assertEqual(e, "__TEST__")
        self.assertEqual(k, "")
        self.assertEqual(e2, "__TEST__.dunno.whatever")

    def test_entity_on_cli(self):
        from mgi.entity.helpers import paths_rdr_factory as rdr_factory

        rdr = rdr_factory("sample1")
        self.assertTrue(bool(rdr))

        got = []
        for path_d in rdr:
            got.append(path_d)
        expected = [{"entity": "sample1"}]
        self.assertListEqual(got, expected)

    def test_tsv_rdr(self):
        from mgi.entity.helpers import paths_rdr_factory as rdr_factory

        fn = os.path.join(self.temp_d.name, "paths.tsv")
        with open(fn, "w") as f:
            f.write("\t".join(["value", "exists"])+"\n")
            f.write("\t".join(["file1", "1"])+"\n")
            f.write("\t".join(["file2", "0"])+"\n")

        rdr = rdr_factory(fn)
        self.assertTrue(bool(rdr))

        got = []
        for path_d in rdr:
            got.append(path_d)
        expected = [{"value": "file1", "exists": "1"}, {"value": "file2", "exists": "0"}]
        self.assertListEqual(got, expected)

    def test_value_rdr(self):
        from mgi.entity.helpers import paths_rdr_factory as rdr_factory

        fn = os.path.join(self.temp_d.name, "paths.tsv")
        with open(fn, "w") as f:
            f.write("file1\n")
            f.write("file2\n")

        rdr = rdr_factory(fn)
        self.assertTrue(bool(rdr))

        got = []
        for path_d in rdr:
            got.append(path_d)
        expected = [{"value": "file1"}, {"value": "file2"}]
        self.assertListEqual(got, expected)

    def test_gcp_rdr(self):
        from mgi.entity.helpers import paths_rdr_factory as rdr_factory

        fn = os.path.join(self.temp_d.name, "paths.gcpstat")
        with open(fn, "w") as f:
            f.write("""gs://fc-secure-3aa171b5-8208-4467-8743-c7879f3da6da/H_XS-356091-0186761975.cram:
    Creation time:          Tue, 18 Jun 2019 15:43:30 GMT
    Update time:            Tue, 18 Jun 2019 15:43:30 GMT
    Storage class:          STANDARD
    Content-Language:       en
    Content-Length:         17129017157
    Content-Type:           application/octet-stream
    Metadata:
        goog-reserved-file-mtime:1499626893
    Hash (crc32c):          dhjnMQ==
    Hash (md5):             gLU4quAMng1xZm7B8u+VbQ==
    ETag:                   CKCXgsyv8+ICEAE=
    Generation:             1560872610728864
    Metageneration:         1
gs://fc-secure-3aa171b5-8208-4467-8743-c7879f3da6da/H_XS-345839-0186762084.cram:
    Creation time:          Tue, 18 Jun 2019 15:43:31 GMT
    Update time:            Tue, 18 Jun 2019 15:43:31 GMT
    Storage class:          STANDARD
    Content-Language:       en
    Content-Length:         17179033227
    Content-Type:           application/octet-stream
    Metadata:
        goog-reserved-file-mtime:1499099273
    Hash (crc32c):          nrTiSg==
    ETag:                   CJmzrsyv8+ICEAE=
    Generation:             1560872611453337
    Metageneration:         1
""")

        rdr = rdr_factory(fn)
        self.assertTrue(bool(rdr))

        got = []
        for path_d in rdr:
            got.append(path_d)
        expected = [{"value": "gs://fc-secure-3aa171b5-8208-4467-8743-c7879f3da6da/H_XS-356091-0186761975.cram", "exists": "1", "checksum": "gLU4quAMng1xZm7B8u+VbQ=="}, {"value": "gs://fc-secure-3aa171b5-8208-4467-8743-c7879f3da6da/H_XS-345839-0186762084.cram", "exists": "1", "checksum": "nrTiSg=="}]
        self.assertListEqual(got, expected)

# -- EntityPathFactory

if __name__ == '__main__':
    unittest.main(verbosity=2)
