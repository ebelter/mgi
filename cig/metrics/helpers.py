import gzip, os, re, sys
from Bio import SeqIO

def str_to_number_if_number(s):
    if not s.replace(".", "").isnumeric():
        print(f"NOT NUMERIC: {s}")
        return s
    return str_to_number(s)
#-- str_to_number

def str_to_number(s):
    if "." in s:
        return round(float(s), (2))
    else:
        return int(s)
#-- str_to_number

zeros_p = re.compile(r"^0+$")
def number_to_str(n):
    n = str(n)
    tokens = n.split(".")
    if len(tokens) > 1 and re.match(zeros_p, tokens[1]):
        return tokens[0]
    return n
#-- str_to_number

def resolve_labels(labels, files, out):
    if labels is None:
        if out is not None:
            label = os.path.basename(out)
            return [out for i in range(0, len(files))]
        else:
            return list(map(lambda sf: os.path.basename(sf).split(".")[0], files))

    labels = labels.split(",")
    if len(labels) != len(files):
        raise Exception(f"ERROR Unequal number of labels {len(labels)} => {labels}) given for files: {len(files)}")
        #return [labels[0] for i in range(0, len(files))]
    return labels
#-- resolve_labels

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
