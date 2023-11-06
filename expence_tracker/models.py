from django.db import models

class ExpenceCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Expence(models.Model):
    category_id = models.ForeignKey(ExpenceCategory, on_delete=models.CASCADE)
    expence = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return "date - %s, spend on - %s, price - Rs. %s" %(self.date,  self.expence, self.price)

class ExpenceMaster(models.Model):
    expence_limit_per_day = models.CharField(max_length=50, default=0)
    expence_limit_per_month = models.CharField(max_length=50)
    current_expence_amount = models.CharField(max_length=50)
    reward_price = models.IntegerField()
    reward_calculated_till = models.DateField()