from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .auth import JWTAuthentication
from .decorators import allowed_users
from .forms import LoginForm, UpdateForm, RegistrationForm_

User = get_user_model()


def login_view(request):
    try:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # authenticate
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                jwt_token = JWTAuthentication.create_payload(user)
                data = {
                    'email': email,
                    'jwt': jwt_token
                }
                request.session['token'] = jwt_token
                return redirect('dashboard_index')
            else:
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form})
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def register_view(request):
    try:
        form = RegistrationForm_(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            if User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phone_number).exists():
                messages.warning(request, f'{email} or {phone_number} already exists')
                return redirect('dashboard_users')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data.get('last_name', '')
            password = form.cleaned_data['password']

            add_user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            add_user.save()
            messages.success(request, f'User {email} added Successfully')
            return redirect('dashboard_users')
        else:
            messages.warning(request, f'{form.errors}')
            return render(request, 'users/users.html', {"form": form})

    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_user_view(request, email):
    try:
        user_instance = User.objects.get(email=email)

        if request.method == 'POST':
            form = UpdateForm(request.POST, instance=user_instance)
            if form.is_valid():
                form.save()
                messages.success(request, f'User {email} Updated Successfully')
                return redirect('dashboard_users')
            else:
                messages.error(request, 'Invalid form data. Please check the fields.')

        else:
            form = UpdateForm(instance=user_instance)

        context = {"form": form}
        return render(request, 'users/users_edit.html', context)

    except User.DoesNotExist:
        e = "User not found"
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_user(request, email):
    try:
        user = get_object_or_404(User, email=email)
        user_name = user.email
        user.delete()
        messages.success(request, f'{user_name} deleted')
        return redirect('dashboard_users')
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_user(request, email):
    try:
        user = get_object_or_404(User, email=email)
        user_name = user.email
        user.delete()
        messages.success(request, f'{user_name} deleted')
        return redirect('dashboard_users')
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
def update_user(request):
    try:
        if request.method == 'POST':
            u_form = UpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                return redirect('user_profile')
        else:
            u_form = UpdateForm(instance=request.user)
        context = {
            'u_form': u_form
        }
        return render(request, 'users/profile_update.html', context)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
def get_user_profile(request):
    try:
        user = request.user
        if user is not None:
            user = User.objects.filter(email=user.email).first()
            user_dict = {
                'user': {'FirstName': user.first_name,
                         'LastName': user.last_name,
                         'Email': user.email,
                         'PhoneNumber': user.phone_number,
                         'DateJoined': user.date_joined.strftime("%d-%m-%Y %H:%M"), }
            }
            return render(request, 'users/profile.html', user_dict)
        else:
            return Response(data={"msg": "Invalid Operation."},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)
