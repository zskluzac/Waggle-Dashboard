from flask import Flask, render_template
import requests
import csv

app = Flask('plots')
fieldNames = ["timestamp", "< One Minute", "< Five Minutes", "< Thirty Minutes", "< One Hour", "< Six Hours",
              "< One Day", "> One Day"]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data.csv')
def data():
    jdata = apirequest("http://10.10.10.137:8000/nodeApi")
    keyList = []
    for x in jdata:
        keyList.append(x)
    keyList.sort()
    tempFile = open("static/temp.csv", "w")
    writer = csv.DictWriter(tempFile, fieldnames=fieldNames)
    writer.writeheader()
    for key in keyList:
        onemin = 0
        fivemin = 0
        thirtymin = 0
        hour = 0
        sixhour = 0
        day = 0
        week = 0
        for x in jdata[key]:
            if x < 60:
                onemin += 1
            elif x < 60*5:
                fivemin += 1
            elif x < 60*30:
                thirtymin += 1
            elif x < 60*60:
                hour += 1
            elif x < 60*60*6:
                sixhour += 1
            elif x < 60*60*24:
                day += 1
            else:
                week += 1
        writer.writerow({"timestamp": key, "< One Minute": onemin, "< Five Minutes": fivemin,
                         "< Thirty Minutes": thirtymin, "< One Hour": hour, "< Six Hours": sixhour,
                         "< One Day": day, "> One Day": week})
    file = open("static/gendata.csv").read()
    tempFile.close()
    tempFile = open("static/temp.csv").read()
    return tempFile


def apirequest(url):
    """
    This function sends a request to an api, and then converts the received data into JSON.
    :param url: The url of the chosen api.
    :return: The received data in JSON format.
    """
    req = requests.get(url)
    json_data = req.json()
    return json_data


if __name__ == '__main__':
    app.run(debug=True, port=3535)
