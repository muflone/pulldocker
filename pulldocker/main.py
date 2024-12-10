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
    pulldocker = PullDocker(filename=options.configuration)
    for profile in pulldocker.configuration.get_profiles():
        print(profile)
        if profile.status:
            repository = profile.repository
            repository.find_head()
            hash_initial = repository.get_hash()
            branch = repository.get_branch()
            print(repository.get_author(),
                  repository.get_email(),
                  repository.get_datetime(),
                  hash_initial,
                  repository.get_summary())

            # Execute git pull on each remote
            remotes = profile.remotes or repository.get_remotes()
            for remote in remotes:
                repository.pull(remote=remote,
                                branch=branch)
            # Compare hash to detect if new changes arrived
            repository.find_head()
            hash_final = repository.get_hash()
            if hash_initial != hash_final:
                print(repository.get_author(),
                      repository.get_email(),
                      repository.get_datetime(),
                      hash_final,
                      repository.get_summary())
                for tag_name in repository.get_tags():
                    tag = repository.get_tag(tag_name)
                    if tag.hash == hash_final:
                        # This is the latest tag
                        print('This is the latest tag:', tag.name)
        print()


if __name__ == '__main__':
    main()
