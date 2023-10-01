
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
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/433d1b38-8af0-4397-b4da-c48a354a49e7)

The run this command in terminal

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
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/9e03ff82-bdb6-44be-8d9d-a8c90484ed53)

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
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/3cbc7407-30f1-4ff2-acd2-3e17b5ef40ce)
Credit Score Calculation
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/e044e391-3112-4aa6-b531-6b051b945e23)



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
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/17e0a974-35f2-48e2-8223-ad9d6e76e7d0)


## Make Payment  
### Endpoint
- **Endpoint**: `/api/make_payment/`
- **Method**: POST

I have change the current date to 2023-10-01 because this is the first emi date
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/21cc5899-fb99-4696-9aec-d1c85294ca36)

### Request Body (JSON)
```json
{
  "loan_id": 14,
  "amount": 10000.00
}

```

Output:
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/2545a525-6cc5-4c41-aa45-461b9236d435)


If i try to make payment again it will check in backend is there any emi due if not it will send this message
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/be63029f-8612-4a5e-8c95-44f3c03c33de)



## Get Statement
### Endpoint
- **Endpoint**: `/api/get_statement/`
- **Method**: POST

### Request Body (JSON)
```json
{
    "loan_id":14
}

```
Output
![image](https://github.com/jay-arora31/Loan-Management-System/assets/68243425/39dfcbc8-e357-4268-88c1-607c755c561a)



