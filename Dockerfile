# Project PyAutomata Docker

# Build stage for compiling Rust code
FROM rust:latest as rust-builder
WORKDIR /usr/src/rust
COPY pyautomata/rust .
RUN cargo build --release

# Python/Final Stage
FROM python:3.11.6-slim as python-builder

WORKDIR /usr/src/app
COPY --from=rust-builder /usr/src/rust/target/release/libpyautomata_rust.so .
COPY . .

RUN pip install -r requirements.txt
EXPOSE 8888
ENV NAME PyAutomata

CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]

