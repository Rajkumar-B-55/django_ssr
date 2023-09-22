from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render
from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import JWTAuthentication, IsAdminUser, IsProfileOwnerOrAdmin
from .forms import LoginForm, RegistrationForm

User = get_user_model()


def home(request):
    return render(request, 'login.html')


def skip_admin():
    admin_user = User.objects.filter(role='admin').count()
    return admin_user


class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
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
                    return Response({'token': jwt_token}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterUser(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                if User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phone_number).exists():
                    return Response(data={"msg": "User already exists with this Email or Phone Number. Please login."},
                                    status=status.HTTP_302_FOUND)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data.get('last_name')
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                add_user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name if last_name is not None else "",
                    email=email,
                    phone_number=phone_number if phone_number is not None else "",
                    password=password
                )
                add_user.save()
                return Response(data={'msg': 'User Added Successfully', 'Credentials': 'Check your Email'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data={"msg": "Invalid form data. Please check your input."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class UpdateUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user_email = user.email
            if user_email is not None:
                user = User.objects.filter(email=user_email).first()
                user.first_name = request.data.get('first_name', user.first_name)
                user.last_name = request.data.get('last_name', user.last_name)
                user.phone_number = request.data.get('phone_number', user.phone_number)
                user.save()
                return Response(data={'msg': 'User profile updated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response(data={"msg": "Invalid Operation."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class GetUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user is not None:
                user = User.objects.filter(email=user.email).first()
                user_dict = {
                    'FirstName': user.first_name,
                    'LastName': user.last_name,
                    'Email': user.email,
                    'PhoneNumber': user.phone_number,
                    'DateJoined': user.date_joined.strftime("%d-%m-%Y %H:%M"),
                }
                return Response(data={'Msg': 'User Profile', 'info': user_dict}, status=status.HTTP_200_OK)
            else:
                return Response(data={"msg": "Invalid Operation."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class ListUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            list_user = User.objects.all()
            users_list = [
                {'user_id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email,
                 'phone_number': user.phone_number,
                 'is_active': user.is_active,
                 'role': user.role,
                 'date_joined': user.date_joined.strftime("%d-%m-%Y %H:%M"),
                 'last_login': str(user.last_login)
                 }
                for user in list_user
            ]
            return Response(data={"users": users_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class GetCountUserByWeek(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(weeks=1)).count()
            weekly_count = user - skip_admin()
            return Response(data={'users_count': weekly_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class GetCountUserByMonth(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=30)).count()
            monthly_count = user - skip_admin()
            return Response(data={'users_count': monthly_count}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class GetTotalCount(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.count()
            total_user = user - skip_admin()
            return Response(data={'users_count': total_user}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)
