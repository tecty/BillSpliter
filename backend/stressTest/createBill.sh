#!/usr/bin/sh

AB_TEST="ab -n 500 -c 100 -T application/json -H \"Authorization: `./getjwt.py`\" -p \"createBill.data\" \"http://localhost:8000/v0/bills/\" "

echo $AB_TEST | sh 