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

import yaml

from pulldocker.profile import Profile


class YamlParser(object):
    def __init__(self, filename: str):
        self.profiles = {}
        with open(filename, 'r') as file:
            values = {item['NAME']: item
                      for item in yaml.load_all(stream=file,
                                                Loader=yaml.Loader)
                      if item}
        # Load profiles
        for name, values in values.items():
            self.profiles[name] = Profile(
                name=name,
                status=values.get('STATUS', True),
                directory=values['REPOSITORY_DIR'],
                remotes=values.get('REMOTES'),
                tags_regex=values.get('TAGS'),
                compose_file=values.get('COMPOSE_FILE'),
                detached=values.get('DETACHED', True),
                build=values.get('BUILD', False),
                recreate=values.get('RECREATE', False),
                command=values.get('COMMAND'),
                commands_before=values.get('BEFORE'),
                commands_after=values.get('AFTER'),
                commands_begin=values.get('BEGIN'),
                commands_end=values.get('END'),
            )

    def get_profiles(self) -> list[Profile]:
        """
        Return the configuration profiles

        :return: profiles list
        """
        return list(self.profiles.values())
