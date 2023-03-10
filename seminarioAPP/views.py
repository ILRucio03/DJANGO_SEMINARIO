from cgitb import reset
from datetime import timezone
from email import message
from re import A
from django.shortcuts import redirect, render
from django.urls import is_valid_path
from seminarioAPP.models import seminario
from seminarioAPP.forms import FormProyecto
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from .serialiazers import SeminarioSerializer

def index(request):
    return render(request, 'index.html')
    
def listadoseminario(request):
    seminarios = seminario.objects.all()
    data = {'seminario': seminarios}
    return render(request, 'seminario.html', data)

def agregarSeminario(request):
    form = FormProyecto()
    if request.method == 'POST':
        form = FormProyecto(request.POST)
        if  form.is_valid():
            form.save()
        return index(request) 

    data = {'form' : form}
    return render(request, 'agregarSeminario.html', data)

def eliminarseminario(request, id):
    Res = seminario.objects.get(id= id)
    Res.delete()
    return redirect('/seminario')

def actualizarseminario(request, id):
    Res= seminario.objects.get(id = id)
    form=FormProyecto(instance=Res)
    if request.method=='POST':
        form=FormProyecto(request.POST, instance=Res)
        if form.is_valid():
            form.save()
        return index (request)
    data ={'form':form}
    return render (request, 'agregarseminario.html',data)


class Listaseminario(APIView):
    def get(self, request):
        Semi = seminario.objects.all()
        serial = SeminarioSerializer(Semi, many=True)
        return Response(serial.data)

    def post(self, request):
        serial = SeminarioSerializer(data = request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

class Detalleseminario(APIView):
    def get_object(self, pk):
        try:
            return seminario.objects.get(id=pk)
        except seminario.DoesNotExist:
            return Http404

    def get(self, request, pk):
        Semi = self.get_object(pk)
        serial = SeminarioSerializer(Semi)
        return Response(serial.data)

    def put(self, request, pk):
        Semi = self.get_object(pk)
        serial = SeminarioSerializer(Semi, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Semi = self.get_object(pk)
        Semi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
