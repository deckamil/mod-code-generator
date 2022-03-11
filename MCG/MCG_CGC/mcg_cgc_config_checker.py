#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           11 MAR 2022
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


# Class:
# ConfigChecker()
#
# Description:
# This is base class responsible for verification of the configuration file.
class ConfigChecker(object):

    # initialize class data
    config_file = []

    # indexes of config checker list
    CONFIG_FILE_VALIDITY_INDEX = 0
    CONFIG_FILE_INDEX = 1

    # Method:
    # set_config_file_path()
    #
    # Description:
    # This method sets path to configuration file, which contain input configuration to MCG CGC.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def set_config_file_path(config_file_path):

        # open file and read content, then close file
        config_file_disk = open(config_file_path, "r")
        config_file = config_file_disk.readlines()
        config_file = [line.strip() for line in config_file]
        config_file_disk.close()

        # set config file
        ConfigChecker.config_file = config_file

    # Method:
    # check_config_file()
    #
    # Description:
    # This method checks if content of configuration file is correct.
    #
    # Returns:
    # This method returns config checker list, which contains configuration file.
    @staticmethod
    def check_config_file():
        tbd = ""

