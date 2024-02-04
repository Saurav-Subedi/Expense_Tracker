from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.

import os
import json
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from .models import UserPreference
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required(login_url='/authentication/login')
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'expense', 'currencies.json')

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            currency_data = [{'name': k, 'value': v} for k, v in data.items()]
    except FileNotFoundError:
        messages.error(request, 'FileNotFoundError: currencies.json not found.')

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    elif request.method == 'POST':
        currency = request.POST.get('currency')

        if currency:
            if exists:
                user_preferences.currency = currency
                user_preferences.save()
            else:
                UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Changes saved')
        else:
            messages.error(request, 'Invalid currency selection.')

        return HttpResponseRedirect('/preferences/')  # Redirect to avoid form resubmission

