import csv, json, tabulate, yaml
from jinja2 import BaseLoader, Environment
from cig.metrics.helpers import number_to_str, percentify

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
    _write_tabulate_report(output_h, m, "mediawiki")
#--

def write_table_report(output_h, m):
    _write_tabulate_report(output_h, m, "simple")
#--

def _write_tabulate_report(output_h, m, tablefmt):
    fieldnames, rows = _resolve_data_for_report(m.df, normalizers=[percentify])
    output_h.write(tabulate.tabulate(rows, fieldnames, tablefmt=tablefmt))
#--

def write_yaml_report(output_h, m):
    output_h.write(yaml.dump(json.loads(json.dumps(_resolve_data_for_serialization(m.df))),))
#--

def _resolve_data_for_report(df, normalizers=[]):
    fieldnames = df.index.values
    #fieldnames = list(df.index.values)
    rows = [[l] for l in df.columns.values]
    normalizers.append(number_to_str)
    for label, row in df.iterrows():
        i = 0
        for k, v in row.items():
            for normalizer in normalizers:
                v = normalizer(v, key=k)
            rows[i].append(v)
            i += 1
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
