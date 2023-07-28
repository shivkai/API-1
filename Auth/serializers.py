from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('first_name','last_name', 'email', 'password')

        def set_password(self, password):
            self.password = self.set_password(password)