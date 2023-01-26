#from .models to json?
from rest_framework import serializers
from .models import tvn


class TvnSerializer(serializers.ModelSerializer):
    class Meta:
        model = tvn
        fields = ['id','headline','date','hour','link'] 