from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = CustomUser
        fields = ['id','email','username']
    

class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','username','password']
    
    def save(self):
        user = CustomUser.objects.create_user(
        email=self.validated_data['email'],
        username=self.validated_data['username'],
        password=self.validated_data['password'])


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['userid'] = self.user.id
        data['admin'] = self.user.is_superuser
        return data