from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from .forms import ExpenceForm
from .models import ExpenceCategory, Expence, ExpenceMaster

def home(request):
    from_date = datetime.today().strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')
    if 'from_date' in request.GET and 'to_date' in request.GET:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']

    today_expences = Expence.objects.filter(date__range=(from_date, to_date)).order_by('date')
    expence_cateories = ExpenceCategory.objects.filter()

    total_expence = 0
    for expence in today_expences:
        total_expence += expence.price

    form = ExpenceForm()

    expence_master = ExpenceMaster.objects.get()

    params = { 'today_expences' : today_expences, 'total_expence' : total_expence, 'from_date' : from_date, 'to_date' : to_date, 'expence_cateories' : expence_cateories, 'form' : form, 'expence_master' : expence_master }

    return render(request, 'expence_tracker/index.html', params)

def bar_chart(request):
    from_date = datetime.today().strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')
    if 'from_date' in request.GET and 'to_date' in request.GET:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']

    expence_cateories = ExpenceCategory.objects.filter()
    expence_total = Expence.objects.filter(date__range=(from_date, to_date))
    labels = []
    for label in expence_cateories:
        labels.append(label.category)
    
    chartLabel = "Expence data Summary"
    chartdata = []

    for label in expence_cateories:
        total_expence = 0
        for expence in expence_total:
            if label.category == expence.category_id.category:
                total_expence += expence.price
        chartdata.append(total_expence)

    data = { "labels":labels, "chartLabel":chartLabel, "chartdata":chartdata, 'from_date' : from_date, 'to_date' : to_date} 
    return JsonResponse(data)

def add_new_expence(request):
    if request.method == "POST":
        form = ExpenceForm(request.POST)  # Initialize the form with request data
        if form.is_valid():
            form.save()  # Save the form to create a new Expence instance
            return redirect('home')  # Redirect to the 'home' page after successfully adding a new expense
    else:
        form = ExpenceForm()

    return render(request, 'expence_tracker/index.html', {'form': form, 'msg' : 'Expence Added Successfully'})

def calculate_expence_reward(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    expence_master = ExpenceMaster.objects.get()
    reward_cal_till = expence_master.reward_calculated_till

    if str(today_date) == str(reward_cal_till):
        return redirect('home')

    expence_total = Expence.objects.filter(date__range=(reward_cal_till, today_date)).order_by('date')

    reward_price = expence_master.current_expence_amount
    expence_price = 0
    for expence in expence_total:
        if str(reward_cal_till) != str(expence.date):
            if int(expence_master.expence_limit_per_day) > int(expence_price):
                reward_price = int(reward_price) - int(expence_master.reward_price)
            else:
                reward_price = int(reward_price) - int(expence_master.reward_price)

            reward_cal_till = expence.date
            expence_price = 0

        else:
            expence_price += int(reward_price)

    master = ExpenceMaster.objects.get(id=expence_master.id)
    master.current_expence_amount = reward_price
    master.reward_calculated_till = reward_cal_till

    master.save()

    return redirect('home')

        


    