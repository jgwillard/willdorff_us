# Notes

## Deployment

* [Initial server setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) (create non-root user, set up SSH access and firewall)
* [Django setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) (install dependencies, set up virtualenv, create django project, configure gunicorn and nginx)
  * [Environment varialbes for gunicorn](https://stackoverflow.com/questions/25076295/gunicorn-environment-variable-setting)
* [Create DNS records](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain/)
* [HTTPS with Let's Encrypt](https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04)
  * [Install certbot](https://certbot.eff.org/instructions) (note that `snapd` is likely already installed)
* [Redirect www.site to site](https://www.digitalocean.com/community/tutorials/how-to-redirect-www-to-non-www-with-nginx-on-centos-7)
