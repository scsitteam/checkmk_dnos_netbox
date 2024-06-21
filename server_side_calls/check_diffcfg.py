# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
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

from collections.abc import Iterator

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    replace_macros,
    Secret,
)


class Params(BaseModel, frozen=True):
    host: str | None = None
    netbox: str
    netbox_token: Secret
    server: str
    server_token: Secret
    ignore: list[str] | None = None


def commands_function(
    params: Params,
    host_config: object,
) -> Iterator[ActiveCheckCommand]:
    command_arguments = []

    if 'host' in params:
        command_arguments += ['--host', params.host]
    else:
        command_arguments += ['--host', replace_macros('$HOSTNAME$', host_config.macros)]

    command_arguments += ['--netbox', params.netbox]
    command_arguments += ['--netbox-token', params.netbox_token.unsafe()]
    command_arguments += ['--server', replace_macros(params.server, host_config.macros)]
    command_arguments += ['--server-token', params.server_token.unsafe()]

    for item in params.ignore:
        command_arguments += ['--ignore', item]

    yield ActiveCheckCommand(
        service_description='Config Diff',
        command_arguments=command_arguments,
    )


active_check_crl_url = ActiveCheckConfig(
    name='diffcfg',
    parameter_parser=Params.model_validate,
    commands_function=commands_function,
)
