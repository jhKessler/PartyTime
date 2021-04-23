docker-compose -f docker-compose.prod.yml down
git pull
docker build -t partytime .
docker-compose -f docker-compose.prod.yml up -d
