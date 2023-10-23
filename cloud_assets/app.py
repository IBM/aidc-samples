import datetime
import uuid
import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from flask import Flask, request, abort,current_app
import aidc
import logging

#logging.basicConfig(filename='/tmp/flask.log',
#level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %('f'name)s %(threadName)s : %(message)s')

app = Flask(__name__)

WOS_CREDENTIALS = {
    "url": "https://eu-de.aiopenscale.cloud.ibm.com",
    "username": "not_used",
    "apikey": "your_key",
}

parms = {
        "url": WOS_CREDENTIALS["url"],
        "username": WOS_CREDENTIALS["username"],
        "apikey": WOS_CREDENTIALS["apikey"]
}

def custom_metrics_provider(parms = parms):
    ### Edit the values for your custom performance model. ###
    TruePositiveCost = "0"
    FalsePositiveCost = "-LoanAmount*0.03"
    FalseNegativeCost = "-LoanAmount*0.5"
    TrueNegativeCost = "LoanAmount*0.3"
    ModelDecisionCost = "-0.02"
    HumanDecisionCost = "-0.05"
    ###

    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"

    def get_cloud_access_token():
        apikey = parms['apikey']
        url     = "https://iam.cloud.ibm.com/identity/token"
        headers = { "Content-Type" : "application/x-www-form-urlencoded" }
        data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        response  = requests.post( url, headers=headers, data=data)
        iam_token = response.json()["access_token"]
        return iam_token

    # Get the access token
    def get_cp4d_access_token():
        url = '{}/icp4d-api/v1/authorize'.format(parms['url'])
        payload = {
            'username': parms['username'],
            'api_key': parms['apikey']
        }
        response = requests.post(url, headers=headers, json=payload, verify=False)
        json_data = response.json()
        access_token = json_data['token']
        return access_token

    #Update the run status to Finished in the Monitor Run
    def update_monitor_run_status(base_url, access_token, custom_monitor_instance_id, run_id, status, error_msg = None):
        monitor_run_url = base_url + '/v2/monitor_instances/' + custom_monitor_instance_id + '/runs/'+run_id
        completed_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        patch_payload  = []
        base_path = "/status"
        patch_payload.append(get_patch_request_field(base_path, "state", status))
        patch_payload.append(get_patch_request_field(base_path, "completed_at", completed_timestamp))
        if error_msg != None:
            error_json = get_error_json(error_msg)
            patch_payload.append(get_patch_request_field(base_path, "failure", error_json))
        headers["Authorization"] = "Bearer {}".format(access_token)
        response = requests.patch(monitor_run_url, headers=headers, json = patch_payload, verify=False)
        monitor_run_response = response.json()
        return response.status_code, monitor_run_response

    def get_error_json(error_message):
        trace = str(uuid.uuid4())
        error_json = {
            'trace': trace,
            'errors': [{
                'code': "custom_metrics_error_code",
                'message': str(error_message)
            }]
        }
        return error_json

    def get_patch_request_field(base_path, field_name, field_value, op_name="replace"):
        field_json = {
            "op": op_name,
            "path": "{0}/{1}".format(base_path, field_name),
            "value": field_value
        }
        return field_json

    def sum_performance(payload_data,taskmodel):
        total_value=0
        probability_position=payload_data['records'][0]['fields'].index("probability")        

        for i in range(len(payload_data['records'][0]['values'])):
            probability=payload_data["records"][0]["values"][i][probability_position][0]
            difference=aidc.sumPerProbability(taskmodel,probability)
            total_value+=difference

        return total_value

    def collect_feedback_dataset(access_token, data_mart_id, feedback_dataset_id):        
        offset = 0
        limit = 1000
        reading_data = True
        json_data = None
        annotations = {"annotations": []}
        fields = {"fields": []}
        values = {"values": []}
        result = None
        while reading_data:
            if feedback_dataset_id is not None:
                headers["Authorization"] = "Bearer {}".format(access_token)
                DATASETS_STORE_RECORDS_URL = parms["url"] + "/openscale/{0}/v2/data_sets/{1}/records?offset={2}&limit={3}&format=list".format(data_mart_id, feedback_dataset_id, offset, 1000)
                response = requests.get(DATASETS_STORE_RECORDS_URL, headers=headers, verify=False)
                json_data = response.json()                
                offset += 1000                
                if len(json_data["records"]) != 0:                                
                    annotations["annotations"] = json_data["records"][0]["annotations"]
                    fields["fields"] = json_data["records"][0]["fields"]
                    for val in json_data["records"][0]["values"]:
                        values["values"].append(val)
                if len(json_data["records"]) == 0:
                    reading_data = False                                        
        result = {"records":[{"annotations": annotations["annotations"], "fields": fields["fields"], 
                              "values": values["values"]}]}
        return result

    def collect_payload_dataset(access_token, data_mart_id, payload_dataset_id):
        json_data = None
        if payload_dataset_id is not None:
            headers["Authorization"] = "Bearer {}".format(access_token)
            DATASETS_STORE_RECORDS_URL = parms["url"] + "/openscale/{0}/v2/data_sets/{1}/records?limit={2}&format=list".format(data_mart_id, payload_dataset_id, 100)
            response = requests.get(DATASETS_STORE_RECORDS_URL, headers=headers, verify=False)
            json_data = response.json()
        return json_data

    def get_metrics(access_token, data_mart_id, subscription_id,
                    feedback_dataset_id,payload_dataset_id):
        json_data = collect_feedback_dataset(access_token, data_mart_id, feedback_dataset_id)
        payload_data = collect_payload_dataset(access_token, data_mart_id, payload_dataset_id)

        decisioncost_value=0
        performance_value=0
        impact_value=0
        ml_value=0
        human_value=0
        roi=0
        if json_data is not None and len(json_data["records"][0]['values'])>0:
            fields = json_data['records'][0]['fields']
            values = json_data['records'][0]['values']
            feedback_data = pd.DataFrame(values, columns = fields)
            table = aidc.load_pandas_data(feedback_data)
            taskmodel_data={
              'id': "0",
              'name': "taskModel",
              'description': "aidc"
            }
            taskmodel=aidc.create_task_model(table,taskmodel_data)
            aidc.set_custom_indicators(taskmodel, TruePositiveCost, FalsePositiveCost,
                                       FalseNegativeCost, TrueNegativeCost,
                                       ModelDecisionCost, HumanDecisionCost)
            metrics = aidc.get_indicators(taskmodel)
            performance_value = float(metrics["Performance"])
            impact_value = float(metrics["Impact"])
            decisioncost_value = float(metrics["Decision Cost"])
            ml_value = float(metrics["ml volume"])
            human_value = float(metrics["human volume"])

        if payload_data is not None and len(payload_data["records"])>0 and performance_value>0:
            roi=sum_performance(payload_data,taskmodel)

        metrics = {"decisioncost": decisioncost_value,
                   "performance": performance_value, 
                   "impact": impact_value, 
                   "ml": ml_value, 
                   "human": human_value,
                   "roi": roi}
        return metrics

    # Publishes the Custom Metrics to OpenScale
    def publish_metrics(base_url, access_token, data_mart_id, subscription_id,
                        custom_monitor_id, custom_monitor_instance_id, custom_monitoring_run_id,
                        feedback_dataset_id, timestamp,payload_dataset_id):
        # Generate an monitoring run id, where the publishing happens against this run id
        custom_metrics = get_metrics(access_token, data_mart_id, 
                                     subscription_id, feedback_dataset_id,payload_dataset_id)
        measurements_payload = [
                  {
                    "timestamp": timestamp,
                    "run_id": custom_monitoring_run_id,
                    "metrics": [custom_metrics]
                  }
                ]
        headers["Authorization"] = "Bearer {}".format(access_token)
        measurements_url = base_url + '/v2/monitor_instances/' \
        + custom_monitor_instance_id + '/measurements'
        response = requests.post(measurements_url, headers=headers, 
                                 json = measurements_payload, verify=False)
        published_measurement = response.json()
        return response.status_code, published_measurement

    def publish( input_data ):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")        
        payload = input_data.get("input_data")[0].get("values")
        data_mart_id = payload['data_mart_id']
        subscription_id = payload['subscription_id']
        custom_monitor_id = payload['custom_monitor_id']
        custom_monitor_instance_id = payload['custom_monitor_instance_id']
        custom_monitor_instance_params  = payload['custom_monitor_instance_params']
        custom_monitor_run_id = payload['custom_monitor_run_id']
        payload_dataset_id = payload.get('payload_dataset_id')
        feedback_dataset_id = payload.get('feedback_dataset_id')
        base_url = parms['url'] + '/openscale' + '/' + data_mart_id
        access_token = get_cloud_access_token()
        published_measurements = []
        error_msgs = []
        run_status = "finished"
        try:
            last_run_time = custom_monitor_instance_params.get("last_run_time")
            max_records = custom_monitor_instance_params.get("max_records")
            min_records = custom_monitor_instance_params.get("min_records")
            error_msg = None
            status_code, published_measurement = publish_metrics(base_url, access_token, 
                                                                 data_mart_id,
                                                                 subscription_id,
                                                                 custom_monitor_id,
                                                                 custom_monitor_instance_id,
                                                                 custom_monitor_run_id,
                                                                 feedback_dataset_id, timestamp, 
                                                                 payload_dataset_id)
            if int(status_code) in [200, 201, 202]:
                published_measurements.append(published_measurement)
            else:
                run_status = "error"
                error_msg = published_measurement
                error_msgs.append(error_msg)
            status_code, response = update_monitor_run_status(base_url, access_token,
                                                              custom_monitor_instance_id,
                                                              custom_monitor_run_id,
                                                              run_status, error_msg)
            if int(status_code) not in [200, 201, 202]:
                error_msgs.append(response)
        except Exception as ex:
            error_msgs.append(str(ex))
        if len(error_msgs) == 0:
            response_payload = {
                "predictions" : [{ 
                    "values" : published_measurements
                }]
            }
        else:
            response_payload = {
                "predictions":[],
                "errors": error_msgs
            }
        return response_payload
    return publish

@app.route('/<openscale>',methods=['GET', 'POST'])
def wml_online(openscale):
    aidc_function=custom_metrics_provider()
    custom_metric_response=aidc_function(request.json)
    return custom_metric_response

if __name__ == '__main__':
    app.run(debug=True, port=8082, host='127.0.0.1')
