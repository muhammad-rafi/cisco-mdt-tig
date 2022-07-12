## Cisco MDT with Docker Compose TIG Server Stack

### Introduction 

#### Model-driven Telemetry (MDT)

Model-driven Telemetry (MDT) is a modern technique to monitor the network devices using push a model where data is streamed from the MDT capable devices continuously either on specific (user defined) intervals or on-change. Example of intervals (also called cadence) can be cpu, memory, interfaces statistics etc. and on-change can be interface status change, bgp neighbours flapping, cdp neighbours etc.

Model-driven telemetry uses different roles as described below.

__Publisher__ (pub): Device that sends the telemetry data and create subscriptions.

__Subscriber__ (sub): Application that requests subscriptions.

__Collector__: Application that collects the telemetry data e.g. Logstash, Telegraf. 

__Datastore__: Time series database that stores telemetry data metrics e.g. Influxdb, elasticsearch.

__Visualisation__: A software that visualise the telemetry data in pretty format using graph e.g. Kibana, Grafana.

There are two types of telemetry sessions in MDT: 

__Dial-in Mode__
In a dial-in mode, an MDT receiver dials in to the router, and subscribes dynamically to one or more sensor paths or subscriptions. The router acts as the server and the receiver is the client. The router streams telemetry data through the same session. The dial-in mode of subscriptions is dynamic. This dynamic subscription terminates when the receiver cancels the subscription or when the session terminates.

__Dial-out Mode__
In a dial-out mode, the router dials out to the receiver. This is the default mode of operation. The router acts as a client and receiver acts as a server. In this mode, sensor-paths and destinations are configured and bound together into one or more subscriptions. The router continually attempts to establish a session with each destination in the subscription, and streams data to the receiver. The dial-out mode of subscriptions is persistent. When a session terminates, the router continually attempts to re-establish a new session with the receiver every 30 seconds.

There are many application stacks that can be used for the MDT and two most popular ones are TIG (Telegraf, InfluxDB and Grafana) or ELK (Elastisearch, Logstash and Kibana). 

This repository is focused on TIG (Telegraf, InfluxDB and Grafana) stack. 

#### TIG Server Stack 

TIG (Telegraf, InfluxDB and Grafana) stack is a collection of very powerful open-source tools for the modern-day monitoring solution. Here is the brief definition for each element in the TIG stack.

__Telegraf__ is an open-source server agent (also called collector), for collecting and reporting metrics, it has output plugins to send metrics to a variety of databases, such as InfluxDB, Graphite etc.

__InfluxDB__ is an open-source time series database and provides datastore for metrics, events, and real-time analytics. It has InfluxDB query language (InfluxQL) which is very similar to SQL-like query that allows any user to query its data and filter it.

__Grafana__ is a data visualization and monitoring tool and supports time series datastores such as Graphite, InfluxDB, Prometheus, Elasticsearch.

### Prerequisites

Before you can clone and use the repo, you need to make sure you have git, docker and docker compose are installed. 

### Usage

Clone the repository 
```bash
$ git clone https://github.com/muhammad-rafi/cisco-mdt.git
```

Go to the cisco-mdt-tig folder and run the docker compose command in detached mode to bring the TIG stack up
```bash
$ cd cisco-mdt-tig
$ docker-compose up -d
```

Verify the TIG stack is up and running 
```bash
$ docker-compose ps -a
```
note: you may need to use 'sudo' if your docker-compose requires.

Check logs for troubleshooting 
```bash
$ sudo docker-compose logs
$ docker logs --tail 50 --follow --timestamps grafana
$ docker logs --tail 50 --follow --timestamps influxdb
$ docker logs --tail 50 --follow --timestamps telegraf
```

To login to the containers
```bash
$ docker exec -it telegraf /bin/bash
$ docker exec -it influxdb /bin/bash
$ docker exec -it grafana /bin/bash
```

To bring down containers
```bash
$ docker-compose down
```

### Demo

![App Screenshot](https://github.com/muhammad-rafi/cisco-mdt-tig/blob/main/images/tig_install.png)

![App Screenshot](https://github.com/muhammad-rafi/cisco-mdt-tig/blob/main/images/grafana_login_page.png)

![App Screenshot](https://github.com/muhammad-rafi/cisco-mdt-tig/blob/main/images/add_influxdb_grafana_1.png)

![App Screenshot](https://github.com/muhammad-rafi/cisco-mdt-tig/blob/main/images/add_influxdb_grafana_2.png)

### Reference: 

Programmability Configuration Guide, Cisco IOS XE Amsterdam 17.3.x
*https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/173/b_173_programmability_cg/model_driven_telemetry.html*

Cisco Nexus 9000 Series NX-OS Programmability Guide, Release 9.3(x)
*https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_0101001.html*

Getting Started with Model-Driven Programmability on Cisco Nexus 9000 Series Switches White Paper
*https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-741518.html#_Toc528621687*

Telemetry Configuration Guide for Cisco ASR 9000 Series Routers, IOS XR Release 6.1.x
*https://www.cisco.com/c/en/us/td/docs/iosxr/asr9000/telemetry/b-telemetry-cg-asr9000-61x/b-telemetry-cg-asr9000-61x_chapter_011.html*

Githubs links for MDT
*https://github.com/jeremycohoe/cisco-ios-xe-mdt*
*https://github.com/jeremycohoe/CLUS-DEVWKS-3270*
*https://github.com/guaguila/CLive2022_DEVWKS-3240*

YouTube Links 

Getting started with Cisco YANG Suite
*https://www.youtube.com/watch?v=smrhjL5Ayz0*

NETCONF with YANG Suite
*https://www.youtube.com/watch?v=dTun33611JA&t=389s*

### Author 
[Muhammad Rafi](https://www.linkedin.com/in/muhammad-rafi-0a37a248/)

