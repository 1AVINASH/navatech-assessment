This project is hosted completely on docker. 
* It uses fastApi for the backend framework and uvicorn for the server (which is based on the ASGI framework). For production builds, we will ideally us gunicorn and spawn multiple workers (child processes, the routing is managed by gunicorn). 
* It uses postgres as the backend Database

## Commands to run this
* To start the infra and python backend, simply run `docker compose up --build -d` or run `bash setup.sh`
* To exec into the hosted postgres, use `docker compose exec -it db psql -U admin -d postgres_db`
    * To see all databases, use `\l`
    * To see all tables, use `\d`
* To check live logs of a container, use `docker compose logs -f <service_name>`
* To check the auto generated swagger docs, go to `http://localhost:8000/docs`. This assumes your local port 8000 is mapped for the fastapi service. If not, just replace the port 8000 with the port mapped in docker-compose