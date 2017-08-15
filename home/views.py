from django.shortcuts import render, get_object_or_404, redirect
from .models import GuestDetails


def home(request):
    if 'username' in request.session:
        return render(request, 'home.html', {'name': request.session['username']})
    return render(request, 'home.html')


def login(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if '@' in str(user_name):
            record = get_object_or_404(GuestDetails, email=user_name)
        else:
            record = get_object_or_404(GuestDetails, user_name=user_name)
        if password == record.password:
            request.session['username'] = record.first_name+" "+record.last_name
            request.session['user_id'] = record.email
            return redirect('home')
        else:
            return render(request, 'login.html', {'message': 'User id or password is incorrect'})
    return render(request, 'login.html')


def signup(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address1') + "," + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        adhaar_no = request.POST.get('adhaar_no')

        try:
            record = GuestDetails.objects.get(email=str(email))
            return render(request, 'signup.html', {'message': 'Email already exists. Please login to continue'})
        except GuestDetails.DoesNotExist:
            new_user = GuestDetails(user_name=user_name, email=email, first_name=first_name, last_name=last_name,
                                    password=password, phone_number=phone_number, address=address, state=state,
                                    city=city, country=country, adhaar_no=adhaar_no)
            new_user.save()
            return redirect('home')
    return render(request, 'signup.html')


def logout(request):
    if 'username' in request.session:
        del request.session['username']
        return redirect('home')


def dashboard(request):
    if 'username' in request.session:
        return render(request, 'dashboard.html', {'name': request.session['username']})
    else:
        return redirect('home')


def profile(request):
    if 'username' in request.session:
        record = get_object_or_404(GuestDetails, email=request.session['user_id'])
        return render(request, 'profile.html', {'name': request.session['username'], 'record': record})
    else:
        return redirect('home')


