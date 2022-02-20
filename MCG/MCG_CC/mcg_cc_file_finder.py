#   FILE:           mcg_cc_file_finder.py
#
#   DESCRIPTION:
#       This module contains definition of FileFinder class, which is child
#       class or Reader class and is responsible for finding .exml files, which
#       describe model content.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           20 FEB 2022
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


from os import listdir
from mcg_cc_reader import Reader
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_logger import Logger


# Class:
# FileFinder()
#
# Description:
# This is child class responsible for finding .exml files, which describe model content.
class FileFinder(Reader):

    # initialize class data
    activity_dir_path = ""
    interface_dir_path = ""
    activity_source_list = []
    interface_source_list = []
    component_index = 0
    package_index = 0
    number_of_activity_sources = 0

    # initialize file finder list data
    model_element_name = ""
    activity_source = ""
    activity_file = []
    input_interface_source = ""
    input_interface_file = []
    output_interface_source = ""
    output_interface_file = []
    local_data_source = ""
    local_data_file = []

    # indexes of file finder list
    FILES_FOUND_INDEX = 0
    MODEL_ELEMENT_NAME_INDEX = 1
    ACTIVITY_SOURCE_INDEX = 2
    ACTIVITY_FILE_INDEX = 3
    INPUT_INTERFACE_SOURCE_INDEX = 4
    INPUT_INTERFACE_FILE_INDEX = 5
    OUTPUT_INTERFACE_SOURCE_INDEX = 6
    OUTPUT_INTERFACE_FILE_INDEX = 7
    LOCAL_DATA_SOURCE_INDEX = 8
    LOCAL_DATA_FILE_INDEX = 9

    # Method:
    # set_model_dir_path()
    #
    # Description:
    # This method sets path to model directory with .exml files, which describe model content.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def set_model_dir_path(model_dir_path):

        # get activity directory path
        FileFinder.activity_dir_path = model_dir_path + str("\\Standard.Activity")
        # get interface directory path
        FileFinder.interface_dir_path = model_dir_path + str("\\Standard.Interface")

        # get list of activity sources, i.e. names of .exml files
        FileFinder.activity_source_list = listdir(FileFinder.activity_dir_path)
        # get list of interface sources, i.e. names of .exml files
        FileFinder.interface_source_list = listdir(FileFinder.interface_dir_path)

        # get number of activity .exml files
        FileFinder.number_of_activity_sources = len(FileFinder.activity_source_list)

    # Method:
    # clear_collected_data()
    #
    # Description:
    # This method clears collected data, which represents either component or package element.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def clear_collected_data():

        # clear collected data
        FileFinder.model_element_name = ""
        FileFinder.activity_source = ""
        FileFinder.activity_file = []
        FileFinder.input_interface_source = ""
        FileFinder.input_interface_file = []
        FileFinder.output_interface_source = ""
        FileFinder.output_interface_file = []
        FileFinder.local_data_source = ""
        FileFinder.local_data_file = []

    # Method:
    # check_interface_file()
    #
    # Description:
    # This method checks if content of given interface file represents desired interface element.
    #
    # Method:
    # This method returns interface marker.
    @staticmethod
    def check_interface_file(model_element_type, interface_type, interface_file):

        # interface marker shows whether interface was found or not
        interface_found = False

        # search for interface details in interface file
        for i in range(0, len(interface_file)):

            # if given line contains definition of desired interface type
            if (interface_type in interface_file[i]) and ("Standard.Interface" in interface_file[i]) and \
                    (FileFinder.model_element_name in interface_file[i + 1]) and \
                    (model_element_type in interface_file[i + 1]):

                # change interface marker
                interface_found = True
                # exit "for i in range" loop
                break

        # return interface marker
        return interface_found

    # Method:
    # find_interface_files()
    #
    # Description:
    # This function looks for content of .exml files, which represent interface elements of either
    # component or package element.
    #
    # Returns:
    # This method returns interface marker.
    @staticmethod
    def find_interface_files(model_element_type):

        # find interface files
        Logger.save_in_log_file("*** find interface files")

        # interface markers show whether interface was found or not
        interface_found = False
        input_interface_found = False
        output_interface_found = False
        local_data_found = False

        # find input interface element
        for interface_source in FileFinder.interface_source_list:
            # get interface file path
            interface_file_path = FileFinder.interface_dir_path + str("\\") + str(interface_source)

            # open file and read content, then close file
            interface_file_disk = open(interface_file_path, "r")
            interface_file = interface_file_disk.readlines()
            interface_file = [line.strip() for line in interface_file]
            interface_file_disk.close()

            # check interface file
            input_interface_found = FileFinder.check_interface_file(model_element_type,
                                                                    "Input Interface",
                                                                    interface_file)

            # if input interface element has been found
            if input_interface_found:
                # set input interface source
                FileFinder.input_interface_source = interface_source
                # set input interface file
                FileFinder.input_interface_file = interface_file
                # break "for interface_source in" loop
                break

        # find output interface element
        for interface_source in FileFinder.interface_source_list:
            # get interface file path
            interface_file_path = FileFinder.interface_dir_path + str("\\") + str(interface_source)

            # open file and read content, then close file
            interface_file_disk = open(interface_file_path, "r")
            interface_file = interface_file_disk.readlines()
            interface_file = [line.strip() for line in interface_file]
            interface_file_disk.close()

            # check interface file
            output_interface_found = FileFinder.check_interface_file(model_element_type,
                                                                     "Output Interface",
                                                                     interface_file)

            # if output interface element has been found
            if output_interface_found:
                # set output interface source
                FileFinder.output_interface_source = interface_source
                # set output interface file
                FileFinder.output_interface_file = interface_file
                # break "for interface_source in" loop
                break

        # find local data element
        for interface_source in FileFinder.interface_source_list:
            # get interface file path
            interface_file_path = FileFinder.interface_dir_path + str("\\") + str(interface_source)

            # open file and read content, then close file
            interface_file_disk = open(interface_file_path, "r")
            interface_file = interface_file_disk.readlines()
            interface_file = [line.strip() for line in interface_file]
            interface_file_disk.close()

            # check interface file
            local_data_found = FileFinder.check_interface_file(model_element_type,
                                                               "Local Data",
                                                               interface_file)

            # if local data element has been found
            if local_data_found:
                # set local data source
                FileFinder.local_data_source = interface_source
                # set local data file
                FileFinder.local_data_file = interface_file
                # break "for interface_source in" loop
                break

        # check if interface files have been found
        if "Standard.Component" in model_element_type:
            # if input interface element has not been found
            if not input_interface_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_INP_INT_IN_COM, "none", "none")
            # if output interface element has not been found
            if not output_interface_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_OUT_INT_IN_COM, "none", "none")
            # if local data element has not been found
            if not local_data_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_LOC_DAT_IN_COM, "none", "none")
        else:
            # if input interface element has not been found
            if not input_interface_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_INP_INT_IN_PAC, "none", "none")
            # if output interface element has not been found
            if not output_interface_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_OUT_INT_IN_PAC, "none", "none")
            # if local data element has not been found
            if not local_data_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_NO_LOC_DAT_IN_PAC, "none", "none")

        # if all interface files have been found
        if input_interface_found and output_interface_found and local_data_found:
            # change interface marker
            interface_found = True

        # return interface marker
        return interface_found

    # Method:
    # check_activity_file()
    #
    # Description:
    # This method checks if content of activity file represents desired activity element.
    #
    # Returns:
    # This method returns activity marker and model element name.
    @staticmethod
    def check_activity_file(model_element_type, activity_file):

        # activity marker shows whether activity was found or not
        activity_found = False

        # model element name
        model_element_name = ""

        # search for activity details in activity file
        for i in range(0, len(activity_file)):

            # if given line contains definition of activity diagram
            if ("Standard.Activity" in activity_file[i]) and (model_element_type in activity_file[i + 1]):
                # change activity marker
                activity_found = True
                # get line
                line = activity_file[i + 1]
                # get line number
                line_number = i + 2
                # get model element name
                model_element_name = FileFinder.get_name(line, line_number)
                # exit "for i in range" loop
                break

        # return activity marker and model element name
        return activity_found, model_element_name

    # Method:
    # find_activity_file()
    #
    # Description:
    # This function looks for content of .exml file, which represents activity element of either
    # component or package element.
    #
    # Returns:
    # This method returns activity marker.
    @staticmethod
    def find_activity_file(model_element_type):

        # find activity files
        Logger.save_in_log_file("*** find activity file")

        # get source list index
        if "Standard.Component" in model_element_type:
            # set activity index to component index
            activity_index = FileFinder.component_index
        else:
            # set activity index to package index
            activity_index = FileFinder.package_index

        # activity marker shows whether activity was found or not
        activity_found = False

        # repeat until activity is not found
        while not activity_found:

            # if all sources have not been read yet
            if activity_index < FileFinder.number_of_activity_sources:

                # get activity file path
                activity_file_path = FileFinder.activity_dir_path + str("\\") + \
                                     str(FileFinder.activity_source_list[activity_index])

                # get activity source
                activity_source = FileFinder.activity_source_list[activity_index]

                # increment activity index
                activity_index = activity_index + 1

                # open file and read content, then close file
                activity_file_disk = open(activity_file_path, "r")
                activity_file = activity_file_disk.readlines()
                activity_file = [line.strip() for line in activity_file]
                activity_file_disk.close()

                # check activity file
                activity_found, model_element_name = FileFinder.check_activity_file(model_element_type,
                                                                                    activity_file)

                # if activity has been found
                if activity_found:
                    # set model element name
                    FileFinder.model_element_name = model_element_name
                    # set activity source
                    FileFinder.activity_source = activity_source
                    # set activity file
                    FileFinder.activity_file = activity_file

            # else if end of source list is reached
            else:
                # exit "while not activity_found" loop
                break

        # set source list index
        if "Standard.Component" in model_element_type:
            # set component index to activity index
            FileFinder.component_index = activity_index
        else:
            # set package index to activity index
            FileFinder.package_index = activity_index

        # return activity marker
        return activity_found

    # Method:
    # find_files()
    #
    # Description:
    # This method looks for set of .exml files, which describe entire content of one model element
    # (either component or package element), i.e. activity diagram and related interface elements.
    #
    # Returns:
    # This method returns file finder list, which contains activity and interface files.
    @staticmethod
    def find_files(model_element_type):

        # markers shows whether desired elements were found or not
        files_found = False
        activity_found = False
        interface_found = False

        # clear collected data
        FileFinder.clear_collected_data()

        # file finder
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FILE FINDER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # if model element type is correct
        if ("Standard.Component" in model_element_type) or ("Standard.Package" in model_element_type):

            # find activity file
            activity_found = FileFinder.find_activity_file(model_element_type)

            # find interface files
            if activity_found:
                interface_found = FileFinder.find_interface_files(model_element_type)

        # else display warning notification
        else:
            print()
            print("Unknown model element type in FileFinder.find_next_file_set() function: " + str(model_element_type))
            print()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # check activity and interface markers
        if activity_found and interface_found:
            # change files marker
            files_found = True

            # print details
            if "Standard.Component" in model_element_type:
                Logger.save_in_log_file("\nComponent Source:    " + str(FileFinder.activity_source))
                Logger.save_in_log_file("Component Name:      " + str(FileFinder.model_element_name))
            else:
                Logger.save_in_log_file("\nPackage Source:      " + str(FileFinder.activity_source))
                Logger.save_in_log_file("Package Name:        " + str(FileFinder.model_element_name))

            Logger.save_in_log_file("")
            Logger.save_in_log_file("Interface Source:    " + str(FileFinder.input_interface_source))
            Logger.save_in_log_file("Interface Type:      " + str("Input Interface"))

            Logger.save_in_log_file("")
            Logger.save_in_log_file("Interface Source:    " + str(FileFinder.output_interface_source))
            Logger.save_in_log_file("Interface Type:      " + str("Output Interface"))

            Logger.save_in_log_file("")
            Logger.save_in_log_file("Interface Source:    " + str(FileFinder.local_data_source))
            Logger.save_in_log_file("Interface Type:      " + str("Local Data"))

        else:
            # clear once again collected data before return
            FileFinder.clear_collected_data()

            # files not found
            Logger.save_in_log_file("FILES NOT FOUND")

        # end of file finder
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF FILE FINDER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to file finder list
        file_finder_list = []
        file_finder_list.insert(FileFinder.FILES_FOUND_INDEX, files_found)
        file_finder_list.insert(FileFinder.MODEL_ELEMENT_NAME_INDEX, FileFinder.model_element_name)
        file_finder_list.insert(FileFinder.ACTIVITY_SOURCE_INDEX, FileFinder.activity_source)
        file_finder_list.insert(FileFinder.ACTIVITY_FILE_INDEX, FileFinder.activity_file)
        file_finder_list.insert(FileFinder.INPUT_INTERFACE_SOURCE_INDEX, FileFinder.input_interface_source)
        file_finder_list.insert(FileFinder.INPUT_INTERFACE_FILE_INDEX, FileFinder.input_interface_file)
        file_finder_list.insert(FileFinder.OUTPUT_INTERFACE_SOURCE_INDEX, FileFinder.output_interface_source)
        file_finder_list.insert(FileFinder.OUTPUT_INTERFACE_FILE_INDEX, FileFinder.output_interface_file)
        file_finder_list.insert(FileFinder.LOCAL_DATA_SOURCE_INDEX, FileFinder.local_data_source)
        file_finder_list.insert(FileFinder.LOCAL_DATA_FILE_INDEX, FileFinder.local_data_file)

        # return file finder list
        return file_finder_list
