import csv, tabulate
from jinja2 import BaseLoader, Environment
from cig.metrics.helpers import number_to_str

def available_reports():
    return ("csv", "table", "mw",)
#-- available_report_formats

def write_report_csv(output_h, rnaseqm):
    fieldnames, rows = _resolve_data_for_report(rnaseqm.df)
    wtr = csv.writer(output_h, delimiter=",", lineterminator="\n")
    wtr.writerow(["metric"]+list(fieldnames))
    wtr.writerows(rows)
#--

def write_report_mw(output_h, rnaseqm):
    fieldnames, rows = _resolve_data_for_report(rnaseqm.df)
    _write_report_tabulate(output_h, fieldnames, rows, "mediawiki")
#--

def write_report_table(output_h, rnaseqm):
    fieldnames, rows = _resolve_data_for_report(rnaseqm.df)
    _write_report_tabulate(output_h, fieldnames, rows, "simple")
#--

def _write_report_tabulate(output_h, fieldnames, rows, tablefmt):
    output_h.write(tabulate.tabulate(rows, fieldnames, tablefmt=tablefmt))
#--

def X_resolve_data_for_report(df):
    fieldnames = map(str.upper, list(df.columns.values))
    rows = []
    for label, row in df.iterrows():
        rows.append([label] + list(map(number_to_str, row.values)))
    return fieldnames, rows
#--

def _resolve_data_for_report(df):
    fieldnames = df.index.values
    #fieldnames = list(df.index.values)
    rows = [[l] for l in df.columns.values]
    for label, row in df.iterrows():
        for i, v in enumerate(row):
            rows[i].append(number_to_str(v))
    return fieldnames, rows
#--
