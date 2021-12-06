#!/bin/bash

ryu run --observe-links --ofp-tcp-listen-port 10001 --wsapi-port 8082  voip_slice.py &
ryu run --observe-links --ofp-tcp-listen-port 10002 --wsapi-port 8083  data_slice.py &
ryu run --observe-links --ofp-tcp-listen-port 10003 --wsapi-port 8084  controller.py &
