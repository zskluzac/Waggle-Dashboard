from flask import Flask, Response
import json
import time

app = Flask('testapi')


@app.route('/')
def statsback():
    apidata = [
        {
            'alive': 1, "location": 'Chicago', 'id': 100001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'New York', 'id': 100010, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Minneapolis', 'id': 100011, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Los Angeles', 'id': 100100, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Munich", "id": 100101, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 100110, "location": "Budapest", "lastupdate": str(time.asctime())
        },
        {
            'alive': 1, "location": 'Phoenix', 'id': 100111, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Kansas City', 'id': 101000, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Saint Paul', 'id': 101001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Boston', 'id': 101010, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Dallas", "id": 101011, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 101100, "location": "Toronto", "lastupdate": str(time.asctime())
        },



        {
            'alive': 1, "location": 'Chicago', 'id': 100001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'New York', 'id': 100010, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Minneapolis', 'id': 100011, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Los Angeles', 'id': 100100, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Munich", "id": 100101, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 100110, "location": "Budapest", "lastupdate": str(time.asctime())
        },
        {
            'alive': 1, "location": 'Phoenix', 'id': 100111, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Kansas City', 'id': 101000, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Saint Paul', 'id': 101001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Boston', 'id': 101010, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Dallas", "id": 101011, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 101100, "location": "Toronto", "lastupdate": str(time.asctime())
        },
        {
            'alive': 1, "location": 'Chicago', 'id': 100001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'New York', 'id': 100010, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Minneapolis', 'id': 100011, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Los Angeles', 'id': 100100, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Munich", "id": 100101, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 100110, "location": "Budapest", "lastupdate": str(time.asctime())
        },
        {
            'alive': 1, "location": 'Phoenix', 'id': 100111, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Kansas City', 'id': 101000, "lastupdate": "Mon Aug 10 09:17:11 2016"
        },
        {
            'alive': 1, "location": 'Saint Paul', 'id': 101001, "lastupdate": str(time.asctime())
        },
        {
            'alive': 0, "location": 'Boston', 'id': 101010, "lastupdate": "Thurs May 2 22:01:57 2017"
        },
        {
            "location": "Dallas", "id": 101011, "alive": 1, "lastupdate": str(time.asctime())
        },
        {
            "alive": 1, "id": 101100, "location": "Toronto", "lastupdate": str(time.asctime())
        }
    ]
    return Response(json.dumps(apidata), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
