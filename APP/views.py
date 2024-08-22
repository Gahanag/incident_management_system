from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': serializers(refresh),
        'access': serializers(refresh.access_token),
    }


class IncidentAPIview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,incident_id=None):
        data=request.data
        if incident_id is not None:
            obj=Incident.objects.filter(incident_id=incident_id)
            if obj:
                obj=Incident.objects.filter(incident_id=incident_id)
            else:
                return Response({'message':'No such Id Present'})
        else:
            obj=Incident.objects.filter(created_by=request.user)

        serializer=IncidentSerializer(obj,many=True)
        return Response(serializer.data)

    def post(self,request):
        data=request.data
        serializer=IncidentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'message':'DATA IS SAVED'})
        else:
            return Response(serializer.errors)
        
    def delete(self,request,incident_id):
        data=request.data
        obj=Incident.objects.filter(incident_id=incident_id).exists()
        if obj:
            objs=Incident.objects.get(incident_id=incident_id)
            objs.delete()
            return Response({'mesage':'YOUR INCIDENT IS DELETED'})
        else:
            return Response({'mesage':'NO SUCH ID FOUND'})
    
    def patch(self,request):
        data=request.data
        obj=Incident.objects.get(incident_id=data['incident_id'])
        if obj.status == 'C':
            return Response({'message':'DATA can not be updated.....'})

        serializer=IncidentSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'DATA UPDATED SUCCESFULLY.....'})
        else:
            return Response(serializer.errors)


class RegistrationAPIview(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid():
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token': token ,'message':'USER REGISTRATION IS SUCCESFULL'})
        else:
            return Response(serializer.errors)

class LoginAPIview(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user:
                token=get_tokens_for_user(user)
                return Response({'token': token ,'message':'YOU ARE LOGGINED'})
            else:
                return Response({'MESSAGE':'PASSWORD IS INCORRECT....or MAYBE EMAIL....'})
        else:
            return Response(serializer.errors)

class ChangeUserPasswordAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        serializer=ChangePasswordSerializer(data=data,context={'user':request.user})
        if serializer.is_valid():
            return Response({'message':'Password is Changed Succesfully'})
        else:
            return Response(serializer.errors)

class SendPasswordResetLinkAPIView(APIView):
    def post(self,request):
        data=request.data
        serializer=PasswordResetLinkSerializer(data=data)
        if serializer.is_valid():
            link2=serializer.validated_data
            link=link2['link']
            return Response({'link':link,'message':'LINK HAS BEEN SEND ON YOUR REGISTERED EMAIL ADRESS..'})
        else:
            return Response(serializer.errors)

class CompletePasswordResetAPIView(APIView):
    def post(self,request,uid,token):
        data=request.data
        serializer=DoneResetPasswordProcessSerializer(data=data,context={'uid':uid, 'token':token})
        if serializer.is_valid():
            return Response({'message':'YOUR PASSWORD IS RESET BROTHER'})
        else:
            return Response(serializer.errors)
        




