FROM node:18-bullseye

WORKDIR /app
RUN git clone https://github.com/wokwi/rp2040js.git .
RUN mkdir -p img/
RUN wget https://adafruit-circuit-python.s3.amazonaws.com/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-8.0.2.uf2
RUN sed 's#fat12.img#/app/img/fat12.img#g' -i demo/micropython-run.ts

RUN npm install
ENTRYPOINT ["tail", "-f", "/dev/null"]
