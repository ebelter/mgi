import csv, json, yaml
import pandas as pd
from jinja2 import BaseLoader, Environment
import seaborn as sns

def available_reports():
    return ("csv", "json", "plot_bins_number", "plot_bins_length", "plot_dist", "text", "yaml")
#-- avalible_reports

def write_text_report(output_h, seqlendist):
    template_str = """SAMPLE    {{metrics.label}}
COUNT     {{metrics.count}}
BASES     {{metrics.length}} bp
MEAN      {{metrics.mean}} bp
MEDIAN    {{metrics.median}} bp
N50       {{metrics.n50}} bp
LARGEST   {{metrics.max}} bp
        LOWER -- UPPER         COUNT          BASES      PCT
{% for b in distbins %}BIN  {{'%8s -- %-8s %10i ( %12i bp ) %.2f%%'|format(b.lower, b.upper, b.length, b.length, b.length_pct)}}
{% endfor %}
"""
    template = Environment(loader=BaseLoader()).from_string(template_str)
    for label, row in seqlendist.summary_df.iterrows():
        metrics = {"label": label}
        for k, v in row.to_dict().items():
            metrics[k] = int(v)
        distbins = []
        for i, b in enumerate(seqlendist.distbins):
            distbin = { "lower": seqlendist.distbins[i], "upper": i }
            if i + 1 > len(seqlendist.distbins) - 1:
                upper = "+"
            else:
                upper = seqlendist.distbins[i+1] - 1
            distbin["upper"] = upper
            distbin["num"] = seqlendist.bins_df.loc[(label, i)]["count"]
            bin_length = seqlendist.bins_df.loc[(label, i)]["length"]
            distbin["length"] = bin_length
            distbin["length_pct"] = bin_length / metrics["length"] * 100
            distbins.append(distbin)
        output_h.write(template.render(metrics=metrics, distbins=distbins))
#-- write_text_report

def write_csv_report(output_h, seqlendist):
    fieldnames = ("label", "count", "length", "min", "max", "mean", "median", "n50")
    wtr = csv.DictWriter(output_h, fieldnames=fieldnames, delimiter=",", lineterminator="\n")
    wtr.writeheader()
    for label, row in seqlendist.summary_df.iterrows():
        row_metrics = {"label": label}
        for k, v in row.to_dict().items():
            row_metrics[k] = int(v)
        wtr.writerow(row_metrics)
#-- write_csv_report

def write_json_report(output_h, seqlendist):
    metrics = []
    for label, row in seqlendist.summary_df.iterrows():
        row_metrics = {"label": label}
        for k, v in row.to_dict().items():
            row_metrics[k] = int(v)
        metrics.append(row_metrics)
    if len(metrics) == 1:
        output_h.write(json.dumps(metrics[0]))
    else:
        output_h.write(json.dumps(metrics))
#-- write_json_report

def write_yaml_report(output_h, seqlendist):
    metrics = []
    for label, row in seqlendist.summary_df.iterrows():
        row_metrics = {"label": label}
        for k, v in row.to_dict().items():
            row_metrics[k] = int(v)
        metrics.append(row_metrics)
    if len(metrics) == 1:
        output_h.write(yaml.dump(metrics[0]))
    else:
        output_h.write(yaml.dump(metrics))
#-- write_yaml_report

def write_plot_bins_length_report(out_h, seqlendist):
    print(f"\n{seqlendist.bins_df}")
    #axes = sns.barplot(x="Bin", y="Length", data=pd.DataFrame(data={"Bin": map(str, seqlendist.distbins), "Length": seqlendist.bins_df["length"].values}), err_kws={'linewidth': 0})
    axes = sns.barplot(x="bin", y="length", data=seqlendist.bins_df, err_kws={'linewidth': 0})
    axes.set_yticklabels(['{:,.0f}'.format(y) + 'K' for y in axes.get_yticks()/1000])
    #for i in ax.containers: # add labels to bars
    #    ax.bar_label(i,)
    axes.get_figure().savefig(out_h)
#-- write_plot_bins_report

def write_plot_bins_number_report(out_h, seqlendist):
    axes = sns.barplot(x="Bin", y="Number", data=pd.DataFrame(data={"Bin": map(str, seqlendist.distbins), "Number": seqlendist.bins_df["count"].values}), err_kws={'linewidth': 0})
    #for i in ax.containers: # add labels to bars
    #    ax.bar_label(i,)
    axes.get_figure().savefig(out_h)
#-- write_plot_bins_report

def write_plot_dist_report(out_h, seqlendist):
    grid = sns.FacetGrid(seqlendist.lengths_df, col="label", sharey="row", margin_titles=True)
    grid.map(sns.histplot, "length")
    grid.set_titles(col_template="{col_name}")
    grid.set(xlabel="Length", ylabel="Count")
    m_sum = int((seqlendist.summary_df['n50'].median() + seqlendist.summary_df['median'].mean())/2)
    grid.set(xlim=(0, m_sum * 4))
    grid.savefig(out_h)
#-- write_plot_dist_report
