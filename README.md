# led-display-data-service
Data aggregation service for my LED display. When running you can call
  http://localhost:5000/api/nre/MDS/list
  http://localhost:5000/api/tfl/490004960N/list
to get lists of trains or buses.

Best use python environments and see requirements.txt, or may need to install pip, flask, flask_cors, suds
```
$ sudo easy_install pip
$ sudo pip install flask flask_cors suds
```

To start
```
$ python entry.py
```
