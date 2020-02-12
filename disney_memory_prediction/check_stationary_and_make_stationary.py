#Importing libraries
from disney_memory_prediction.load_save_data import load_and_generate_data
from statsmodels.tsa.stattools import adfuller

class stationarySeries():
    def __init__(self):
        load_data = load_and_generate_data()
        self.original_data, self.imputed_data = load_data.getData()
        # self.stationary_data_original = self.check_and_make_stationary(self.original_data)

    def check_and_make_stationary(self, data):
        count = 0
        stationary_data = {}
        for device in data:
            stationary_data[device] = {}
            for node in data[device]:
                if len(list(data[device][node]['train'].memory)) > 2:
                    result = adfuller(list(data[device][node]['train'].memory))
                    stationary_data[device][node] = {}
                    stationary_data[device][node]['train'] = data[device][node]['train']
                    stationary_data[device][node]['test'] = data[device][node]['test']
        #                 if result[0] > result[4]['1%']:
        #                     count+=1
        # #                     plt.plot(data[device][node]['train'].memory)
        # #                     plt.show()
        # #                     plt.close()
        #                 else:
        #                     stationary_data[device] = {}
        #                     stationary_data[device][node] = {}
        #                     stationary_data[device][node]['train'] = data[device][node]['train']
        #                 print('ADF Statistic: %f' % result[0])
        #                 print('p-value: %f' % result[1])
        #                 print('Critical Values:')
        #                 for key, value in result[4].items():
        #                     print('\t%s: %.3f' % (key, value))
        #     print(count)
        return stationary_data

    def getStationaryData(self):
        return self.check_and_make_stationary(self.imputed_data)


