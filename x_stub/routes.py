from flask import request, make_response, Blueprint
import urllib, json

x_routes = Blueprint('x_stub', __name__, template_folder='templates')


def arrival(a):
    arrival = {
        "id": a["id"],
        "destinationName": a["destinationName"],
        "expectedArrival": a["expectedArrival"],
        "lineName": a["lineName"],
	"timeToStation": a["timeToStation"]
        }
    return arrival


@x_routes.route('/api/x/list', methods=['GET'])
def get_x_list():
    stopPoint1 = "490020191MU";
    items1 = getStopPointArrivals(stopPoint1)
    stopPoint2 = "490004960N";
    items2 = getStopPointArrivals(stopPoint2)

    x = { "stops" : [{
        "description": stopPoint1,
		"items": items1
        },{
	"description": stopPoint2,
		"items": items2
	}]
    }
    response_body= json.dumps(x)

    resp = make_response(response_body)
    resp.mimetype = 'application/json'
    return resp

def getStopPointArrivals(stopPoint):
    tfl_url = "https://api.tfl.gov.uk/StopPoint/%s/Arrivals?app_id=&app_key=" % stopPoint
    response = urllib.urlopen(tfl_url)
    arrivals = json.loads(response.read())
    items = map(arrival, sorted(arrivals, key=lambda arrival: arrival["expectedArrival"]))
    return items

