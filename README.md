#### About
Simple django pet-project for finance planning, counting etc.

--- 
#### Requirements
docker, docker-compose

--- 
#### Installation
Create file: 

    touch ./conf/secret_settings.py 

and write your configuration by following pattern:

	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.domain.com'
	EMAIL_HOST_USER = 'username@domain.com'
	EMAIL_HOST_PASSWORD = 'password'
	EMAIL_PORT = 587

Put SSL-certs: fullchain.pem, privkey.pem at

    cp /yourdir/fullchain.pem ./nginx/certs
    cp /yourdir/privkey.pem ./nginx/certs

Make shure yourhost:80 and yourhost:443 is not busy.

Make it run!


    docker-compose up

