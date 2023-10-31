import pandas
from cig.metrics.helpers import SeqFile

# Need count, count pct, bps, bps pct
class SeqLenDist():
    @staticmethod
    def lengths_for(distbin_type):
        if distbin_type == "asm":
            #asm_lengths = [1, 2001, 5001, 10001, 100001, 250001, 1000000]
            return [1, 2001, 5001, 10001, 100001, 250001, 1000000]
        elif distbin_type == "lr":
            #longread_lengths = [1, 201, 501, 1001, 2001, 5001, 10001, 20001]
            return [1, 201, 501, 1001, 2001, 5001, 10001, 20001]
        else:
            #two50_lengths = np.arange(1, 20001, 250)
            raise Exception(f"Unknown binning type: {distbin_type}")
    #-- lengths_for

    def __init__(self, distbin_type):
        self.lengths = []
        self.distbins = SeqLenDist.lengths_for(distbin_type)
    #-- __init__

    def load(self, seqfile):
        with SeqFile(seqfile) as sf:
            for entry in sf:
                x = len(entry.seq)
                for i, l in enumerate(reversed(self.distbins)):
                    if x >= l:
                        break
                j = len(self.distbins) - i - 1
                self.lengths.append([sf.label, x, j])
    #-- load

    def complete(self):
        lengths_df = pandas.DataFrame(data=self.lengths, columns=["label", "length", "bin"])
        self.lengths = []

        summary_df = lengths_df.groupby(['label']).agg(min=('length', 'min'), max=('length', 'max'), mean=('length', 'mean'), length=('length', 'sum'), count=('length', 'count'))
        summary_df["n50"] = 0

        bins_df = lengths_df.groupby(['label', 'bin']).agg(min=('length', 'min'), max=('length', 'max'), mean=('length', 'mean'), length=('length', 'sum'), count=('length', 'count'))

        for label in summary_df.index:
            label_length = bins_df.xs(label, ).length.sum()
            half_length = int(label_length / 2)
            current_length = 0

            #bins_df["pct_"] = bins_df["count"] / bins_df["length"] * 100
            for i, b in enumerate(self.distbins):
                if (label, i) not in bins_df.index:
                    continue
                bin_length = bins_df.loc[(label, i)].length
                if current_length +bin_length > half_length:
                    break
                current_length += bin_length
            for l in sorted(lengths_df.loc[(lengths_df['label'] == label) & (lengths_df['bin'] == i)].length.values):
                current_length += l
                if current_length > half_length:
                    break
            summary_df.at[label, "n50"] = l
        self.lengths_df = lengths_df
        self.summary_df = summary_df
        self.bins_df = bins_df
    #-- complete
#-- SeqLenDist
