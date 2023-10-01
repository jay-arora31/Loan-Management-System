from celery import shared_task
import pandas as pd
from .models import UserProfile

@shared_task
def calculate_credit_score(user_id):
    df=pd.read_csv('static/transactions_data_Backend.csv')
    sum_credit_transactions = df[(df['user'] == user_id) & (df['transaction_type'] == 'CREDIT')]['amount'].sum()
    sum_dedit_transactions = df[(df['user'] == user_id) & (df['transaction_type'] == 'DEBIT')]['amount'].sum()
    total_balance= abs( sum_credit_transactions-sum_dedit_transactions)
    if total_balance >= 1000000:
        credit_score= 900
    elif total_balance <= 100000:
        credit_score= 300
    else:
        credit_score=300 + (total_balance - 100000) // 15000 * 10
    user = UserProfile.objects.get(user_id=user_id)
    user.credit_score=credit_score
    user.save()
    return "Calculated successfully"

       
