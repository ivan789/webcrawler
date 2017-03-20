#--coding: utf-8 --


from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .models import kingofsatTabs
from .tables import SimpleTable
from .tables import searchtable
from .models import Kanali
from django.http import HttpResponseRedirect
import csv
from django.template import RequestContext
from .forms import DocumentForm
from django.core.urlresolvers import reverse
import os
from .models import Document
from django.core.management import call_command
import subprocess
from .forms import PostForm
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
import tempfile, zipfile
from django.conf import settings
import mimetypes
from django_tables2 import RequestConfig


''' Ovaj Django view prima korinicki fajl, te poziva skriptu koja radi parsanje zeljenog HTML-a,
    ovaj view takodjer servira i CSV i ispisuje parsane rezultate na frontend, takodjer generira
    django search tables tables, radi lakseg pretrazivanja rezultata dobivenih iz web crawlera!
        
'''
def scaner(request):
    if (request.POST.get('mybtn')):

        kingofsatTabs.objects.all().delete()
        os.system("python main.py /home/KingofsatCrawler/kroler_kingofsat/kingofsat/list.txt")
        with open('outfile.csv', 'r') as f:
            #reader = csv.reader(f)
            next(f)
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                #tmp = Person.objects.create()
                try:
                    tmp = kingofsatTabs.objects.create()
                    tmp.kanal = line[0]
                    tmp.satelit = line[1]
                    tmp.polarizacija = line[2]
                    tmp.stupnjevi = line[3]
                    tmp.frekvencija = line[4]
                    tmp.sid = line[5]
                    tmp.paket = line[6]
                    tmp.dvb = line[7]
                    tmp.modulacija = line[8]
                    tmp.symbol_rate = line[9]
                    tmp.fec = line[10]
                    tmp.tid = line[11]
                    tmp.onid = line[12]
                    tmp.enkripcija = line[13]
                    tmp.tip = line[14]
                    tmp.save()
                except IOError:
                    print "Oops!"

        f.close()
    if (request.POST.get('download')):
       
        filename = "/home/KingofsatCrawler/kroler_kingofsat/kingofsat/outfile.csv"
        download_name ="kingofsat.csv"
        wrapper      = FileWrapper(open(filename))
        content_type = mimetypes.guess_type(filename)[0]
        response     = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length']      = os.path.getsize(filename)    
        response['Content-Disposition'] = "attachment; filename=%s"%download_name        
        return response

    return render(request, 'kingofsat/kingofsat.html')

def post_kingofsat(request):
    post = kingofsatTabs.objects.all().values('kanal','satelit','polarizacija','stupnjevi', 'frekvencija', 'sid', 'paket', 'dvb', 'modulacija', 'symbol_rate', 'fec', 'tid', 'onid', 'enkripcija', 'tip')
    lista_za_ispis = []


    for parametri in post:
        lista_za_ispis.append({
            'kanal':parametri['kanal'],
            'satelit': parametri['satelit'],
            'polarizacija': parametri['polarizacija'],
            'stupnjevi': parametri['stupnjevi'],
            'tid': parametri['tid'],
            'frekvencija': parametri['frekvencija'],
            'sid': parametri['sid'],
            'paket': parametri['paket'],
            'dvb': parametri['dvb'],
            'modulacija': parametri['modulacija'],
            'symbol_rate': parametri['symbol_rate'],
            'fec': parametri['fec'],
            'onid': parametri['onid'],
            'enkripcija': parametri['enkripcija'],
            'tip': parametri['tip'],
        })
    return render(request, 'kingofsat/index.html', {'post':post, 'lista_za_ispis':lista_za_ispis})


def channel_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'kingofsat/post_channel.html',{'form':form})

def channel_list(request):
    post_kanala = Kanali.objects.all().values('channel')
    lista_channel = []


    for kanali in channel_list:
        lista_channel.append({
            'channel':kanali['channel']

        })
    return render(request, 'kingofsat/index.html', {'post_kanala':post_kanala, 'lista_channel':lista_channel})

def list(request):
    lista_kanala = "/home/KingofsatCrawler/kroler_kingofsat/kingofsat/list.txt"

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            docfile = request.FILES['docfile']
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
        else:
            print "Kliknio si prazno"
            return HttpResponse("Molim odaberite file za upload !!!")
    else:
        form = DocumentForm()
        documents = Document.objects.all()


    # Render list page with the documents and the form
    return render_to_response('kingofsat/list.html', {'documents': documents, 'form': form},context_instance=RequestContext(request))



def filterview(request):
    
  
    filtrirani_sateliti = kingofsatTabs.objects.filter(satelit__in=['Eutelsat 16A', 'Astra 1N', 'Astra 1L', 'Astra 1M', 'Astra 1KR', 'Hot Bird 13B', 'Hot Bird 13C','Hot Bird 13E']).order_by('tip').values('kanal','satelit','polarizacija','stupnjevi', 'frekvencija', 'sid', 'paket', 'dvb', 'modulacija', 'symbol_rate', 'fec', 'tid', 'onid', 'enkripcija', 'tip')
    filter_lista = []
    if (request.POST.get('download')):
        
        filename = "/home/KingofsatCrawler/kroler_kingofsat/kingofsat/filter.csv"
        download_name ="kingofsat_Filtrirana.csv"
        wrapper      = FileWrapper(open(filename))
        content_type = mimetypes.guess_type(filename)[0]
        response     = HttpResponse(wrapper,content_type=content_type)
        response['Content-Length']      = os.path.getsize(filename)    
        response['Content-Disposition'] = "attachment; filename=%s"%download_name        
        return response

    for fils in filtrirani_sateliti:
        filter_lista.append({
            'kanal':fils['kanal'],
            'satelit': fils['satelit'],
            'polarizacija': fils['polarizacija'],
            'stupnjevi': fils['stupnjevi'],
            'tid': fils['tid'],
            'frekvencija': fils['frekvencija'],
            'sid': fils['sid'],
            'paket': fils['paket'],
            'dvb': fils['dvb'],
            'modulacija': fils['modulacija'],
            'symbol_rate': fils['symbol_rate'],
            'fec': fils['fec'],
            'onid': fils['onid'],
            'enkripcija': fils['enkripcija'],
            'tip': fils['tip'],
        })

    if (request.POST.get('filterButon')):
        outfile = open('filter.csv', 'wb')
        headers = ('FREKVENCIJA', 'KANAL' ,'FEC', 'SATELIT','PAKET',  'ONID', 'STUPNJEVI', 'SYMBOL_RATE', 'POLARIZACIJA', 'TIP', 'DVB', 'MODULACIJA' , 'SID', 'TID', 'ENKRIPCIJA')
        writer1 = csv.writer(outfile, delimiter=';')
        writer1.writerow(headers)
        for csvfilter in filter_lista:           
            writer1.writerow(csvfilter.values())
            

        outfile.close()

                

    return render(request, 'kingofsat/filter.html', {'filtrirani_sateliti':filtrirani_sateliti, 'filter_lista':filter_lista})


def simple_list(request):
    queryset = Kanali.objects.all()
    table = SimpleTable(queryset)
    RequestConfig(request, paginate={"per_page": 30}).configure(table)

    return render(request, 'djangotabs.html', {'table': table})



def dataTabs(request):
    queryset = kingofsatTabs.objects.all()
    postdata = searchtable(queryset)
    return render(request, "datatable.html", {'postdata': postdata})
