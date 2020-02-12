import numpy as np
from disney_memory_prediction.load_save_data import load_and_generate_data
from disney_memory_prediction.check_stationary_and_make_stationary import stationarySeries
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle

class arima_model():
    def __init__(self):
        load_data = load_and_generate_data()
        stationary_series = stationarySeries()
        self.original_data, self.imputed_data = load_data.getData()
        # stationary_data_original = stationarySeries.getStationaryData(original_data)
        self.stationary_data_imputed = stationary_series.getStationaryData()

    def return_results(self, device, node, pred, target, forcast, lower, upper, history_date, history, error, total):
        pred[str(device)][node]['expected'].append(target)
        pred[str(device)][node]['forecast'].append(forcast)
        pred[str(device)][node]['lower'].append(lower)
        pred[str(device)][node]['upper'].append(upper)
        pred[str(device)][node]['history_date'].append(history_date)
        pred[str(device)][node]['history'].append(history)
        pred[str(device)][node]['error'].append(str(error))
        pred[str(device)][node]['total'].append(total)
        return pred

    def model(self, stationary_data, data):
        pred = {}
        for device in stationary_data:
            pred[str(device)] = {}
            for node in stationary_data[device]:
                app_data_train = list(stationary_data[device][node]['train'].memory)
                app_data_test = list(stationary_data[device][node]['test'].memory)
                date_data_train = list(stationary_data[device][node]['train'].date)
                date_data_test = list(stationary_data[device][node]['test'].date)
                total_data_test = list(stationary_data[device][node]['test'].total)
                pred[str(device)][node] = {}
                pred[str(device)][node]['expected'] = []
                pred[str(device)][node]['lower'] = []
                pred[str(device)][node]['upper'] = []
                pred[str(device)][node]['error'] = []
                pred[str(device)][node]['history'] = [x for x in app_data_train]
                pred[str(device)][node]['history_date'] = [str(x) for x in date_data_train]
                pred[str(device)][node]['forecast'] = [x for x in app_data_train]
                pred[str(device)][node]['total'] = [x for x in list(stationary_data[device][node]['train'].total)]
                predictions = list()
                if len(app_data_train) > 2:
                    for t in range(len(app_data_test)):
                        target = app_data_test[t]
                        if np.mean(app_data_train) == app_data_train[0]:
                            pred = self.return_results(device, node, pred, target, target,
                                                  app_data_train[0] - 500, app_data_train[0] + 500,
                                                  date_data_test[t], target, 0, total_data_test[0])
                        else:
                            model = ARIMA(pred[str(device)][node]['history'], order=(1, 0, 0))
                            model_fit = model.fit(trend='nc', disp=False)
                            forecast, stderr, conf = model_fit.forecast()
                            pred = self.return_results(device, node, pred, target, forecast, conf[0][0], conf[0][1],
                                                  date_data_test[t], target, stderr, total_data_test[0])
                            predictions.append(forecast)
                    if len(predictions) > 0:
                        pred[str(device)][node]['test_data_date'] = date_data_test
                elif len(app_data_train) != 0:

                    for t in range(len(app_data_test)):
                        target = app_data_test[t]
                        pred = self.return_results(device, node, pred, app_data_test[t], target,
                                              app_data_train[0] - 500, app_data_train[0] + 500, date_data_test[t],
                                              target, str(sqrt(mean_squared_error(target, target))), total_data_test[0])
        return pred

    def getPredictions(self):
        predictions = self.model(self.stationary_data_imputed, self.imputed_data)
        with open(os.path.join(settings.BASE_DIR, 'predictions/predictions.pickle'), 'wb') as fp:
            pickle.dump(predictions, fp, protocol=pickle.HIGHEST_PROTOCOL)
        return predictions

