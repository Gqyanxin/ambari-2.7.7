.. _getting_started:

===============
Getting Started
===============

Requirements for integration
============================

1. Red Hat Enterprise Linux 6.x (64-bit) or CentOS equivalent.
2. You must have Ambari installed and thus transitively fulfill
   `Ambari's requirements <http://docs.hortonworks.com/HDPDocuments/Ambari-2.1.2.1/bk_Installing_HDP_AMB/content/_meet_minimum_system_requirements.html>`_.
3. Oracle's JDK 1.8u60+ for Trino version 400 and over, and
   1.8u40+ for Trino versions before 0.148. We recommend you read the section on
   :ref:`jdk-configuration-label` to fully understand
   the relationship between Trino and Ambari's JDK.
4. Disable ``requiretty``. On RHEL 6.x this can be done by editing the
   ``/etc/sudoers`` file and commenting out ``Defaults    requiretty``.
5. Install ``wget`` on all nodes that will run a Trino component.

Adding the Trino service
=========================

This section and all others that follow within :ref:`Getting Started <getting_started>`
walk you through the integration steps needed to get Trino working with
Ambari. By default, this integration code installs Trino version ``400``,
the latest version at the time of writing. To install the latest Teradata
Trino release (``406`` at the time of writing), download the Ambari
integration package from `here <http://www.teradata.com/trino>`_ and follow
the remaining instructions below. To change the distribution to install
another version, see :ref:`Build and custom distributions <build_and_custom_distributions>`.

To integrate the Trino service with Ambari, follow the steps outlined below:

* Assuming HDP 3.1 was installed with Ambari, create the following directory on
  the node where the ``ambari-server`` is running:

  .. code-block:: bash

    $ mkdir /var/lib/ambari-server/resources/stacks/HDP/3.1/services/Trino
    $ cd /var/lib/ambari-server/resources/stacks/HDP/3.1/services/Trino

* Place the integration files within the newly created TRINO directory.
  Download the integration package that installs Teradata's version from
  `here <http://www.teradata.com/trino>`_ or download the integration package
  that installs ``400`` from the `releases section of this project <https://github.com/trinodb/ambari-presto-service/releases>`_. Upload the integration archive to your cluster and extract it like so:

  .. code-block:: bash

    $ tar -xvf /path/to/integration/package/ambari-trino-1.3.tar.gz -C /var/lib/ambari-server/resources/stacks/HDP/3.1/services/TRINO
    $ mv /var/lib/ambari-server/resources/stacks/HDP/3.1/services/TRINO/ambari-trino-1.3/* /var/lib/ambari-server/resources/stacks/HDP/3.1/services/TRINO
    $ rm -rf /var/lib/ambari-server/resources/stacks/HDP/3.1/services/TRINO/ambari-trino-1.3

* Finally, make all integration files executable and restart the Ambari server:

  .. code-block:: bash

    $ chmod -R +x /var/lib/ambari-server/resources/stacks/HDP/3.1/services/TRINO/*
    $ ambari-server restart

* Once the server has restarted, point your browser to it and on the main
  Ambari Web UI page click the ``Add Service`` button and follow the on
  screen wizard to add Trino. The following sections provide more details
  on the options and choices you will make when adding Trino.

Supported topologies
====================

The following two screens will allow you to assign the Trino processes among
the nodes in your cluster. Once you pick a topology for Trino and finish the
installation process it is impossible to modify that topology.

Trino is composed of a coordinator and worker processes. The same code runs
all nodes because the same Trino server RPM is installed for both workers and
coordinator. It is the configuration on each node that determines how a
particular node will behave. Trino can run in pseudo-distributed mode, where
a single Trino process on one node acts as both coordinator and worker, or it
can run in distributed mode, where the Trino coordinator runs on one node and
the Trino workers run on other nodes.

The client component of Trino is the ``trino-cli`` executable JAR. You
should place it on all nodes where you expect to access the Trino server via
this command line utility. The ``trino-cli`` executable JAR does not need to
be co-located with either a worker or a coordinator, it can be installed on
its own. Once installed, the CLI can be found at
``/usr/lib/trino/bin/trino-cli``.

**Do not place a worker on the same node as a coordinator.** Such an attempt
will fail the installation because the integration software will attempt to
install the RPM twice. In order to schedule work on the Trino coordinator,
effectively turning the process into a dual worker/coordinator, please enable
the ``node-scheduler.include-coordinator`` toggle available in the
configuration screen.

Pseudo-distributed
------------------

Pick a node for the Trino coordinator and **do not assign any Trino workers**.
On the configuration screen that follows, you must also enable
``node-scheduler.include-coordinator`` by clicking the toggle.

Distributed
-----------

Pick a node for the Trino coordinator and assign as many Trino workers to
nodes as you'd like. Feel free to also place the client component on any node.
Remember to not place a worker on the same node as a coordinator.

Configuring Trino
==================

The one configuration property that does not have a default and requires
input is ``discovery.uri``. The expected value is
``http://<FQDN-of-node-hosting-coordinator>:8285``. Note that it is **http**
and not **https** and that the port is 8285. If you change the value of
``http-server.http.port``, make sure to also change it in ``disovery.uri``.

Some of the most popular properties are displayed in the Settings tab
(open by default). In the Advanced tab, set custom properties by opening up
the correct drop down and specifying a key and a value. Note that specifying
a property that Trino does not recognize will cause the installation to
finish with errors as some or all servers fail to start.

Change the Trino configuration after installation by selecting the Trino
service followed by the Configs tab. After changing a configuration option,
make sure to restart Trino for the changes to take effect.

If you are running a version of Ambari that is older than 2.1
(version number numerically less than 2.1), then you must omit the memory
suffix (GB) when setting the following memory related configurations:
``query.max-memory-per-node`` and ``query.max-memory``. For these two
properties the memory suffix is automatically added by the integration
software. For all other memory related configurations that you add as
custom properties, you'll have to include the memory suffix when specifying
the value.

Adding and removing connectors
------------------------------

To add a connector modify the ``connectors.to.add`` property, whose format is
the following: ``{'connector1': ['key1=value1', 'key2=value2', etc.],
'connector2': ['key3=value3', 'key4=value4'], etc.}``.
Note the single quotes around each individual element. This property only
adds connectors and will not delete connectors. Thus, if you add
``connector1``, save the configuration, restart Trino, then specify ``{}``
for this property, ``connector1`` will not be deleted. If you specify
incorrect values in your connector settings, for example setting the
``hive.metastore.uri`` in the Hive connector to point to an invalid hostname,
then Trino will fail to start.

For example, to add the Hive and Kafka connectors, set the `connectors.to.add` property to:

  .. code-block:: none

    {
        'hive': ['connector.name=hive-cdh4', 'hive.metastore.uri=thrift://example.net:9083'],
        'kafka': ['connector.name=kafka', 'kafka.table-names=table1,table2', 'kafka.nodes=host1:port,host2:port']
    }

To delete a connector modify the ``connectors.to.delete`` property, whose
format is the following: ``['connector1', 'connector2', etc.]``. Again,
note the single quotes around each element. The above value will delete
connectors ``connector1`` and ``connector2``. Note that the ``tpch``
connector cannot be deleted because it is used to smoketest Trino after
it starts. The presence of the ``tpch`` connector has negligible impact on
the system.

For example, to delete the Hive and Kafka connectors, set the
``connectors.to.delete`` property to: ``['hive', 'kafka']``.

.. _jdk-configuration-label:

JDK Configuration
=================

During Ambari's installation, the user is allowed to pick the JDK
that Ambari will use to start itself as well as other services it controls.
This JDK can be edited at any time after installation by running
``ambari-server setup`` on the host running the Ambari server process and
then restarting that process by running ``ambari-server restart`` for
the changes to take effect.

When choosing the JDK version to run, the user is presented with three
options: ``1.8``, ``1.7`` or a custom JDK. If the ``1.8`` or ``1.7``
option is chosen then Ambari will download a JDK of that major version.
However, the update (minor) versions of the JDK differs based on Ambari's
version. For example, Ambari ``2.2.0+`` will download ``1.8u60`` and
versions before will download ``1.8u40``.

When Ambari installs Trino, the JDK used is going to be the JDK
that Ambari was configured with (specifically, the value of
``java.home`` in ``/etc/ambari-server/conf/ambari.properties``).
However, unlike other services, once Trino is installed it will
use the same JDK it was installed with even if Ambari's JDK
is re-configured. The reason for this is that during RPM installation,
Trino's JDK is set in ``/etc/trino/env.sh``. To
re-configure Trino's JDK, edit ``/etc/trino/env.sh`` on all
hosts where Trino will run.
