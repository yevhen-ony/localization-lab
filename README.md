# Localization Lab

Localization Lab is a modular simulation framework for experimenting with radio-based localization. It is inspired by UWB systems and is initially focused on **TDoA (Time Difference of Arrival)** localization and **TDMA (Time Division Multiple Access)** synchronization.

## Goals

* Experiment with TDoA localization and tracking algorithms.
* Simulate TDMA synchronization and radio propagation.
* Keep physics, communication, and localization independent.
* Support interchangeable transports (in-memory, MQTT, ...).

## Architecture

```text
Clock
   │
   ▼
World
   ├── Terrain
   ├── Drones
   └── Medium
   │
   ▼
Stations
   │
   ▼
Ground
```

## Status

Early prototype under active development.
