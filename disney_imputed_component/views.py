import django
from django.shortcuts import render
import pickle
from disney_memory_prediction.plot import plot_results
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
import os
from disney_dashboard import settings
from django.http import JsonResponse, HttpResponse
import json
import base64


# Create your views here.


# Create your views here.
def return_device_nodes(predictions):
    devices_nodes = {}
    for device in predictions:
        devices_nodes[device] = [node for node in predictions[device]]
    return devices_nodes

def get_high_low_devices(predictions):
    safe_devices = 0
    critical_devices = 0
    for device in predictions:
        for node in predictions[device]:
            if predictions[device][node]['history'][-1] <= 740:
                critical_devices += 1
            else:
                safe_devices += 1
    return {'safe': safe_devices, 'critical': critical_devices}

def getTopDevices(predictions):
    low_app_memory = sorted([predictions[device][node]['history'][-1] for device in predictions for node in predictions[device]])[:10]
    top_devices = {}
    top_devices['devices'] = {}
    for device in predictions:
        for node in predictions[device]:
            if predictions[device][node]['history'][-1] in low_app_memory:
                if device not in top_devices['devices']:
                    top_devices['devices'][device] = {}
                if node not in top_devices['devices'][device]:
                    top_devices['devices'][device][node] = {}
                top_devices['devices'][device][node]['history'] = predictions[device][node]['history'][-1]
                top_devices['devices'][device][node]['total'] = predictions[device][node]['total'][-1]
    return top_devices

def getDashBoardData(request, *args, **kwargs):
    with open(os.path.join(settings.BASE_DIR, 'predictions/predictions.pickle'), 'rb') as handle:
        predictions = pickle.load(handle)
    top_devices = getTopDevices(predictions)
    top_devices['device_nodes'] = return_device_nodes(predictions)
    top_devices['safe_critical'] = get_high_low_devices(predictions)
    return render(request, 'cisco_dashboard.html', {'top_devices': top_devices})

def getTimeSeriesGraph(request, *args, **kwargs):
    with open(os.path.join(settings.BASE_DIR, 'predictions/predictions.pickle'), 'rb') as handle:
        predictions = pickle.load(handle)
    device = request.GET.get('device')
    node = request.GET.get('node')
    get_last_seven_days(predictions, int(device), node)
    plotResults = plot_results(predictions, int(device), node)
    plotResults.plot_train_test_pred()
    with open(os.path.join(settings.BASE_DIR, 'templates/fig.html')) as f:
        fileContent = f.read()
    with open(os.path.join(settings.BASE_DIR, 'static/img/widget3.png'),'rb') as f:
        imageContent = base64.b64encode(f.read()).decode()
    return JsonResponse({'fileContent': fileContent, 'imageContent': imageContent}, status=200, content_type='application/json')

def get_last_seven_days(predictions, device, node):
    last_pred = predictions[device][node]['history'][-7:]
    last_date = predictions[device][node]['history_date'][-7:]
    min_range = min(last_pred) - 10
    max_range = max(last_pred) + 10
    plt.figure(figsize=(10, 6))
    plt.title("Device: "+str(device)+" Node: "+node)
    plt.bar(last_date, last_pred)
    plt.ylim([min_range, max_range])
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/img/widget3.png'))
    plt.close()


