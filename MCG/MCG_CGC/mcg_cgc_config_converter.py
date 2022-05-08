#   FILE:           mcg_cgc_config_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigConverter class, which allows to
#       generate source code modules from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           8 MAY 2022
#
#   LICENSE:
#       This file is part of Mod Code Generator (MCG).
#
#       MCG is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       MCG is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#       GNU General Public License for more details.
#
#       Under Section 7 of GPL version 3, you are granted additional
#       permissions described in the MCG Output Exception, version 1, which
#       copy you should have received along with this program.
#
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


import datetime
from mcg_cgc_module import Module


# Description:
# This class allows to generate source code modules from the configuration file.
class ConfigConverter(object):

    # Description:
    # This method generates source code modules from the configuration file.
    @staticmethod
    def generate_code_from_config_file(config_file):

        # get date
        date = datetime.datetime.now()

        # set file index
        file_index = 0
        # set number of config file lines
        number_of_config_file_lines = len(config_file)

        # continue conversion until end of the configuration file is reached
        while file_index < number_of_config_file_lines:
            tbd = ""
            break
