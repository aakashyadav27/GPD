# Standard library imports
import json
import re
import os

# Third party imports
import requests
from flask import Flask, redirect, request, url_for, jsonify, render_template, make_response
import pandas as pd
from functions import *

app = Flask(__name__)
data=pd.read_excel('planisware_data.xlsx')
print(data.columns)
NTID={"camachodj":"Cintron,Debra J","dentp":"Dent,Philip Damian"}

def username_mapping(input_dicto):
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
    new_dict=json.dumps(new_dict)
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
    content_type1 = request.headers.get('Content-Type')
    category1 = request.json
    if any(category1.values()):
        category1=ntid_mapping(category1)
        new_data=data[data['Owner'] == category1['username']]
        new_data= pd.Series(new_data['Name'].reset_index(drop='index').unique())
        new_data = new_data.to_json()
    else:
        new_data = pd.Series(data['Name'].reset_index(drop='index').unique())
        new_data = new_data.to_json()
    return new_data

"""
@app.route("/ownerList", methods=['POST'])
def GetOwnerList():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        category = request.json
        all_json = json.dumps(category)
        res = json.loads(all_json)
        URL = ownerName(res)
        if URL != 'No filter selected':
            r = requests.get(url=URL, headers=headers)
            data = r.json()
            # pd.DataFrame(res['value'])['owner'].tolist()
            data = json.dumps(data)
            return (data, URL)
        else:
            return URL
    else:
        return 'Content-Type not supported!'


@app.route("/projectList", methods=['POST'])
def Projectnames():
    content_type1 = request.headers.get('Content-Type')
    print('==================>', content_type1)
    category1 = request.json
    all_json1 = json.dumps(category1)
    res1 = json.loads(all_json1)
    URL1 = ProjectName(res1)
    print(URL1)
    r = requests.get(url=URL1, headers=headers)
    data1 = r.json()
    # pd.DataFrame(res['value'])['owner'].tolist()
    data1 = json.dumps(data1)
    return (data1)
"""

if __name__ == '__main__':
    app.run(debug=True)

