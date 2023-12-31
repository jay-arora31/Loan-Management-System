from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta,date
from .models import UserProfile,EMI,LoanApplication
from .tasks import calculate_credit_score
from .serializers import LoanApplicationSerializer
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.utils.dateparse import parse_date
import pandas as pd
@api_view(['POST'])


def register_user(request):
    name = request.data.get('name')
    email = request.data.get('email')
    annual_income = request.data.get('annual_income')
    user_id = request.data.get('user_id')
    df = pd.read_csv('static/transactions_data_Backend.csv')
    user = UserProfile.objects.create(
        name=name,
        email=email,
        annual_income=annual_income,
        user_id=user_id
    )
    if user:
        calculate_credit_score.delay(user_id)
    return Response({'Error':None,'User Id ': user_id})


@api_view(['POST'])
def apply_loan(request):
    # Extract data from the request
    user_id = request.data.get('user_id')
    loan_type = request.data.get('loan_type')
    loan_amount = request.data.get('loan_amount')
    interest_rate = request.data.get('interest_rate')
    term_period = request.data.get('term_period')
    disbursement_date = parse_date(request.data.get('disbursement_date'))

    # Check if the user exists
    user = UserProfile.objects.filter(user_id=user_id).first()
    if not user:
        return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check credit score and income requirements
    if user.credit_score < 450:
        return Response({'error': 'User does not meet credit score requirements.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.annual_income < 150000:
        return Response({'error': 'User income is below the minimum required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check loan amount bounds
    max_loan_amounts = {
        'Car': 750000,
        'Home': 8500000,
        'Education': 5000000,
        'Personal': 1000000,
    }

    if loan_type not in max_loan_amounts:
        return Response({'error': 'Invalid loan type.'}, status=status.HTTP_400_BAD_REQUEST)

    if loan_amount > max_loan_amounts[loan_type]:
        return Response({'error': 'Loan amount exceeds the maximum allowed.'}, status=status.HTTP_400_BAD_REQUEST)

    total_interest = (loan_amount * interest_rate * term_period) / (12 * 100)

    # Calculate emi_start_date as the last day of the month of disbursement_date
    nextmonth = disbursement_date.replace(day=1) + timedelta(days=32) # Start with the first day of disbursement_date
    emi_start_date = datetime(nextmonth.year, nextmonth.month, 1)
    loan_data = {
        'user': user.id,
        'loan_type': loan_type,
        'loan_amount': loan_amount,
        'interest_rate': interest_rate,
        'term_period': term_period,
        'disbursement_date': disbursement_date,
        'emi_start_date': emi_start_date.date(),
        'total_interest': total_interest,
        'is_approved': True  
    }

    serializer = LoanApplicationSerializer(data=loan_data)

    if serializer.is_valid():
        loan_application = serializer.save()

        # Calculate and save EMI records
        emi_amount = loan_amount / term_period
        emi_data = []

        for _ in range(term_period):
            emi = EMI(
                loan=loan_application,
                actual_emi_date=emi_start_date.date(),
                amount_due=emi_amount
            )
            emi_data.append(emi)
            emi_start_date += relativedelta(months=1)

        EMI.objects.bulk_create(emi_data)

        return Response({
            'Loan_id': loan_application.id,
            'Due_dates': [{'Date': emi.actual_emi_date, 'Amount_due': emi.amount_due} for emi in emi_data]
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_payment(request):
    loan_id = request.data.get('loan_id')
    amount_paid = Decimal(request.data.get('amount'))

    # Check if the loan exists
    loan = LoanApplication.objects.filter(id=loan_id).first()
    if not loan:
        return Response({'error': 'Loan does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    current_date =date.today()

    due_emis = EMI.objects.filter(loan=loan, actual_emi_date__lte=current_date, is_paid=True).order_by('actual_emi_date').first()
    if due_emis:
        return Response({'error': 'No Due is Pending'})
    else: 
        due_emis = EMI.objects.filter(loan=loan, actual_emi_date=current_date, is_paid=False).order_by('actual_emi_date')
        for i in due_emis:
            if i.actual_emi_date>current_date:
                break
            if i.actual_emi_date==current_date and i.is_paid==False:
                i.is_paid=True
                i.amount_paid=amount_paid
                i.payment_date=current_date
                i.save()
                if amount_paid<i.amount_due or amount_paid>i.amount_due:
                    due_emis = EMI.objects.filter(loan=loan, actual_emi_date__gt=i.actual_emi_date, is_paid=False).order_by('actual_emi_date')
                    due_count=due_emis.count()
                    amount_diff=(i.amount_due-amount_paid)/due_count
                    for k in due_emis:
                        if amount_paid<i.amount_due:
                            k.amount_due-=amount_diff
                        else:
                            k.amount_due+=amount_diff

                        next_emi=k.amount_due
                        k.save()
                    if amount_paid<i.amount_due:
                        return Response({'error':None,'message': 'Current Month Emi is Successfully Paid But You have Paid Less than the Due Amount'})
                    else:
                        return Response({'error':None,'message': 'Current Month Emi is Successfully Paid But You have Paid Greater than the Due Amount'})
                return Response({'error':None,'message': 'Current Month Emi is Successfully Paid'})
        due_emis = EMI.objects.filter(loan=loan, actual_emi_date__lt=current_date, is_paid=False).order_by('actual_emi_date')
        due_count=due_emis.count()
        for j in due_emis:
            if j.actual_emi_date<current_date and j.is_paid==False:
                j.is_paid=True
                j.amount_paid=amount_paid
                j.payment_date=current_date
                j.save()
                if amount_paid<j.amount_due or amount_paid>j.amount_due:
                    due_emis = EMI.objects.filter(loan=loan, actual_emi_date__gt=j.actual_emi_date, is_paid=False).order_by('actual_emi_date')
                    due_count=due_emis.count()
                    amount_diff=(j.amount_due-amount_paid)/due_count
                    for k in due_emis:
                        if amount_paid<i.amount_due:
                            k.amount_due-=amount_diff
                        else:
                            k.amount_due+=amount_diff
                        next_emi=k.amount_due
                        k.save()
                    if  amount_paid<j.amount_due or amount_paid>j.amount_due:
                        return Response({'error':None,'message': 'Due Emi is paid and u have paid less amount than the due amount ','No of dues::':due_count,'Next emi amount is':next_emi})
                    else:
                        return Response({'error':None,'error': 'Due Emi is paid and u have paid greater amount than the due amoun','No of dues::':due_count,'Next emi amount is':next_emi})
                return Response({'error':None,'error': 'Due Emi is paid Successfully','no of dues::':due_count})
        
        return Response({'Error': 'Error'})    

@api_view(['GET'])
def get_statement(request):
    loan_id = request.query_params.get('loan_id')

    # Check if the loan exists
    loan = LoanApplication.objects.filter(id=loan_id).first()

    if not loan:
        return Response({'error': 'Loan does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        upcoming_due_emis = EMI.objects.filter(loan=loan,is_paid=False).order_by('actual_emi_date')
        past_due_emis = EMI.objects.filter(loan=loan,is_paid=True).order_by('actual_emi_date')
        upcoming_transaction=[]
        past_transaction=[]
        # getting data for upcoming_transaction
        for l in upcoming_due_emis:
            data={
                'Date':l.actual_emi_date,
                'Amount':l.amount_due
            }
            upcoming_transaction.append(data)
        amount_paid_total=0
        # getting data for past_transaction
        for o in past_due_emis:
            data={
                'Date':o.actual_emi_date,
                'Principal':o.loan.loan_amount,
                'Interest':str(o.loan.interest_rate)+str("%"),
                'Amount Due':o.amount_due,
                'Amount Paid':o.amount_paid
            }
            amount_paid_total+=o.amount_paid
            past_transaction.append(data)
        response_data = {
        'Error': None,
        'Past_transactions': past_transaction,
        'Upcoming_transactions': upcoming_transaction,
    }
    return Response(response_data, status=status.HTTP_200_OK)
