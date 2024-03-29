# Project PyAutomata

<p align="center">
  <img src="https://github.com/Michael-C-Buckley/pyautomata/blob/master/resources/rule30-250.png" alt="Wolfram Rule 30" />
</p>

PyAutomata is an in-progress library and tool set designed for computing and evaluating cellular automata.

The first series of support automata are Steven Wolfram's original series of cellular automata (notably including Rule 30).

The library consists of Jupyter-friendly Python elements with computational heavy loads being handled invisibly in Rust for performance.

## Requirements

* [Docker](https://docs.docker.com/engine/install/)

All other requirements are handled by Docker at build and container launch.

## Installation

* Clone repository
* Build with Docker
* Launch with `docker compose up`

The resulting Jupyter instance will be bound to `localhost:8888`.

## Presentation Notebooks

There are example Jupyter notebooks under the branch `presentation` with filled in data.  The notebooks under the main branch are unexecuted.

* [Sample notebook](https://github.com/Michael-C-Buckley/pyautomata/blob/presentation/notebooks/sample.ipynb): Shows examples of the library generating automata
* [Benchmark/performance notebook](https://github.com/Michael-C-Buckley/pyautomata/blob/presentation/notebooks/perfomance.ipynb): compares the project's Rust and Python performance