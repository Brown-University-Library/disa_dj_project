# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect

log = logging.getLogger(__name__)


class Document(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    display_text = models.CharField( max_length=190, default='', help_text='auto-populated from associated citation title' )
    known_date = models.DateField( blank=True, null=True )
    range_start_date = models.DateField( blank=True, null=True, help_text='for when a specific date is unknown (start-range)' )
    range_end_date = models.DateField( blank=True, null=True, help_text='for when a specific date is unknown (end-range)' )

    @property
    def default_date(self):
        "Returns a default document-date."
        rtrn_dt = self.known_date
        if self.known_date is None:
            rtrn_dt = self.range_start_date
        return rtrn_dt

    def __str__(self):
        return f'{self.default_date} -- {self.display_text[0:10]}'


class DocumentColonyState(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    name = models.CharField( max_length=190 )
    documents = models.ManyToManyField( Document, related_name='document_colony_state' )
    def __str__(self):
        return self.name[0:10]


class DocumentRecordType(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    name = models.CharField( max_length=190 )
    documents = models.ManyToManyField( Document, related_name='document_record_types' )
    def __str__(self):
        return self.name[0:10]


class DocumentSourceType(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    name = models.CharField( max_length=190 )
    documents = models.ManyToManyField( Document, related_name='document_source_types' )
    def __str__(self):
        return self.name[0:10]


class DocumentLocation(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    name = models.CharField( help_text='city/town', max_length=190 )
    documents = models.ManyToManyField( Document, default=None )
    def __str__(self):
        return self.name[0:10]


class Citation(models.Model):
    created = models.DateTimeField( auto_now_add=True )
    modified = models.DateTimeField( auto_now=True )
    citation_string = models.CharField( max_length=190 )
    # document = models.ForeignKey( Document, on_delete=models.CASCADE )
    document = models.ForeignKey( Document, on_delete=models.CASCADE )

    def __str__(self):
        return self.citation_string[0:10]


# class Person(models.Model):
#     created = models.DateTimeField( auto_now_add=True )
#     modified = models.DateTimeField( auto_now=True )
#     display_name = models.CharField( max_length=190, default='', help_text='auto-populated from associated first&last Name' )

#     def __str__(self):
#         return self.display_name[0:10]






