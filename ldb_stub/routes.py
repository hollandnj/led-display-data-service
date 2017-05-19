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
        "expected": a["expected"],
        "scheduledDateTime": None,
        "expectedDateTime": a["expectedArrival"],
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
        "expected": a["etd"],
        "scheduledDateTime": a["std_datetime"],
        "expectedDateTime": a["etd_datetime"],
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
        try:
            std_datetime = datetime.datetime.combine(board.generated_at,
                datetime.datetime.strptime(service.std,'%H:%M').time())
        except ValueError:
            std_datetime = None

        try:
            etd_datetime = datetime.datetime.combine(board.generated_at,
                datetime.datetime.strptime(service.etd,'%H:%M').time())
            #timeToStation = parsed_estimated_datetime - board.generated_at
            # todo handle cancelled
        except ValueError:
            # Could be 'On time' or 'Cancelled'
            # in either case use scheduled time
            etd_datetime = std_datetime
            #print estimated_time_string
            #parsed_estimated_datetime = None
            #timeToStation = None

        if etd_datetime is not None:
            timeToStation = etd_datetime - board.generated_at
        else:
            timeToStation = None

        train_services.append(
    	    {
            "id": service.service_id,
    		"platform": service.platform,
    		"destination_text": service.destination_text,
    		"std": service.std,
    		"etd": service.etd,
            "std_datetime": std_datetime.isoformat(),
            "etd_datetime": etd_datetime.isoformat(),
            "timeToStation" : int(timeToStation.total_seconds())
    	    })

    items = map(trainArrival, train_services)
    return items


def getStopPointArrivals(stopPoint):
    tfl_url = "https://api.tfl.gov.uk/StopPoint/%s/Arrivals?app_id=&app_key=" % stopPoint
    response = urllib.urlopen(tfl_url)
    arrivals = json.loads(response.read())
    items = []
    for arr in arrivals:
        arr["expected"] = datetime.datetime.strftime(
            datetime.datetime.strptime(arr["expectedArrival"],"%Y-%m-%dT%H:%M:%SZ"),
            "%H:%M")
        items.append(arrival(arr))
    return items
