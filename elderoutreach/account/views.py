from django.shortcuts				import render
from django.http					import HttpResponse, JsonResponse
from django							import forms
from django.contrib.auth.forms		import UserCreationForm
from .forms							import RegisterForm
from django.contrib.auth			import get_user_model
from django.contrib.auth			import login
from django.contrib					import messages
from django.shortcuts				import redirect
from django.contrib.auth			import login, authenticate #add this
from django.contrib					import messages
from django.contrib.auth.forms		import AuthenticationForm
from rest_framework.parsers			import JSONParser
from rest_framework.views			import APIView
from rest_framework.response		import Response
from rest_framework.permissions		import IsAuthenticated
from django.views.decorators.csrf	import csrf_exempt
from django.http					import QueryDict
from requests import post
from json import loads
#from account.models import Contact, Message, UserInterests, Interests
#from account.serializers import ContactSerializer, MessageSerializer, UserInterestsSerializer
import sys

# Create your views here.
User = get_user_model()

ENDPOINT_BASE = "https://matthewhoffman.biz"
ENDPOINT_TOKEN = "/auth/token-request/"
ENDPOINT_DETAILS = "/push/api-push-user-details/"

HEADERS = {
    "Authorization": f"Token rpl_token"
}

def sessioncheck(request):
	return HttpResponse("SessionCheck")

def get_token(username, password):
    data = {"username": username, "password": password}
    response = post(f"{ENDPOINT_BASE}{ENDPOINT_TOKEN}", json=data)
    return response.text

def push_user_details(username, token, state, suburb, name, travel_dist):
	headers = HEADERS.copy()
	headers["Authorization"] = headers["Authorization"].replace("rpl_token", token)
	print(headers)
	data = {"username": username, "state": state, "suburb": suburb, "real_name": name, "travel_dist": f"{travel_dist}"}
	print(data)
	response = post(f"{ENDPOINT_BASE}{ENDPOINT_DETAILS}", headers=headers, data=data)
	return response.text


class APICreateAccount(APIView):
	def post(self, request):
		query_dict = QueryDict('', mutable = True)
		query_dict.update(request.POST)
		print(query_dict)
		register_form = RegisterForm(query_dict)
		error_list = [" ".join(item) for item in list(register_form.errors.values())]
		username = str(request.POST.get("username"))
		email = str(request.POST.get("email"))
		state = str(request.POST.get("state"))
		suburb = str(request.POST.get("suburb"))
		real_name = str(request.POST.get("real_name"))
		travel_dist = int(request.POST.get("travel_dist"))
		password = request.POST.get("password1")
		# Unsure what to do with this tho
		if username != email and username is not None and email is not None:
			error_list.append(f"Emails specified did not match: '{username}' and '{email}'")
		if not register_form.is_valid() or error_list != []:#note (cooper): just going to return the first error for simplicity
			content = {"status": "failure", "messages": f"{error_list[0]}"}
			return Response(content)
		register_form.save()
		messages.success(request, "User successfuly created.")
		user_token = loads(get_token(username, password))
		print(user_token)
		detail_response = loads(push_user_details(username, user_token["token"], state, suburb, real_name, travel_dist))
		return Response(detail_response)

	def get(self, request):
		content = {"status": "get_not_allowed"}
		return Response(content)

def create(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			print("Valid my dude")
			form.save()
			messages.success(request, 'Account created successfully')
			return redirect('create')
		print("Invalid my dude")
		print(f.errors, file = sys.stderr)
	else:
		form = RegisterForm()
	return render(request, 'main/registration.html', {'form': form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request = request, template_name = "main/success.html")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request = request, template_name = "main/login.html", context = {"login_form":form})

