# The XO Game
Simple XO Game built using
- python
- pipenv  
- aiohttp
- sqlalchemy
- dependency_injector  
- PostgreSQL
- Docker & docker-compose
## Live demo
Live demo is available at https://xo.dvlkv.ru
## Building & running
### Requirements
- Docker (>= 19.03.0)
- docker-compose (>= 1.27.0)

Run in repository root directory:
```bash
docker-compose -f docker-compose.dev.yaml up --build
```
The app will be running at http://localhost:8080, docs will be available at http://localhost:8080/api/v1/docs

## Testing
To run tests in local application environment, use:
```bash
 docker-compose -f docker-compose.dev.yaml exec app "pytest" 
```
