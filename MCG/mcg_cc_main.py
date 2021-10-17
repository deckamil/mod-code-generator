#   FILE:           mcg_cc_main.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Converter Component (CC)
#       and it contains definition of MCGCCMain class, which uses other MCG CC classes
#       to convert component and package content from .exml file into configuration
#       file. The configuration file will be used by Mod Code Generator (MCG) Code
#       Generator Component (CGC) to generate C code from the model.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           17 OCT 2021
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
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


from sys import argv
from mcg_cc_file_finder import FileFinder
from mcg_cc_converter import Converter
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_logger import Logger
from mcg_cc_component_reader import ComponentReader
from mcg_cc_component_sorter import ComponentSorter
from mcg_cc_component_converter import ComponentConverter
from mcg_cc_package_reader import PackageReader
from mcg_cc_package_sorter import PackageSorter
from mcg_cc_package_converter import PackageConverter


# Class:
# MCGCCMain()
#
# Description:
# This is base class, which uses other MCG CC classes to generate configuration file.
class MCGCCMain(object):

    # This parameter defines expected number of command line arguments passed to MCG CC,
    # i.e. list of arguments:
    #       - model dir path
    #       - output dir path
    #       - print additional info flag
    NUMBER_OF_MCG_CC_CMD_LINE_ARGS = 3

    # indexes of MCG CC command line arguments
    MODEL_DIR_PATH_INDEX = 1
    OUTPUT_DIR_PATH_INDEX = 2
    PRINT_EXTRA_INFO_INDEX = 3

    # This parameter allows other MCG CC classes to determine whether to print extra information
    # during conversion process or not.
    PRINT_EXTRA_INFO = False

    # Method:
    # main()
    #
    # Description:
    # This is main method of MCGCCMain class.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def main():

        # display short notice
        print()
        print("Mod Code Generator (MCG)")
        print("Copyright (C) 2021 Kamil Deć github.com/deckamil")
        print("This is Converter Component (CC) of Mod Code Generator (MCG)")
        print()
        print("License GPLv3+: GNU GPL version 3 or later.")
        print("This is free software; see the source for copying conditions. There is NO")
        print("warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
        print()

        # check if number of command line arguments is correct
        if len(argv) - 1 == MCGCCMain.NUMBER_OF_MCG_CC_CMD_LINE_ARGS:

            # get model directory path from cmd line argument
            model_dir_path = str(argv[MCGCCMain.MODEL_DIR_PATH_INDEX])
            # get output directory path from cmd line argument
            output_dir_path = str(argv[MCGCCMain.OUTPUT_DIR_PATH_INDEX])

            # get extra info flag from cmd line argument
            if "EXTRA_INFO" in str(argv[MCGCCMain.PRINT_EXTRA_INFO_INDEX]):
                MCGCCMain.PRINT_EXTRA_INFO = True
            else:
                MCGCCMain.PRINT_EXTRA_INFO = False

            # set path to model directory
            FileFinder.set_model_path(model_dir_path)
            # set path to configuration file directory
            Converter.set_configuration_file_path(output_dir_path)
            # set path to log file directory
            Logger.set_log_file_path(output_dir_path)

            # convert model
            MCGCCMain.convert_model()

        # else display info and exit
        else:
            print("Incorrect number of command line arguments, MCG CC process cancelled.")
            print("Usage: python mcg_cc_main.py \"<model_dir_path>\" \"<output_dir_path>\" \"<extra_info>\"")
            print("Arguments:")
            print("    <model_dir_path>       Path to model directory, where all catalogs with .exml files are stored")
            print("    <output_dir_path>      Path to output directory, where results from MCG will be saved")
            print("    <extra_info>           Flag, which defines whether to print extra info during MCG process")
            print("                           or not, can be set to either EXTRA_INFO or NO_INFO")
            print("")
            print("Keep specific order of arguments, as pointed in usage above.")
            print("See Mod Code Generator Manual for further information.")

    # Method:
    # convert_model()
    #
    # Description:
    # This method invokes conversion of model content in form of .exml files into configuration file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def convert_model():

        # process components content from .exml files into configuration file
        MCGCCMain.process_components()

        # process packages content from .exml files into configuration file
        MCGCCMain.process_packages()

    # Method:
    # process_components()
    #
    # Description:
    # This method is responsible for processing of component content from .exml file
    # into configuration file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def process_components():

        # files marker shows whether desired component files were found or not
        files_found = True

        # repeat until all components are converted into configuration file
        while files_found:

            # file searching
            Logger.record_in_log("******************************** FILE SEARCHING *******************************")

            # find component files
            file_finder_list = FileFinder.find_files("Standard.Component")
            # get files marker
            files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

            # check errors
            ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                      file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                      "Standard.Component")

            # end of file searching
            Logger.record_in_log("**************************** END OF FILE SEARCHING ****************************")

            # if component files were found
            if files_found:

                # component processing
                Logger.record_in_log("***************************** COMPONENT PROCESSING ****************************")

                # initialize component reader
                component_reader = ComponentReader(file_finder_list)
                # read component content
                component_reader_list = component_reader.read_component()

                # check errors
                ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                          file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                          "Standard.Component")

                # initialize component sorter
                component_sorter = ComponentSorter(component_reader_list)
                # sort component content
                component_sorter_list = component_sorter.sort_component()

                # check errors
                ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                          file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                          "Standard.Component")

                # initialize component converter
                component_converter = ComponentConverter(component_reader_list, component_sorter_list)
                # convert component content
                component_converter.convert_component()

                # end of component processing
                Logger.record_in_log("************************* END OF COMPONENT PROCESSING *************************")

    # Method:
    # process_packages()
    #
    # Description:
    # This method is responsible for processing of package content from .exml file
    # into configuration file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def process_packages():

        # files marker shows whether desired package files were found or not
        files_found = True

        # repeat until all packages are converted into configuration file
        while files_found:

            # file searching
            Logger.record_in_log("******************************** FILE SEARCHING *******************************")

            # find package files
            file_finder_list = FileFinder.find_files("Standard.Package")
            # get files marker
            files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

            # check errors
            ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                      file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                      "Standard.Package")

            # end of file searching
            Logger.record_in_log("**************************** END OF FILE SEARCHING ****************************")

            # if package files were found
            if files_found:

                # package processing
                Logger.record_in_log("****************************** PACKAGE PROCESSING *****************************")

                # initialize package reader
                package_reader = PackageReader(file_finder_list)
                # read package content
                package_reader_list = package_reader.read_package()

                # check errors
                ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                          file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                          "Standard.Package")

                # initialize package sorter
                package_sorter = PackageSorter(package_reader_list)
                # sort package content
                package_sorter_list = package_sorter.sort_package()

                # check errors
                ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                          file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                          "Standard.Package")

                # initialize package converter
                package_converter = PackageConverter(package_reader_list, package_sorter_list)
                # convert package content
                package_converter.convert_package()

                # end of package processing
                Logger.record_in_log("************************** END OF PACKAGE PROCESSING **************************")


# Mod Code Generator (MCG) Converter Component (CC) entrance
MCGCCMain.main()
