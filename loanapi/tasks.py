from celery import shared_task
import pandas as pd
from .models import UserProfile

@shared_task
def calculate_credit_score(user_id):
    df = pd.read_csv("transactions_data_Backend.csv")
    sum_credit_transactions = df[(df['user'] == user_id) & (df['transaction_type'] == 'CREDIT')]['amount'].sum()
    sum_dedit_transactions = df[(df['user'] == user_id) & (df['transaction_type'] == 'DEBIT')]['amount'].sum()
    total_balance= abs( sum_credit_transactions-sum_dedit_transactions)
    thresholds = [(100000, 15000), (1000000, 0)]
    credit_score = 300
    for threshold, increment in thresholds:
        if total_balance >= threshold:
            credit_score += (total_balance - threshold) // 15000 * 10
            break
    user = UserProfile.objects.get(user_id=user_id)
    user.credit_score=min(900, credit_score)
    user.save()
    return "Calculated successfully"

       
