from flask import Flask, render_template, url_for, request
import requests

app = Flask('app2')

key_list = ["id", "location", "alive", "lastupdate"]  # A list of keys of relevant incoming JSON data.
api_url = 'http://127.0.0.1:4000'  # The url of the Beehive API.


@app.route('/')
def dashboard():
    """

    Update Argument Parsing!

    This function is a route to the dashboard homepage, and calls all of the functions necessary for rendering the
    data table.
    :return: An HTML template that replaces a Jinja block with the HTML table generated in DASHTABLE.
            The DASHTABLE parameter in the return statement connects the Jinja block in 'dashboard.html' to the HTML
            generated in the DASHTABLE function.
    """
    # http://127.0.0.1:5000/?location=chicago&status=alive
    location = str(request.args.get('location'))
    status = str(request.args.get('status'))
    table = dashtable(apirequest(api_url), location, status)
    # print(apirequest("http://10.10.10.137:7000/nodeApi"))
    return render_template('dashboard.html', dashtable=table)


def apirequest(url):
    """
    This function sends a request to an api, and then converts the received data into JSON.
    :param url: The url of the chosen api.
    :return: The received data in JSON format.
    """
    req = requests.get(url)
    json_data = req.json()
    return json_data


def dashtable(data, argloc, argstat):
    """

    Update new parameters!

    This function generates a table based on the data received from the api.
    The table headers must be updated manually to match any new figures.
    :param data: This is JSON data passed in the DASHBOARD function from the APIREQUEST function.
    :param argloc: location arg
    :param argstat: status arg
    :return: A string of HTML code that generates a readable table of data.
    """

    print(argloc)
    print(argstat)
    testData = data
    tbl = []

    # This section generates the table headers.
    # This must be manually updated when new columns are to be introduced.
    tbl.append("<tr>")
    tbl.append("<th>Node ID</th>")
    tbl.append("<th>Location</th>")
    tbl.append("<th>Status</th>")
    tbl.append("<th>Last Update</th>")
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


@app.route('/documentation')
def documentation():
    """
    This route renders a template to an HTML documentation page.
    :return: HTML template for documentation page.
    """
    return render_template('documentation.html')


@app.route('/server')
def server():
    return render_template('serverdash.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
