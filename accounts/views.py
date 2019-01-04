from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import PreSetAuthorizedUserForm, SetNewUserPasswordForm, CreateClientForm, SetPinForm
from accounts.models import PreSetAuthorizedUser, User, Trainer, Client
from session.models import Session
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from accounts.tools import cost_for_week, cost_for_month, get_present_week
from session.test_tools import get_all_weeks, get_history_from_week

from django.utils import timezone
from datetime import datetime




@login_required
def home(request):

    trainer = Trainer.objects.get(user=request.user)
    # clients = Client.objects.filter(trainer=trainer) always there
    total_sessions_served = Session.objects.filter(trainer=trainer).count()
    trainers = Trainer.objects.filter(user__is_staff=False)

    total_sessions_this_week = Session.week.all().count()
    total_sessions_this_month = Session.month.all().count()

    # Computing area

    trainer_scheme = []
    week_dues_list = []

    for trainer in trainers:
        trainer_week_count = Session.week.filter(trainer=trainer).count()
        trainer_month_count = Session.month.filter(trainer=trainer).count()
        scheme = [trainer, trainer_week_count, trainer_month_count]
        trainer_scheme.append(scheme)
        week_dues_list.append(cost_for_week(trainer_week_count, trainer_month_count))

    ################

    today = datetime.today()
    sessions_today = Session.objects.filter(date_time__month=today.month,
                                            date_time__day=today.day,
                                            date_time__year=today.year).count()

    pay_period = get_present_week()
    starting_friday = pay_period[0].strftime('%m/%d/%Y')
    ending_thursday = pay_period[6].strftime('%m/%d/%Y')



    context = {
        'user': request.user,
        'trainer': trainer,
        # 'clients': clients,
        'total_sessions_served': total_sessions_served,
        'trainers': trainers,

        'total_sessions_this_week': total_sessions_this_week,
        'total_sessions_this_month': total_sessions_this_month,

        'trainer_scheme': sorted(trainer_scheme, key=lambda x: x[1], reverse=True),
        'week_dues': sum(week_dues_list),

        'sessions_today': sessions_today,

        'starting_friday': starting_friday,
        'ending_thursday': ending_thursday
    }
    return render(request, 'home.html', context)






class RegisterAuthorizedUserView(View):

    def get(self, request):
        context = {
            'form': PreSetAuthorizedUserForm()
        }
        return render(request, 'register_authorized_user_form.html', context)

    def post(self, request):
        form = PreSetAuthorizedUserForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'register_authorized_user_form.html', context)

        first_name = form.cleaned_data['first_name'].capitalize()
        last_name = form.cleaned_data['last_name'].capitalize()
        email = form.cleaned_data['email']
        code = form.cleaned_data['code']

        try:
            correct_user = PreSetAuthorizedUser.objects.get(first_name=first_name,
                                                            last_name=last_name,
                                                            email=email,
                                                            code=code)

            # Registration may proceed (credentials are correct)
            type_of_user = correct_user.type

            if type_of_user == 'trainer':
                new_user = User.objects.create_user(email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)

            elif type_of_user == 'staff':
                new_user = User.objects.create_staff_user(email=email,
                                                          first_name=first_name,
                                                          last_name=last_name)

            messages.add_message(request, messages.SUCCESS, 'Awesome you are authorized to signup')
            return redirect(reverse('set_new_user_password', kwargs={'new_user_id': new_user.id}))

        except PreSetAuthorizedUser.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Incorrect Credentials, cannot register')
            return redirect(reverse('home'))

        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'You have already registered, please log in normally')
            return redirect(reverse('home'))





class SetNewUserPasswordView(View):

    def get(self, request, new_user_id):
        context = {
            'form': SetNewUserPasswordForm()
        }
        return render(request, 'set_new_user_password_form.html', context)

    def post(self, request, new_user_id):
        form = SetNewUserPasswordForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'set_new_user_password_form.html', context)

        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        new_user = User.objects.get(id=new_user_id)

        if password1 == password2:
            new_user.set_password(password1)
            new_user.save()

        else:
            messages.add_message(request, messages.ERROR, 'passwords do not match try again')
            return redirect(reverse('set_new_user_password', kwargs={'new_user_id': new_user.id}))


        # SAFETY NET TO MAKE NEW TRAINER FROM NEW USER DATA
        if new_user.is_admin == False:

            new_trainer = Trainer.objects.create(user=new_user)
            new_trainer.save()

        messages.add_message(request, messages.SUCCESS, 'password setup you can now log in normally from now on')
        return redirect(reverse('home'))




class SetPinView(View):
    def get(self, request):
        trainer = Trainer.objects.get(user=request.user)
        context = {
            'form': SetPinForm(),
            'trainer': trainer
        }
        return render(request, 'set_pin.html', context)

    def post(self, request):
        form = SetPinForm(request.POST)
        trainer = Trainer.objects.get(user=request.user)
        if not form.is_valid():
            context = {
                'form': form,
                'trainer': trainer
            }
            return render(request, 'set_pin.html', context)

        pin1 = form.cleaned_data['pin1']
        pin2 = form.cleaned_data['pin2']
        agree = form.cleaned_data['agree_to_use_as_signature']

        if agree == False:
            messages.add_message(request, messages.ERROR, 'You must check box to agree to use pin as signature to proceed')
            return redirect(reverse('set_pin'))

        if pin1.isdigit() and pin2.isdigit() == True:

            if len(pin1) and len(pin2) == 4:

                if pin1 == pin2:

                    # SUCCESS
                    trainer.pin = pin1
                    trainer.save()
                    messages.add_message(request, messages.SUCCESS, 'You have successfully Changed/Added your pin')
                    return redirect(reverse('home'))

                else:
                    messages.add_message(request, messages.ERROR, 'Pins do not match try again')
                    return redirect(reverse('set_pin'))

            else:
                messages.add_message(request, messages.ERROR, 'Pins must be 4 numbers long, try again')
                return redirect(reverse('set_pin'))

        else:
            messages.add_message(request, messages.ERROR, 'Pins must be all numerical characters try again')
            return redirect(reverse('set_pin'))




class CreateClientView(View):
    def get(self, request):
        form = CreateClientForm()
        context = {
            'form': form,
        }
        return render(request, 'create_client_view.html', context)

    def post(self, request):
        form = CreateClientForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'create_client_view.html', context)

        first_name = form.cleaned_data['first_name'].capitalize()
        last_name = form.cleaned_data['last_name'].capitalize()

        form.cleaned_data['first_name'] = first_name
        form.cleaned_data['last_name'] = last_name


        form.save()
        messages.add_message(request, messages.SUCCESS, 'You successfully added a cliernt')
        return redirect(reverse('home'))




class SetClientPinView(View):
    def get(self, request, client_id):
        trainer = Trainer.objects.get(user=request.user)
        client = Client.objects.get(id=client_id)
        context = {
            'form': SetPinForm(),
            'client': client,
            'trainer': trainer,
        }
        return render(request, 'set_pin.html', context)

    def post(self, request, client_id):
        form = SetPinForm(request.POST)
        trainer = Trainer.objects.get(user=request.user)
        client = Client.objects.get(id=client_id)
        if not form.is_valid():
            context = {
                'form': form,
                'client': client,
                'trainer': trainer,
            }
            return render(request, 'set_pin.html', context)

        pin1 = form.cleaned_data['pin1']
        pin2 = form.cleaned_data['pin2']
        agree = form.cleaned_data['agree_to_use_as_signature']

        client = Client.objects.get(id=client_id)

        if agree == False:
            messages.add_message(request, messages.ERROR, 'You must check box to agree to use pin as signature to proceed')
            return redirect(reverse('set_pin'))

        if pin1.isdigit() and pin2.isdigit() == True:

            if len(pin1) and len(pin2) == 4:

                if pin1 == pin2:

                    # SUCCESS
                    client.pin = pin1
                    client.save()
                    messages.add_message(request, messages.SUCCESS, '{} has successfully Changed/Added their pin'.format(client.first_name))
                    return redirect(reverse('home'))

                else:
                    messages.add_message(request, messages.ERROR, 'Pins do not match try again')
                    return redirect(reverse('set_client_pin', kwargs={'client_id': client_id}))

            else:

                messages.add_message(request, messages.ERROR, 'Pins must be 4 characters long try again')
                return redirect(reverse('set_client_pin', kwargs={'client_id': client_id}))

        else:
            messages.add_message(request, messages.ERROR, 'Pins must be all numerical characters try again')
            return redirect(reverse('set_client_pin', kwargs={'client_id': client.id}))





class ClientView(View):
    def get(self, request):
        trainers_clients = Client.objects.filter(trainer__user=request.user)

        clients_scheme = []

        for client in trainers_clients:
            client_week_count = Session.week.filter(client=client).count()
            client_month_count = Session.month.filter(client=client).count()
            scheme = [client, client_week_count, client_month_count]
            clients_scheme.append(scheme)

        context = {
            'trainers_clients': trainers_clients,

            'clients_scheme': clients_scheme
        }
        return render(request, 'clients.html', context)




class SingleClientView(View):
    def get(self, request, client_id):

        trainer = Trainer.objects.get(user=request.user)
        client = Client.objects.get(id=client_id)

        # Query for session history for Trainer by Trainer only with Specific client
        session_history = Session.objects.filter(trainer=trainer, client=client).order_by('-date_time')
        # Query for session history for Staff including ALL sessions regardless of trainer
        if request.user.is_staff == True:
            session_history = Session.objects.filter(client=client).order_by('-date_time')

        serviced_sessions = session_history.count()

        client_week_count = Session.week.filter(client=client).count()
        client_month_count = Session.month.filter(client=client).count()


        context = {
            'client': client,
            'session_history': session_history,
            'serviced_sessions': serviced_sessions,

            'client_week_count': client_week_count,
            'client_month_count': client_month_count
        }
        return render(request, 'single_client.html', context)




class TrainerView(View):
    def get(self, request):

        trainers = Trainer.objects.filter(user__is_staff=False)
        trainer_client_schemes = []

        for trainer in trainers:

            trainer_week_count = Session.week.filter(trainer=trainer).count()
            trainer_month_count = Session.month.filter(trainer=trainer).count()
            trainers_clients = Client.objects.filter(trainer=trainer)

            trainer_scheme = [trainer, trainer_week_count, trainer_month_count]
            clients_scheme = []

            for client in trainers_clients:
                client_week_count = Session.week.filter(client=client).count()
                client_month_count = Session.month.filter(client=client).count()
                scheme = [client, client_week_count, client_month_count]
                clients_scheme.append(scheme)

            clients_scheme.insert(0, trainer_scheme)
            trainer_client_schemes.append(clients_scheme)

        context = {
            'trainers': trainers,
            'trainer_client_schemes': trainer_client_schemes,
        }
        return render(request, 'trainers.html', context)




class SingleTrainerView(View):
    def get(self, request, trainer_id):

        trainer = Trainer.objects.get(id=trainer_id)
        trainers_clients = trainer.get_all_clients()
        all_sessions = Session.objects.filter(trainer=trainer).order_by('-date_time')

        this_week = Session.week.filter(trainer=trainer)
        this_week_count = this_week.count()

        this_month = Session.month.filter(trainer=trainer)
        this_month_count = this_month.count()

        pay_period = get_present_week()
        starting_friday = pay_period[0].strftime('%m/%d/%Y')
        ending_thursday = pay_period[6].strftime('%m/%d/%Y')

        context = {
            'trainer': trainer,
            'trainers_clients': trainers_clients,

            'all_sessions': all_sessions,

            'this_week': this_week,
            'this_week_count': this_week_count,

            'this_month': this_month,
            'this_month_count': this_month_count,

            'cost_for_week': cost_for_week(this_week_count, this_month_count),

            'starting_friday': starting_friday,
            'ending_thursday': ending_thursday


        }
        return render(request, 'single_trainer.html', context)




class AllWeeksView(View):
    def get(self, request):
        all_weeks = get_all_weeks()
        trainers = Trainer.objects.all().first().get_all_trainers()

        per_week_sessions = []

        for week in all_weeks:
            per_week_sessions.append([get_history_from_week(week=week)])



        context = {
            'all_weeks': all_weeks,
            'per_week_sessions': per_week_sessions,
        }
        return render(request, 'weeks_report.html', context)








