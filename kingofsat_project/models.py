#!/usr/local/bin/python
#--coding: utf-8 --
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from kingofsat.storage import OverwriteStorage



class kingofsatTabs(models.Model):

    kanal = models.CharField(max_length=225, db_index=True)
    satelit = models.CharField(max_length=225, db_index=True)
    polarizacija = models.CharField(max_length=225, db_index=True)
    stupnjevi = models.CharField(max_length=225, db_index=True)
    frekvencija = models.CharField(max_length=225, db_index=True)
    sid = models.CharField(max_length=225, db_index=True)
    paket = models.CharField(max_length=225, db_index=True)
    dvb = models.CharField(max_length=225, db_index=True)
    modulacija = models.CharField(max_length=225, db_index=True)
    symbol_rate = models.CharField(max_length=225, db_index=True)
    fec = models.CharField(max_length=225, db_index=True)
    tid = models.CharField(max_length=225, db_index=True)
    onid = models.CharField(max_length=225, db_index=True)
    enkripcija = models.CharField(max_length=225, db_index=True)
    tip = models.CharField(max_length=225, db_index=True)


    def __str__(self):
        return str(self.id)

class Kanali(models.Model):
    channel = models.CharField(max_length=225, db_index=True)


class Document(models.Model):

    docfile = models.FileField(storage=OverwriteStorage(),upload_to='')




























