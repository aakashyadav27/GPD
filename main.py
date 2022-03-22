# Standard library imports
import json
import re
import os

# Third party imports
import requests
from flask import Flask, redirect, request, url_for, jsonify, render_template, make_response
import pandas as pd
from flask_cors import CORS,cross_origin
from functions import *

app = Flask(__name__)
CORS(app)
data=pd.read_excel('planisware_data_1.xlsx')
print(data.columns)


sample={
    "value":[]
}
def username_mapping(input_dicto):
    sample1= {
        "value": []
    }
    new_dict=json.loads(input_dicto)
    for k, v in new_dict.items():
        print("yes")
        if v == "camachodj":
            new_dict[k] = "Cintron,Debra J"
            print(new_dict)
        elif v == "dentp":
            new_dict[k] = "Dent,Philip Damian"
        else:
            pass
    for k, v in new_dict.items():
        ap1 = {"owner": v}
        sample1['value'].append(ap1)
    new_dict=json.dumps(sample1)
    return new_dict

def ntid_mapping(ntid_dict):

    #print(type(ntid_dict))
    ntid_dictn = ntid_dict
    for k, v in ntid_dictn .items():
        if v == "Cintron,Debra J":
            ntid_dictn [k] = "camachodj"
            print(ntid_dictn)
        elif v == "Dent,Philip Damian":
            ntid_dictn[k] = "dentp"
        else:
            pass
    #new_dict=json.dumps(sample)
    #ntid_dictn = json.dumps(ntid_dictn)
    return ntid_dictn


@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route("/ownerList", methods=['POST'])
def GetOwnerList():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        input= request.json
        i = 0
        if any(input.values()):
            for k, v in input.items():
                if v != '':
                    if i == 0:
                        output_data = data[data[k] == v]
                        i = i + 1
                    else:
                        output_data = output_data[output_data[k] == v]
        else:
            no_filter_selected=pd.Series(data['Owner'].reset_index(drop='index').unique())
            no_filter_selected = no_filter_selected.to_json()
            no_filter_selected = username_mapping(no_filter_selected)
            return  no_filter_selected
        output_data = pd.Series(output_data['Owner'].reset_index(drop='index').unique())
        output_data= output_data.to_json()
        output_data = username_mapping(output_data)
        return output_data
    else:
        return 'Not found'
    
@app.route("/projectList", methods=['POST'])
def Projectnames():
    sample2 = {
        "value": []
    }
    content_type1 = request.headers.get('Content-Type')
    category1 = request.json
    if any(category1.values()):

        category1=ntid_mapping(category1)
        new_data=data[data['Owner'] == category1['username']]
        new_data= pd.Series(new_data['Name'].reset_index(drop='index').unique())
        new_data = new_data.to_json()
        new_data=json.loads(new_data)
        print(type(new_data),'================================')
        for k, v in new_data.items():
            ap2 = {"name": v}
            sample2['value'].append(ap2)
        new_data=sample2
        new_data = json.dumps(new_data)
    else:
        new_data = pd.Series(data['Name'].reset_index(drop='index').unique())
        new_data = new_data.to_json()
        new_data = json.loads(new_data)
        print(type(new_data), '================================')
        for k, v in new_data.items():
            ap2 = {"name": v}
            sample2['value'].append(ap2)
        new_data = sample2
        new_data = json.dumps(new_data)
    return new_data


@app.route("/activityData", methods=['POST'])
def activity_data():
    final_data={}
    input2 = request.json
    #try:
    print(any(input2.values()))
    if any(input2.values()):
        for x in range(len(input2['value'])):
            new_data=input2['value'][x]['project_name']
            f = open('{}.json'.format(new_data))
            data = json.load(f)
            #print(type(data))
            final_data['activity{}'.format(x)]=data['value'][0]
        data =json.dumps(final_data)
        return data
    else:
        return "Please select the project"
    #except:
        #return "Exception:Please select the project"
if __name__ == '__main__':
    app.run(debug=True)

