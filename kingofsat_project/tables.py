# -*- coding: utf-8 -*-
import django_tables2 as tables
from  models import Kanali
from  models import kingofsatTabs
from table import Table
from table.columns import Column

class SimpleTable(tables.Table):
    class Meta:
        model = Kanali
        exclude = ('id', )
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}



class searchtable(Table):


    
    kanal = Column(field='kanal', header='channel')
    satelit = Column(field='satelit', header='satelit')
    polarizacija = Column(field='polarizacija', header='polarization')
    stupnjevi = Column(field='stupnjevi', header='degrees')
    frekvencija = Column(field='frekvencija', header='frequency')
    sid = Column(field='sid', header='sid')
    paket = Column(field='paket', header='package')
    dvb = Column(field='dvb', header='dvb')
    modulacija = Column(field='modulacija', header='modulation')
    symbol_rate = Column(field='symbol_rate', header='symbol_rate')
    fec = Column(field='fec', header='fec')
    tid = Column(field='tid', header='tid')
    onid = Column(field='onid', header='nid')
    tip = Column(field='tip', header='type')


    class Meta:
        model = kingofsatTabs

        attrs = {'class': 'custom_class'}



        



