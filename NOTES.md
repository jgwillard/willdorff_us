# Notes

## Deployment

* [Initial server setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) (create non-root user, set up SSH access and firewall)
* [Django setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) (install dependencies, set up virtualenv, create django project, configure gunicorn and nginx)
  * [Environment variables for gunicorn](https://stackoverflow.com/questions/25076295/gunicorn-environment-variable-setting)
* [Create DNS records](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain/)
* [HTTPS with Let's Encrypt](https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04)
  * [Install certbot](https://certbot.eff.org/instructions) (note that `snapd` is likely already installed)
* [Redirect www.site to site](https://www.digitalocean.com/community/tutorials/how-to-redirect-www-to-non-www-with-nginx-on-centos-7)

## Sample nginx config

`/etc/nginx/sites-available/willdorff_us`:
```
server {
    server_name willdorff.us;

    location = /favicon.ico { access_log off; log_not_found off; }

    # serve static/media files via nginx
    location /static/ {
        root /path/to/project;
    }
    location /media/ {
        root /path/to/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/project/project.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/willdorff.us/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/willdorff.us/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    # redirect http requests to https
    if ($host = willdorff.us) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name willdorff.us;
    return 404; # managed by Certbot
}
```

`/etc/nginx/sites-available/www_willdorff_us`:
```
server {
    # redirect wwww.willdorff.us to willdorff.us
    server_name www.willdorff.us;
    return 301 $scheme://willdorff.us$request_uri;

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/willdorff.us/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/willdorff.us/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = www.willdorff.us) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    server_name www.willdorff.us;
    listen 80;
    return 404; # managed by Certbot
}
```

## Sample gunicorn config

`/etc/systemd/system/gunicorn.service`:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=yourname
Group=www-data
WorkingDirectory=/path/to/project
EnvironmentFile=/path/to/project/.env
ExecStart=/path/to/project/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/project/project.sock project.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Deploying changes

```sh
cd project
git pull
source venv/bin/activate
pip install -r requirements.txt # if dependencies were updated
./manage.py migrate # if schemas were updated
./manage.py collectstatic # if static resources were updated
sudo systemctl restart gunicorn
```
