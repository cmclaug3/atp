from datetime import datetime, timedelta
from .models import Trainer




'''
Utility functions
'''




def cost_for_week(week_count, month_count):
    '''
    return cost for week taking for a trainer taking into account the 80 per month rule
    '''
    if month_count <= 80:
        dues = week_count * 20
    elif month_count - week_count > 80:
        dues = week_count * 15
    else:
        ot_sessions = month_count - 80
        undertime = 20 * (week_count - ot_sessions)  # this needs a fix
        overtime = 15 * ot_sessions
        dues = undertime + overtime
    return dues



def total_dues_for_week(week):
    trainers = Trainer.objects.filter(user__is_staff=False)
    week_dues_list_for_each_trainer = []

    for trainer in trainers:

        for day in week:
            trainer_week_count = Session.objects.filter(date_time__month=day.month,
                                   date_time__day=day.day,
                                   date_time__year=day.year).count()

            trainer_month_count = Session.objects.filter(date_time__month=day.month,
                                   date_time__year=day.year).count()

        week_dues_list_for_each_trainer.append(cost_for_week(trainer_week_count, trainer_month_count))
    return sum(week_dues_list_for_each_trainer)



def cost_for_month(month_count):
    '''
    return cost for month for a trainer taking into account the 80 per month rule
    '''
    if month_count <= 80:
        dues = month_count * 20
    else:
        undertime = 80 * 20
        overtime = 15 * (month_count - 80)
        dues = undertime + overtime
    return dues



def get_present_week(other_date=None):
    '''
    return list of 7 day week of current pay period (friday-thursday)
    optional argument other_date is a datetime day and will give the pay period that day falls in
    '''
    if other_date == None:
        today = datetime.today()
    else:
        today = other_date
    formatted_day = datetime(today.year, today.month, today.day)
    today_num = formatted_day.weekday()

    # Get friday of the given week (first day of pay period)

    if today_num == 4:
        starting_friday = formatted_day

    elif today_num < 4:
        starting_friday = formatted_day - timedelta(days=today_num + 3)

    elif today_num > 4:
        starting_friday = formatted_day - timedelta(days=today_num - 4)

    # Create list of 7 day week starting from that Friday

    week = []

    for week_days in range(7):
        week.append(starting_friday)
        starting_friday += timedelta(days=1)

    return week



# def get_all_weeks():
#     '''
#
#     list of days in particular week (pay period) for each week from earliest to most recent session
#
#     '''
#     earliest_session = Session.objects.all().order_by('date_time').first()
#     latest_session = Session.objects.all().order_by('date_time').last()
#
#     first_week = get_present_week(other_date=earliest_session.date_time)
#     last_week = get_present_week(other_date=latest_session.date_time)
#
#     friday_first_week = first_week[0]
#     friday_last_week = last_week[0]
#
#     weeks_list = []
#
#     while (friday_first_week.year, friday_first_week.month, friday_first_week.day) \
#             <= (friday_last_week.year, friday_last_week.month, friday_last_week.day):
#         weeks_list.append(get_present_week(other_date=friday_first_week))
#         friday_first_week += timedelta(days=7)
#
#     weeks_list.reverse()
#
#     return weeks_list


