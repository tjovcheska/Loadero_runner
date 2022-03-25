import time
import requests
import sys

def get_test(args):
        url="https://api.loadero.com/v2/projects/{0}/tests/{1}/".format(args.project_id, args.test_id)
        payload={}
        headers={}
        headers["Authorization"]=args.auth_token
    
        try:
            response=requests.get(url, headers=headers, data=payload)
            response.raise_for_status()
            print(response.status_code)
            if(response.status_code==200):
                json_response=response.json()
                print(json_response)
                return json_response

        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))
            sys.exit(1)

def start_test(args, test_id):
    url="https://api.loadero.com/v2/projects/{0}/tests/{1}/runs/".format(args.project_id, test_id)
    payload={}
    headers={}
    headers["Authorization"]=args.auth_token

    try:
        response=requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        print(response.status_code)
        if(response.status_code==202):
            json_response=response.json()
            test_run_id=json_response['id']
            print(test_run_id)
            return test_run_id

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)

def get_test_run_id_status(args, test_id, test_run_id):
    url="https://api.loadero.com/v2/projects/{0}/tests/{1}/runs/{2}/".format(args.project_id, test_id, test_run_id)
    payload={}
    headers={}
    headers["Authorization"]=args.auth_token

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        print(response.status_code)
        if(response.status_code==200):
            json_response=response.json()
            status=json_response['status']
            print(status)
            return status

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)

def wait_for_test_completion(args, test_id, test_run_id, status):
    while status in [None, 'pending', 'initializing', 'running', 'waiting-results']:
        time.sleep(10)
        url="https://api.loadero.com/v2/projects/{0}/tests/{1}/runs/{2}/".format(args.project_id, test_id, test_run_id)
        payload={}
        headers={}
        headers["Authorization"]=args.auth_token
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        print(response.status_code)
        if(response.status_code==200):
            json_response=response.json()
            new_status=json_response['status']
            if(new_status=="done"):
                return new_status
            elif(status!=new_status):
                print('Test status: ', new_status)
            else:
                sys.exit('Test Result: Test failed with status: {0}.'.format(new_status))


def check_status(args, test_id, test_run_id):
    url="https://api.loadero.com/v2/projects/{0}/tests/{1}/runs/{2}/".format(args.project_id, test_id, test_run_id)
    payload={}
    headers={}
    headers["Authorization"]=args.auth_token

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        print(response.status_code)
        if(response.status_code==200):
            json_response=response.json ()
            success_rate=json_response['success_rate']
            print(success_rate)
            if(success_rate==1):
                print('Test passed with success rate: {0}%'.format(success_rate * 100))
            else:
                sys.exit('Test failed with success rate: {0}%'.format(success_rate * 100))
            
    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
        sys.exit(1)
        