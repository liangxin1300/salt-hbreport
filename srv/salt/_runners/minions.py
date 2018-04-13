# -*- coding: utf-8 -*-

import logging
import salt.client

log = logging.getLogger(__name__)

class Minions(object):

    def __init__(self, **kwargs):
        self.local = salt.client.LocalClient()
        self.minions = self._query()

    def _query(self):
        with __utils__['runner_utils.stdchannel_redirected']():
            ret = self.local.cmd('*', 'saltutil.pillar_refresh')
            minions = self.local.cmd('*', 'pillar.get', ['minions'], tgt_type="compound")

        for minion in minions:
            if minions[minion]:
                return minions[minion]

        log.error("minions is not set")
        return []


def show(**kwargs):
    target = Minions()
    return target.minions
