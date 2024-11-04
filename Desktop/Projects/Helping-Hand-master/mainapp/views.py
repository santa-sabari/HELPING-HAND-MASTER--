from django.shortcuts import render, redirect
from mainapp.models import Event
from django.contrib.auth.decorators import login_required

def home_page(request):
    id = request.GET.get('id')
    events = Event.objects.all()
    events_food = events.filter(event_type='Food')
    events_clothes = events.filter(event_type='Clothes')
    events_medical = events.filter(event_type='Medical')
    events_other = events.filter(event_type='Other')

    user = request.user if request.user.is_authenticated else None

    if user and id:
        event = Event.objects.filter(id=id).first()
        if event:
            if user in event.interested.all():
                event.interested.remove(user)
            else:
                event.interested.add(user)
            event.save()

    for event in events:
        event.is_interested = user in event.interested.all() if user else False

    context = {
        'events': events,
        'events_clothes': events_clothes,
        'events_food': events_food,
        'events_medical': events_medical,
        'events_other': events_other,
        'user': user,
    }

    return render(request, 'mainapp/home.html', context)

@login_required
def create_event(request):
    if request.method == 'POST':
        event_organizer = request.POST.get('event_organizer')
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        place_name = request.POST.get('place_name')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')

        event = Event(
            event_organizer=event_organizer,
            event_name=event_name,
            event_date=event_date,
            description=description,
            place_name=place_name,
            event_type=event_type,
            lat=lat,
            lon=lon
        )
        event.save()
        return redirect('mainapp:home_page')

    return render(request, 'mainapp/create_event.html')
