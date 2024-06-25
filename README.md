# api-clients-version

API em Python e Flask para criar recursos. 

Docker-compose para buildar e subir containers pelo WSL, sem a necessidade do dockerDesktop.

docker compose up -d flask_db
docker compose up --build flask_app

Testes usando httpie:

 sudo nala install httpie ;
 
 https GET http://localhost:4000/test ;
 https -v POST http://localhost:4000/users username=bebe email=test@mail.com ;
 https -v POST http://localhost:4000/users username=bebe2 
 email=test2@mail.com ;
 https GET http://localhost:4000/users ;
 https -v DELETE http://localhost:4000/users/1 username=bebe email="test@mail.com" ;
 https -v PUT http://localhost:4000/users/2 username=ALTERADO email=CAXAALTA@asdamail.com ;
 https GET http://localhost:4000/users/2 ;
