# -*- coding: utf-8 -*-
"""
    rhodecode.controllers.admin.users_groups
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Users Groups crud controller for pylons
    
    :created_on: Jan 25, 2011
    :author: marcink
    :copyright: (C) 2009-2011 Marcin Kuzminski <marcin@python-works.com>    
    :license: GPLv3, see COPYING for more details.
"""
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your opinion) any later version of the license.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import logging
import traceback
import formencode

from formencode import htmlfill
from pylons import request, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from pylons.i18n.translation import _

from rhodecode.lib.exceptions import DefaultUserException, UserOwnsReposException
from rhodecode.lib import helpers as h
from rhodecode.lib.auth import LoginRequired, HasPermissionAllDecorator, \
    fill_perms
from rhodecode.lib.base import BaseController, render

from rhodecode.model.db import User, UsersGroup
from rhodecode.model.forms import UserForm, UsersGroupForm
from rhodecode.model.user import UserModel
from rhodecode.model.users_group import UsersGroupModel

log = logging.getLogger(__name__)

class UsersGroupsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('users_group', 'users_groups')

    @LoginRequired()
    @HasPermissionAllDecorator('hg.admin')
    def __before__(self):
        c.admin_user = session.get('admin_user')
        c.admin_username = session.get('admin_username')
        super(UsersGroupsController, self).__before__()
        c.available_permissions = config['available_permissions']

    def index(self, format='html'):
        """GET /users_groups: All items in the collection"""
        # url('users_groups')
        c.users_groups_list = self.sa.query(UsersGroup).all()
        return render('admin/users_groups/users_groups.html')

    def create(self):
        """POST /users_groups: Create a new item"""
        # url('users_groups')
        users_group_model = UsersGroupModel()
        users_group_form = UsersGroupForm()()
        try:
            form_result = users_group_form.to_python(dict(request.POST))
            users_group_model.create(form_result)
            h.flash(_('created users group %s') % form_result['users_group_name'],
                    category='success')
            #action_logger(self.rhodecode_user, 'new_user', '', '', self.sa)
        except formencode.Invalid, errors:
            return htmlfill.render(
                render('admin/users_groups/users_group_add.html'),
                defaults=errors.value,
                errors=errors.error_dict or {},
                prefix_error=False,
                encoding="UTF-8")
        except Exception:
            log.error(traceback.format_exc())
            h.flash(_('error occurred during creation of users group %s') \
                    % request.POST.get('users_group_name'), category='error')

        return redirect(url('users_groups'))

    def new(self, format='html'):
        """GET /users_groups/new: Form to create a new item"""
        # url('new_users_group')
        return render('admin/users_groups/users_group_add.html')

    def update(self, id):
        """PUT /users_groups/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('users_group', id=ID),
        #           method='put')
        # url('users_group', id=ID)


        users_group_model = UsersGroupModel()
        c.users_group = users_group_model.get(id)
        c.group_members = [(x.user_id, x.user.username) for x in
                           c.users_group.members]

        c.available_members = [(x.user_id, x.username) for x in
                               self.sa.query(User).all()]
        users_group_form = UsersGroupForm(edit=True,
                                          old_data=c.users_group.get_dict(),
                                          available_members=[str(x[0]) for x
                                                in c.available_members])()

        try:
            form_result = users_group_form.to_python(request.POST)
            users_group_model.update(id, form_result)
            h.flash(_('updated users group %s') % form_result['users_group_name'],
                    category='success')
            #action_logger(self.rhodecode_user, 'new_user', '', '', self.sa)
        except formencode.Invalid, errors:
            return htmlfill.render(
                render('admin/users_groups/users_group_edit.html'),
                defaults=errors.value,
                errors=errors.error_dict or {},
                prefix_error=False,
                encoding="UTF-8")
        except Exception:
            log.error(traceback.format_exc())
            h.flash(_('error occurred during update of users group %s') \
                    % request.POST.get('users_group_name'), category='error')

        return redirect(url('users_groups'))



    def delete(self, id):
        """DELETE /users_groups/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('users_group', id=ID),
        #           method='delete')
        # url('users_group', id=ID)

    def show(self, id, format='html'):
        """GET /users_groups/id: Show a specific item"""
        # url('users_group', id=ID)

    def edit(self, id, format='html'):
        """GET /users_groups/id/edit: Form to edit an existing item"""
        # url('edit_users_group', id=ID)

        c.users_group = self.sa.query(UsersGroup).get(id)
        if not c.users_group:
            return redirect(url('users_groups'))

        c.users_group.permissions = {}
        c.group_members = [(x.user_id, x.user.username) for x in
                           c.users_group.members]
        print c.group_members, 'x' * 100
        c.available_members = [(x.user_id, x.username) for x in
                               self.sa.query(User).all()]
        defaults = c.users_group.get_dict()

        return htmlfill.render(
            render('admin/users_groups/users_group_edit.html'),
            defaults=defaults,
            encoding="UTF-8",
            force_defaults=False
        )
