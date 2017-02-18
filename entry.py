from flask import Flask
from flask_cors import CORS, cross_origin
from x_stub.routes import x_routes
from ldb_stub.routes import ldb_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(x_routes)
app.register_blueprint(ldb_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
