## Install Openconfig Modules on Cisco Nexus Switch

### Step1: Opening the Bash Shell on the Device
RPM installation on the switch is performed in the bash shell. Make sure feature bash is configured on the device.

```bash
cml-dist-sw01# configure terminal
Enter configuration commands, one per line. End with CNTL/Z.
cml-dist-sw01(config)# feature bash-shell
cml-dist-sw01(config)# end
cml-dist-sw01# run bash sudo su
bash-4.3#
```

To return to the device CLI prompt from bash, type exit or Ctrl-D .

### Step2: Verify Device Readiness
You can use the following CLI show commands to confirm the readiness of the device before installation of an RPM.

show module — Indicates whether all modules are up.

```bash
cml-dist-sw01# show module
Mod Ports             Module-Type                      Model           Status
--- ----- ------------------------------------- --------------------- ---------
1    64   Nexus 9000v 64 port Ethernet Module   N9K-X9364v            ok        
27   0    Virtual Supervisor Module             N9K-vSUP              active *  

Mod  Sw                       Hw    Slot
---  ----------------------- ------ ----
1    9.3(8)                   0.0    LC1 
27   NA                       0.0    SUP1


Mod  MAC-Address(es)                         Serial-Num
---  --------------------------------------  ----------
1    52-1a-3d-fe-01-01 to 52-1a-3d-fe-01-40  9CS96X2S6KQ
27   52-1a-3d-fe-1b-01 to 52-1a-3d-fe-1b-12  9SS10A3ZG58

Mod  Online Diag Status
---  ------------------
1    Pass
27   Pass

* this terminal session 
```

`show module` show system redundancy status — Indicates whether the standby device is up and running and in HA mode. If a standby sync in progress, the RPM installation may fail.

`show system redundancy status` If the line cards have failed to come up, enter the createrepo /rpms command in the bash shell.

```bash
cml-dist-sw01# show system redundancy status
Redundancy mode
---------------
      administrative:   HA
         operational:   None

This supervisor (sup-1)
-----------------------
    Redundancy state:   Active
    Supervisor state:   Active
      Internal state:   Active with no standby

Other supervisor (sup-2)
------------------------
    Redundancy state:   Not present
cml-dist-sw01# 
```

### Step3: Downloading Components from the Cisco Artifactory
The NX-OS Programmable Interface Component RPMs can be downloaded from the Cisco Artifactory at the following URL:

https://devhub.cisco.com/artifactory/open-nxos-agents

Check your NXOS version and download the package for that specific version

```bash
cml-dist-sw01# show version | grep version
Nexus 9000v is a demo version of the Nexus Operating System
  BIOS: version 
 NXOS: version 9.3(8)
  System version: 
cml-dist-sw01# 
```

Here I am downloading the `mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm` under the `9.3-8` as per my Cisco nexus version 

wget https://devhub.cisco.com/artifactory/open-nxos-agents/9.3-8/x86_64/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm

```bash
ubuntu@devnet-box:~/cisco-mdt-tig$ wget https://devhub.cisco.com/artifactory/open-nxos-agents/9.3-8/x86_64/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm
--2022-10-23 18:21:42--  https://devhub.cisco.com/artifactory/open-nxos-agents/9.3-8/x86_64/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm
Resolving devhub.cisco.com (devhub.cisco.com)... 44.207.18.39, 44.208.174.134, 52.1.146.142
Connecting to devhub.cisco.com (devhub.cisco.com)|44.207.18.39|:443... connected.
HTTP request sent, awaiting response... 200 
Length: 52428595 (50M) [application/x-rpm]
Saving to: ‘mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm’

mtx-openconfig-all-1.0.0.0-9.3.8. 100%[==========================================================>]  50.00M  32.2MB/s    in 1.6s    

2022-10-23 18:21:44 (32.2 MB/s) - ‘mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm’ saved [52428595/52428595]

ubuntu@devnet-box:~/cisco-mdt-tig$ ls -l
total 51272
-rw-r----- 1 ubuntu ubuntu     1070 Sep 25 22:04 LICENSE
-rw-r----- 1 ubuntu ubuntu     6325 Oct  5 02:52 README.md
drwxr-x--- 2 ubuntu ubuntu     4096 Oct  5 02:52 certs
drwxr-x--- 2 ubuntu ubuntu     4096 Sep 25 22:04 cli_configs
-rw-r----- 1 ubuntu ubuntu     1333 Oct  5 02:52 docker-compose.yml
drwxr-x--- 5 ubuntu ubuntu     4096 Oct 23 18:14 grafana_data
drwxr-x--- 2 ubuntu ubuntu     4096 Sep 25 22:04 images
drwxr-x--- 5 ubuntu ubuntu     4096 Sep 25 22:10 influxdb_data
drwxr-x--- 2 ubuntu ubuntu     4096 Sep 25 22:04 mdt_python_scripts
-rw-r----- 1 ubuntu ubuntu 52428595 Aug  6  2021 mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm
-rw-r----- 1 ubuntu ubuntu    23579 Oct  5 02:52 secure_grpc_iosxe.md
drwxr-x--- 3 ubuntu ubuntu     4096 Oct  5 02:52 telegraf_data
drwxr-x--- 2 ubuntu ubuntu     4096 Sep 25 22:04 yangsuite_mdt
ubuntu@devnet-box:~/cisco-mdt-tig$ 
```

### Step4: Copy the RPM package from your local system to the Cisco NXOS switch

If the line cards have failed to come up, enter the createrepo /rpms command in the bash shell.

```bash
bash-4.3# createrepo /rpms
43/43 - nia-1.4.1.1-9.3.8.lib32_n9000.rpm                                       
Saving Primary metadata
Saving file lists metadata
Saving other metadata
bash-4.3#
```

Or copy the downloaded RPM package from your system to the Cisco NXOS switch via SCP command. 

```shell
ubuntu@devnet-box:~/cisco-mdt-tig$ scp mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm admin@cml-dist-sw01:bootflash:
The authenticity of host 'cml-dist-sw01 (10.100.5.207)' can't be established.
RSA key fingerprint is SHA256:37M7j6b5KDW/ZdCskbs3v/4Z50Ruhz8msNQBJbq/xd8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'cml-dist-sw01' (RSA) to the list of known hosts.
User Access Verification
Password: 
mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm                                                   100%   50MB   3.1MB/s   00:16    
ubuntu@devnet-box:~/cisco-mdt-tig$ 
```

### Step5: Installing the RPM package 

Login to Cisco NXOS bash and follow the method below 

```shell
bash-4.3# cd /bootflash 
bash-4.3# pwd
/bootflash
bash-4.3# ls -l
total 1964160
-rw-rw-r-- 1 root  root                   0 Sep 22 18:17 bootflash_sync_list
-rw-r----- 1 admin network-admin       2139 Oct 21 08:11 ca-cert.pem
drwxrwxrwx 2 root  root                4096 Sep 22 18:18 eem_snapshots
drwxrwxrwx 2 root  root                4096 Sep 22 18:18 evt_log_snapshot
drwxrwxr-x 3 admin network-admin       4096 Oct 23 14:32 home
-rw-r----- 1 admin network-admin   52428595 Oct 23 15:01 mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm
-rw-rw-rw- 1 root  root          1956867584 Aug  4  2021 nxos.9.3.8.bin
-rw-rw-r-- 1 admin network-admin          0 Sep 23 11:19 platform-sdk.cmd
drwxrwxrwx 2 root  root                4096 Sep 22 18:18 scripts
---------- 1 root  root                 104 Oct 11 12:51 snmp_salt_convert.log
drwxrwxrwx 2 root  root                4096 Sep 22 18:18 virtual-instance

bash-4.3# yum install mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm
Loaded plugins: downloadonly, importpubkey, localrpmDB, patchaction, patching,
              : protect-packages
groups-repo                                              |  951 B     00:00 ... 
groups-repo/primary                                      |  34 kB     00:00 ... 
groups-repo                                                               43/43
localdb                                                  |  951 B     00:00 ... 
patching                                                 |  951 B     00:00 ... 
thirdparty                                               |  951 B     00:00 ... 
wrl-repo                                                 |  951 B     00:00 ... 
wrl-repo/primary                                         | 4.2 kB     00:00 ... 
wrl-repo                                                                  12/12
Setting up Install Process
Examining mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm: mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000
Marking mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package mtx-openconfig-all.lib32_n9000 0:1.0.0.0-9.3.8 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package
        Arch        Version Repository                                     Size
================================================================================
Installing:
 mtx-openconfig-all
        lib32_n9000 1.0.0.0-9.3.8
                            /mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000 173 M

Transaction Summary
================================================================================
Install       1 Package

Total size: 173 M
Installed size: 173 M
Is this ok [y/N]: y
Downloading Packages:
Running Transaction Check
Running Transaction Test
Transaction Test Succeeded
Running Transaction
** Found 1 pre-existing rpmdb problem(s), 'yum check' output follows:
busybox-1.23.2-r0.0.x86_64 has missing requires of busybox-syslog
  Installing : mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000                 1/1 

Installed:
  mtx-openconfig-all.lib32_n9000 0:1.0.0.0-9.3.8                                

Complete!
Install operation 1 completed successfully at Sun Oct 23 15:06:13 2022.

[####################] 100%
bash-4.3# 
```

### Step6: Verify RPM package installation 

Verify via `show version` command and notice the `Active Package(s):`, you can see `mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000` has been installed successfully.

```bash
cml-dist-sw01# show version
Cisco Nexus Operating System (NX-OS) Software
TAC support: http://www.cisco.com/tac
Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_serie
s_home.html
Copyright (c) 2002-2021, Cisco Systems, Inc. All rights reserved.
The copyrights to certain works contained herein are owned by
other third parties and are used and distributed under license.
Some parts of this software are covered under the GNU Public
License. A copy of the license is available at
http://www.gnu.org/licenses/gpl.html.

Nexus 9000v is a demo version of the Nexus Operating System

Software
  BIOS: version 
 NXOS: version 9.3(8)
  BIOS compile time:  
  NXOS image file is: bootflash:///nxos.9.3.8.bin
  NXOS compile time:  8/4/2021 13:00:00 [08/04/2021 22:25:26]


Hardware
  cisco Nexus9000 C9300v Chassis 
  Intel(R) Xeon(R) Gold 6142 CPU @ 2.60GHz with 8160792 kB of memory.
  Processor Board ID 9SS10A3ZG58

  Device name: cml-dist-sw01
  bootflash:    4287040 kB
Kernel uptime is 12 day(s), 4 hour(s), 3 minute(s), 3 second(s)

Last reset 
  Reason: Unknown
  System version: 
  Service: 

plugin
  Core Plugin, Ethernet Plugin

Active Package(s):
        mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000
cml-dist-sw01#  
```

Verify via Cisco NXOS bash 

```bash
bash-4.3# yum list installed | grep mtx
mtx-device.lib32_n9000                 2.0.0.0-9.3.8                 installed  
mtx-grpc-agent.lib32_n9000             2.1.0.0-9.3.8                 installed  
mtx-infra.lib32_n9000                  2.0.0.0-9.3.8                 installed  
mtx-netconf-agent.lib32_n9000          2.0.0.0-9.3.8                 installed  
mtx-openconfig-all.lib32_n9000         1.0.0.0-9.3.8                 @/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000
mtx-restconf-agent.lib32_n9000         2.0.0.0-9.3.8                 installed  
mtx-telemetry.lib32_n9000              2.0.0.0-9.3.8                 installed  
bash-4.3# 
```

```bash
cml-dist-sw01# dir
       4096    Oct 23 15:06:11 2022  .rpmstore/
       4096    Sep 22 18:18:11 2022  .swtam/
          0    Sep 22 18:17:59 2022  bootflash_sync_list
       2139    Oct 21 08:11:49 2022  ca-cert.pem
       4096    Sep 22 18:18:14 2022  eem_snapshots/
       4096    Sep 22 18:18:10 2022  evt_log_snapshot/
       4096    Oct 23 14:32:08 2022  home/
   52428595    Oct 23 15:01:28 2022  mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n900
0.rpm
 1956867584    Aug 04 22:58:29 2021  nxos.9.3.8.bin
          0    Sep 23 11:19:51 2022  platform-sdk.cmd
       4096    Sep 22 18:18:53 2022  scripts/
        104    Oct 11 12:51:49 2022  snmp_salt_convert.log
       4096    Sep 22 18:18:38 2022  virtual-instance/

Usage for bootflash://
 2079916032 bytes used
 2173902848 bytes free
 4253818880 bytes total
cml-dist-sw01# 
```

### To remove the package 

```bash
bash-4.3# yum remove mtx-openconfig-all.lib32_n9000
Loaded plugins: downloadonly, importpubkey, localrpmDB, patchaction, patching,
              : protect-packages
Setting up Remove Process
Resolving Dependencies
--> Running transaction check
---> Package mtx-openconfig-all.lib32_n9000 0:1.0.0.0-9.3.8 will be erased
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package
        Arch        Version
                           Repository                                      Size
================================================================================
Removing:
 mtx-openconfig-all
        lib32_n9000 1.0.0.0-9.3.8
                           @/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000 173 M

Transaction Summary
================================================================================
Remove        1 Package

Installed size: 173 M
Is this ok [y/N]: y
Downloading Packages:
Running Transaction Check
Running Transaction Test
Transaction Test Succeeded
Running Transaction
  Erasing    : mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000                 1/1 

Removed:
  mtx-openconfig-all.lib32_n9000 0:1.0.0.0-9.3.8                                

Complete!
Install operation 5 completed successfully at Sun Oct 23 19:41:51 2022.

[####################] 100%
bash-4.3# 
bash-4.3# yum list installed | grep mtx
mtx-device.lib32_n9000                 2.0.0.0-9.3.8                   installed
mtx-grpc-agent.lib32_n9000             2.1.0.0-9.3.8                   installed
mtx-infra.lib32_n9000                  2.0.0.0-9.3.8                   installed
mtx-netconf-agent.lib32_n9000          2.0.0.0-9.3.8                   installed
mtx-restconf-agent.lib32_n9000         2.0.0.0-9.3.8                   installed
mtx-telemetry.lib32_n9000              2.0.0.0-9.3.8                   installed
bash-4.3# 
```

## Useful Links

[Cisco Nexus 9000 Series NX-OS Programmability Guide, Release 9.3(x)](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_011000.html)

[Cisco NXOS 9.3(8) Yang Models](https://github.com/YangModels/yang/tree/main/vendor/cisco/nx/9.3-8)

[Introduction to OpenConfig](https://www.ciscolive.com/c/dam/r/ciscolive/us/docs/2019/pdf/DEVNET-1775.pdf)

[Using OpenConfig YANG Models on Nexus Switches](https://github.com/networktocode/ntc-misc/blob/master/cisco/yang/nxos-nc-yang-m3.md)

[Exploring IOS-XE and NX-OS based RESTCONF Implementations with YANG and Openconfig](https://blog.networktocode.com/post/Exploring-IOS-XE-and-NX-OS-based-RESTCONF-Implementations-with-YANG-and-Openconfig/)

[Getting Started with Model-Driven Programmability on Cisco Nexus 9000 Series Switches White Paper](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-741518.html)

[Deep Dive Into Model Driven Programmability with NETCONF and YANG](https://pubhub.devnetcloud.com/media/netdevops-live/site/files/s01t03.pdf)

[Expert Hub – Telemetry / Flow Monitoring](https://community.dataminer.services/expert-hub-openconfig/)

[Configure BGP with YDK-Python on NX](http://yang.ciscolive.com/pod0/labs/lab6/lab6-m3)

[Open NX-OS Programmability](https://developer.cisco.com/docs/nx-os/#!model-driven-programmability-with-yang/the-rise-of-network-automation)

[Introducing OpenConfig Telemetry on NX-OS with gNMI and Telegraf!](https://blogs.cisco.com/datacenter/hot-off-the-press-introducing-openconfig-telemetry-on-nx-os-with-gnmi-and-telegraf)

[Cisco gNMI Telemetry Monitoring](https://www.influxdata.com/integration/cisco-gnmi-telemetry/)

[How to stream software telemetry from NX-OS using gNMI](https://www.youtube.com/watch?v=AHE3kGVp5zM)



