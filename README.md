# led-display-data-service
Data aggregation service for my LED display. When running you can call
  http://localhost:5000/api/nre/MDS/list
  http://localhost:5000/api/tfl/490004960N/list
to get lists of trains or buses.

Best use python environments and see requirements.txt
```
$ mkdir Projects
$ cd Projects
$ git clone https://github.com/hollandnj/led-display-data-service.git
$ cd led-display-data-service
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

To start
```
(env) $ python entry.py
```

To deactivate
```
(env) $ deactivate
```
