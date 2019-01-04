from django.db import models
from datetime import datetime, timedelta

from accounts.models import Trainer, Client

from django.utils import timezone
from accounts.tools import get_present_week




class SessionManager(models.Manager):
    def get_history_from_week(self, week):
        sessions = []
        for day in week:
            day_seshes = Session.objects.filter(date_time__month=day.month,
                                                date_time__day=day.day,
                                                date_time__year=day.year)

            sessions.append(day_seshes)
        return sessions






class WeekSessionManager(models.Manager):
    def get_queryset(self):

        # Get present week (pay period)

        week = get_present_week()

        # Create list of querysets of sessions per day in week

        this_weeks_sessions = []

        for day in week:
            day_sessions = Session.objects.filter(date_time__year=day.year,
                                                  date_time__month=day.month,
                                                  date_time__day=day.day)
            if day_sessions.count() == 0:
                continue
            this_weeks_sessions.append(day_sessions)



        # Merge those quersets into one queryset so it will be chainable

        return_queryset = Session.objects.none()

        for queryset in this_weeks_sessions:
            return_queryset = return_queryset | queryset

        return return_queryset



    def session_count(self):
        return Session.week.all().count()



    # THIS MAY ONLY WORK ON QUERSET AFTER IT HAS ALREADY BEEN FILTERED FOR CERTAIN TRAINER!!!!!!
        # it is currently treating all sessions like one and if they go over 80 all sessions will be billed at 15

    def dues(self):
        month_count = Session.month.session_count()
        week_count = Session.week.session_count()

        if month_count <= 80:
            dues = week_count * 20
        else:
            ot_sessions = month_count - 80
            undertime = 20 * (week_count - ot_sessions) # this needs a fix
            overtime = 15 * ot_sessions
            dues = undertime + overtime
        return dues







class MonthSessionManager(models.Manager):
    def get_queryset(self):
        today = datetime.today()
        month_sessions = Session.objects.filter(date_time__month=today.month, date_time__year=today.year)
        return month_sessions

    def session_count(self):
        return Session.month.all().count()


    def dues(self):
        session_count = Session.month.session_count()
        if session_count <= 80:
            dues = session_count * 20
        else:
            undertime = 80 * 20
            overtime = 15 * (session_count - 80)
            dues = undertime + overtime
        return dues




class YearSessionManager(models.Manager):
    pass






    # def get_sessions_from_trainer(self, trainer):
    #     trainer_sessions = Session.objects.filter(trainer=trainer).order_by('-datetime_served')
    #     return trainer_sessions







SESSION_TYPE_CHOICES = (
    ('Served', 'Served'),
    ('Burned', 'Burned'),
)

class Session(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    type = models.CharField(max_length=25, choices=SESSION_TYPE_CHOICES, blank=True, null=True)

    objects = SessionManager()
    week = WeekSessionManager()
    month = MonthSessionManager()

    def __str__(self):
        return self.trainer.get_full_name()