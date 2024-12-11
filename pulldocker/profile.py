##
#     Project: PullDocker
# Description: Watch git repositories for Docker compose configuration changes
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2024 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import datetime
import subprocess

from pulldocker.repository import Repository
from pulldocker.tag import Tag


class Profile():
    def __init__(self,
                 name: str,
                 status: bool,
                 directory: str,
                 remotes: list[str] = None,
                 tags_regex: str = None,
                 compose_file: str = None,
                 detached: bool = True,
                 build: bool = False,
                 recreate: bool = False,
                 command: list[str] | str = None,
                 commands_before: list[list[str] | str] = None,
                 commands_after: list[list[str] | str] = None,
                 commands_begin: list[list[str] | str] = None,
                 commands_end: list[list[str] | str] = None,
                 ):
        self.name = name
        self.status = status
        self.remotes = remotes
        self.directory = directory
        self.repository = Repository(directory=directory)
        self.tags_regex = '.*' if tags_regex == '*' else tags_regex
        self.compose_file = compose_file
        self.detached = detached
        self.build = build
        self.recreate = recreate
        self.command = command
        self.commands_before = commands_before or []
        self.commands_after = commands_after or []
        self.commands_begin = commands_begin or []
        self.commands_end = commands_end or []

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'name="{self.name}", '
                f'status={self.status}'
                ')')

    def _execute_commands(self,
                          commands: list[list[str] | str],
                          tag: Tag) -> None:
        """
        Execute commands
        """
        now = datetime.datetime.now()
        replacements_map = {
            '${DATE}': now.strftime('%Y-%m-%d'),
            '${TIME}': now.strftime('%H:%M:%S'),
        }
        if tag is not None:
            replacements_map['${TAG}'] = tag.name
            replacements_map['${TAG_AUTHOR}'] = tag.author
            replacements_map['${TAG_MESSAGE}'] = tag.message
            replacements_map['${TAG_SUMMARY}'] = tag.summary
            replacements_map['${TAG_HASH}'] = tag.hash
            replacements_map['${TAG_DATE}'] = tag.date_time.strftime('%Y-%m-%d')
            replacements_map['${TAG_TIME}'] = tag.date_time.strftime('%H:%M:%S')

        for command in commands:
            new_arguments = []
            for argument in command if isinstance(command, list) else [command]:
                for key, value in replacements_map.items():
                    argument = argument.replace(key, value if value is not None else '')
                new_arguments.append(argument)
            subprocess.call(args=new_arguments,
                            shell=not isinstance(command, list),
                            cwd=self.directory)

    def begin(self) -> None:
        """
        Execute commands at the beginning
        """
        self._execute_commands(commands=self.commands_begin,
                               tag=None)

    def end(self) -> None:
        """
        Execute commands at the end
        """
        self._execute_commands(commands=self.commands_end,
                               tag=None)

    def execute(self,
                tag: Tag) -> None:
        """
        Execute commands from the profile
        """
        # Execute commands before docker compose
        self._execute_commands(commands=self.commands_before,
                               tag=tag)
        # Execute docker compose command
        if self.command:
            arguments = self.command
        else:
            arguments = ['docker', 'compose']
            if self.compose_file:
                arguments.extend(['-f', self.compose_file])
            arguments.append('up')
            if self.detached:
                arguments.append('-d')
            if self.build:
                arguments.append('--build')
            if self.recreate:
                arguments.append('--force-recreate')
        self._execute_commands(commands=[arguments],
                               tag=tag)
        # Execute commands after docker compose
        self._execute_commands(commands=self.commands_after,
                               tag=tag)
