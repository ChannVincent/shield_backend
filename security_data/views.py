from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Commune
from rest_framework.permissions import AllowAny


class CommuneListView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def get(self, request):
        communes = Commune.objects.all().order_by('name_full').values('id', 'name_full')
        return Response(communes)