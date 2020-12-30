import inspect
import os
import sys
import re

command_core_show_channels= [ "asterisk -rx 'sip show peers' | grep 'sip peers' | grep 'Monitored' | grep 'Unmonitored'" ]
test = '20 sip peers [Monitored: 13 online, 6 offline Unmonitored: 1 online, 0 offline]'

command_core_show="asterisk -rx 'sip show peers' | grep 'sip peers' | grep 'Monitored' | grep 'Unmonitored'"
for core_show_channels in command_core_show_channels:
    array = os.popen(core_show_channels).readlines()
print(test)
print(array)


test1 = os.popen(command_core_show).read()


[sip_peers, monitored_online, monitored_offline, unmonitored_offline, unsmonitored_offline] = re.findall("\d+", test)


print("sip_peers: " +sip_peers)
print("monitored_online: " +monitored_online)
print("monitored_offline: " +monitored_offline)
print("unmonitored_offline: " +unmonitored_offline)
print("unsmonitored_offline: " +unsmonitored_offline)

    # active_channels = array[1].rstrip()
    # active_calls = array[2].rstrip()
    # calls_processed = array[3].rstrip()
    
    # print("active calls: "+active_calls)
    # print("active channels: "+active_channels)
    # print("calls processed: "+calls_processed)






