#   FILE:           mcg_cc_main.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Converter Component (CC)
#       and is responsible for conversion of component and package content from
#       .exml file into configuration file, which will be used by Mod Code Generator
#       (MCG) Code Generator Component (CGC) to generate C code for the model.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           10 OCT 2021
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
from mcg_cc_supporter import Supporter
from mcg_cc_file_finder import FileFinder
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_component_reader import ComponentReader
from mcg_cc_component_sorter import ComponentSorter
from mcg_cc_component_converter import ComponentConverter
from mcg_cc_package_reader import PackageReader
from mcg_cc_package_sorter import PackageSorter
from mcg_cc_package_converter import PackageConverter


# Function:
# process_components()
#
# Description:
# This function is responsible for processing of component content from .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def process_components():

    # files marker shows whether desired component files were found or not
    files_found = True

    # repeat until all components are converted into configuration file
    while files_found:

        # find component files
        file_finder_list = FileFinder.find_files("Standard.Component")
        # get files marker
        files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

        # check errors
        ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                  file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                  "Standard.Component")

        # if component files were found
        if files_found:

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


# Function:
# process_packages()
#
# Description:
# This function is responsible for processing of package content from .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def process_packages():

    # files marker shows whether desired package files were found or not
    files_found = True

    # repeat until all packages are converted into configuration file
    while files_found:

        # find package files
        file_finder_list = FileFinder.find_files("Standard.Package")
        # get files marker
        files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

        # check errors
        ErrorHandler.check_errors(file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                  file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                  "Standard.Package")

        # if package files were found
        if files_found:

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


# Function:
# convert_model()
#
# Description:
# This is main function of this module, which invokes conversion of model content in form of .exml files
# into configuration file.
#
# Returns:
# This function does not return anything.
def convert_model():

    # process components content from .exml files into configuration file
    process_components()

    # process packages content from .exml files into configuration file
    process_packages()


# Mod Code Generator (MCG) Converter Component (CC) entrance

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
if len(argv) - 1 == Supporter.NUMBER_OF_MCG_CC_CMD_LINE_ARGS:

    # get model directory path from cmd line argument
    model_dir_path = str(argv[1])

    # set path to model directory
    FileFinder.set_paths(model_dir_path)

    # convert model
    convert_model()

# else display info and exit
else:
    print("Incorrect number of command line arguments, MCG CC process cancelled.")
