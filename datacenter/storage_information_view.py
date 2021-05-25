import django
from django.shortcuts import render
from datacenter.models import Passcard
from datacenter.models import Visit


# import datetime


def format_duration(duration):
    '''
    Превращает длительность визита в строку, готовит к выводу на страницу.
    '''
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f'{int(hours)}ч {int(minutes)}мин'


def storage_information_view(request):
    not_leaved = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for visit in not_leaved:
        passcard = visit.passcard
        entered_at_utc = visit.entered_at
        entered_at = django.utils.timezone.localtime(entered_at_utc)
        duration = visit.get_duration()
        formatted_duration = format_duration(duration)

        non_closed_visits.append(
            {
                "who_entered": passcard.owner_name,
                "entered_at": entered_at,
                "duration": formatted_duration,
                "is_strange": visit.is_long() 
            }
        )

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
