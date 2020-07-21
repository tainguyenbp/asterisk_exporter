asterisk exporter
===================

## Description
Montior calls in the asterisk core, include: active calls, active channels, call processed 

## Setup
- do you have to install python3.4

- Install prometheus module
```
$ pip3.4 install prometheus
```

- Run it:

```
$ python3.4 asterisk_exporter.py
```

- Go to http://127.0.0.1:9200/metrics or http://IP:9200/metrics

