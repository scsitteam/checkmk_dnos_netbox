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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    ListOf,
    RegExp,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
try:
    from cmk.gui.plugins.wato.active_checks import RulespecGroupActiveChecks
except Exception:
    from cmk.gui.plugins.wato.active_checks.common import RulespecGroupActiveChecks


def _valuespec_active_checks_diffcfg():
    return Dictionary(
        title = "Check diff of commited and rendered config",
        help = "Check if rendered config of a Switch differs from the commited config.",
        elements = [
            (
                'host',
                TextAscii(
                    title = _("Host"),
                    allow_empty = False
                ),
            ),
            (
                'netbox',
                TextAscii(
                    title = _("Netbox-Server"),
                    allow_empty = False
                ),
            ),
            (
                'netbox-token',
                TextAscii(
                    title = _("Netbox API Token"),
                    allow_empty = False
                ),
            ),
            (
                'server',
                TextAscii(
                    title = _("HTTP Server"),
                    allow_empty = False
                ),
            ),
            (
                'server-token',
                TextAscii(
                    title = _("HTTP Server API Token"),
                    allow_empty = False
                ),
            ),            
            (
                'ignore',
                ListOf(
                    valuespec=RegExp(
                        title = _("Pattern (Regex)"),
                        size = 50,
                        mode = RegExp.infix,
                    ),
                    title = _("Ignore lines"),
                    help=_(
                        "You can optionally define one or multiple regular expressions."
                        " Matching lines are excluded."
                        " This allows to ignore lines which can never be found in both configs."
                    ),
                    allow_empty = False
                ),
            ),
        ],
        required_keys=['netbox', 'netbox-token', 'server', 'server-token'],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupActiveChecks,
        match_type='all',
        name='active_checks:diffcfg',
        valuespec=_valuespec_active_checks_diffcfg,
    ))
