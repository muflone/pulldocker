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
                 cache: str = None,
                 remotes: list[str] = None,
                 tags_regex: str = None,
                 compose_file: str = None,
                 detached: bool = True,
                 build: bool = False,
                 recreate: bool = False,
                 command: list[str] = None,
                 commands_before: list[list[str]] = None,
                 commands_after: list[list[str]] = None,
                 ):
        self.name = name
        self.status = status
        self.cache = cache
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

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'name="{self.name}", '
                f'status={self.status}'
                ')')

    def execute(self,
                tag: Tag):
        """
        Execute commands from the profile
        """
        # Execute commands before docker compose
        for command in self.commands_before:
            arguments = self._process_arguments(arguments=command,
                                                tag=tag)
            subprocess.call(args=arguments,
                            cwd=self.directory)
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
        subprocess.call(args=arguments,
                        cwd=self.directory)
        # Execute commands after docker compose
        for command in self.commands_after:
            arguments = self._process_arguments(arguments=command,
                                                tag=tag)
            subprocess.call(args=arguments,
                            cwd=self.directory)

    def _process_arguments(self,
                           arguments: list[str],
                           tag: Tag
                           ) -> list[str]:
        """
        Process a list of arguments by adding the tag information
        :param arguments: arguments list
        :param tag: tag object
        :return: final arguments list
        """
        result = []
        now = datetime.datetime.now()
        replacements_map = {
            '${TAG}': tag.name,
            '${TAG_AUTHOR}': tag.author,
            '${TAG_MESSAGE}': tag.message,
            '${TAG_SUMMARY}': tag.summary,
            '${TAG_HASH}': tag.hash,
            '${TAG_DATE}': tag.date_time.strftime('%Y-%m-%d'),
            '${TAG_TIME}': tag.date_time.strftime('%H:%M:%S'),
            '${DATE}': now.strftime('%Y-%m-%d'),
            '${TIME}': now.strftime('%H:%M:%S'),
        }
        for argument in arguments:
            for key, value in replacements_map.items():
                argument = argument.replace(key, value if value is not None else '')
            result.append(argument)
        return result
