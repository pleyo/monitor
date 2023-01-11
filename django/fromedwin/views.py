from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

from projects.models import Project
from incidents.models import InstanceDownIncident

from django.templatetags.static import static

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.decorators.cache import never_cache

def public(request, id):
    """
    Show Public view of a project status
    """

    project = get_object_or_404(Project, pk=id)

    if not project.enable_public_page:
        raise Http404()

    number_days = 30

    start_date = timezone.now() - timezone.timedelta(days=number_days)
    incidents = InstanceDownIncident.objects.filter(service__project=project, startsAt__gte=start_date, severity=2)

    days = []
    for day in range(number_days):
        day = timezone.now() - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'incidents': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_enabled=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)).order_by('startsAt'),
            'outrage': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_enabled=True, service__is_critical=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
            'degradated': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_enabled=True, service__is_critical=False).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
        })

    return render(request, 'public.html', {
        'project': project,
        'services': project.services.filter(is_public=True, is_enabled=True),
        'incidents': incidents,
        'availability': {
            '1': project.availability(days=1),
            '7': project.availability(days=7),
            '30': project.availability(days=30),
        },
        'days': days,
        'days_reverses': reversed(days),
    })

@never_cache
def badge(request, id):
    """
    Show Public view of a project status
    """

    project = get_object_or_404(Project, pk=id)

    if not project.enable_public_page:
        file = 'badge-disabled.svg'
    elif project.is_offline():
        file = 'badge-offline.svg'
    elif project.is_warning():
        file = 'badge-degraded.svg'
    else:
        file = 'badge-online.svg'
    
    # path will look like /this/project/path/monitor/fromedwin
    path = str(Path(__file__).resolve().parent) 
    image_data = open(f'{path}/static/badges/{file}', mode='r').read()

    return HttpResponse(image_data, content_type="image/svg+xml")


def restricted(request):
    return render(request, 'restricted.html', {
    })
