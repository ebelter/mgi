import csv, json, yaml
from jinja2 import BaseLoader, Environment

def available_reports():
    return ("csv", "json", "png", "text", "yaml")
#-- avalible_reports

def write_text_report(output_h, seqlendist):
    template_str = """SAMPLE    {{metrics.label}}
COUNT     {{metrics.count}}
BASES     {{metrics.length}} bp
AVG       {{metrics.mean}} bp
N50       {{metrics.n50}} bp
LARGEST   {{metrics.max}} bp
{% for b in distbins %}SEQS {{'%8s -- %-8s ( %12i bp ) %.2f%%'|format(b.lower, b.upper, b.length, b.length_pct)}}
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
            if (label, i) not in seqlendist.bins_df.index:
                distbin["length"] = 0
                distbin["length_pct"] = 0.0
            else:
                bin_length = seqlendist.bins_df.loc[(label, i)].length
                distbin["length"] = bin_length
                distbin["length_pct"] = bin_length / metrics["length"] * 100
            distbins.append(distbin)
        output_h.write(template.render(metrics=metrics, distbins=distbins))
#-- write_text_report

def write_csv_report(output_h, seqlendist):
    fieldnames = ("label", "count", "length", "min", "max", "mean", "n50")
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

def write_png_report(out_h, seqlendist):
    from plotnine import ggplot, ggsave, aes, geom_line, geom_histogram, geom_density, geom_segment, scale_y_continuous, scale_x_continuous, theme_bw, facet_grid, coord_cartesian
    means_sum = int((seqlendist.summary_df['n50'].mean() + seqlendist.summary_df['mean'].mean())/2)
    xlim = means_sum * 10
    plot = (
            ggplot(seqlendist.lengths_df)
            + aes(x="length", xmin=0)
            + geom_histogram(binwidth=25,boundary=0,closed="left",color="black")
            + facet_grid("label ~ .")
            + scale_x_continuous(name="Length")
            + scale_y_continuous(name="Count")
            #+ xlim(1, seqlendist.distbins[-1])
            + coord_cartesian(xlim=(1, xlim))
            + theme_bw()
            )
    ggsave(plot, out_h)
#-- get_dist_plot
