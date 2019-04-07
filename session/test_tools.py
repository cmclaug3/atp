from accounts.models import User, PreSetAuthorizedUser, Trainer, Client
from .models import Session
import random
from datetime import datetime
from datetime import timedelta

from accounts.tools import get_present_week




RANDOM_SESSION_AMOUNT_HIGH = 480
START_DATE = datetime(2018, 1, 1)
END_DATE = datetime(2019, 3, 26)


def create_trainer_clients_list():
    '''

    Return a list of lists of a trainer (non-staff) followed by all of their clients

    '''
    trainer_client_list = []
    for trainer in Trainer.objects.filter(user__is_staff=False):
        client_list = list(Client.objects.filter(trainer=trainer))
        client_list.insert(0, trainer)
        trainer_client_list.append(client_list)
    return trainer_client_list


def random_date():
    '''

    Returns a random date between hard coded start and end dates above

    '''
    start = START_DATE
    end = END_DATE
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_sample_data():
    """

    Creates between 1-40 sessions at a random time for each client of each trainer

    """
    for trainer_clients in create_trainer_clients_list():
        trainer = trainer_clients[0]
        clients = trainer_clients[1:]
        for client in clients:
            random_sessions_amount = random.randrange(5, RANDOM_SESSION_AMOUNT_HIGH)
            for session in range(random_sessions_amount):
                sesh = Session.objects.create(trainer=trainer, client=client, date_time=random_date(), type="Served")
                sesh.save()
    return 'Just added a bunch of shit'



def get_all_weeks():
    '''

    list of days in particular week (pay period) for each week from earliest to most recent session

    '''


    earliest_session = Session.objects.all().order_by('date_time').first()
    latest_session = Session.objects.all().order_by('date_time').last()

    first_week = get_present_week(other_date=earliest_session.date_time)
    last_week = get_present_week(other_date=latest_session.date_time)

    friday_first_week = first_week[0]
    friday_last_week = last_week[0]

    weeks_list = []

    while (friday_first_week.year, friday_first_week.month, friday_first_week.day) \
            <= (friday_last_week.year, friday_last_week.month, friday_last_week.day):
        weeks_list.append(get_present_week(other_date=friday_first_week))
        friday_first_week += timedelta(days=7)

    weeks_list.reverse()

    return weeks_list


def get_history_from_week(week):
    '''

    all sessions from a particular week (list of 7 days in week/pay period)

    '''
    sessions = []
    for day in week:
        day_seshes = Session.objects.filter(date_time__month=day.month,
                                            date_time__day=day.day,
                                            date_time__year=day.year).order_by('date_time')

        sessions.append(day_seshes)
    return sessions

def get_final_session_count():
    weeks = get_all_weeks()
    count = 0
    for week in weeks:
        day_sessions = get_history_from_week(week)
        for day in day_sessions:
            count += len(day)
    return count














""""



login to site - overview

    example of what css does (html without it VS with it)
        
        
        
        
        
    ADMIN vs TRAINER Actions
        ADMIN
            add PreSetAuthorizedUsers (Django Admin)
            add new Clients for Trainer (Logged into main site)
        TRAINER
            Serve session with Client (Site)
            Add/edit Client Pin (Site)
        BOTH
            Change pin of logged in User (Site)
            
            
            
            
    What the Django admin is
        why its cool
        how Admins will use it (create PreSetAuthorizedUser)
        
        
        
        
    
    Add a new PreSetAuthorizedUser
        see result in admin login
        login as new Trainer
            no clients
        login as admin
            add client for new trainer
        login as new trainer
            set trainer pin
            set client pin
            serve session
            
            
            
    Things I am still planning to DO
    
        Get rid of Burn Session
    
        Add security question to Trainer and Client objects
            add further authorization for editing certain settings (Edit Pin, Client Pin)
            
        Finish Session History Log View
            ListView -> show table of weeks (pay periods) from earliest to present week Session stats
                friday-thursday date (link), total sessioned served, session tax total for week,
            DetailView -> table with trainers from that pay period with there respected Clients
                Trainer: sessions that week, payment that week, if overtime
                    Client: sessions that week,
                    
        Move current week variable to navbar
        
        Trainer/Client DetailView Session history table
            Only show current pay period with options to View last week/month/year/all
            
            
            
            
    QUESTIONS FOR ALVIN
    
        when i createsuperuser it doesnt create my first and last name i have to do that manually in the admin
        
        what to do with deployment
        
        background color for navarbar dropdown menu
        
        using html buttons for actions in templates
        
        
        
        
        
        
            

"""

