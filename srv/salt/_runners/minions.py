# -*- coding: utf-8 -*-

import utils
import logging
import salt.client

log = logging.getLogger(__name__)

class Minions(object):

    def __init__(self, **kwargs):
        self.local = salt.client.LocalClient()
        self.minions = self._query()
        self.matches = self._matches()

    def _query(self):
        with utils.stdchannel_redirected():
            ret = self.local.cmd('*', 'saltutil.pillar_refresh')
            minions = self.local.cmd('*', 'pillar.get', ['minions'], tgt_type="compound")

        for minion in minions:
            if minions[minion]:
                return minions[minion]

        log.error("minions is not set")
        return []

    def _matches(self):
        if self.minions:
            with utils.stdchannel_redirected():
                result = self.local.cmd(self.minions, 'pillar.get', ['id'], tgt_type="compound")
            return list(result.keys())
        return []


def show(**kwargs):
    target = Minions()
    return target.minions


def matches(**kwargs):
    target = Minions()
    return target.matches
