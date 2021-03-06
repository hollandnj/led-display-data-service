from flask import Flask
from ldb_stub.routes import ldb_routes

app = Flask(__name__)

app.register_blueprint(ldb_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
