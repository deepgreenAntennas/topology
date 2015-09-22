# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP <asicapi@hp.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Debug engine platform module for topology.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import logging
from collections import OrderedDict

from six import iterkeys

from .base import BasePlatform, BaseNode
from ..libraries.manager import libraries


log = logging.getLogger(__name__)


class DebugPlatform(BasePlatform):
    """
    Plugin to build a topology for debugging.

    See :class:`topology.platforms.base.BasePlatform` for more information.
    """

    def __init__(self, timestamp, nmlmanager):
        super(DebugPlatform, self).__init__(timestamp, nmlmanager)

    def pre_build(self):
        """
        See :meth:`BasePlatform.pre_build` for more information.
        """
        log.debug('[HOOK] pre_build')

    def add_node(self, node):
        """
        See :meth:`BasePlatform.add_node` for more information.
        """
        log.debug('[HOOK] add_node({})'.format(
            node
        ))
        return DebugNode(node.identifier, name=node.name, **node.metadata)

    def add_biport(self, node, biport):
        """
        See :meth:`BasePlatform.add_biport` for more information.
        """
        log.debug('[HOOK] add_biport({}, {})'.format(
            node, biport
        ))

    def add_bilink(self, nodeport_a, nodeport_b, bilink):
        """
        See :meth:`BasePlatform.add_bilink` for more information.
        """
        log.debug('[HOOK] add_bilink({}, {}, {})'.format(
            nodeport_a, nodeport_b, bilink
        ))

    def post_build(self):
        """
        See :meth:`BasePlatform.post_build` for more information.
        """
        log.debug('[HOOK] post_build()')

    def destroy(self):
        """
        See :meth:`BasePlatform.destroy` for more information.
        """
        log.debug('[HOOK] destroy()')


class DebugNode(BaseNode):
    """
    Engine Node for debugging.
    """

    def __init__(self, identifier, **kwargs):
        super(DebugNode, self).__init__(identifier, **kwargs)
        self._functions = OrderedDict()

        # Add support for communication libraries
        for libname, registry in libraries():
            for register in registry:
                key = '{}_{}'.format(libname, register.__name__)
                self._functions[key] = register

    def send_command(self, command, shell=None):
        """
        Implementation of the ``send_command`` interface.

        See :meth:`topology.platforms.base.BaseNode.send_command` for more
        information.
        """
        log.debug('{}.send_command({}, shell={})'.format(
            str(self), command, shell
        ))
        return command

    def available_shells(self):
        """
        Implementation of the ``available_shells`` interface.

        See :meth:`topology.platforms.base.BaseNode.available_shells` for more
        information.
        """
        log.debug('{}.available_shells()'.format(str(self)))
        return []

    def send_data(self, data, function=None):
        """
        Implementation of the ``send_data`` interface.

        See :meth:`topology.platforms.base.BaseNode.send_data` for more
        information.
        """
        log.debug('{}.send_data({}, data={}, function={})'.format(
            str(self), data, function
        ))
        if function is None and self._functions:
            function = list(iterkeys(self._functions))[0]
        elif function not in self._functions.keys():
            raise Exception(
                'Function {} is not supported.'.format(function)
            )
        return self._functions[function](data)

    def available_functions(self):
        """
        Implementation of the ``available_functions`` interface.

        See :meth:`topology.platforms.base.BaseNode.available_functions` for
        more information.
        """
        log.debug('{}.available_functions()'.format(str(self)))
        return list(iterkeys(self._functions))

    def __str__(self):
        return 'DebugNode(identifier={}, metadata={})'.format(
            self.identifier, self.metadata
        )


__all__ = ['DebugPlatform', 'DebugNode']
