import atexit, csv, os, yaml
from mgi.models import Entity, EntityFeature

def get_entity(name, kind):
    return Entity.query.filter(Entity.name == name, Entity.kind == kind).one_or_none()

def add_entity(name, kind):
    return Entity(name=name, kind=kind)
#-- add_entity

def resolve_entity_and_kind_from_value(value):

    known_exts = set(["bam", "cram", "crai", "fai", "fasta", "fastq", "g", "md5", "tbi", "vcf"])
    skip_exts = set(["*", "gz", "tgz", "tar", "tgz", "txt"])
    bn = os.path.basename(value)
    fn_tokens = bn.split(".")
    entity_tokens, ext_tokens = [], []
    for t in fn_tokens:
        if t in skip_exts:
            continue
        if t not in known_exts:
            entity_tokens.append(t)
        else:
            ext_tokens.append(t)

    entity_name = fn_tokens[0]
    kind =  " ".join(ext_tokens)
    entity_alt_name = ".".join(entity_tokens)
    return entity_name, kind, entity_alt_name
#-- resolve_entity_and_kind_from_fn

class GcpStatReader():
    def __init__(self, fn):
        with open(fn, "r") as f:
            self.gcp_d = yaml.safe_load(f)
        self.gcp_i = iter(self.gcp_d)

    def __iter__(self):
        return self

    def __next__(self):
        value = next(self.gcp_i)
        checksum = self.gcp_d[value].get("Hash (md5)", None)
        if checksum is None:
            checksum = self.gcp_d[value].get("Hash (crc32c)", None)
        return {
                "value": value,
                "exists": "1",
                "checksum": checksum,
                }
#-- GcpStatReader

def paths_rdr_factory(fn):
    if not os.path.exists(fn):
        return [{"entity": fn}]

    if fn.endswith(".gcpstat"):
        return GcpStatReader(fn)

    f = open(fn, "r")
    atexit.register(lambda: f.close())
    first_ln = f.readline()
    f.seek(0)
    fieldnames = first_ln.rstrip().split("\t")
    if "value" in fieldnames:
        rdr = csv.DictReader(f, delimiter="\t")
    else: # No header, assume it is all just files
        rdr = csv.DictReader(f, fieldnames=["value"], delimiter="\t")
    return rdr
#-- rdr_factory
