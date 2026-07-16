# Localization Lab

Localization Lab is a modular simulation framework for experimenting with radio-based localization. It is inspired by UWB systems and is initially focused on **TDoA (Time Difference of Arrival)** localization and **TDMA (Time Division Multiple Access)** synchronization.

## Goals

* Experiment with TDoA localization and tracking algorithms.
* Simulate TDMA synchronization and radio propagation.
* Keep physics, communication, and localization independent.
* Support interchangeable transports (in-memory, MQTT, ...).



## Architecture

```text
 +-------+        Tick       +-------------+
 | Clock | ----------------> | MQTT Broker |
 +-------+                   +------+------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
 +------------+-----+     +---------+------+     +--------+--------+
 |      World       |     |    Stations    |     |   Localizer     |
 |------------------|     |----------------|     |-----------------|
 | Drones           |     | receive Signal |     | consumes reports|
 | Terrain          |     | emit reports   |     | emits locations |
 | Radio medium     |     | emit heartbeat |     +--------+--------+
 +------------+-----+     +---------+------+              |
              |                     |                     |
              | Signal              | StationReport       | LocalizedSample
              | DroneTruthSample    |                     |
              v                     v                     v
         +----+---------------------+---------------------+----+
         |                    MQTT Broker                      |
         +----+---------------------+---------------------+----+
              |                                           |
              v                                           v
     +--------+--------+                         +--------+--------+
     |    Ingestor     | <---- TrackSample ----- |     Tracker     |
     |-----------------|                         |-----------------|
     | writes tracks   |                         | emits tracks    |
     | writes truth    |                         +-----------------+
     +--------+--------+
              |
              v
       +------+------+
       |   MongoDB   |
       +------+------+
              |
              v
       +------+------+
       |   Viewer    |
       |   backend   |
       +------+------+
              |
              v
       +------+------+
       | JS frontend |
       +-------------+
```

#### Main data flows:

```text
Clock --|MQTT|-> World
Clock --|MQTT|-> Stations
```
```test
World --|MQTT|-> Stations         : Signal
World --|MQTT|-> Ingestor         : DroneTruthSample
```

```text
Stations  --|MQTT|-> Localizer    : StationReport
Localizer --|MQTT|-> Tracker      : LocalizedSample
Tracker   --|MQTT|-> Ingestor     : TrackSample
```

```text
Ingestor -> MongoDB               : only writer
Viewer   -> MongoDB               : only reader
Viewer   -> Frontend              : HTTP/WebSocket
```


## Get Started

The lab runs as a set of Docker Compose services: MQTT broker, MongoDB, viewer,
clock, world simulator, stations, localizer, tracker, and ingestor.

Build the application image:

```sh
make build
```

Start the lab:

```sh
make up
```

The main endpoints are:

- Viewer: http://localhost:8080
- Mongo Express: http://localhost:8081
- MQTT broker: localhost:1883
- MongoDB: localhost:27017

To watch service logs:

```sh
docker compose logs -f
```

To stop the lab and remove MongoDB data:

```sh
make down
```

## Status

Early prototype under active development.
