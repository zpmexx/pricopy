from django.utils import timezone
import datetime

from .models import BarInformations,OpeningHours, RealizationHours, RealizationStatus

def bar_informations(request):
    try:
        # w przyszłości albo będziemy wyciągać jeden, albo bedzie mogl byc tylko 1 obiekt danego modelu albo dodamy filter do wyboru, zaleznosci od potrzeby
        bar_informations = BarInformations.objects.all().first()
        return {'bar_informations' : bar_informations}
    except BarInformations.DoesNotExist:
        return None
    

# def opening_hours(request):
#     try:
#         opening_hours = OpeningHours.objects.all()
#         return {'opening_hours': opening_hours}
#     except OpeningHours.DoesNotExist:
#         return None
def realization_status(request):
    try:
        realization_status = RealizationStatus.objects.all().first()
        return {'realization_status' : realization_status}
    except RealizationStatus.DoesNotExist:
        return None

def opening_hours(request):
    try:
        opening_hours = OpeningHours.objects.all()
        if(len(opening_hours)) > 0:
            hours_from = []
            hours_to = []
            minutes_from = []
            minutes_to = []
            weekdays = []
            iterator = 0
            for day in opening_hours:
                hours_from.append(day.get_from_hour_hour())
                hours_to.append(day.get_to_hour_hour())
                minutes_from.append(day.get_from_hour_minute())
                minutes_to.append(day.get_to_hour_minute())
                weekdays.append(day.get_weekday())
                iterator+=1
            for i in range (0,len(minutes_from)):
                if minutes_from[i]<10:
                    minutes_from[i]="0"+str(minutes_from[i])
            for i in range (0,len(minutes_to)):
                if minutes_to[i]<10:
                    minutes_to[i]="0"+str(minutes_to[i])
            days = [[],[],[],[],[],[],[]]
            hours = [[],[],[],[],[],[],[]]
            days_iterator = 0
            days[days_iterator].append(weekdays[days_iterator])
            contact_time_from = f'{hours_from[days_iterator]}:{minutes_from[days_iterator]}'
            contact_time_to = f'{hours_to[days_iterator]}:{minutes_to[days_iterator]}'
            hours[days_iterator].append(contact_time_from)
            hours[days_iterator].append(contact_time_to)

            for i in range (1,len(weekdays)):
                if hours_from[i] == hours_from [i-1] and minutes_from[i] == minutes_from [i-1] and hours_to[i] == hours_to [i-1] and minutes_to[i] == minutes_to [i-1]:
                    if len(days[days_iterator]) < 2:
                        days[days_iterator].append(weekdays[i])
                    else:
                        days[days_iterator][1] = weekdays[i]
                else:
                    days_iterator += 1
                    days[days_iterator].append(weekdays[i])
                    contact_time_from = f'{hours_from[i]}:{minutes_from[i]}'
                    contact_time_to = f'{hours_to[i]}:{minutes_to[i]}'
                    hours[days_iterator].append(contact_time_from)
                    hours[days_iterator].append(contact_time_to)
        
            final_dictionary = {}
            for i in range (0,len(days)):
                if len(days[i]) == 1:
                    final_dictionary[days[i][0]] = f'{hours[i][0]} - {hours[i][1]}'
                elif len(days[i]) == 2:
                    final_dictionary[f'{days[i][0]} - {days[i][1]}'] = f'{hours[i][0]} - {hours[i][1]}'
            return {'final_dictionary': final_dictionary,
            'opening_hours' : opening_hours}
        else:
            return {'opening_hours': opening_hours}
    except OpeningHours.DoesNotExist:
        return None

def realization_hours(request):
    try:
        realization_hours = RealizationHours.objects.all()
        if(len(realization_hours)) > 0:
            hours_from = []
            hours_to = []
            minutes_from = []
            minutes_to = []
            weekdays = []
            iterator = 0
            for day in realization_hours:
                hours_from.append(day.get_from_hour_hour())
                hours_to.append(day.get_to_hour_hour())
                minutes_from.append(day.get_from_hour_minute())
                minutes_to.append(day.get_to_hour_minute())
                weekdays.append(day.get_weekday())
                iterator+=1
            for i in range (0,len(minutes_from)):
                if minutes_from[i]<10:
                    minutes_from[i]="0"+str(minutes_from[i])
            for i in range (0,len(minutes_to)):
                if minutes_to[i]<10:
                    minutes_to[i]="0"+str(minutes_to[i])
            days = [[],[],[],[],[],[],[]]
            hours = [[],[],[],[],[],[],[]]
            days_iterator = 0
            days[days_iterator].append(weekdays[days_iterator])
            contact_time_from = f'{hours_from[days_iterator]}:{minutes_from[days_iterator]}'
            contact_time_to = f'{hours_to[days_iterator]}:{minutes_to[days_iterator]}'
            hours[days_iterator].append(contact_time_from)
            hours[days_iterator].append(contact_time_to)

            for i in range (1,len(weekdays)):
                if hours_from[i] == hours_from [i-1] and minutes_from[i] == minutes_from [i-1] and hours_to[i] == hours_to [i-1] and minutes_to[i] == minutes_to [i-1]:
                    if len(days[days_iterator]) < 2:
                        days[days_iterator].append(weekdays[i])
                    else:
                        days[days_iterator][1] = weekdays[i]
                else:
                    days_iterator += 1
                    days[days_iterator].append(weekdays[i])
                    contact_time_from = f'{hours_from[i]}:{minutes_from[i]}'
                    contact_time_to = f'{hours_to[i]}:{minutes_to[i]}'
                    hours[days_iterator].append(contact_time_from)
                    hours[days_iterator].append(contact_time_to)
            final_dictionary = {}
            for i in range (0,len(days)):
                if len(days[i]) == 1:
                    final_dictionary[days[i][0]] = f'{hours[i][0]} - {hours[i][1]}'
                elif len(days[i]) == 2:
                    final_dictionary[f'{days[i][0]} - {days[i][1]}'] = f'{hours[i][0]} - {hours[i][1]}'
            return {'final_dictionary_realization_hours': final_dictionary,
            'realization_hours' : realization_hours}
        else:
            return {'realization_hours': realization_hours}
    except RealizationHours.DoesNotExist:
        return None

def getRestaurantStatus(request):
    try:
        realization_status = RealizationStatus.objects.all().first()
        today_date = timezone.now() # dziejsza data
        today_day = datetime.datetime.now().weekday() # dzisiejszy dzień
        today_realization_date = RealizationHours.objects.filter(weekday = today_day).first() # dzień z realizacji godzin
        final_realization_status = 1 #1 - mozliwosc zamawiania, 2 -brak
        final_realization_message = '' #wiadomośc zwrotna

        if realization_status == None:
            final_realization_status = 1
            final_realization_message = 'Brak danych o statusie, ale można zmawiać'
        elif realization_status.status == 3:
            final_realization_status = 2
            final_realization_message = realization_status.message
        elif realization_status.status == 2:
            if realization_status.from_date <= today_date <= realization_status.to_date:
                final_realization_status = 2 #brak możliwści zamawiania
                final_realization_message = realization_status.message
                final_realization_message += " Planowane otwarcie restauracji: " + realization_status.to_date.strftime('%Y-%m-%d %H:%M')
            else:
                final_realization_status = 1
                final_realization_message = 'Mimo statusu zamkneitego mozna zamawiac'
        else:
            if today_realization_date == None:
                final_realization_status = 2
                final_realization_message = 'Nie można zamawiać ponieważ na dzień dzisiejszy nie są skonfigurowane godziny realizacji zamówień'
            elif today_realization_date.status == 2:
                final_realization_status = 2
                final_realization_message = 'Restauracja jest dzisiaj zamknięta. Zapraszamy w inny dzień.'
            elif today_realization_date.from_hour <= today_date.time() <= today_realization_date.to_hour:
                final_realization_status = 1
                final_realization_message = 'Można zamawiać!'
            else:
                final_realization_status = 2
                final_realization_message = 'Obecnie dokonywanie zamówień jest niemożliwe, zapraszamy w godzinach pracy.'
        return {'final_realization_message_context': final_realization_message, 'final_realization_status_context': final_realization_status}
    except RealizationHours.DoesNotExist:
        return None
    except RealizationStatus.DoesNotExist:
        return None
