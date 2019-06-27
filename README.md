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

Make shure yourhost:80 and yourhost:443 are not busy.

Make it run!
Add -d flag for detached mode


    docker-compose up
    # OR
    docker-compose up -d 
    
<br>
HTTPS 

Connect to nginx docker-container and run:

    apt-get update
    apt-get install python-certbot-nginx
    certbot --nginx -d raccoonbooker.com -d www.raccoonbooker.com
    
    crontab -e
    0 12 * * * /usr/bin/certbot renew --quiet