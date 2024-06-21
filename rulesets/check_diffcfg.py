# -*- encoding: utf-8; py-indent-offset: 4 -*-
##
# Copyright (C) 2024  Lamberto Grippi <lamberto.grippi@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from typing import Mapping
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    List,
    MatchingScope,
    migrate_to_password,
    Password,
    RegularExpression,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic


def _migrate_diffcfg(model: object) -> Mapping[str, object]:
    return {
        key.replace('-', '_'): value
        for key, value in model.items()
    }


def migrate_string_to_password(model: object):
    if isinstance(model, str):
        model = ("password", model)
    return migrate_to_password(model)


def _form_active_checks_diffcfg():
    return Dictionary(
        elements = {
            'host': DictElement(
                parameter_form=String(
                    title=Title('Host'),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                    macro_support=True,
                ),
                required=False,
            ),
            'netbox': DictElement(
                parameter_form=String(
                    title=Title('Netbox-Server'),
                    custom_validate=(
                        validators.Url([validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS]),
                    ),
                ),
                required=True,
            ),
            'netbox_token': DictElement(
                parameter_form=Password(
                    title=Title('Netbox API Token'),
                    migrate=migrate_string_to_password,
                ),
                required=True,
            ),
            'server': DictElement(
                parameter_form=String(
                    title=Title('HTTP Server'),
                    custom_validate=(
                        validators.Url([validators.UrlProtocol.HTTP, validators.UrlProtocol.HTTPS]),
                    ),
                ),
                required=True,
            ),
            'server_token': DictElement(
                parameter_form=Password(
                    title=Title('HTTP Server API Token'),
                    migrate=migrate_string_to_password,
                ),
                required=True,
            ),
            'ignore': DictElement(
                parameter_form=List(
                    title=Title('Ignore lines'),
                    help_text=Help(
                        'You can optionally define one or multiple regular expressions.'
                        ' Matching lines are excluded.'
                        ' This allows to ignore lines which can never be found in both configs.'
                    ),
                    element_template=RegularExpression(predefined_help_text=MatchingScope.INFIX),
                ),
                required=False,
            ),
        },
        migrate=_migrate_diffcfg,
    )


rule_spec_crl_url = ActiveCheck(
    title=Title('Check diff of commited and rendered config'),
    help_text=Help('Check if rendered config of a Switch differs from the commited config.'),
    topic=Topic.NETWORKING,
    name='diffcfg',
    parameter_form=_form_active_checks_diffcfg,
)
