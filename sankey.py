"""Sankey Diagram"""
import pandas as pd

df_stations = pd.read_csv("data/df_stations.csv")

def gen_sankey(df=df_stations):
    """function to generate a sankey-graph for the start- and endstations"""

    all_nodes = df["Start station"].values.tolist() + df["End station"].values.tolist()
    all_nodes = list(dict.fromkeys(all_nodes))
    source_indices = [all_nodes.index(startstat) for startstat in df["Start station"]]
    target_indices = [all_nodes.index(endstat) for endstat in df["End station"]]

    # creating the sankey diagram output-figure
    data = dict(
        type='sankey',
        node=dict(pad=15,
                  thickness=20,
                  line=dict(width=0.5),
                  label=all_nodes,
                  color="#535E7A"),
        link=dict(source=source_indices,
                  target=target_indices,
                  value=df["Duration"].values,
                  label=df["Duration"].values))
    layout = dict(
        title="Most important routes",
        titlefont=dict(color="#ff7f0e", size='22'),
        height=600,
        margin=dict(l=0, r=50, t=70, b=0),
        font=dict(size=16))

    fig_dict = dict(data=[data], layout=layout)

    return fig_dict
