
# Backend Problem Statement : Loan Management System

# Elevator System Project Structure

```plaintext
loanmain/
│
├── loanapi/
│   ├── migrations/
│   ├── admin.py
│   ├── app.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│
├── loanmain/
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│  
├── manage.py
├── requirements.txt
├── README.md

```

<h2>Setup :</h2>

Clone the repository to your local machine:
```sh
$ git clone https://github.com/jay-arora31/Elevator-Challenge.git
$ cd loanmain
```
Install the required dependencies:
```sh
$ virtualenv venv


```
```sh
$ venv\scripts\activate


```
```sh
$ pip install -r requirements.txt


```
Download Redis

https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.msi

After Installing Run ping in redis terminal
```sh

$ ping


```
Apply database migrations:
```sh
$ python manage.py migrate


```

Start the development server:
```sh
$ python manage.py runserver


```

This API provides endpoints to manage user registration, loan applications, loan payments, and retrieve loan statements.

## Register User
### Endpoint
- **Endpoint**: `/api/register_user/`
- **Method**: POST

### Request Body (JSON)
```json
{
  "name": "jay",
  "email": "jay@gmail.com",
  "annual_income": 60000,
  "user_id": "f5abc955-889d-4a17-87b9-45b362eb673b"
}
