<div align="center">
    <h1>Trajectopy Web</h1>
    <h3>Simple web interface for quick trajectory comparisons</h3>

This is a simple web interface for comparing trajectories. It is based on [Trajectopy](https://github.com/gereon-t/trajectopy) and implements basic functionality for comparing trajectories.


<p align="center">
  <img style="border-radius: 10px;" src=.images/frontend.png>
</p>

</div>


## Installation

The easiest way to run the web interface is to use docker compose. The following command will start the web interface on port 5000.

Create a docker-compose.yml file with the following content:

```yaml
version: '3.8'

services:
  frontend:
    image: gtombrink/trajectopy-web:latest

  backend:
    image: gtombrink/trajectopy-api:latest

  reverse-proxy:
    image: nginx
    depends_on:
      - frontend
      - backend
    ports:
      - "5000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

Create a nginx.conf file with the following content:

```nginx
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    sendfile on;

    client_max_body_size 20M;

    server {
        listen 80;

        location / {
            proxy_pass http://frontend:3000/;
        }

        location /api/ {
            rewrite ^/api(/.*)$ $1 break;
            proxy_pass http://backend:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Start the web interface with the following command:

```bash
docker-compose up
```