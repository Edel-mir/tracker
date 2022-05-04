import profile
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from django.views import View as BaseView
from .models import Expense, Profile, Tag
from .forms import NewExpenseForm, NewTagForm, NewUserForm


class ExpenseListCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        all_exp = Expense.objects.filter(
            user=request.user).select_related('tag').order_by('-date')
        all_tag = Tag.objects.filter(user=request.user)
        return render(request, "tracker/list.html", {"all_exp": all_exp, "all_tag": all_tag})

    def post(self, request, *args, **kwargs):
        user = request.user
        type = request.POST.get('type', None)
        tag = request.POST.get('tag', None)
        amount = request.POST.get('amount', None)
        date = request.POST.get('date', None)
        description = request.POST.get('description', '')
        profile = Profile.objects.get(user=user)
        if type == 'Доход':
            if amount and date:
                exp = Expense.objects.create(
                    user=user, type=type, amount=amount, date=date, description=description)
                profile.income += int(amount)
                profile.save()
                return redirect('listPage')
        else:
            if tag and amount and date:
                tag, isCreated = Tag.objects.get_or_create(user=user, name=tag)
                exp = Expense.objects.create(
                    user=user, type=type, tag=tag, amount=amount, date=date, description=description)
                exp.save()
                profile.outcome += int(amount)
                profile.save()
                return redirect('listPage')


@login_required
def ExpenseDeleteView(request, pk):
    if pk:
        expense = Expense.objects.get(pk=pk)
        if expense:
            expense.delete()
            return redirect('listPage')


@login_required
def ExpenseEditPage(request, pk):
    expense = Expense.objects.filter(pk).select_related('tag')
    return render(request, 'tracker/list.html')


@login_required
def StatisticPage(request):
    today = timezone.now()
    month = timezone.now() - timezone.timedelta(weeks=4)

    dayLabels = []
    dayData = []

    monthLabels = []
    monthData = []

    tags = Tag.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
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

    return render(request, 'tracker/statistic.html', {'dayLabels': dayLabels, 'dayData': dayData, 'monthLabels': monthLabels, 'monthData': monthData, 'profile': profile})


class Login(LoginView):
    template_name = 'tracker/login.html'


def RegisterView(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    return render(request, 'tracker/register.html')
