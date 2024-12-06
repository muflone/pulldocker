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


class Profile():
    def __init__(self,
                 name: str,
                 status: bool,
                 directory: str,
                 cache: str = None,
                 remotes: list = None):
        self.name = name
        self.directory = directory
        self.status = status
        self.cache = cache
        self.remotes = remotes

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'name="{self.name}", '
                f'status={self.status}'
                ')')
