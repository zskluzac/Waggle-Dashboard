from flask import Flask, render_template, url_for, request
import requests
import csv

app = Flask('app2')

# These are variables declared at the top for accessibility. They may need to be changed often to update collected data.
key_list = ["id", "location", "alive", "lastupdate"]  # A list of keys of relevant incoming JSON data.
api_url = 'http://127.0.0.1:4000'  # The url of the API for the node dashboard.
fieldNames = ["time", "< One Minute", "< Five Minutes", "< Thirty Minutes", "< One Hour", "< Six Hours",
              "< One Day", "> One Day"]

# Here are the utility functions
# ======================================================================================================================


def apirequest(url):
    # TODO: Add a function that changes the input data to properly formatted data.
    """
    This function sends a request to an api, and then converts the received data into JSON.
    :param url: The url of the chosen api.
    :return: The received data in JSON format.
    """
    req = requests.get(url)
    json_data = req.json()
    return jsonformat(json_data, 3000)
    # print(json_data)
    #return json_data


def jsonformat(json_data, binlength):

    stamplist = []
    timeDict = {}
    timeMax = 0
    timeMin = 0
    endpoint = 0
    for line in json_data:
        timestamp = float(line)
        if timeMax == 0:
            timeMin = timestamp
        if timestamp > timeMax:
            timeMax = timestamp
        if timestamp < timeMin:
            timeMin = timestamp
    duration = timeMax - timeMin
    binNum = duration // binlength
    binlength = duration / binNum

    for bin in range(int(binNum)):
        timeDict[bin] = []
        for timestamp in json_data:
            if endpoint < timestamp < (endpoint + binlength):
                timeDict[bin] = timeDict.get(bin).append(json_data.get(timestamp))
        print(bin)
    print(timeDict)

    # begin = min(stamplist)
    # end = max(stamplist)
    # duration = end - begin
    # numBin = duration // binlength
    # binlength = duration / numBin
    # endpoint = 0
    # binArray = []
    # for bin in range(numBin):
    #     binArray.append([])

    return json_data

# Here are the functions for generating Beehive Node Dashboard
# ======================================================================================================================


@app.route('/')
def dashboard():
    """
    This function is a route to the dashboard homepage, and calls all of the functions necessary for rendering the
    data table. This function also reads and relays the arguments entered into the URL.
    :return: An HTML template that replaces a Jinja block with the HTML table generated in DASHTABLE.
            The DASHTABLE parameter in the return statement connects the Jinja block in 'dashboard.html' to the HTML
            generated in the DASHTABLE function.
    """
    # http://127.0.0.1:5000/?location=chicago&status=alive
    location = str(request.args.get('location'))
    status = str(request.args.get('status'))
    cat = str(request.args.get('cat'))
    table = dashtable(apirequest(api_url), location, status, cat)
    # print(apirequest("http://10.10.10.137:7000/nodeApi"))
    return render_template('dashboard.html', dashtable=table)


def filterdata(data, location, status, cat):
    # TODO: Make this function actually usefully filter the data in a way the user may want.
    """
    The purpose of this function is to filter the data being provided to the table so that only the data chosen by the
    the user is displayed
    :param data: raw, unfiltered JSON data used to populate the table
    :param location: location specification
    :param status: 1 or 0 corresponds to alive and dead.
    :return: filtered data
    """
    fildata = data
    # for row in fildata:
    #     # TODO: For some reason, I can't filter out cat if it's equal to None.
    #     if cat != "" and cat != "None" and cat is not None:
    #         cat = int(cat)
    #         print(cat)
    #         if cat == 1:
    #             print("cat1")
    #         elif cat == 2:
    #             print("cat2")
    #         elif cat == 3:
    #             print("cat3")
    #         elif cat == 4:
    #             print("cat4")
    #         elif cat == 5:
    #             print("cat5")
    #         elif cat == 6:
    #             print("cat6")
    #         if cat == 7:
    #             print("cat7")
    #     if status != "" and status != "None" and status is not None:
    #         if status == "alive":
    #             if row.get('alive') == 1 or row.get("alive") == 1:
    #                 print(row)
    #                 fildata.remove(row)
    #
    #     if int(row.get('id')) == 1000010:
    #
    #         fildata.remove(row)
    return fildata


def dashtable(data, argloc, argstat, argcat):
    """
    This function generates a table based on the JSON data received from the api.
    The table headers must be updated manually to match any new figures.
    :param data: This is JSON data passed in the DASHBOARD function from the APIREQUEST function.
    :param argloc: location arg
    :param argstat: status arg (1 or 0 >> Alive or Dead)
    :return: A string of HTML code that generates a readable table of data.
    """

    # print(argloc)
    print(argcat)
    testData = filterdata(data, argloc, argstat, argcat)
    # testData = data
    tbl = []

    # This section generates the table headers.
    # This must be manually updated when new columns are to be introduced.
    tbl.append("<tr>")
    tbl.append("<th style='cursor: pointer;'>Node ID</th>")
    tbl.append("<th style='cursor: pointer;'>Location</th>")
    tbl.append("<th style='cursor: pointer;'>Status</th>")
    tbl.append("<th style='cursor: pointer;'>Last Update</th>")
    tbl.append("</tr>")

    # This section generates a table that has as many rows as there are nodes, and as many columns as there are elements
    # in the KEY_LIST variable instantiated at the top of the file.
    for i in testData:
        tbl.append("<tr>")
        for j in key_list:
            if j == "alive":
                if i.get(j) == 0:
                    tbl.append("<td bgcolor='red'>")
                    tbl.append("Dead")
                else:
                    tbl.append("<td bgcolor='green'>")
                    tbl.append("Alive")
            else:
                tbl.append("<td>")
                tbl.append(str(i.get(j)))
            tbl.append("</td>")
        tbl.append("</tr>")
    return ''.join(tbl)  # This returns a single string of HTML code, which will produce the table.

# Here are the functions for generating the Beehive Server Dashboard
# ======================================================================================================================


@app.route('/server')
def server():
    """
    This function renders the server dashboard page and supplies it all of the necessary data.
    :return: a rendered webpage
    """
    serverTable = servertable()
    return render_template('serverdash.html', servertable=serverTable, serverlog=serverlog())


@app.route('/data.tsv')
def data():
    """
    This function fetches the node metric data from the api, and then interprets it for the D3.js graph on the server
    dashboard page. It does this by sorting the node uptimes into one of several categories, and then normalizing
    the sizes of the categories.
    :return: serves the file object containing all of the data. (Note: The data is also written to a real file.)
    """
    # Fetches the data from the API
    jdata = apirequest("http://10.10.10.137:8000/nodeApi")

    # Organizes a list of timestamp keys to make the graph chronological
    timespan = []
    for time in jdata:
        timespan.append(time)
    timespan.sort()

    # Opens the csv that will hold the data and writes its column headers
    tempFile = open("static/temp.csv", "w")
    writer = csv.DictWriter(tempFile, delimiter="\t", fieldnames=fieldNames)
    writer.writeheader()

    # This section iterates over all of the data and accumulates all of the uptimes into different categories.
    for timestamp in timespan:
        onemin = 0
        fivemin = 0
        thirtymin = 0
        hour = 0
        sixhour = 0
        day = 0
        week = 0
        for nodeID in jdata.get(timestamp).keys():
            up = jdata.get(timestamp).get(nodeID).get("uptime")
            if up < 60:
                onemin += 1
            elif up < 60*5:
                fivemin += 1
            elif up < 60*30:
                thirtymin += 1
            elif up < 60*60:
                hour += 1
            elif up < 60*60*6:
                sixhour += 1
            elif up < 60*60*24:
                day += 1
            else:
                week += 1

        # This is where the data is normalized, so that it is a percentage of the total rather than a quantity.
        total = sum([onemin, fivemin, thirtymin, hour, sixhour, day, week])
        total /= 100
        onemin /= total
        fivemin /= total
        thirtymin /= total
        hour /= total
        sixhour /= total
        day /= total
        week /= total

        # This bit of code writes each line at the end of each iteration.
        writer.writerow({"time": timestamp, "< One Minute": onemin, "< Five Minutes": fivemin,
                         "< Thirty Minutes": thirtymin, "< One Hour": hour, "< Six Hours": sixhour,
                         "< One Day": day, "> One Day": week})

    # This section closes the write-only version of the CSV and opens a read-only version of the same file.
    tempFile.close()
    tempFile = open("static/temp.csv").read()

    return tempFile


def servertable():
    # TODO: Make this function so that it automatically extends the table when needed.
    """
    This function generates HTML code for a table of server information.
    :return: A string of HTML code to populate the table.
    """
    tbl = []
    tbl.append("<tr>")
    tbl.append("<th>Timestamp</th>")
    tbl.append("<th>Active Nodes (%)</th>")
    tbl.append("<th>Median Uptime</th>")
    tbl.append("<th>Malfunctioning Nodes Count</th>")
    tbl.append("</tr>")
    for x in range(15):
        tbl.append("<tr>")
        tbl.append("<td>N/A</td>")
        tbl.append("<td>N/A</td>")
        tbl.append("<td>N/A</td>")
        tbl.append("<td>N/A"
                   "</td>")
        tbl.append("</tr>")
    return ''.join(tbl)


def serverlog():
    tbl = []
    for x in range(100, 0, -1):
        tbl.append("<tr>")
        tbl.append("<td> Data Received " + str(x) +"</td>")
        tbl.append("</tr>")
    return ''.join(tbl)

# Here are the functions used to generate the documentation page.
# ======================================================================================================================


@app.route('/documentation')
def documentation():
    # TODO: Keep updating this with new information.
    """
    This route renders a template to an HTML documentation page.
    :return: HTML template for documentation page.
    """
    return render_template('documentation.html')

# Here are the functions used to generate the node pages.
# ======================================================================================================================


@app.route('/node/<nodeID>')
def showNodePage(nodeID):
    nodeInfo = nodeTable(nodeID)
    return render_template('nodepage.html', nodeID=nodeID, nodeInfo=nodeInfo)


def nodeTable(nodeID):
    upData = []
    nodeData = apirequest("http://10.10.10.137:8000/nodeApi")
    print nodeData
    # sorted(nodeData, key=lambda d: d[""])
    for row in nodeData:
        for node in nodeData.get(row):
            if node == "Node " + str(nodeID):
                upData.append('<tr><td>')
                upData.append("Uptime: "+str(nodeData.get(row).get(node).get('uptime')))
                upData.append('</td></tr>')
    return ''.join(upData)

# ======================================================================================================================


if __name__ == '__main__':
    app.run(debug=True, port=5000)
