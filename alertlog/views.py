from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from alertlog.models import Filterlog, Logroles,Systems,  Rule, UsersRole,UsersSystem, Room
from alertlog.serializers import AllFilterLogSerializer, RoleSerializer, LogUpdateSerializer
from rest_framework import status
from django.db.models import Q
from django.db import connection

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, LogRoleSerializer ,SystemsSerializer, RoleSerializer,UserSerializer,UserdataSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

class AllowPostOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)


# Create your views here.
def  index(request):
    return HttpResponse("Welcome")

class AlertLogListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [AllowPostOnly ]
    http_method_names = ['get', 'put','post', 'patch', 'head', 'options', 'trace', 'delete',]

    queryset = Filterlog.objects.all().order_by('-timestamp')
    serializer_class = AllFilterLogSerializer

    def get_queryset(self):
        user = self.request.user.id
        hostname = self.request.GET.get('hostname')
        severity = self.request.GET.get('severity')
        time1 = self.request.GET.get('time1')
        time2 = self.request.GET.get('time2')
        rolename = self.request.GET.get('rolename')
        is_know  = self.request.GET.get('is_know')


        #filterlogs = self.queryset
        filterlogs= Filterlog.objects.filter(users=user)
        #print(user_data, "user data")
        

        if severity:
            filterlogs = filterlogs.filter(severity__icontains=severity)
        if is_know:
            filterlogs = filterlogs.filter(is_know__icontains =is_know)
        if hostname:
            filterlogs = filterlogs.filter(Q(hostname__icontains=hostname))
        if rolename:
            filterlogs = filterlogs.filter(Q(role__icontains=rolename))
        if time1 and time2:
            filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

        return filterlogs
 



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
            
        # 'is_known' sütununu güncelle
        is_known = request.data.get('is_know')
       


        # SQL sorgusunu çalıştır
        with connection.cursor() as cursor:
            sql_query = "UPDATE alertlog_filterlog SET is_know = %s WHERE id = %s"
            cursor.execute(sql_query, [is_known, instance.id])

        return Response({"message": "Records updated successfully."})

    

class RulesListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.AllowAny ]
    http_method_names = ['get', 'put','post', 'patch', 'head', 'options', 'trace', 'delete',]
    queryset = Logroles.objects.all()
    serializer_class = LogRoleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    
    def perform_destroy(self, instance):
        instance.delete()



class TodoListApiView(APIView):
    #
    permission_classes = [permissions.AllowAny]
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #todos = Filterlog.objects.filter(user = request.user.id)
        todos = Filterlog.objects.all()
        serializer = AllFilterLogSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





# class CountLogs(APIView):
#     def get(self, request):
        
#         today = datetime.now().date()
#         last_month = today - timedelta(days=30)
#         last_week = today - timedelta(days=7)
#         print(today)
#         today1 = date.today()
#         start_of_week = today1 - timedelta(days=today1.weekday())
#         end_of_week = start_of_week + timedelta(days=6)
        
      
        
#         start_of_day = datetime.combine(today, datetime.min.time())
#         end_of_day = datetime.combine(today, datetime.max.time())
        
#         data = self.request.GET.get('date')
#         if date == 'month':
#             alldata = Filterlog.objects.all().filter(Q(timestamp__gte=last_month) & Q(timestamp__lte=today) & Q(is_know =False))
#             allcount = alldata.count()
#             warning_count = alldata.filter(severity__icontains='warning').count()
#             info_count = alldata.filter(severity__icontains='info').count()
#             error_count = alldata.filter(severity__icontains='ERR').count()
            
#             response_data = {
#             'total' : allcount,
#             'warning': warning_count,
#             'info': info_count,
#             'error': error_count,           
#             }
#             return Response(response_data)
            
#         if date == 'week':
#             print("week gecdi")
#             alldata = Filterlog.objects.filter(timestamp__date__range=[start_of_week, end_of_week]& Q(is_know =False))
#             #alldata = Filterlog.objects.all().filter(Q(timestamp__gte=last_week) & Q(timestamp__lte=today))
#             allcount = alldata.count()
#             warning_count = alldata.filter(severity__icontains='warning').count()
#             info_count = alldata.filter(severity__icontains='info').count()
#             error_count = alldata.filter(severity__icontains='ERR').count()
            
#             response_data = {
#             'total' : allcount,
#             'warning': warning_count,
#             'info': info_count,
#             'error': error_count,           
#             }
#             return Response(response_data)
            
        
#         if date == 'today':
            
#             alldata = Filterlog.objects.filter(timestamp__range=(start_of_day, end_of_day)& Q(is_know =False))
#             #alldata = Filterlog.objects.all().filter(Q(timestamp__date=today))
#             allcount = alldata.count()
#             warning_count = alldata.filter(severity__icontains='warning').count()
#             info_count = alldata.filter(severity__icontains='info').count()
#             error_count = alldata.filter(severity__icontains='ERR').count()
#             print(alldata)
#             response_data = {
#             'total' : allcount,
#             'warning': warning_count,
#             'info': info_count,
#             'error': error_count,           
#             }
#             return Response(response_data)
        
#             # queryset = YourModel.objects.filter(Q(created_at__gte=last_month) & Q(created_at__lte=today))
#         allcount = Filterlog.objects.filter(is_know =False).all().count()
#         warning_count = Filterlog.objects.filter(severity__icontains='warning').count()
#         info_count = Filterlog.objects.filter(severity__icontains='info').count()
#         error_count = Filterlog.objects.filter(severity__icontains='ERR').count()
#         response_data = {
#             'total' : allcount,
#             'warning': warning_count,
#             'info': info_count,
#             'error': error_count,           
#         }
#         return Response(response_data)

class FilterLogsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AllFilterLogSerializer
    
    queryset = Filterlog.objects.all().order_by('-timestamp')

    def get_queryset(self):
        hostname = self.request.GET.get('hostname')
        severity = self.request.GET.get('severity')
        time1 = self.request.GET.get('time1')
        time2 = self.request.GET.get('time2')
        rolename = self.request.GET.get('rolename')
        is_know  = self.request.GET.get('is_know')


        filterlogs = self.queryset

        if severity:
            filterlogs = filterlogs.filter(severity__icontains=severity)
        if is_know:
            filterlogs = filterlogs.filter(is_know__icontains =is_know)
        if hostname:
            filterlogs = filterlogs.filter(Q(hostname__icontains=hostname))
        if rolename:
            filterlogs = filterlogs.filter(Q(role__icontains=rolename))
        if time1 and time2:
            filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

        return filterlogs


class ReporAPIVIEW(APIView):
    def get(self, request, *args , **kwargs):
            hostname = request.GET.get('hostname')
            severity = request.GET.get('severity')
            time1 = request.GET.get('time1')
            time2 = request.GET.get('time2')
            rolename  = request.GET.get('rolename')
            filterlogs = Filterlog.objects.all().order_by('-timestamp')
            if hostname:
                filterlogs = filterlogs.filter(Q(hostname__icontains=hostname)) 
            if severity :
                filterlogs = filterlogs.filter(severity__icontains = severity)
            if  time1 and time2 :
                print(time1, "ok  ",time2 )
                filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

            serializer = AllFilterLogSerializer(filterlogs, many=True)
            return Response({
                "data":serializer.data,
               }
                ,
                status=status.HTTP_200_OK)
           # else:
            #    return Response({"message":"Sizin rugsadynyz yok"}, status=status.HTTP_404_NOT_FOUND)




class LogUpdateView(APIView):
    def put(self, request, format=None):
        serializer = LogUpdateSerializer(data=request.data)
        if serializer.is_valid():
            ids = request.data.get('id')
            print("my ids: ",ids)
            is_know = request.data.get('is_know')
            Filterlog.objects.filter(id__in=ids).update(is_know=is_know)
            return Response({"message": "Records updated successfully."})
        return Response(serializer.errors, status=400)




class ProcessDataView(APIView):
    def post(self, request):
        message = request.data.get('message')
        split_character = request.data.get('split_character')
        index_number = request.data.get('index_number')

#        if message is None or split_character is None or index_number is None:
#            return Response({'error': 'Invalid request data'}, status=400)

        data = message.split(split_character)
        if index_number < len(data):
            result = data[index_number]
            return Response({'result': result})
        else:
            return Response({'error': 'Invalid index number'}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SystemsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Systems.objects.all()
    serializer_class = SystemsSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Additional custom logic after obtaining the token pair
        # You can modify the response or perform additional tasks here
        return response

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Additional custom logic after refreshing the token
        # You can modify the response or perform additional tasks here
        return response




class UsersSystemViewSet(viewsets.ModelViewSet):
    queryset = UsersSystem.objects.all()
    serializer_class = SystemsSerializer
    basename = 'userssystem'  # basename'i belirtin

    def get_queryset(self):
        user_id = self.request.user.id
        system_ids = UsersSystem.objects.filter(users_id=user_id).values('system_id')
        queryset = Systems.objects.filter(id__in=system_ids)
        #data = Systems.objects.filter(id=1)
        return queryset
        
        

  


class UsersRoleViewSet(viewsets.ModelViewSet):
    queryset = UsersRole.objects.all()
    serializer_class = RoleSerializer
    basename = 'usersrole'

    def get_queryset(self):
        user_id = self.request.user.id
        role_ids = UsersRole.objects.filter(user_id=user_id).values('role_id')
        queryset = Rule.objects.filter(id__in=role_ids)
        return queryset

class RolesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Rule.objects.all()
    serializer_class = RoleSerializer
    

class UserRegistrationView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
   
    
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        is_active = request.data.get('is_active')
        role_id = request.data.get('role')
        system_ids = request.data.get('system')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.is_active = is_active
        user.save()
        
        room =Room.objects.create(name=username,slug =username).save()
        
        role = get_object_or_404(Rule, id=role_id)

        systems = []
        for system_id in system_ids:
            system = get_object_or_404(Systems, id=system_id)
            systems.append(system)

        roles = UsersRole.objects.create(user_id=user, role_id=role)
        for system in systems:
            UsersSystem.objects.create(users_id=user, system_id=system)

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        username = request.data.get('username')
        password = request.data.get('password')
        is_active = request.data.get('is_active')
        role_id = request.data.get('role')
        system_ids = request.data.get('system')

        user = get_object_or_404(User, id=user_id)
        user.username = username
        user.set_password(password)
        user.is_active = is_active
        user.save()

        role = get_object_or_404(Rule, id=role_id)

        systems = []
        for system_id in system_ids:
            system = get_object_or_404(Systems, id=system_id)
            systems.append(system)

        UsersRole.objects.filter(user_id=user).delete()
        UsersSystem.objects.filter(users_id=user).delete()

        roles = UsersRole.objects.create(user_id=user, role_id=role)
        for system in systems:
            UsersSystem.objects.create(users_id=user, system_id=system)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SystemsRolesViewSet(viewsets.ViewSet):
    def list(self, request):
        systems = Systems.objects.all()
        roles = Rule.objects.all()

        systems_serializer = SystemsSerializer(systems, many=True)
        roles_serializer = RoleSerializer(roles, many=True)

        return Response({'systems': systems_serializer.data, 'roles': roles_serializer.data})
    
    
    #        duzetmeli
class TestApivew(APIView):
    def get(self, request):
        all_users = User.objects.all()

    

        users_data = []

        

        for user in all_users:

            users_systems = UsersSystem.objects.filter(users_id=user.id).values('system_id__name', 'system_id__id')

            users_roles = UsersRole.objects.filter(user_id=user.id).values('role_id__role_name', 'role_id__id')

            

            data = {

                'username': user.username,

                'date_joined': user.date_joined,

                'is_active': user.is_active,

                'role': list(users_roles),

                'system': list(users_systems),

            }

            

            users_data.append(data)
        return Response(users_data)
    
class UserdataRegistrationView(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserdataSerializer