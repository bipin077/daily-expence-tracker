from django import forms
from .models import Expence

class ExpenceForm(forms.ModelForm):
  class Meta:
    model = Expence
    fields = ["category_id", "expence", 'price', 'date']
    labels = {'category_id': "Expence Category", "expence": "Expence Detail",  "price": "Spend Amount",  "date": "Spend Date",}