import csv, tabulate
from cig.metrics.helpers import number_to_str
from cig.metrics.hic.metadata import get_metadata

def available_reports():
    return ("csv", "table", "mw",)
#-- available_report_formats

def write_report_csv(output_h, metrics):
    fieldnames, rows = _resolve_data_for_report(metrics.df)
    wtr = csv.writer(output_h, delimiter=",", lineterminator="\n")
    wtr.writerow(["metric"]+list(fieldnames))
    wtr.writerows(rows)
#--

def write_report_mw(output_h, metrics):
    fieldnames, rows = _resolve_data_for_report(metrics.df)
    _write_report_tabulate(output_h, fieldnames, rows, "mediawiki")
#--

def write_report_table(output_h, metrics):
    fieldnames, rows = _resolve_data_for_report(metrics.df)
    _write_report_tabulate(output_h, fieldnames, rows, "simple")
#--

def _write_report_tabulate(output_h, fieldnames, rows, tablefmt):
    output_h.write(tabulate.tabulate(rows, fieldnames, tablefmt=tablefmt, floatfmt=".0f"))
#--

def _resolve_data_for_report(df):
    fieldnames = df.index.values
    rows = [[l] for l in df.columns.values]
    for label, row in df.iterrows():
        for i, v in enumerate(row):
            rows[i].append(number_to_str(v))
    return fieldnames, rows
#--
