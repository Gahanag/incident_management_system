from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import *

class IncidentSerializer(serializers.ModelSerializer):
    Reporter_Name=serializers.SerializerMethodField()

    # name =serializers.CharField(
        # source="created_by.name", read_only=True
    # )

    class Meta:
        model=Incident
        fields=['TITILE_OF_INCIDENT','incident_id','description','Incident_related_field','status','Reporter_Name']

    def get_Reporter_Name(self,data):
        return data.created_by.Reporter_Name


# ================AUTHENTICATION SERIALIZERS ========================
class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','Reporter_Name','password','password2','Address', 'City', 'Country', 'Pin_code', 'phone_number']
        extra_stuff={
            'password':{'write_only':True}
        }

    def validate(self,data):
        p1=data.get('password')
        p2=data.get('password2')

        if p1!=p2:
            raise serializers.ValidationError("PASSWORD DOES NOT MATCH..")

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model=User
        fields=['email','password']

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    password=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=200,style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['old_password','password','password2']
    
    def validate_old_password(self,data):
        user=self.context.get('user')
        if not user.check_password(data):
            raise serializers.ValidationError("your old password is in correct..")
        return data
        

    def validate(self,data):
        p1=data.get('password')
        p2=data.get('password2')

        user=self.context.get('user')
        print(user.password)

        if p1!=p2:
            raise serializers.ValidationError("password does not MATCH..")

        user.set_password(p1)
        user.save()
        return data

class PasswordResetLinkSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=255)
    class Meta:
        fields=['email']

    def validate(self,data):
        email=data.get('email')
        user=User.objects.filter(email=email).exists()
        if user:
            obj=User.objects.get(email=data['email'])
            uid=urlsafe_base64_encode(force_bytes(obj.id))
            token=PasswordResetTokenGenerator().make_token(obj)
            link='/'+uid+'/'+token
            data['link']=link
            body=link
            saman={
                'subject':'Reset Link Is Here..->  ',
                'body':body,
                'to_email':obj.email
            }

            Util.send_email(saman)
            return data
        else:
            raise serializers.ValidationError("THIS EMAIL DOES NOT EXISTS")
    
class DoneResetPasswordProcessSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=200 , style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=200 , style={'input_type':'password'},write_only=True)

    class Meta:
        fields=['password','password2']
    
    def validate(self, data):
        try:
            password=data.get('password')
            password2=data.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("the passwords don't match..")
            
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator():
                raise serializers.ValidationError("something went wrong...Maybe the Token is Expired or Invalid..")
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as d:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("something went wrong..")
