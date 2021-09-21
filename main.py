# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
import json
from datetime import datetime

app = Flask(__name__)
data = {}
issue_data = {}

def writeIssueDataBase():
    with open('./issue.json','w') as file:
        global issue_data
        file.write(json.dumps(issue_data,ensure_ascii=False))
    readIssueDataBase()

def writeDataBase():
    with open('./user.json','w') as file:
        global data
        file.write(json.dumps(data,ensure_ascii=False))
    readDataBase()

# def readIssueDataBase():
#     with open('./issue.json','r') as file:
#         global issue_data
#         print(file.read())
#         issue_data = json.loads(file.read())
#         print(issue_data)

def readIssueDataBase():
    with open('./issue.json','r') as file:
        global issue_data
        readdata = file.read()
        print(readdata)
        data = json.loads(readdata)
#         issue_data = json.loads(file.read())
#         print(issue_data)
        issue_data = data
        print(issue_data)
        
def readDataBase():
    with open('./user.json','r') as file:
        global data
        readdata = file.read()
        print(readdata)
        data = json.loads(readdata)
        print(data)

@app.route('/')
def index():
    return 'index'

# birthAndName = 1998年1月27號,蔣志成
@app.route('/getHistoryIssue/<birthAndName>')
def getHistoryIssue(birthAndName):
    global issue_data , data
    birth , name = birthAndName.split(',')
    ssid = ""
    for inside_json in data["User"]:
        if(inside_json["Name"] == name and inside_json["Birth"] == birth):
            ssid = inside_json["SSID"]
            break
    if(ssid == ""):
        data["User"].append({"SSID": str(len(data["User"])),"Name": name,"Birth": birth})
        #write data base
        writeDataBase()
        result = {}
        result["result"]=[]
        return json.dumps(result,ensure_ascii=False)
    result = {}
    result["result"]=[]
    count = 0
    for issue in issue_data["Issues"]:
        if(issue["SSID"] == ssid):
            result["result"].append({"Time":issue["Time"],"Issue":issue["Issue"]})
            count += 1
#         if(count == 3):
#             break
    print(ssid)
    print(result["result"])
    result["result"] = result["result"][-3:]
    return json.dumps(result,ensure_ascii=False)

@app.route('/newIssue/<birthAndNameandIssue>')
def newIssue(birthAndNameandIssue):
    global issue_data , data
    now = datetime.now()
    birth , name , issue = birthAndNameandIssue.split(',')
    ssid = ""
    print("step 1")
    for inside_json in data["User"]:
        if(inside_json["Name"] == name and inside_json["Birth"] == birth):
            ssid = inside_json["SSID"]
            break
    if(ssid == ""):
        return None
    print("step 2")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time=year+"年"+month+"月"+day+"號"
    issue_data["Issues"].append({"SSID":ssid,"Time":date_time,"Issue":issue})
    print("step 3")
    print(issue_data)
    writeIssueDataBase()
    print("step 4")
    return "Success" ,200
    
if(__name__ == "__main__"):
    readDataBase()
    readIssueDataBase()
    app.run(host="0.0.0.0",port=3000)