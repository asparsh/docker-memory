
#Importing libraries
from disney_memory_prediction.load_save_data import load_and_generate_data
from fbprophet import Prophet
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

class prophet():
    def __init__(self):
        load_data = load_and_generate_data()
        self.original_data, self.imputed_data = load_data.getData()
        # self.stationary_data_original = self.check_and_make_stationary(self.original_data)

    def Pmodel(self):
        model = Prophet(growth='linear',
                        changepoints=None,
                        n_changepoints=25,
                        changepoint_range=0.8,
                        yearly_seasonality=False,
                        weekly_seasonality=True,
                        daily_seasonality=False,
                        holidays=None,
                        seasonality_mode='multiplicative',
                        seasonality_prior_scale=0.1,
                        holidays_prior_scale=0.1,
                        changepoint_prior_scale=0.05,
                        mcmc_samples=0,
                        interval_width=0.95,
                        uncertainty_samples=10)
        return model

    def train_test_prophet(self):
        ''' 
        1. Training the model on the Train set, and predicting on both the Train and Test sets
        2. Setting growth = 'linear'. To use Logistic growth (appropriate parameter for this problem), 
            it requires domain inputs such as cap and floor of the Application Available, 
            which should provide better results for this problem
        3. Will be returning the forecasts on train & test, model, and Dates of future weeks for Predicton
        4. dev_node is the whole dataframe for a specific device_node pair and it has 2 columns ['ds','y'], where ds=dates, y= application_available
        '''
        pred_prophet = {}
        for device in self.original_data:
            pred_prophet[device] = {}
            for node in self.original_data[device]:
                app_data_train = list(self.original_data[device][node]['train'].memory)
                app_data_test = list(self.original_data[device][node]['test'].memory)
                date_data_train = list(self.original_data[device][node]['train'].date)
                date_data_test = list(self.original_data[device][node]['test'].date)
                total_data_test = list(self.original_data[device][node]['test'].total)
                pred_prophet[device][node] = {}
                pred_prophet[device][node]['expected'] = []
                pred_prophet[device][node]['lower'] = []
                pred_prophet[device][node]['upper'] = []
                pred_prophet[device][node]['error'] = []
                pred_prophet[device][node]['history'] = [x for x in app_data_train]
                pred_prophet[device][node]['history_date'] = [x for x in date_data_train]
                pred_prophet[device][node]['forecast'] = [x for x in app_data_train]
                pred_prophet[device][node]['total'] = [x for x in list(self.original_data[device][node]['train'].total)]
                pred_prophet = pd.DataFrame({'ds': date_data_train, 'y': app_data_train})
                prediction = ()
                train = pd.DataFrame({'ds': date_data_train, 'y': app_data_train})
                test = pd.DataFrame({'ds': date_data_test, 'y': app_data_test})
                if len(app_data_train) > 2:
                    model = Prophet(growth='linear',
                        changepoints=None,
                        n_changepoints=25,
                        changepoint_range=0.8,
                        yearly_seasonality=False,
                        weekly_seasonality=True,
                        daily_seasonality=False,
                        holidays=None,
                        seasonality_mode='multiplicative',
                        seasonality_prior_scale=0.1,
                        holidays_prior_scale=0.1,
                        changepoint_prior_scale=0.05,
                        mcmc_samples=0,
                        interval_width=0.95,
                        uncertainty_samples=10)
                    trained_model = model.fit(train)

                    forecast = trained_model.predict(test)
                    print("forecasting", forecast)
                    future_weeks = model.make_future_dataframe(periods=100, freq='W', include_history=False)
                    future_weeks = future_weeks.loc[future_weeks.ds > test.ds.max()]
                    future_weeks = future_weeks.head(54).reset_index().drop(['index'], axis=1)


    def getStationaryData(self):
        return self.check_and_make_stationary(self.imputed_data)

p = prophet()
p.train_test_prophet()