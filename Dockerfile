# Project PyAutomata Docker
FROM jupyter/scipy-notebook
USER root

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

# Install Rust
RUN apt-get update && apt-get install -y curl build-essential
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"

EXPOSE 8888
ENV NAME PyAutomata