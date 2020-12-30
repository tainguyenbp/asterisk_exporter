import inspect
import os
import sys

command_core_show_channels= [ "/usr/sbin/asterisk -rx 'core show channels' | awk '{print $1}'" ]

for core_show_channels in command_core_show_channels:
    array = os.popen(core_show_channels).readlines()
    
    active_channels = array[1].rstrip()
    active_calls = array[2].rstrip()
    calls_processed = array[3].rstrip()
    
    print("active calls: "+active_calls)
    print("active channels: "+active_channels)
    print("calls processed: "+calls_processed)






