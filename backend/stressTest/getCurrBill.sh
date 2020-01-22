#!/usr/bin/sh

AB_TEST="ab -n 100 -c 30 -T application/json -H \"Authorization: `./getjwt.py`\" \"http://localhost:8000/v0/bills/current/\""

echo $AB_TEST | sh 