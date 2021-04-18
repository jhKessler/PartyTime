# PartyTime

###Run docker image
1. ```docker-compose up -d```
2. ``docker build -t partytime .``
3. ```docker-compose up -f docker-compose.prod.yml up```


### SSH into docker image with bash
1. ```docker-compose up -d```
2. ``docker build -t partytime .``
3. ``docker run --network partytime --entrypoint "/bin/sh" -it partytime``
