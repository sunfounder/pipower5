.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!

.. _faq:

FAQ
===

How to Reinstall PiPower 5
--------------------------

If PiPower 5 is not working correctly and you want to perform a clean reinstall, follow these steps:

**1. Uninstall the current installation:**

.. code-block:: shell

   cd ~/pipower5
   sudo python3 install.py --uninstall

**2. Reinstall from source:**

.. code-block:: shell

   git clone https://github.com/sunfounder/pipower5
   cd pipower5
   sudo python3 install.py

**3. Reboot the Raspberry Pi when prompted.**

After reboot, verify the installation:

.. code-block:: shell

   pipower5 -a
   sudo systemctl status pipower5.service

.. tip::

   If the ``~/pipower5`` directory no longer exists from the original installation, skip the uninstall step and go directly to the reinstall step.


Dashboard Shows "Database Required" or No Data
----------------------------------------------

**What you see**: The Web Dashboard opens normally in your browser, but all data panels are empty or show "database required".

**What this usually means**: This is rarely a hardware problem. In most cases, the InfluxDB backend has a configuration issue — a corrupted database, a missing bucket, or an expired token.

**Check these, in order:**

1. **Check that the PiPower 5 service is running:**

   .. code-block:: shell

      sudo systemctl status pipower5

   If the service is not active, start it:

   .. code-block:: shell

      sudo systemctl start pipower5

2. **Check whether the InfluxDB bucket exists:**

   .. code-block:: shell

      sudo influx bucket list

   Look for a bucket named ``pipower5`` in the output. If it is missing, the database needs to be recreated.

3. **Check the service logs for errors:**

   .. code-block:: shell

      journalctl -u pipower5 -n 50

   Look for error messages related to InfluxDB, such as:

   - ``unauthorized`` or ``token`` — indicates an authentication token issue.
   - ``bucket not found`` — the database bucket is missing.
   - ``connection refused`` — InfluxDB is not running.

4. **If InfluxDB itself is down**, restart it:

   .. code-block:: shell

      sudo systemctl restart influxdb
      sudo systemctl restart pipower5

.. note::

   If InfluxDB was installed manually or migrated from an older version, configuration paths or authentication tokens may have changed. In that case, a clean reinstall of PiPower 5 (see above) will also reinitialize the InfluxDB setup.
