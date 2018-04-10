
sync master:
  salt.state:
    - tgt: {{ salt['pillar.get']('master_minion') }}
    - sls: crmsh.sync
