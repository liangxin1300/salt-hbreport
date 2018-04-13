
master_minion_default:
master_minion: {{ salt['pillar.get']('master_minion', master_minion_default) }}

minions_default:
minions: {{ salt['pillar.get']('minions', minions_default) }}
