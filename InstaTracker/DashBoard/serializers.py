from rest_framework import serializers
from .models import account

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = "__all__"