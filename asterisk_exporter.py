#!/usr/bin/env python3.4
import inspect
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

import threading
from http.server import HTTPServer
import socket
import time

from prometheus.collectors import Gauge
from prometheus.registry import Registry
from prometheus.exporter import PrometheusMetricHandler

PORT_NUMBER = 9200

def gather_data(registry):
    """Gathers the metrics"""
    host = socket.gethostname()

    asterisk_total_active_channels_metric = Gauge("asterisk_active_channels", "Total current acitve channels",
                       {'host': host})
    asterisk_total_active_calls_metric = Gauge("asterisk_active_calls", "Total current acitve calls",
                       {'host': host})
    asterisk_total_calls_processed_metric = Gauge("asterisk_calls_processed", "Total current calls processed",
                       {'host': host})

    registry.register(asterisk_total_active_calls_metric)
    registry.register(asterisk_total_active_channels_metric)
    registry.register(asterisk_total_calls_processed_metric)

    while True:
        time.sleep(1)
        command_core_show_channels= [ "/usr/sbin/asterisk -rx 'core show channels' | awk '{print $1}'" ]
        # command_active_channels = "asterisk -rx 'core show channels' | grep 'active channels' | awk '{print $1}'"
        # command_active_calls = "asterisk -rx 'core show channels' | grep 'active calls' | awk '{print $1}'"
        # command_calls_processed = "asterisk -rx 'core show channels' | grep 'calls processed' | awk '{print $1}'"

        # active_channels = os.popen(command_active_channels).read()
        # asterisk_total_active_channels_metric.set({'type': "active channels", }, active_channels)

        # active_calls = os.popen(command_active_calls).read()
        # asterisk_total_active_calls_metric.set({'type': "active calls", }, active_calls)

        # calls_processed = os.popen(command_calls_processed).read()
        # asterisk_total_calls_processed_metric.set({'type': "calls processed", }, calls_processed)

        for core_show_channels in command_core_show_channels:
            sstdin , stdout, stderr = os.popen(core_show_channels)
            array = stdout.readlines()

            active_channels = array[1].rstrip()
            active_calls = array[2].rstrip()
            calls_processed = array[3].rstrip()

            asterisk_total_active_channels_metric.set({'type': "active channels", }, active_channels)

            asterisk_total_active_calls_metric.set({'type': "active calls", }, active_calls)

            asterisk_total_calls_processed_metric.set({'type': "calls processed", }, calls_processed)


if __name__ == "__main__":

    registry = Registry()

    thread = threading.Thread(target=gather_data, args=(registry, ))
    thread.start()
    try:
        def handler(*args, **kwargs):
            PrometheusMetricHandler(registry, *args, **kwargs)

        server = HTTPServer(('', PORT_NUMBER), handler)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
        thread.join()
