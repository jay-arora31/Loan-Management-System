
# Backend Problem Statement : Loan Management System


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
├── static/
│   ├── transactions_data_Backend.csv
├── manage.py
├── requirements.txt
├── README.md

```

<h2>Setup :</h2>

Clone the repository to your local machine:
```sh
$ git clone https://github.com/jay-arora31/Loan-Management-System.git
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

After Installing redis go to this path
```sh
C:\Program Files\Redis
```
Double click redis_cli
![image](https://github.com/jay-arora31/book/assets/68243425/8108a171-2de8-4349-8d53-cbe7faa43afc)

Then run this command in terminal

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
Open a new terminal and run this command

```sh
celery -A loanmain.celery worker --pool=solo -l info
```
![image](https://github.com/jay-arora31/book/assets/68243425/6e8f9a0e-b84c-4711-a794-5c2c9fdbbedc)

This API provides endpoints to manage user registration, loan applications, loan payments, and retrieve loan statements.
# System API Contracts

## Register User
### Endpoint
- **Endpoint**: `/api/register_user/`
- **Method**: POST

### Request Body (JSON)
```json
{
  "name": "jay",
  "email": "jay@gmail.com",
  "annual_income": 600000,
  "user_id": "f5abc955-889d-4a17-87b9-45b362eb673b"
}

```
Output:
![image](https://github.com/jay-arora31/book/assets/68243425/f9a02b41-eb94-4b5d-9b71-1247db0fc0a1)

Credit Score Calculation
![image](https://github.com/jay-arora31/book/assets/68243425/7cacd512-778b-4cf8-9244-e3f1384220cf)



## Apply Loan
### Endpoint
- **Endpoint**: `/api/apply_loan/`
- **Method**: POST

### Request Body (JSON)
```json
{
  "user_id": "f5abc955-889d-4a17-87b9-45b362eb673b",
  "loan_type": "Car",
  "loan_amount": 500000,
  "interest_rate": 15,
  "term_period": 50,
  "disbursement_date": "2023-9-15"
}

```
Output:
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/89383307-b16c-452d-84c6-1aa30129a4fd)


## Make Payment  
### Endpoint
- **Endpoint**: `/api/make_payment/`
- **Method**: POST

I have change the current date to 2023-10-01 because this is the first emi date
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/95c90374-0d68-4508-a302-c75e15f85cff)

### Request Body (JSON)
```json
{
  "loan_id": 16,
  "amount": 10490.00
}

```
Emi amount is 10000 but I have paid 10490 so it will recalculate and update the amount of upcoming emi's
Output:
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/4f0a18d8-0de5-42e7-8ab7-7fc5551b9502)


If I try to make payment again, it will check in backend if there any emi due. If not, it will send below message
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/737930bf-4735-454e-b849-05769f615b53)



## Get Statement
### Endpoint
- **Endpoint**: `/api/get_statement/`
- **Method**: POST

### Request Body (JSON)
```json
{
    "loan_id":16
}

```
Output
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/12bcdf67-4471-401a-93fd-a282f4e26881)



