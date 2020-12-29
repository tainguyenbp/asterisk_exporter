#!/bin/bash

SCRAPE_INTERVAL=5
METRIC_FILE="/etc/asterisk_exporter/asterisk_exporter.prom"
TEMP_FILE=$(mktemp)

append_gauge () {
  echo "# TYPE $1 gauge" >> $TEMP_FILE
  echo "$1 $2" >> $TEMP_FILE
}

append_counter() {
    echo "# Type $1 counter" >> $TEMP_FILE
    echo "$1 $2" >> $TEMP_FILE
}

publish () {
  mv -f $TEMP_FILE $METRIC_FILE
}

collect () {
  local x=$(asterisk -rx 'core show uptime seconds')
  AST_UPTIME_SEC=$(echo $x | cut -d' ' -f3)
  AST_LAST_RELOAD_SEC=$(echo $x | cut -d' ' -f6)

  append_counter "asterisk_uptime_seconds" $AST_UPTIME_SEC
  append_counter "asterisk_last_core_reload_seconds" $AST_LAST_RELOAD_SEC

  x=$(asterisk -rx 'core show channels' | tail -3)
  AST_ACTIVE_CHANNELS=$(echo $x | cut -d' ' -f1)
  AST_ACTIVE_CALLS=$(echo $x | cut -d' ' -f4)
  AST_CALLS_PROCESSED=$(echo $x | cut -d' ' -f7)

  append_gauge "asterisk_active_channels" $AST_ACTIVE_CHANNELS
  append_gauge "asterisk_active_calls" $AST_ACTIVE_CALLS
  append_counter "asterisk_calls_processed" $AST_CALLS_PROCESSED

  AST_THREADS=$(asterisk -rx 'core show threads' | tail -1 | cut -d' ' -f1)
  append_gauge "asterisk_core_threads" $AST_THREADS

  AST_EXTEN_UNKNOWN_STATUS=$(asterisk -rx 'sip show peers' | grep -P '^\d{3,}.*UNKNOWN\s' | wc -l)
  append_gauge "asterisk_exten_status_unknown" $AST_EXTEN_UNKNOWN_STATUS

  AST_EXTEN_QUALIFIED_STATUS=$(asterisk -rx 'sip show peers' | grep -P '^\d{3,}.*OK\s\(\d+' | wc -l)
  append_gauge  "asterisk_exten_status_qualified" $AST_EXTEN_QUALIFIED_STATUS
}

while true
do
 collect
 publish
 sleep $SCRAPE_INTERVAL
 TEMP_FILE=$(mktemp)
done
