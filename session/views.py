from django.shortcuts import render, redirect
from django.views import View
from .forms import ServeSessionForm, BurnSessionForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from accounts.models import Trainer, Client
from .models import Session

from datetime import datetime
from django.utils import timezone

from .test_tools import get_all_weeks, get_present_week








class ServeSessionView(View):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        date_time = timezone.now()
        context = {
            'client': client,
            'trainer': Trainer.objects.get(user=request.user),
            'form': ServeSessionForm(),
            'datetime': date_time
        }
        return render(request, 'serve_session.html', context)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        form = ServeSessionForm(request.POST)
        trainer = Trainer.objects.get(user=request.user)
        datetime = timezone.now()

        all_weeks = get_all_weeks()


        if not form.is_valid():
            context = {
                'client': client,
                'trainer': trainer,
                'form': form,
                'datetime': datetime
            }
            return render(request, 'serve_session.html', context)

        # date = form.cleaned_data['date']
        trainer_pin = form.cleaned_data['trainer_pin']
        client_pin = form.cleaned_data['client_pin']

        if trainer_pin == trainer.pin:

            if client_pin == client.pin:
                new_session = Session.objects.create(trainer=trainer, client=client, type='Served')
                new_session.date_time = timezone.now()
                # present_week = get_present_week(new_session.date_time)
                # index = all_weeks.index(present_week)
                # new_session.week = index



                messages.add_message(request, messages.SUCCESS, 'You have successfully served a session with {}'.format(client.first_name))
                return redirect(reverse('home'))
            else:
                messages.add_message(request, messages.ERROR, 'Client pin is incorrect')
                return redirect(reverse('serve_session', kwargs={'client_id': client.id}))

        else:
            messages.add_message(request, messages.ERROR, 'Trainer pin is incorrect')
            return redirect(reverse('serve_session', kwargs={'client_id': client.id}))





class BurnSessionView(View):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        context = {
            'client': client,
            'trainer': Trainer.objects.get(user=request.user),
            'form': BurnSessionForm()
        }
        return render(request, 'burn_session.html', context)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        form = BurnSessionForm(request.POST)
        trainer = Trainer.objects.get(user=request.user)
        if not form.is_valid():
            context = {
                'client': client,
                'trainer': trainer,
                'form': form
            }
            return render(request, 'burn_session.html', context)

        # date = form.cleaned_data['date']
        trainer_pin = form.cleaned_data['trainer_pin']
        confirmation = form.cleaned_data['confirmation']


        if confirmation == True:

            if trainer_pin == trainer.pin:
                print('trainer pin is correct')
                new_session = Session.objects.create(trainer=trainer, client=client, type='Burned')
                sesh = new_session.save(commit=False)
                sesh.date_time = timezone.now()
                sesh.save()
                messages.add_message(request, messages.SUCCESS, 'You have burned a session from {}'.format(client.first_name))
                return redirect(reverse('home'))
            else:
                print('trainer pin is incorrect')
                messages.add_message(request, messages.ERROR, 'Trainer pin is incorrect')
                return redirect(reverse('serve_session', kwargs={'client_id': client.id}))
        else:
            messages.add_message(request, messages.ERROR, 'You need to check the confirm box to proceed')
            return redirect(reverse('serve_session', kwargs={'client_id': client.id}))


