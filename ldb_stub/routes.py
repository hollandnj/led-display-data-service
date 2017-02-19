from flask import Response, request, make_response, Blueprint, jsonify
import urllib, json, datetime
from webservice import DarwinLdbSession
from settings import API_KEY

ldb_routes = Blueprint('ldb_stub', __name__, template_folder='templates')
wsdl_url = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx'


def arrival(a):
    arrival = {
        "id": a["id"],
        "mode": "bus",
        "destinationName": a["destinationName"],
        "platformName": a["platformName"],
        "lineName": a["lineName"],
        "scheduled": None,
        "expected": a["expectedArrival"],
        "timeToStation": a["timeToStation"]
    }
    return arrival


def trainArrival(a):
    arrival = {
        "id": a["id"],
        "mode": "train",
        "destinationName": a["destination_text"],
        "platformName": a["platform"],
        "lineName": None,
        "scheduled": a["std"],
        "expected": a["expected"],
        "timeToStation": a["timeToStation"]
    }
    return arrival

@ldb_routes.route('/api/nre/<crs>/list', methods=['GET'])
def get_train_list(crs):
    departures = getNationalRailArrivals(crs)
    response_body= json.dumps(departures)
    resp = make_response(response_body)
    resp.mimetype = 'application/json'
    return resp

@ldb_routes.route('/api/tfl/<stop_point>/list', methods=['GET'])
def get_bus_list(stop_point):
    departures = getStopPointArrivals(stop_point)
    response_body= json.dumps(departures)
    resp = make_response(response_body)
    resp.mimetype = 'application/json'
    return resp

#@ldb_routes.route('/api/unified/list', methods=['GET'])
#def get_unified_list():
#    departures = []
#    stopPoint1 = "490020191MU";
#    buses1 = getStopPointArrivals(stopPoint1)
#    departures = departures + buses1
#    stopPoint2 = "490004960N";
#    buses2 = getStopPointArrivals(stopPoint2)
#    departures = departures + buses2

#    trains = getNationalRailArrivals('MDS')
#    departures = departures + trains
#    ordered_departures = sorted(departures, key=lambda arrival: arrival["expected"])
#    response_body= json.dumps(ordered_departures)

#    resp = make_response(response_body)
#    resp.mimetype = 'application/json'
#    return resp


def getNationalRailArrivals(crs):
    darwin_session = DarwinLdbSession(wsdl=wsdl_url, api_key=API_KEY)
    board = darwin_session.get_station_board(crs)

    train_services = []
    for service in board.train_services:
        estimated_time_string = service.std if service.etd == 'On time' else service.etd
        try:
            parsed_estimated_datetime = datetime.datetime.combine(board.generated_at,
                datetime.datetime.strptime(estimated_time_string,'%H:%M').time())
            timeToStation = parsed_estimated_datetime - board.generated_at
            # todo handle cancelled
            train_services.append(
        	    {
                "id": service.service_id,
        		"platform": service.platform,
        		"destination_text": service.destination_text,
        		"std": service.std,
        		"etd": estimated_time_string,
                "expected": parsed_estimated_datetime.isoformat(),
                "timeToStation" : int(timeToStation.total_seconds())
        	    })
        except ValueError:
            print estimated_time_string
            parsed_estimated_datetime = None


    items = map(trainArrival, train_services)
    return items


def getStopPointArrivals(stopPoint):
    tfl_url = "https://api.tfl.gov.uk/StopPoint/%s/Arrivals?app_id=&app_key=" % stopPoint
    response = urllib.urlopen(tfl_url)
    arrivals = json.loads(response.read())
    items = map(arrival, arrivals)
    return items
