#!/bin/bash

ryu run --observe-links --ofp-tcp-listen-port 10001 --wsapi-port 8082  office1.py &
ryu run --observe-links --ofp-tcp-listen-port 10002 --wsapi-port 8083  office2.py &
ryu run --observe-links --ofp-tcp-listen-port 10003 --wsapi-port 8084  controller.py &
ryu run --observe-links --ofp-tcp-listen-port 10004 --wsapi-port 8085  office3.py &
