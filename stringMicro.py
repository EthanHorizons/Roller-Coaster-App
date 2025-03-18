from flask import Flask, jsonify
import requests

app = Flask(__name__)
homeURL = "http://localhost:5000"
headers = {
    'Content-Type': "application/ld+json"
}
#goes through each possibilty and changes the sub string
def strOptions(status):
    statusName = status.get('name')
    if(statusName):
        statusName = statusName.replace("status.operating", "Operating")
        statusName = statusName.replace("status.closed.temporarily", "Temporarily Closed")
        statusName = statusName.replace("status.closed.definitely", "Permenantly Closed")
        statusName = statusName.replace("status.construction", "Under Construction")
        statusName = statusName.replace("status.relocated", "Relocated")
        statusName = statusName.replace("status.retracked", "Retracked")
    return statusName
#can receive either hydra list or single coaster, changes substring
def changeString(coasterData):#receives json
    if coasterData.get('hydra:member', []):
        coasters = coasterData.get('hydra:member', [])
        for coaster in coasters:
            status = coaster.get('status', {})
            status['name'] = strOptions(status)
    else:
        status = coasterData.get('status', {})
        status['name'] = strOptions(status)
    return coasterData


@app.route('/string/<int:opt>', methods=['GET'])
def string(opt):
    if opt == 0:
        servingRes = requests.get(f"{homeURL}/serveString/0")
    else:
        servingRes = requests.get(f"{homeURL}/serveString/1")
    if servingRes.status_code == 200:
        data = servingRes.json()
        returnData = changeString(data)
    return jsonify(returnData)

if __name__ == '__main__':
    app.run(port=5300)  

