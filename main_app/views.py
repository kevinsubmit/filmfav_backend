

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class Home(APIView):
    def get(self,request):
        message = {'mes':'weclome'}
        return Response(message)

