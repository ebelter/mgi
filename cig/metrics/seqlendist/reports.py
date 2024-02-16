import csv, json, yaml
import pandas as pd
from jinja2 import BaseLoader, Environment
import seaborn as sns

def available_reports():
    return ("plot_bins_number", "plot_bins_length", "plot_dist", "plot_dist2", "text")
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
{% for b in distbins %}BIN  {{'%8s -- %-8s %10i ( %12i bp ) %.2f%%'|format(b.lower, b.upper, b.num, b.length, b.length_pct)}}
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

def write_plot_bins_length_report(out_h, seqlendist):
    #print(f"\n{seqlendist.bins_df}")
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
    grid = sns.FacetGrid(seqlendist.lengths_df, col="label", margin_titles=True, col_wrap=2)
    grid.map(sns.histplot, "length", element="poly", shrink=0)
    grid.set_titles(col_template="{col_name}")
    grid.set(xlabel="Length", ylabel="Count")
    m_sum = int((seqlendist.summary_df['n50'].median() + seqlendist.summary_df['median'].mean())/2)
    grid.set(xlim=(0, m_sum * 4))
    grid.savefig(out_h)
#-- write_plot_dist_report


def write_plot_dist2_report(out_h, seqlendist):
    from plotnine import ggplot, ggsave, aes, geom_histogram, scale_y_continuous, scale_x_continuous, theme_bw, facet_grid, coord_cartesian
    means_sum = int((seqlendist.summary_df['n50'].mean() + seqlendist.summary_df['mean'].mean())/2)
    xlim = means_sum * 10
    plot = (
            ggplot(seqlendist.lengths_df)
            + aes(x="length", xmin=0)
            + geom_histogram(binwidth=25,boundary=0,closed="left",color="black")
            + facet_grid("label ~ .")
            + scale_x_continuous(name="Length")
            + scale_y_continuous(name="Count")
            + coord_cartesian(xlim=(1, xlim))
            + theme_bw()
            )
    ggsave(plot, out_h)
#-- write_plot_dist2_report
