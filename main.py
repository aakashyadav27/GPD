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

# Opening JSON file
f = open('attributes_mapping.json')

# returns JSON object as
# a dictionary
fixer = json.load(f)

sample={
    "value":[]
}
def fix_dictionary(dict_,fixer):
    return { fixer.get(k, k): v for k, v in dict_.items() }
def lower_dict(d):
    new_dict = dict((k.lower(), v) for k, v in d.items())
    return new_dict
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


@app.route("/filterData", methods=['GET'])
def FilterData():
    with open('filter_data.json') as f:
        json_data = json.load(f)
    return json_data

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
@app.route("/AttributeNames",methods=["GET"])
def grouping():
    f = open('grouping.json')
    attribute_data = json.load(f)
    h = []
    for key, value in attribute_data.items():
        v1 = {}
        v1['group'.format(key)] = key
        h.append(v1)
        v1['checked'] = 'false'
        new_key = [{'name': val, 'checked': 'false'} for val in value]
        v1['data'] = new_key
    attribute_data = json.dumps(h)
    return attribute_data

@app.route("/activityData", methods=['POST'])
def activity_data():
    final_data={"activity":[]}
    input2 = request.json
    print(any(input2.values()))
    if any(input2.values()):
        for x in range(len(input2['value'])):
            new_data=input2['value'][x]['project_name']
            f = open('{}.json'.format(new_data))
            data1 = json.load(f)
            for x in data1['value'][0]['activity']:
                final_data['activity'].append(fix_dictionary(x,lower_dict(fixer)))
        data =json.dumps(final_data)
        return data
    else:
        return "Please select the project"
    #except:
        #return "Exception:Please select the project"
if __name__ == '__main__':
    app.run(debug=True)

