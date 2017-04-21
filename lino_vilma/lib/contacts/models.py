# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _
from lino.utils import join_words

from lino_xl.lib.contacts.models import *


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


@dd.python_2_unicode_compatible
class Person(Person):
    
    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')
        
    def __str__(self):
        words = []
        words.append(self.first_name)
        words.append(self.last_name)
        return join_words(*words)


class PersonDetail(PersonDetail):
    
    main = "general contact"

    general = dd.Panel("""
    overview info_box
    contacts.RolesByPerson
    """, label=_("General"))

    info_box = """
    id:5
    language:10
    email:40
    """
    
    contact = dd.Panel("""
    address_box:60 contact_box:30
    remarks faculties.OffersByEndUser
    """, label=_("Contact"))

    name_box = "last_name first_name:15 gender #title:10"

    
class CompanyDetail(CompanyDetail):
    main = "general contact"

    general = dd.Panel("""
    overview info_box
    contacts.RolesByCompany 
    """, label=_("General"))

    info_box = """
    id:5
    language:10
    email:40
    """
    
    contact = dd.Panel("""
    address_box:60 contact_box:30 
    remarks faculties.OffersByEndUser
    """, label=_("Contact"))

# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Companies.set_detail_layout(CompanyDetail())
Persons.set_detail_layout(PersonDetail())
Person.column_names = 'last_name first_name gsm email city *'
