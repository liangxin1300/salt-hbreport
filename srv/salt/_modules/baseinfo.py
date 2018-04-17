# -*- coding: utf-8 -*-

import salt.utils.path


class Node(object):

    def __init__(self):
        self.members = self.get_member()
        self.cluster_name = self.get_cluster_name()

    def is_ha_node(self):
        pass

    def is_live_node(self):
        pass

    def get_member(self):
        pass

    def get_cluster_name(self):
        pass
