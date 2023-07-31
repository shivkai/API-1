from rest_framework import serializers
from Pokemon.models  import Pokemondata
from rest_framework.exceptions import ErrorDetail, ValidationError
class PokeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Pokemondata
        fields = ('name','attribute', 'weight','height','evolution')

        