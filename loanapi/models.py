from django.db import models
from datetime import date, timedelta

# Create your models here.
import uuid


# Create your models here.
class UserProfile(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField(default=0,blank=True,null=True)


class LoanApplication(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=[('Car', 'Car'), ('Home', 'Home'), ('Education', 'Education'), ('Personal', 'Personal')])
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.PositiveIntegerField()
    disbursement_date = models.DateField()
    emi_start_date = models.DateField()
    last_emi_payment_date= models.DateField(null=True,blank=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)


class EMI(models.Model):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='emis')
    actual_emi_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    # Add more fields as needed

    def __str__(self):
        return f"EMI for Loan {self.loan.id} on {self.actual_emi_date}"


class Payment(models.Model):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(auto_now_add=True)
    late_payment = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Payment of {self.amount} on {self.payment_date} for Loan {self.loan_id}"