#! /usr/bin/python3 
import requests
res = requests.post('http://localhost:8000/v0/jwt/',json={
    "username": "ttt" ,
	"password": "apple123"
})
print("Bearer "+res.json()['access'],sep='')
