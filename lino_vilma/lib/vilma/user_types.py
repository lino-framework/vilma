# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the user types for Lino Vilma.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for Vilma sites.
`.

"""


from lino.core.roles import UserRole, SiteAdmin
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.cal.roles import CalendarReader

from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import ugettext_lazy as _


class EndUser(OfficeUser):
    """An **end user** is somebody who uses our database, but won't work
    on it.

    """
    pass


class Collector(EndUser, ExcerptsUser, ContactsUser):
    """A **collector** is somebody who collects data into the database.

    """
    pass


class Staff(Collector, ExcerptsStaff):
    """A **senior developer** is a *developer* who is additionally
    responsible for triaging tickets

    """
    pass


class SiteAdmin(Staff, SiteAdmin, OfficeStaff, ContactsStaff):
    """Can do everything."""


# class Anonymous(CommentsReader, CalendarReader):
class Anonymous(CalendarReader):
    pass

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),        Anonymous, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),             EndUser, 'user')
add('200', _("Collector"),        Collector, 'collector')
add('800', _("Staff"),            Staff, 'staff')
add('900', _("Administrator"),    SiteAdmin, 'admin')


from lino.core.merge import MergeAction
from lino.api import rt
lib = rt.models
for m in (lib.contacts.Company, ):
    m.define_action(merge_row=MergeAction(
        m, required_roles=set([ContactsStaff])))
