from flask import Response, request, make_response, Blueprint, jsonify
import urllib, json
from webservice import DarwinLdbSession

ldb_routes = Blueprint('ldb_stub', __name__, template_folder='templates')
wsdl_url = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx'


def arrival(a):
    arrival = {
        "id": a["id"],
        "destinationName": a["destinationName"],
        "expectedArrival": a["expectedArrival"],
        "lineName": a["lineName"],
	"timeToStation": a["timeToStation"]
        }
    return arrival


@ldb_routes.route('/api/ldb/list', methods=['GET'])
def get_ldb_list():
    api_key = '7ac169f2-0f80-4b1a-99cd-a8d260d1e702'
    darwin_session = DarwinLdbSession(wsdl=wsdl_url, api_key=api_key)
    board = darwin_session.get_station_board('MDS')
    #resp = response_class(board, '200', 'application/json')
    #resp.mimetype = 'application/json'
    
    train_services = []
    for service in board.train_services:
	train_services.append(
	    {
		"platform": service.platform,
		"destination": service.destination_text,
		"scheduled": service.std,
		"est_departure": service.etd
	    })
    print train_services    
    return jsonify(location_name=board.location_name, crs=board.crs, train_services=train_services)
