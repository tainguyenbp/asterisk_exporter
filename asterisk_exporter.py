#!/usr/bin/env python3.4
import inspect
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

import threading
from http.server import HTTPServer
import socket
import time
import re

from prometheus.collectors import Gauge
from prometheus.registry import Registry
from prometheus.exporter import PrometheusMetricHandler

PORT_NUMBER = 9255

def gather_data(registry):
    """Gathers the metrics"""
    host = socket.gethostname()

    asterisk_total_active_channels_metric = Gauge("asterisk_total_active_channels_metric", "Total current acitve channels",
                       {'host': host})
    asterisk_total_active_calls_metric = Gauge("asterisk_total_active_calls_metric", "Total current acitve calls",
                       {'host': host})
    asterisk_total_calls_processed_metric = Gauge("asterisk_total_calls_processed_metric", "Total current calls processed",
                       {'host': host})

    asterisk_system_uptime_seconds_metric = Gauge("asterisk_system_uptime_seconds_metric", "system uptime",
                       {'host': host})
    asterisk_last_reload_seconds_metric = Gauge("asterisk_last_reload_seconds_metric", "last reload",
                       {'host': host})

    asterisk_total_sip_peers_metric = Gauge("asterisk_total_sip_peers_metric", "ip peers",
                       {'host': host})
    asterisk_total_monitored_online_metric = Gauge("asterisk_total_monitored_online_metric", "monitored online",
                       {'host': host})
    asterisk_total_monitored_offline_metric = Gauge("asterisk_total_monitored_offline_metric", "monitored offline",
                       {'host': host})
    asterisk_total_unmonitored_online_metric = Gauge("asterisk_total_unmonitored_online_metric", "unmonitored online",
                       {'host': host})
    asterisk_total_unmonitored_offline_metric = Gauge("asterisk_total_unmonitored_offline_metric", "unmonitored offline",
                       {'host': host})

    asterisk_total_threads_listed_metric = Gauge("asterisk_total_threads_metric", "total threads listed",
                       {'host': host})
    asterisk_total_sip_status_unknown_metric = Gauge("asterisk_total_sip_status_unknown_metric", "total sip status unknown",
                       {'host': host})
    asterisk_total_sip_status_qualified_metric = Gauge("asterisk_total_sip_status_qualified_metric", "total sip status qualified",
                       {'host': host})

    registry.register(asterisk_total_active_calls_metric)
    registry.register(asterisk_total_active_channels_metric)
    registry.register(asterisk_total_calls_processed_metric)

    registry.register(asterisk_system_uptime_seconds_metric)
    registry.register(asterisk_last_reload_seconds_metric)

    registry.register(asterisk_total_sip_peers_metric)
    registry.register(asterisk_total_monitored_online_metric)
    registry.register(asterisk_total_monitored_offline_metric)
    registry.register(asterisk_total_unmonitored_online_metric)
    registry.register(asterisk_total_unmonitored_offline_metric)

    registry.register(asterisk_total_threads_listed_metric)
    registry.register(asterisk_total_sip_status_unknown_metric)
    registry.register(asterisk_total_sip_status_qualified_metric)

    while True:
        time.sleep(1)
        command_core_show_channels = [ "/usr/sbin/asterisk -rx 'core show channels' | awk '{print $1}'" ]
        command_core_show_uptime = [ "/usr/sbin/asterisk -rx 'core show uptime seconds' | awk '{print $3}'" ]
        command_sip_show_peers = "/usr/sbin/asterisk -rx 'sip show peers' | grep 'sip peers' | grep 'Monitored' | grep 'Unmonitored'"
        command_core_show_threads = "/usr/sbin/asterisk -rx 'core show threads' | tail -1 | cut -d' ' -f1"
        command_sip_show_peers_status_unknown = "/usr/sbin/asterisk -rx 'sip show peers' | grep -P '^\d{3,}.*UNKNOWN\s' | wc -l"
        command_sip_show_peers_status_qualified = "/usr/sbin/asterisk -rx 'sip show peers' | grep -P '^\d{3,}.*OK\s\(\d+' | wc -l"
        
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
            array_core_show_channels = os.popen(core_show_channels).readlines()

            active_channels = array_core_show_channels[1].rstrip()
            active_calls = array_core_show_channels[2].rstrip()
            calls_processed = array_core_show_channels[3].rstrip()

            asterisk_total_active_channels_metric.set({'type': "active channels", }, active_channels)
            asterisk_total_active_calls_metric.set({'type': "active calls", }, active_calls)
            asterisk_total_calls_processed_metric.set({'type': "calls processed", }, calls_processed)

        for core_show_uptime in command_core_show_uptime:
            array_core_show_uptime = os.popen(core_show_uptime).readlines()

            system_uptime = array_core_show_uptime[0].rstrip()
            last_reload = array_core_show_uptime[1].rstrip()

            asterisk_system_uptime_seconds_metric.set({'type': "system uptime seconds", }, active_channels)
            asterisk_last_reload_seconds_metric.set({'type': "last reload seconds", }, active_calls) 
              
        sip_show_peers = os.popen(command_sip_show_peers).read()
        [sip_peers, monitored_online, monitored_offline, unmonitored_online, unmonitored_offline] = re.findall("\d+", sip_show_peers)
        asterisk_total_sip_peers_metric.set({'type': "total sip peers", }, sip_peers)
        asterisk_total_monitored_online_metric.set({'type': "total monitored online", }, monitored_online)
        asterisk_total_monitored_offline_metric.set({'type': "total monitored_offline", }, monitored_offline)
        asterisk_total_unmonitored_online_metric.set({'type': "total unmonitored_online", }, unmonitored_online)
        asterisk_total_unmonitored_offline_metric.set({'type': "total unmonitored offline", }, unmonitored_offline)
        
        core_show_threads = os.popen(command_core_show_threads).read()
        asterisk_total_threads_listed_metric.set({'type': "total threads listed", }, core_show_threads)

        sip_show_peers_status_unknown = os.popen(command_sip_show_peers_status_unknown).read()
        asterisk_total_sip_status_unknown_metric.set({'type': "total sip status unknown", }, sip_show_peers_status_unknown)

        sip_show_peers_status_qualified = os.popen(command_sip_show_peers_status_qualified).read()
        asterisk_total_sip_status_qualified_metric.set({'type': "total sip status qualified", }, sip_show_peers_status_qualified)

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
