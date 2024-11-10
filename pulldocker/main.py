#!/usr/bin/env python3
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

from pulldocker.command_line_options import CommandLineOptions
from pulldocker.pulldocker import PullDocker


def main():
    # Get command-line options
    command_line = CommandLineOptions()
    command_line.add_configuration_arguments()
    options = command_line.parse_options()
    pulldocker = PullDocker()


if __name__ == '__main__':
    main()
