# -*- coding: utf-8 -*-

import os
from salt.utils import which


class Node(object):

    def __init__(self):
        self.get_nodes_cmd = _salt_pillar('get_nodes_cmd')
        self.get_cib_cmd = _salt_pillar('get_cib_cmd')

    def is_ha_node(self):
        if which("pacemakerd") and which("corosync"):
            return True
        return False

    def is_live_node(self):
        if _salt_utils('crmshutils.is_process', 'crmd'):
            return True
        return False

    def get_member(self):
        if self.is_live_node():
            return _salt_run(self.get_nodes_cmd)
        elif self.is_ha_node():
            cib_dir = _salt_pillar('cib_dir')
            cib_file = _salt_pillar('cib_file')
            _env = {"CIB_file": os.path.join(cib_dir, cib_file)}
            return _salt_run(self.get_nodes_cmd, env=_env)
        else:
            return None

    def get_cluster_name(self):
        if self.is_live_node():
            cmd = self.get_cib_cmd + " -o crm_config"
            return _salt_run(cmd)


def get_member():
    node = Node()
    ret = node.get_member()
    if ret:
        return ret.split()

def get_cluster_name():
    node = Node()
    return node.get_cluster_name()

def _salt_pillar(item, action="get"):
    return __salt__['pillar.%s' % action](item)

def _salt_run(cmd, out="stdout", **kwargs):
    return __salt__['cmd.run_all'](cmd, **kwargs)[out]

def _salt_utils(module, *args, **kwargs):
    return __utils__[module](*args, **kwargs)
