from django.shortcuts import render
from events.models import Events, EventProviders, StateSuburbs
from django.http					import HttpResponse, JsonResponse


# Create your views here.
def event_registration(request):
    event_providers = EventProviders.objects.all()
    provider_list = {}
    for event_provider in event_providers:
        provider_list[event_provider.PID] = event_provider.name
    if request.method == "POST":
        print(request.POST)
        try:
            event_name = request.POST.get("q3_eventName")
            event_organiser = request.POST.get("q101_eventOrganiser")
            event_address = request.POST.get("q4_eventLocation")
            event_state = request.POST.get("q4_eventState")
            event_suburb = request.POST.get("q4_eventSuburb")
            event_date = request.POST.get("q4_eventDate")
            event_start = f'{event_date} {request.POST.get("q7_startTime[timeInput]")}'
            event_end = f'{event_date} {request.POST.get("q8_endTime[timeInput]")}'
            event_interests = request.POST.get("q9_keywordsrelevantInterests")
        except Exception as e:
            print(f"invalid registration {e}")
            return JsonResponse({"error": "invalid_request"})
        event_pid = EventProviders.objects.get(PID=int(event_organiser))
        event_ssid = StateSuburbs.objects.get(state=event_state, suburb=event_suburb)
        try:
            new_event = Events(name=event_name, PID=event_pid, address=event_address, SSID=event_ssid, start_time=event_start, end_time=event_end, description=event_interests)
            new_event.save()
        except Exception as e:
            print(f"save error {e}")
            return JsonResponse({"error": "save_error"})
    print(provider_list)
    return render(request, "eventRegistration.html", {"data": provider_list})

def organiser_registration(request):
    if request.method == "POST":
        print(request.POST)
        try:
            organiser_name = request.POST.get("q3_organiserName")
            organiser_email = request.POST.get("q6_email")
            organiser_phone = request.POST.get("q7_phoneNumber[full]")
            organiser_type = request.POST.get("q4_organiserType")
            organiser_state = request.POST.get("q8_stateterritory")
            organiser_suburb = request.POST.get("q9_suburb")
        except:
            pass
        organiser_location = StateSuburbs.objects.get(state=organiser_state, suburb=organiser_suburb)
        new_provider = EventProviders(name=organiser_name, org_type=organiser_type, email=organiser_email, phone=organiser_phone, location=organiser_location)
        new_provider.save()
    return render(request, "organiserRegistry.html")

def transport_provider_registration(request):
    return render(request, "TPR.html")
