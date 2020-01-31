# BillSpliter

This web programme tries to solve the transaction storm in the dormitory.  Now is on the alpha test, so the adding user to a group is not public (but it will go public soon).

## Run this porject

You need to install the 
[Docker](https://www.docker.com/) and 
[Docker-Compose](https://docs.docker.com/compose/)
compose then run:
```shell
$ docker-compose up 
```

## About the mechanism

This site is an implementation of the [two-phase commit](https://da.wikipedia.org/wiki/Two-phase_commit) in real life. After a bill is initiated, only after all the user related to the bill approved, the bill will take effect and unchangeable. User doesn't need to make actual transaction after the settlement started. (Note: after you create a settlement, the settlement waits for all the bill consensus by its' users then it will show the final amount.)  Peers can make the exact amount on the settlement to his receiver, and claim it on the website. Since cross-bank transaction may be cancelled or failed, the receiver should claim he has received the money. After everyone has an agreement on the settlement, the settled bill will truncate into history. It can be view in each settlement view.  

## FAQ

### Why my balance doesn't increase after I created a bill?
> First, your bill won't go anyware and recorded into the system. Your balance will only be affected by the bill that all users agreed. 

### When should I reject a bill?
> When the bill is not related to you or the charges are more than the reality.

### Where did a rejected bill go?
> It becomes on hold; the creator needs to resume it or d

### Should we wait for the settlement finished to create new bills?
> You don't have to; this system can handle those situations. A settlement only includes those bill created before the settlement. The bills after it will be included in the next one. If you sure this settlement is the last one, then you better not create a new bill after it.



## Maintaining Guide

If you already run on a server, update this project can:

```shell
$ git pull && docker-compose up --build -d 
```

### Backup the server data

You can use exec from dockercompose to dump data: 
```shell
$ docker-compose exec web /app/manage.py dumpdata > data.json
```

Then you can use scripts to analyze those data. Don't worry, your password are encryped.


## More Documents

There are two readme on [frontend](frontend/README.md) and [backend](backend/README.md) folders.

## License

This project is protected under MIT License.