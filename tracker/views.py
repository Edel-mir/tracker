from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import Expense, Tag
from .forms import NewExpenseForm, NewTagForm, NewUserForm


@login_required
def listPage(request, expenses=None):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = NewExpenseForm(user, request.POST)
        if form.is_valid():
            ex = form.save(commit=False)
            ex.user = request.user
            ex.save()
        return redirect('/')
    else:
        expenses = Expense.objects \
            .filter(user=request.user).select_related('tag').order_by('-date')
        form = NewExpenseForm(request.user)

        return render(request, 'tracker/list.html', {
            'forms': {'expence': form}, 'expences': expenses
        })


@login_required
def statisticPage(request):
    today = timezone.now()
    month = timezone.now() - timezone.timedelta(weeks=4)

    dayLabels = []
    dayData = []

    monthLabels = []
    monthData = []

    tags = Tag.objects.filter(user=request.user)
    for tag in tags:
        dayLabels.append(tag.name)
        monthLabels.append(tag.name)
        dayAmount = 0
        monthAmount = 0
        for e in Expense.objects.filter(user=request.user, type='Расход', date__exact=today, tag__exact=tag):
            dayAmount += e.amount
        dayData.append(dayAmount)

        for e in Expense.objects.filter(user=request.user, type='Расход', date__gte=month, tag__exact=tag):
            monthAmount += e.amount
        monthData.append(monthAmount)

    return render(request, 'tracker/statistic.html', {'dayLabels': dayLabels, 'dayData': dayData, 'monthLabels': monthLabels, 'monthData': monthData})


class Login(LoginView):
    template_name = 'tracker/login.html'


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    return render(request, 'tracker/register.html')
