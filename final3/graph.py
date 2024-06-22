import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pf
from dist import db_reader
import json

database = db_reader.DB_READER()

def _get_dataset(company):
    data = database.dictionizationoData(company)  

    # return database.dictionizationoData(company)
    # data = {'date': ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05'],
    #         'tax amount': [1200, 150, 300, 450, 200]
    #         }
    return pd.DataFrame(data)


# def taxes(indexed=False, datetimes=False):
#     df = _get_dataset()
#     if datetimes:
#         df["date"] = df["date"].astype("datetime64[ns]")
#     if indexed:
#         df = df.set_index("date")
#         df.columns.name = "tax amount"
#     return df

def ret_graph(company):
    dfz = _get_dataset(company=company)
    fig = px.scatter(dfz, x="Months", y="ActualTax", trendline="ols")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

