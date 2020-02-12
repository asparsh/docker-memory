#Importing libraries
import pandas as pd
print("pandas:", pd.__version__)
import numpy as np
from datetime import timedelta
import math
import os

class load_and_generate_data():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Reading in the csv file extracted on August 12th, 2019
        df = pd.read_csv('../data/disney_August_12.csv')
        # selecting the relevent columns
        df_selected = df[['application_available', 'collectTimeStamp', 'deviceId', 'node1', 'physical_total']]
        dff = df_selected.dropna()
        # Grouping the data based on productId2 and collectTimeStamp
        data_gb_productId = dff.groupby(['deviceId', 'node1', 'collectTimeStamp'])['application_available'].apply(
            lambda x: float(x))
        data_gb_total = dff.groupby(['deviceId', 'node1', 'collectTimeStamp'])['physical_total'].apply(
            lambda x: float(x))
        self.full_data = data_gb_productId.reset_index()
        self.total_data = data_gb_total.reset_index()
        self.min_date = pd.to_datetime(min(dff.collectTimeStamp))
        self.max_date = pd.to_datetime(max(dff.collectTimeStamp))
        self.form_timeSeries()
        self.train_data = self.final_data_parsing()

    # Function to create a list of list of lists:
    def form_timeSeries(self):
        self.df_app = {}
        self.df_date = {}
        self.df_total = {}
        first_device = self.full_data.deviceId[0]
        first_node = self.full_data.node1[0]

        for device, node, date, app, total in zip(self.full_data.deviceId, self.full_data.node1, self.full_data.collectTimeStamp,
                                           self.full_data.application_available, self.total_data.physical_total):
            if device == first_device:
                if device not in self.df_app:
                    self.df_app[device] = {}
                    self.df_date[device] = {}
                    self.df_total[device] = {}
                if node == first_node:
                    if node not in self.df_app[device]:
                        self.df_app[device][node] = []
                        self.df_date[device][node] = []
                        self.df_total[device][node] = []

                    self.df_app[device][node].append(app)
                    self.df_date[device][node].append(date)
                    self.df_total[device][node].append(total)
                else:
                    self.df_app[device][node] = [app]
                    self.df_date[device][node] = [date]
                    self.df_total[device][node] = [total]

            first_device = device
            first_node = node

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)


    def final_data_parsing(self):
        '''
        :param df_app:
        :param df_date:
        :return:
        '''
        final_dictionary = {}
        for device in self.df_app:
            final_dictionary[device] = {}
            for node in self.df_app[device]:
                # get the minimum value of application memory
                min_app_memory = min(self.df_app[device][node])
                # get the maximum value of application memory
                max_app_memory = max(self.df_app[device][node])
                final_dictionary[device][node] = {}
                DATES = [pd.to_datetime(date).date() for date in self.df_date[device][node]]
                index = 0
                total = self.df_total[device][node][0]
                final_dictionary[device][node]['memory'] = []
                final_dictionary[device][node]['date'] = []
                final_dictionary[device][node]['total'] = []
                for single_date in self.daterange(self.min_date.date(), self.max_date.date()):
                    final_dictionary[device][node]['total'].append(total)
                    final_dictionary[device][node]['date'] = final_dictionary[device][node]['date'] + [single_date]
                    if single_date in DATES:
                        final_dictionary[device][node]['memory'] = final_dictionary[device][node]['memory'] + [
                            self.df_app[device][node][index]]
                        index += 1
                    else:
                        if min_app_memory != max_app_memory:
                            final_dictionary[device][node]['memory'] = final_dictionary[device][node]['memory'] + list(
                                np.random.randint(int(min_app_memory),
                                                  int(max_app_memory), 1))
                        else:
                            final_dictionary[device][node]['memory'] = final_dictionary[device][node]['memory'] + list(
                                np.random.randint(self.df_app[device][node][0] - 500,
                                                  self.df_app[device][node][0] + 500, 1))

        return final_dictionary

    def train_test(self, df, size=0.2):
        # test size last 20%
        test_row_size = math.ceil(len(df) * size)
        test = df.iloc[-test_row_size:]
        split_date = test.iloc[0:1, :]['date'].values[0]
        # train size 80%
        train = df.loc[df.date < split_date]
        return train, test

    def split_original_dataset(self):
        original_data = {}
        for device in self.df_app:
            original_data[device] = {}
            for node in self.df_app[device]:
                original_data[device][node] = {}
                original_data[device][node]['train'], original_data[device][node]['test'] = self.train_test(
                    pd.DataFrame({'date': pd.to_datetime(self.df_date[device][node]).date, 'memory': self.df_app[device][node], 'total': self.df_total[device][node]}))
        return original_data

    def split_imputed_dataset(self):
        imputed_data = {}
        for device in self.train_data:
            imputed_data[device] = {}
            for node in self.train_data[device]:
                imputed_data[device][node] = {}
                imputed_data[device][node]['train'], imputed_data[device][node]['test'] = self.train_test(
                    pd.DataFrame({'date': self.train_data[device][node]['date'], 'memory': self.train_data[device][node]['memory'], 'total': self.train_data[device][node]['total']}))
        return imputed_data

    def getData(self):
        return self.split_original_dataset(), self.split_imputed_dataset()