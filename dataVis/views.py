from django.shortcuts import render
from dataVis.models import ENERGY
from .forms import TypeForm, ChartForm
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


obs = ENERGY.objects.all()
obsValues = obs.values("energyYear", "energyType", "energyUsed")
df = pd.DataFrame.from_records(obsValues)


# Create your views here.
def index(request):
    """The home page for dataVis"""

    return render(request, "dataVis/index.html")


def single(request):
    """The home page for dataVis"""

    LINECOLOR = "#86A789"
    BGCOLOR = "#EBF3E8"

    energyType = request.GET.get("energy_Type")
    if not energyType:
        energyType = "Oil"

    typeform = TypeForm(initial={"energy_Type": energyType})
    typeform.fields["energy_Type"].choices.sort()

    dSelect = df[df["energyType"] == energyType].sort_values(by="energyYear")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list(dSelect.energyYear), y=list(dSelect.energyUsed)))

    fig.update_layout(
        title={
            "text": f"{energyType} Energy Use in Manufacturing in Finland, 2011-2021",
            "font_size": 20,
            "font_color": "#555",
            "xanchor": "center",
            "x": 0.5,
        },
        xaxis=dict(tickmode="linear"),
        yaxis=dict(title="Energy Used (Unit: TJ))"),
        plot_bgcolor=BGCOLOR,
        xaxis_tickangle=-45,
    )

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="linear",
        )
    )

    fig.update_traces(
        line_color=LINECOLOR,
        # line_width=2,
    )

    graph = fig.to_html()

    context = {"graph": graph, "typeform": typeform}
    return render(request, "dataVis/single.html", context)


def total(request):
    """The total page for dataVis"""

    chartType = request.GET.get("chart_Type")
    if not chartType:
        chartType = "Scatter"

    chartForm = ChartForm(initial={"chart_Type": chartType})

    dTotal = df.sort_values(by="energyYear")

    if chartType == "2":
        fig = px.scatter(
            dTotal,
            x="energyYear",
            y="energyUsed",
            color="energyType",
            title="Total Energy Use in Manufacturing in Finland, 2011-2021",
            labels={
                "energyYear": "",
                "energyUsed": "Energy Used (unit: TJ)",
                "energyType": "Energy Type",
            },
        )

    elif chartType == "3":
        fig = px.line(
            dTotal,
            x="energyYear",
            y="energyUsed",
            color="energyType",
            title="Total Energy Use in Manufacturing in Finland, 2011-2021",
            labels={
                "energyYear": "",
                "energyUsed": "Energy Used (unit: TJ)",
                "energyType": "Energy Type",
            },
        )

    else:
        fig = px.bar(
            dTotal,
            x="energyYear",
            y="energyUsed",
            color="energyType",
            title="Total Energy Use in Manufacturing in Finland, 2011-2021",
            labels={
                "energyYear": "",
                "energyUsed": "Energy Used (unit: TJ)",
                "energyType": "Energy Type",
            },
            # color_discrete_sequence=TRACESCOLOR,
        )
        fig.update_layout(
            # plot_bgcolor=BGCOLOR,
        )

    fig.update_layout(
        # title={"font_size": 22, "font_color": "#555", "xanchor": "center", "x": 0.5},
        title={"xanchor": "center", "x": 0.5},
        xaxis=dict(tickmode="linear"),
        # yaxis=dict(showline=True, gridcolor="#bbb", gridwidth=1),
        # height=1000,
    )

    graph = fig.to_html()

    context = {"graph": graph, "chartForm": chartForm}
    return render(request, "dataVis/total.html", context)
