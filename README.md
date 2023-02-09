
# CloSho - Clothing Store

E-commerce clothing store web app.

## Tech Stack

- Python
- Django
- Bootstrap
- PostgreSQL

## Run Locally

Clone the project

```
git clone https://github.com/ritik33/CloSho.git
```

Setup a PostgreSQL instance with the following data

```
DB NAME: 'closho',
USER: 'postgres',
PASSWORD: 'postgres',
HOST: 'localhost',
PORT': '5432'
```

OR update `settings.py` file with the following PostgreSQL configuration

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your postgres db name',
        'USER': 'your postgres db user',
        'PASSWORD': 'your postgres db password',
        'HOST': 'your postgres db host',
        'PORT': 'your postgres port',
    }
}
```

Create a virtual environment

```
pip install virtualenv

virtualenv venv
```

Activate the virtual environment

```
venv\scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

Apply migrations

```
python manage.py makemigrations

python manage.py migrate
```

Start the server

```
python manage.py runserver
```

> ⚠ Development server will start [here](http://127.0.0.1:8000/)

## Screenshots
![home](https://user-images.githubusercontent.com/54118809/217818836-1b53dc64-e092-46e5-9fd9-5aa66199a1ed.png) | ![wishlist](https://user-images.githubusercontent.com/54118809/217816260-7018dbf3-d011-4c81-9760-38af1d75b71a.png)
:---:|:---:
![product-detail](https://user-images.githubusercontent.com/54118809/217816284-03697a3f-3bd2-4ee3-b788-d7c9cb414f99.png) | ![cart](https://user-images.githubusercontent.com/54118809/217816337-f89b10fe-bdaa-4592-9d8c-7cc8abe82071.png)
![checkout](https://user-images.githubusercontent.com/54118809/217816301-69a5e9d5-dac9-47ad-a108-b60447c99aca.png) | ![payment](https://user-images.githubusercontent.com/54118809/217819753-cf136eff-4423-46c1-a52f-5904e193d1fa.png)
![profile](https://user-images.githubusercontent.com/54118809/217816354-c3980959-ce7b-4917-9e27-ed22f3936848.png)
