
#- {{ salt.saltutil.runner() }}
from_time: -12H
collect_logs:
  - /var/log/messages 
  - /var/log/pacemaker/pacemaker.log 
  - /var/log/pacemaker.log 
  - /var/log/ha-cluster-bootstrap.log
