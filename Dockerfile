# Project PyAutomata Docker
FROM jupyter/base-notebook
USER root

RUN apt-get update && apt-get install -y curl build-essential
WORKDIR /app

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"

# Build Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project and install it
COPY . /app
RUN pip install /app

# Build Rust library
RUN cd pyautomata/rust && cargo build --release

EXPOSE 8888
ENV NAME PyAutomata