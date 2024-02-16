import pandas as pd
import numpy as np
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
        elif "," in distbin_type:
            lengths = sorted(list(map(int, distbin_type.split(","))))
            if lengths[0] != 1:
                lengths.insert(0, 1)
            return lengths
        elif ":" in distbin_type:
            limit, interval = distbin_type.split(":")
            lengths = np.arange(1, int(limit) + int(interval) + 1, int(interval))
            return list(lengths)
        else:
            raise Exception(f"Unknown binning type: {distbin_type}")
    #-- lengths_for

    def __init__(self, distbin_type):
        self.lengths = []
        self.distbins = SeqLenDist.lengths_for(distbin_type)
    #-- __init__

    def load(self, seqfile, label):
        with SeqFile(seqfile) as sf:
            for entry in sf:
                x = len(entry.seq)
                for i, l in enumerate(reversed(self.distbins)):
                    if x >= l:
                        break
                j = len(self.distbins) - i - 1
                self.lengths.append([label, x, j])
    #-- load

    def complete(self):
        lengths_df = pd.DataFrame(data=self.lengths, columns=["label", "length", "bin"])
        self.lengths = []

        summary_df = lengths_df.groupby(['label']).agg(min=('length', 'min'), max=('length', 'max'), mean=('length', 'mean'), median=('length', 'median'), length=('length', 'sum'), count=('length', 'count'))
        summary_df["n50"] = 0

        bins_df = lengths_df.groupby(['label', 'bin']).agg(min=('length', 'min'), max=('length', 'max'), mean=('length', 'mean'), median=('length', 'median'), length=('length', 'sum'), count=('length', 'count'))

        for label in summary_df.index:
            label_length = bins_df.xs(label, ).length.sum()
            half_length = int(label_length / 2)
            current_length = 0
            # add rows for bins without lengths 
            for i, b in enumerate(self.distbins):
                if (label, i) not in bins_df.index:
                    bins_df.loc[(label, i),:] = [0, 0, 0, 0, 0, 0]
            # re-sort index
            bins_df = bins_df.sort_index()
            # get bin where n50 length is
            for i, b in enumerate(self.distbins):
                bin_length = bins_df.loc[(label, i)].length
                if current_length +bin_length > half_length:
                    break
                current_length += bin_length
            # get n50 length for label
            for l in sorted(lengths_df.loc[(lengths_df['label'] == label) & (lengths_df['bin'] == i)].length.values):
                current_length += l
                if current_length > half_length:
                    break
            # add n50 to summary table
            summary_df.at[label, "n50"] = l
        self.lengths_df = lengths_df
        self.summary_df = summary_df
        self.df = summary_df
        self.bins_df = bins_df
    #-- complete
#-- SeqLenDist
