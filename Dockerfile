# Project PyAutomata Docker
FROM jupyter/scipy-notebook

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

# Install Rust and build Requirements
USER root
RUN apt-get update && apt-get install -y curl build-essential
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"
RUN cd /usr/src/app/pyautomata/rust && cargo build --release
USER jovyan

EXPOSE 8888
ENV NAME PyAutomata

CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]
