from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10
import plotly.graph_objs as go#visualization
from plotly.offline import plot
import os
from disney_dashboard import settings

class plot_results():
    def __init__(self, pred, device, node):
        self.pred = pred
        self.device = device
        self.node = node

    def plot_train_test_pred(self):
        trace1 = {
          "fill": None,
          "mode": "markers",
          "name": "Actual Application Available",
          "type": "scatter",
          "x": self.pred[self.device][self.node]['history_date'],
          "y":self.pred[self.device][self.node]['history'],
        }
        trace2 = {
          "fill": "tonexty",
          #"line": {"color": "#57b8ff"},
          "mode": "lines",
          "name": "upper_band",
          "type": "scatter",
          "x": self.pred[self.device][self.node]['test_data_date'],
          "y":self.pred[self.device][self.node]['upper']

          }
        trace3 = {
          "fill": "tonexty",
         # "line": {"color": "#57b8ff"},
          "mode": "lines",
          "name": "lower_band",
          "type": "scatter",
          "x": self.pred[self.device][self.node]['test_data_date'],
          "y":self.pred[self.device][self.node]['lower'],
         }
        trace4 = {
         # "line": {"color": "##ff6d22"},
          "mode": "lines",
          "name": "model line of best fit",
          "type": "scatter",
          "x": self.pred[self.device][self.node]['history_date'],
          "y": self.pred[self.device][self.node]['forecast']

        }


        data = go.Data([trace1,trace2, trace3,trace4])
        layout = {
          "title": "Memory Prediction for Device:" + str(self.device) +" and Node " + str(self.node),
          "xaxis": {
            "title": "Weekly Dates",
            "ticklen": 5,
            "gridcolor": "rgb(255, 255, 255)",
            "gridwidth": 2,
            "zerolinewidth": 1
          },
          "yaxis": {
            "title": "Application Available",
            "ticklen": 5,
            "gridcolor": "rgb(255, 255, 255)",
            "gridwidth": 2,
            "zerolinewidth": 1
          },

          "plot_bgcolor": "rgb(243, 243, 243)",
          "paper_bgcolor": "rgb(243, 243, 243)"
        }


        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=os.path.join(settings.BASE_DIR, 'templates/fig.html'), auto_open=False)
