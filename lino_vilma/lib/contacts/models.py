# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _
from lino.utils import join_words
from lino.mixins import  Hierarchical

from lino_xl.lib.contacts.models import *
from lino.modlib.comments.mixins import Commentable


PartnerDetail.address_box = dd.Panel("""
    name_box
    country #region city zip_code:10
    #addr1
    #street_prefix street:25 street_no street_box
    #addr2
    """, label=_("Address"))

PartnerDetail.contact_box = dd.Panel("""
    url
    phone
    gsm #fax
    """, label=_("Contact"))

from lino_xl.lib.addresses.mixins import AddressOwner

@dd.python_2_unicode_compatible
class Person(Person, Commentable, AddressOwner):
    
    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')
        
    def __str__(self):
        words = []
        words.append(self.first_name)
        words.append(self.last_name)
        return join_words(*words)

    def get_overview_elems(self, ar):
        elems = super(Person, self).get_overview_elems(ar)
        elems += AddressOwner.get_overview_elems(self, ar)
        return elems

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.setdefault(
            'company', models.ForeignKey(
                'contacts.Company', blank=True, null=True))
        fields.setdefault(
            'skill', models.ForeignKey(
                'faculties.Faculty', blank=True, null=True))
        return super(Person, cls).get_parameter_fields(**fields)
    
    @classmethod
    def get_simple_parameters(cls):
        rv = super(Person, cls).get_simple_parameters()
        rv.add('company')
        rv.add('skill')
        return rv
    
    @classmethod
    def add_param_filter(cls, qs, lookup_prefix='', company=None,
                         skill=None, **kwargs):
        qs = super(Person, cls).add_param_filter(qs, **kwargs)
        if company:
            fkw = dict()
            wanted = company.whole_clan()
            fkw[lookup_prefix + 'rolesbyperson__company__in'] = wanted
            qs = qs.filter(**fkw)
        
        if skill:
            fkw = dict()
            wanted = skill.whole_clan()
            fkw[lookup_prefix + 'end_user_set__faculty__in'] = wanted
        return qs
        

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Person, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.skill:
    #     return qs

# We use the `overview` field only in detail forms, and we
# don't want it to have a label "Description":
dd.update_field(Person, 'overview', verbose_name=None)    

class Company(Company, Hierarchical, Commentable):
    
    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')
        


class PersonDetail(PersonDetail):
    
    main = "general #contact faculties.OffersByEndUser more"

    general = dd.Panel("""
    overview contact_box
    contacts.RolesByPerson:30 comments.CommentsByRFC:30
    """, label=_("General"))

    contact_box = dd.Panel("""
    name_box
    email 
    gsm phone
    """)  #, label=_("Contact"))

    # contact = dd.Panel("""
    # address_box
    # remarks
    # """, label=_("Contact"))

    name_box = "last_name first_name:15 gender #title:10"

    more = dd.Panel("""
    id:5 language:10 url
    remarks
    """, label=_("More"))


class CompaniesByCompany(Companies):
    master_key = 'parent'

    
class CompanyDetail(CompanyDetail):
    main = "general contact faculties.OffersByEndUser more"

    general = dd.Panel("""
    overview contact_box 
    contacts.RolesByCompany:30 comments.CommentsByRFC:30
    """, label=_("General"))

    contact = dd.Panel("""
    address_box
    remarks 
    """, label=_("Contact"))

    contact_box = dd.Panel("""
    email:40 url
    gsm phone
    """, label=_("Contact"))

    more = dd.Panel("""
    id:5 language:10 parent
    CompaniesByCompany
    """, label=_("More"))

    

# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Companies.set_detail_layout(CompanyDetail())
Persons.set_detail_layout(PersonDetail())
Person.column_names = 'last_name first_name gsm email city *'
Persons.params_layout = 'observed_event start_date end_date skill company'
