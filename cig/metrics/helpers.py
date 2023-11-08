import gzip, os, sys
from Bio import SeqIO

class SeqFile():
    def __init__(self, seqfile):
        self.fn = seqfile
        bn = os.path.basename(self.fn)
        bn_tokens = bn.split(".")
        types = set(["fastq", "fasta"]) & set(bn_tokens)
        if len(types) != 1:
            raise Exception(f"Failed to deteremine sequence file type for {seqfile}")
        self.type = types.pop()
        if "gz" in bn_tokens:
            self.is_gzipped = True
        else:
            self.is_gzipped = False
    #-- __init__

    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        if self.is_gzipped:
            self.fh = gzip.open(self.fn, mode="rt")
        else:
            self.fh = open(self.fn, mode="r")
        return self
    #-- __enter__

    def __exit__(self, exception_type, exception_value, exception_traceback):
        # TODO Exception handling here
        self.fh.close()
    #-- __exit__

    def __iter__(self):
        self.seqio = SeqIO.parse(self.fh, self.type)
        return self

    def __next__(self):
        return next(self.seqio)
#-- SeqFile

class OutHandle():
    def __init__(self, bn="-", ext="txt"):
        self.bn = bn
        self.ext = ext
        self.mode = "w"
        if ext == "png":
            self.mode = "wb"
        if bn == "-":
            self.fn = "STDOUT"
        else:
            self.fn = ".".join([bn, ext])
    #-- __init__

    def __enter__(self):
        if self.fn != "STDOUT":
            self.fh = open(self.fn, self.mode)
        else:
            self.fh = sys.stdout
        return self
    #-- __enter__

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.fn != "STDOUT":
            self.fh.close()
    #-- __exit__
#--
