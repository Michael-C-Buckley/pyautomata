# Project PyAutomata Docker

FROM python:3.11.6-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8888
ENV NAME PyAutomata

CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]

