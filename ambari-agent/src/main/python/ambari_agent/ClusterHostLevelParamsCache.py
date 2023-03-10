#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from ambari_agent.ClusterCache import ClusterCache
import logging

logger = logging.getLogger(__name__)

class ClusterHostLevelParamsCache(ClusterCache):
  """
  Maintains an in-memory cache and disk cache of the host level params send from server for
  every cluster. This is useful for having quick access to any of the
  topology properties.

  Host level params. Is parameters used by execution and status commands which can be generated
  differently for every host.
  """

  def __init__(self, cluster_cache_dir, initializer_module):
    """
    Initializes the host level params cache.
    :param cluster_cache_dir:
    :return:
    """
    self.initializer_module = initializer_module
    super(ClusterHostLevelParamsCache, self).__init__(cluster_cache_dir)

  def on_cache_update(self):
    for cluster_id, host_level_params in self.iteritems():
      # FIXME: Recovery manager does not support multiple cluster as of now.
      if 'recoveryConfig' in host_level_params:
        logger.info("Updating recoveryConfig from hostLevelParams")

        self.initializer_module.recovery_manager.cluster_id = cluster_id
        self.initializer_module.recovery_manager.update_recovery_config(host_level_params)


  def get_cache_name(self):
    return 'host_level_params'
