from rest_framework import serializers
from .models import UserAccount,UserAddress

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserAccount 
        fields = ('user_id', 'first_name', 'last_name', 'username','followers', 'email', 'gender', 'phone', 'dp', 'address')

class UserAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAddress
		fields = ('city', 'street_address', 'street_number', 'postal_code', 'country')

class UserRegisterSerializer(serializers.ModelSerializer):
	address = UserAddressSerializer()
	class Meta:
		model = UserAccount
		fields = ('username', 'email', 'password','first_name','last_name','gender', 'phone', 'dp', 'address')
		extra_kwargs = {'password': {'write_only': True}}
		
	def create(self, validated_data):
		address_data = validated_data.pop('address')
		user = UserAccount.objects.create_user(**validated_data)
		UserAddress.objects.create(user=user, **address_data)
		return user
	
class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required = True)
	password = serializers.CharField(required = True)

class UserSerializer(serializers.ModelSerializer):
	address = UserAddressSerializer()
	class Meta:
		model = UserAccount
		fields = ('username', 'email','first_name','last_name','gender', 'phone', 'dp', 'address')