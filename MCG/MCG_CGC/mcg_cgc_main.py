#   FILE:           mcg_cgc_main.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Code Generator Component (CGC)
#       and it contains definition of Main class, which uses other MCG CGC classes
#       to generate C code from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022-2023 Kamil Deć github.com/deckamil
#   DATE:           25 JUN 2023
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


from sys import argv
from mcg_cgc_logger import Logger
from mcg_cgc_error_handler import ErrorHandler
from mcg_cgc_config_checker import ConfigChecker
from mcg_cgc_config_converter import ConfigConverter


# Description:
# This is main class, which controls C code generation process from the configuration file.
class Main(object):

    # This parameter defines expected number of command line arguments passed to MCG CGC,
    # i.e. list of arguments:
    #       - configuration file path
    #       - output dir path
    NUMBER_OF_MCG_CGC_CMD_LINE_ARGS = 2

    # indexes of MCG CGC command line arguments
    CONFIG_FILE_PATH_INDEX = 1
    OUTPUT_DIR_PATH_INDEX = 2

    # MCG CGC version
    MCG_CGC_VERSION = "v0.3.0-alpha"

    # Description:
    # This is main method, which display short notice and start code generation process.
    @staticmethod
    def main():

        # display short notice
        print()
        print("Mod Code Generator (MCG)")
        print("Copyright (C) 2022-2023 Kamil Deć github.com/deckamil")
        print("This is Code Generator Component (CGC) of Mod Code Generator (MCG)")
        print(Main.MCG_CGC_VERSION)
        print()
        print("License GPLv3+: GNU GPL version 3 or later.")
        print("This is free software; see the source for copying conditions. There is NO")
        print("warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
        print()

        # check if number of command line arguments is correct
        if len(argv) - 1 == Main.NUMBER_OF_MCG_CGC_CMD_LINE_ARGS:

            # get configuration file path from cmd line argument
            config_file_path = str(argv[Main.CONFIG_FILE_PATH_INDEX])
            # get output directory path from cmd line argument
            output_dir_path = str(argv[Main.OUTPUT_DIR_PATH_INDEX])

            # set path to configuration file
            ConfigChecker.set_config_file_path(config_file_path)
            # set path to code directory
            ConfigConverter.set_code_dir_path(output_dir_path)
            # set path to log file
            Logger.set_log_file_path(output_dir_path)

            # generate code
            Main.generate_code()

        # else display info and exit
        else:
            print("Incorrect number of command line arguments, MCG CGC process cancelled.")
            print("Usage: python mcg_cgc_main.py \"<config_file_path>\" \"<output_dir_path>\"")
            print("Arguments:")
            print("    <config_file_path>     Path to configuration file, which contains source data to code generation")
            print("    <output_dir_path>      Path to output directory, where results from MCG CGC will be saved")
            print("")
            print("Keep specific order of arguments, as pointed in usage above.")
            print("See Mod Code Generator Manual for further details.")

    # Description:
    # This method invokes process of code generation from the configuration file.
    @staticmethod
    def generate_code():

        # save log file header
        Logger.save_log_file_header()

        # load content of the configuration file
        ConfigChecker.load_config_file()
        # check errors
        ErrorHandler.check_errors()

        # check content of the configuration file
        ConfigChecker.check_config_file()
        # check errors
        ErrorHandler.check_errors()

        # get content of the configuration file
        config_file = ConfigChecker.get_config_file()
        # generate code from the configuration file
        ConfigConverter.generate_code_from_config_file(config_file)
        # check errors
        ErrorHandler.check_errors()

        # save log file footer
        Logger.save_log_file_footer()


# Mod Code Generator (MCG) Code Generator Component (CGC) entrance
Main.main()
