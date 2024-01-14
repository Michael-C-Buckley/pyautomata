# Project PyAutomata

PyAutomata is an in-progress library and tool set designed for computing and evaluating cellular automata.

The first series of support automata are Steven Wolfram's original series of cellular automata (notably including Rule 30).

The library consists of Jupyter-friendly Python elements with computational heavy loads being handled invisibly in Rust for performance.

## Requirements

* [Docker](https://docs.docker.com/engine/install/)

All other requirements are handled by Docker at build and container launch.

## Installation

* Clone repository
* Build with Docker
* Launch with `docker compose up --build`

The resulting Jupyter instance will be bound to `localhost:8888`.