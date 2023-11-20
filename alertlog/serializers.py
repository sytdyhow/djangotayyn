from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AllFilterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filterlog
        fields = '__all__'



class LogRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logroles
        fields = '__all__'

class LogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filterlog
        fields = ['is_know', 'id']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    
class SystemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Systems
        fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'
        #fields = ['id', 'username', 'role_id', 'system_id', 'active', 'is_staff', 'is_active', 'is_superuser', 'date_joined']

    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'      # ['role_name']
        
class UsersystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersSystem
        fields = '__all__'      # ['role_name']
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'  
        fields = ['username','is_active', 'date_joined']
        
##############################




class UserdataSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()

    system = serializers.SerializerMethodField()


    class Meta:

        model = User

        fields = ('username', 'date_joined', 'is_active', 'role', 'system')


    def get_role(self, obj):

        roles = obj.usersrole_set.values_list('role_id__role_name', 'role_id__id')

        return list(roles)


    def get_system(self, obj):

        systems = obj.userssystem_set.values_list('system_id__name', 'system_id__id')

        return list(systems)


############################################################################   users we logroles ucin   serializer ##############################################
class UserSerializer2(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ['id','username']


class PairsListSerializer(serializers.ModelSerializer):

    class Meta:

        model = PairsList

        fields = ['id','name']

class PairsListSerializer2(serializers.ModelSerializer):

    class Meta:

        model = PairsList

        fields = '__all__'

class LogRoleSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Logroles
        fields = ['id','name']

class BaglansykSerializer(serializers.ModelSerializer):

    pairname = PairsListSerializer()

    users = UserSerializer2()

    #logroles = serializers.StringRelatedField()
    logroles = LogRoleSerializer2()


    class Meta:

        model = Baglansyk

        fields = ['id', 'pairname', 'users', 'logroles']