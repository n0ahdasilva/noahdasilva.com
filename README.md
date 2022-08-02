
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

**NOTE:** If there are local overwrite issues, you can reset the branch. This will erase anything tracked by Git and will not touch untracked local files.

```bash
git fetch --all
git reset --hard origin/master
```

When making changes to the project's models, you may need to make apply the migrations.

```bash
source django-venv/bin/activate
python manage.py makemigrations
python manage.py migrate
deactivate
```

Finally, we can restart the server.

If you change the Nginx server block configuration, test the configuration and then restart the Nginx process.

If you update your Django application, you can restart the Gunicorn process to pick up the changes.

```bash
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl restart gunicorn
```