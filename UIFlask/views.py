from tkinter import FIRST
from flask import Flask, render_template, request, jsonify, session
from UIFlask import app
import requests

#coaster data for search
PRIVATE_API_URL = "http://127.0.0.1:5100/fetch"
print("CALLING MICROSERVICE B")
response = requests.get(PRIVATE_API_URL)
coasterData = response.json()
coaster_data = []
filteredCoasters = []
coasters = []
firstTimeFlag = 0
#Get number from Microservice A
def randomNumMicro():
    randomNumberURL = "http://localhost:4000/random"
    for _ in range(20):
        randomNum = requests.get(randomNumberURL)
        if randomNum.status_code == 200:
            ID = randomNum.json().get("number")
            if ID:
                return ID

#getting 20 coasters
def randomCoasters():
    global coasterData
    global coaster_data
    global coasters
    coasterData = changeString(0)
    coaster_ids = []
    print("CALLING MICROSERVICE A")
    for _ in range(20):
        coaster_ids.append(randomNumMicro())

    coasterMembers = coasterData.get('hydra:member',[])
    coasters = []
    index = 0;
    while index < len(coaster_ids):
        coaster_ID = coaster_ids[index]
        found = next((coaster for coaster in coasterMembers if coaster.get('id') == coaster_ID), None)
        if found:
            coasters.append(found)
        else:
            coaster_ids.append(randomNumMicro())
        index += 1
    print("Booting Done")

def changeString(opt):#0 for coasterData, 1 for coaster_data
    print("CALLING MICROSERVICE C")
    changeStringURL = f"http://localhost:5300/string/{opt}"
    changeStringResponse = requests.get(changeStringURL)
    if changeStringResponse.status_code == 200:
        return changeStringResponse.json()

@app.route('/serveString/<int:option>', methods=['GET'])#serves current data, must be json
def serveString(option):
    if option == 0:#asking for array of 
        return coasterData
    else: 
        return coaster_data

        
#color microservice--------------------------------
def randColor():
    print("CALLING MICROSERVICE D")
    randomColorURL = "http://localhost:5500/color"
    randomColor = requests.get(randomColorURL)
    if randomColor.status_code == 200:
        colors = randomColor.json()
        if colors:
            return colors

#-------------------------------------------main Routes
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    global firstTimeFlag
    if firstTimeFlag == 0:
        randomCoasters()
    firstTimeFlag = 1;
    return render_template(
        "home.html", 
        coasters=coasters,
        title="Home Page",
        )

@app.route('/search')
def search():
    query = request.args.get('n', '').lower()
    global firstTimeFlag
    global filteredCoasters
    global coasterData
    if(query):
        findNameURL = f"http://127.0.0.1:5100/name/{query}"
        nameResponse = requests.get(findNameURL)
        coasterData = nameResponse.json()
    coasterList = coasterData.get('hydra:member', [])
    filteredCoasters = [coaster for coaster in coasterList if query in coaster['name'].lower()]
    return render_template(
        "search.html",
        title="Search Page",
        coasters=filteredCoasters)

@app.route('/details/<int:coaster_id>')
def details(coaster_id):
   coaster = next((c for c in filteredCoasters if c['id'] == coaster_id), None)
   if not coaster:
       coaster = next((c for c in coasters if c['id'] == coaster_id), None)
   if coaster:
        find_url = f"http://127.0.0.1:5100/find/{coaster_id}"
        find_response = requests.get(find_url)
        coaster = find_response.json()
        return render_template(
            "details.html",
            coaster=coaster,
            title = "Detail Page")

@app.route('/customize')
def customize():
    return render_template(
        "customize.html",
        title="Customize Page")
@app.route('/randomColor')
def randomColor():
    colorSet = randColor()
    return colorSet
#-----------------------------------------saving data list
@app.route("/saveCoaster", methods=['POST'])
def saveCoaster():
    data=request.get_json()
    if "savedCoasters" not in session:
        session["savedCoasters"] = []#init if not exist

    savedCoasters = session["savedCoasters"]
    savedCoasters.append(data)
    session["savedCoasters"] = savedCoasters#save to session

    return jsonify({"message": "Coaster {data['name']} added"})


@app.route("/list", methods=['GET'])
def list():
    #session.pop("savedCoasters") #this can clear the session
    savedCoasters = session.get("savedCoasters", [])#retrieve
    return render_template(
        "list.html",
        coasters=savedCoasters,
        title = "List")


@app.route('/details/<int:coaster_id>/list')
def listDetails(coaster_id):
    savedCoasters = session.get("savedCoasters", [])#retrieve
    coaster = next((c for c in savedCoasters if c['id'] == coaster_id), None)
    if coaster:
        find_url = f"http://127.0.0.1:5100/find/{coaster_id}"
        find_response = requests.get(find_url)
        coaster = find_response.json()
    return render_template(
        "listDetails.html",
        coaster=coaster,
        title= "List Detail")


@app.route('/removeCoaster/<int:coaster_id>', methods=['DELETE'])
def removeCoaster(coaster_id):
    if "savedCoasters" in session:
        savedCoasters = session["savedCoasters"]
        savedCoasters = [c for c in savedCoasters if c['id'] != coaster_id]#remove
        session["savedCoasters"] = savedCoasters#update
    return jsonify({"message": "success"})