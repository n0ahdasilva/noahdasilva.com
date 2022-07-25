
# noahdasilva.com

noahdasilva.com is a blog/portfolio Django-based website for Noah Da Silva.
## Authors

- [@n0ahdasilva (Noah Da Silva)](https://www.github.com/n0ahdasilva)

## Deployment

To deploy this project, SSH into the machine running the website's services (Nginx server, Postgres database, and python virtual environment).

```bash
  ssh -p 22 user@ip_adress
```

Next, navigate to the project directory

```bash
  cd /projectdir
```

We will need to pull the latest version of the project's repository.

```bash
  git pull
```

When the local repository is up to date with the remote one, we need to apply the changes by restarting required services.

```bash
  sudo systemctl restart nginx
  sudo systemctl restart gunicorn
```