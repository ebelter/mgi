import csv, tabulate
from jinja2 import BaseLoader, Environment
from cig.metrics.helpers import number_to_str

def available_report_types():
    return ("summary",)
#-- available_report_types

def available_report_formats():
    return ("csv", "table", "mw",)
#-- available_report_formats

def write_summary_report_csv(output_h, am):
    fieldnames, rows = _resolve_data_for_summary_report(am.dfs["normalized"])
    #fieldnames_lower = map(str.lower, fieldnames)
    wtr = csv.writer(output_h, delimiter=",", lineterminator="\n")
    wtr.writerow(fieldnames)
    wtr.writerows(rows)
#--

def write_summary_report_mw(output_h, am):
    fieldnames, rows = _resolve_data_for_summary_report(am.dfs["normalized"])
    _write_summary_report_tabulate(output_h, fieldnames, rows, "mediawiki")
#--

def write_summary_report_table(output_h, am):
    fieldnames, rows = _resolve_data_for_summary_report(am.dfs["normalized"])
    _write_summary_report_tabulate(output_h, fieldnames, rows, "simple")
#--

def _write_summary_report_tabulate(output_h, fieldnames, rows, tablefmt):
    output_h.write(tabulate.tabulate(rows, fieldnames, tablefmt=tablefmt))
#--

def _resolve_data_for_summary_report(df):
    index_names = df.index.names
    fieldnames = map(str.upper, index_names + list(df.columns.values))
    #fieldnames = map(lambda v: v.upper(), ["label", "kind"] + list(df.columns.values))
    rows = []
    for label, row in df.iterrows():
        rows.append(map(number_to_str, list(label)+list(row.values)))
    return fieldnames, rows
#--
