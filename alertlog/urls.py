from alertlog import views
from django.urls import path , include
from rest_framework import routers
from .views import Pairlist, SystemsViewSet, UserRegistrationView, BaglansykView,UserdataRegistrationView,UsersSystemViewSet,UsersRoleViewSet, RolesViewSet,UserViewSet,SystemsRolesViewSet

router = routers.DefaultRouter(trailing_slash=False)
 
router.register('logs',views.AlertLogListApiView)  # loglary ulanyja gora filter edyar
router.register('role',views.RulesListApiView)   #  seretmeli log rul


router.register(r'userrulepair', BaglansykView) 
router.register(r'systems', SystemsViewSet)  #  all systems
router.register(r'getsystem', UsersSystemViewSet)  #degisli system
router.register(r'getrole', UsersRoleViewSet)   # degisli role
router.register(r'roles', RolesViewSet)  #  all ulanjylaryn roleleri
router.register(r'users', UserViewSet)  # all user
router.register(r'data', UserdataRegistrationView) 
router.register(r'adduser', UserRegistrationView)  #  add user
router.register(r'systemrole', SystemsRolesViewSet,basename='systemrole')   # systemleri we role hemmesini gaytarya
router.register(r'pairlist', Pairlist) 
#router.register('filter',views.FilterLogsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', views.TodoListApiView.as_view()),  # all filterlog data 
    path('count/',views.CountLogs.as_view()),
    path('test/', views.TestApivew.as_view()), 
    path('check/', views.ProcessDataView.as_view()),   # message  check
    path('logupdate/',views.LogUpdateView.as_view(), name = "log -update"), # birncae loglary update etyan
    path('rolespost/',views.create_pair),
    path('pair/', views.get_pair_by_id),
    path('mytest/', views.mytest),
   
]
