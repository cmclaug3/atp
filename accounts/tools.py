from datetime import datetime, timedelta



'''
Utility functions
'''




def cost_for_week(week_count, month_count):
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


def cost_for_month(month_count):
    if month_count <= 80:
        dues = month_count * 20
    else:
        undertime = 80 * 20
        overtime = 15 * (month_count - 80)
        dues = undertime + overtime
    return dues



def get_present_week(other_date=None):
    if other_date == None:
        today = datetime.today()
    else:
        today = other_date
    today_num = today.weekday()

    # Get friday of the given week (first day of pay period)

    if today_num == 4:
        starting_friday = today

    elif today_num < 4:
        starting_friday = today - timedelta(days=today_num + 3)

    elif today_num > 4:
        starting_friday = today - timedelta(days=today_num - 4)

    # Create list of 7 day week starting for that Monday

    week = []

    for week_days in range(7):
        week.append(starting_friday)
        starting_friday += timedelta(days=1)

    return week


