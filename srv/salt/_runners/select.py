# -*- coding: utf-8 -*-

import logging
import minions
import salt.client

log = logging.getLogger(__name__)


def all_minions():
    target = minions.Minions()
    return target.matches


def ha_nodes():
    local = salt.client.LocalClient()
    target = minions.Minions()
    for minion in target.matches:
        print(minion)
        #print(local.cmd(minion, 'cmd.run', ['crm_node -l']))
