import csv, json, tabulate, yaml
from jinja2 import BaseLoader, Environment
from cig.metrics.helpers import number_to_str

def available_reports():
    return ("csv", "json", "table", "mw", "yaml")
#-- available_reports

def write_csv_report(output_h, m):
    fieldnames, rows = _resolve_data_for_report(m.df)
    wtr = csv.writer(output_h, delimiter=",", lineterminator="\n")
    wtr.writerow(["metric"]+list(fieldnames))
    wtr.writerows(rows)
#-- write_report_csv

def write_json_report(output_h, m):
    output_h.write(json.dumps(_resolve_data_for_serialization(m.df), indent=2))
#-- write_json_report

def write_mw_report(output_h, m):
    fieldnames, rows = _resolve_data_for_report(m.df)
    _write_tabulate_report(output_h, fieldnames, rows, "mediawiki")
#--

def write_table_report(output_h, m):
    fieldnames, rows = _resolve_data_for_report(m.df)
    _write_tabulate_report(output_h, fieldnames, rows, "simple")
#--

def _write_tabulate_report(output_h, fieldnames, rows, tablefmt):
    output_h.write(tabulate.tabulate(rows, fieldnames, tablefmt=tablefmt))
#--

def write_yaml_report(output_h, m):
    output_h.write(yaml.dump(json.loads(json.dumps(_resolve_data_for_serialization(m.df))),))
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

def _resolve_data_for_serialization(df):
    data = []
    for label, row in df.iterrows():
        row_d = dict(row)
        row_d["label"] = label
        data.append(row_d)
    return data
#--
