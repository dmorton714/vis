# Docker 

Docker Cheat Sheet

navigate to db folder:
```bash
cd db 
```
To start:
```bash
docker-compose up -d
```
To stop:
```bash
docker-compose down
```
To stop and delete everything:
```bash
docker-compose down -v
```

exit to quit sql container 
```bash
docker stop bettertire
```

to verify docker is running:
```bash
docker ps
```
to view logs:
```bash
docker logs Prop_DB
```
