#   FILE:           mcg_cc_main.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Converter Component (CC)
#       and it contains definition of Main class, which uses other MCG CC classes
#       to convert model content from set of .exml files into configuration file.
#
#   COPYRIGHT:      Copyright (C) 2021-2024 Kamil Deć github.com/deckamil
#   DATE:           27 JAN 2024
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
from mcg_cc_file_finder import FileFinder
from mcg_cc_file_reader import FileReader
from mcg_cc_file_checker import FileChecker
from mcg_cc_module_sorter import ModuleSorter
from mcg_cc_module_converter import ModuleConverter
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_logger import Logger


# Description:
# This is main class, which controls conversion process of model content into configuration file.
class Main(object):

    # This parameter defines expected number of command line arguments passed to MCG CC,
    # i.e. list of arguments:
    #       - model dir path
    #       - output dir path
    NUMBER_OF_MCG_CC_CMD_LINE_ARGS = 2

    # indexes of MCG CC command line arguments
    MODEL_DIR_PATH_INDEX = 1
    OUTPUT_DIR_PATH_INDEX = 2

    # MCG CC version
    MCG_CC_VERSION = "v0.5.0-in-dev"

    # Description:
    # This is main method, which display short notice and start conversion process.
    @staticmethod
    def main():

        # display short notice
        print()
        print("Mod Code Generator (MCG)")
        print("Copyright (C) 2021-2024 Kamil Deć github.com/deckamil")
        print("This is Converter Component (CC) of Mod Code Generator (MCG)")
        print(Main.MCG_CC_VERSION)
        print()
        print("License GPLv3+: GNU GPL version 3 or later.")
        print("This is free software; see the source for copying conditions. There is NO")
        print("warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
        print()

        # check if number of command line arguments is correct
        if len(argv) - 1 == Main.NUMBER_OF_MCG_CC_CMD_LINE_ARGS:

            # get model directory path from cmd line argument
            model_dir_path = str(argv[Main.MODEL_DIR_PATH_INDEX])
            # get output directory path from cmd line argument
            output_dir_path = str(argv[Main.OUTPUT_DIR_PATH_INDEX])

            # set path to model directory
            FileFinder.set_model_dir_path(model_dir_path)
            # set path to configuration file
            ModuleConverter.set_configuration_file_path(output_dir_path)
            # set path to log file
            Logger.set_log_file_path(output_dir_path)

            # convert model
            Main.convert_model()

        # else display info and exit
        else:
            print("Incorrect number of command line arguments, MCG CC process cancelled.")
            print("Usage: python mcg_cc_main.py \"<model_dir_path>\" \"<output_dir_path>\"")
            print("Arguments:")
            print("    <model_dir_path>       Path to model directory, where all catalogs with .exml files are stored")
            print("    <output_dir_path>      Path to output directory, where results from MCG CC will be saved")
            print("")
            print("Keep specific order of arguments, as pointed in usage above.")
            print("See Mod Code Generator Manual for further details.")

    # Description:
    # This method invokes conversion of model content in form of .exml files into configuration file.
    @staticmethod
    def convert_model():

        # saves log file header
        Logger.save_log_file_header()
        # saves configuration file header
        ModuleConverter.save_configuration_file_header()

        # flag to distinguish if set of matching .exml files has been found for further conversion
        files_found = True

        # repeat until all modules are converted into configuration file
        while files_found:

            # find module files
            file_finder_list = FileFinder.find_files()
            # get files flag
            files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

            # check errors
            ErrorHandler.check_errors()

            # if files have been found
            if files_found:
                # initialize file reader
                file_reader = FileReader(file_finder_list)
                # read module content
                file_reader_list = file_reader.read_files()

                # initialize file checker
                # file_checker = FileChecker(file_reader_list)
                # check module content
                # file_checker.check_files()

                # check errors
                # ErrorHandler.check_errors()

                # initialize module sorter
                module_sorter = ModuleSorter(file_reader_list)
                # sort module content
                module_sorter.sort_module()

                # check errors
                # ErrorHandler.check_errors()

                # initialize module converter
                module_converter = ModuleConverter(file_finder_list, file_reader_list)
                # convert module content
                module_converter.convert_module()

        # saves configuration file footer
        ModuleConverter.save_configuration_file_footer()
        # saves log file footer
        Logger.save_log_file_footer()


# Mod Code Generator (MCG) Converter Component (CC) entrance
Main.main()
