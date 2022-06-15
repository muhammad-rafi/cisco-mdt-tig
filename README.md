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

### Author 
[Muhammad Rafi](https://www.linkedin.com/in/muhammad-rafi-0a37a248/)

