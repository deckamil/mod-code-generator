#   FILE:           mcg_cc_file_finder.py
#
#   DESCRIPTION:
#       This module contains definition of FileFinder class, which is
#       responsible for finding .exml files, that describe model content.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           28 NOV 2022
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
from mcg_cc_logger import Logger
from mcg_cc_supporter import Supporter


# Description:
# This class allows to find .exml files, which describe model content.
class FileFinder(object):

    # class data
    activity_source_path_list = []
    module_source_path_list = []
    number_of_activity_files = 0
    number_of_module_files = 0
    activity_index = 0
    module_index = 0

    # module and activity finder state
    module_finder_state = 0
    activity_finder_state = 0
    # possible states
    NO_MORE_FILES = 10
    FILE_NOT_FOUND = 20
    FILE_FOUND = 30

    # return data
    module_file = []
    activity_file = []
    module_name = ""
    module_uid = ""
    operation_name = ""
    operation_uid = ""
    activity_name = ""
    activity_uid = ""

    # indexes of return data
    FILES_FOUND_INDEX = 0
    MODULE_FILE_INDEX = 1
    ACTIVITY_FILE_INDEX = 2
    MODULE_NAME_INDEX = 3
    MODULE_UID_INDEX = 4
    OPERATION_NAME_INDEX = 5
    OPERATION_UID_INDEX = 6
    ACTIVITY_NAME_INDEX = 7
    ACTIVITY_UID_INDEX = 8

    # Description:
    # This method sets paths to .exml files, that describe model content.
    @staticmethod
    def set_model_dir_path(model_dir_path):

        # get activity directory path
        activity_dir_path = model_dir_path + str("\\Standard.Activity")
        # get list of activity sources, i.e. names of .exml files
        activity_source_list = listdir(activity_dir_path)
        # get list of activity source paths
        for activity_source in activity_source_list:
            # get activity source path
            FileFinder.activity_source_path_list.append(activity_dir_path + str("\\") + str(activity_source))

        # get component directory path
        component_dir_path = model_dir_path + str("\\Standard.Component")
        # get list of component sources, i.e. names of .exml files
        component_source_list = listdir(component_dir_path)
        # get list of component source paths
        component_source_path_list = []
        for component_source in component_source_list:
            # get component source path
            component_source_path_list.append(component_dir_path + str("\\") + str(component_source))

        # get package directory path
        package_dir_path = model_dir_path + str("\\Standard.Package")
        # get list of package sources, i.e. names of .exml files
        package_source_list = listdir(package_dir_path)
        # get list of package source paths
        package_source_path_list = []
        for package_source in package_source_list:
            # get package source path
            package_source_path_list.append(package_dir_path + str("\\") + str(package_source))

        # get list of module source paths
        FileFinder.module_source_path_list = component_source_path_list + package_source_path_list

        # get number of activity .exml files
        FileFinder.number_of_activity_files = len(FileFinder.activity_source_path_list)

        # get number of module .exml files
        FileFinder.number_of_module_files = len(FileFinder.module_source_path_list)

    # Description:
    # This method clears data, that represents module details.
    @staticmethod
    def clear_return_data():

        # clear return data
        FileFinder.module_file = []
        FileFinder.activity_file = []
        FileFinder.module_name = "UNKNOWN_MODULE_NAME"
        FileFinder.module_uid = "UNKNOWN_MODULE_UID"
        FileFinder.operation_name = "UNKNOWN_OPERATION_NAME"
        FileFinder.operation_uid = "UNKNOWN_OPERATION_UID"
        FileFinder.activity_name = "UNKNOWN_ACTIVITY_NAME"
        FileFinder.activity_uid = "UNKNOWN_ACTIVITY_UID"

    # Description:
    # This method looks for .exml files, that represent module element with operation definition
    @staticmethod
    def find_module_file():

        # record info
        Logger.save_in_log_file("FileFinder", "Looking for module .exml file", False)

        # assume that module with operation definition is not found
        FileFinder.module_finder_state = FileFinder.FILE_NOT_FOUND

        # repeat as long as file is not found
        while FileFinder.module_finder_state == FileFinder.FILE_NOT_FOUND:

            # if all modules have not been checked yet
            if FileFinder.module_index < FileFinder.number_of_module_files:
                # get module source path
                module_source_path = FileFinder.module_source_path_list[FileFinder.module_index]

                # open file and read content, then close file
                module_file_disk = open(module_source_path, "r")
                module_file = module_file_disk.readlines()
                module_file = [line.strip() for line in module_file]
                module_file_disk.close()

                # increment module index
                FileFinder.module_index = FileFinder.module_index + 1

                # check if module contains operation definition
                for i in range(0, len(module_file)):

                    # if module name if found
                    if ("<ID name=" in module_file[i] and
                            ("mc=\"Standard.Component\"" in module_file[i] or
                             "mc=\"Standard.Package\"" in module_file[i]) and
                            "<PID name=" in module_file[i+1]):
                        # get module name
                        FileFinder.module_name = Supporter.get_name(module_file[i], i+1)
                        # get module uid
                        FileFinder.module_uid = Supporter.get_uid(module_file[i], i+1)

                    # if operation is defined in module
                    if "<COMP relation=\"OwnedOperation\">" in module_file[i]:
                        # store module file
                        FileFinder.module_file = module_file
                        # get operation name
                        FileFinder.operation_name = Supporter.get_name(module_file[i+2], i+3)
                        # set module finder state
                        FileFinder.module_finder_state = FileFinder.FILE_FOUND
                        # record info
                        Logger.save_in_log_file("FileFinder",
                                                "Have found module " + FileFinder.module_name + " "
                                                + FileFinder.module_uid + ".exml file", False)
                        # exit 'for i in range' loop
                        break

            else:
                # all modules have been checked already
                FileFinder.module_finder_state = FileFinder.NO_MORE_FILES
                # record info
                Logger.save_in_log_file("FileFinder", "No further .exml files have been found", False)

    # Description:
    # This method looks for .exml files, that represent activity element for module operation
    @staticmethod
    def find_activity_file():

        # record info
        Logger.save_in_log_file("FileFinder", "Looking for activity .exml file", False)

        # assume that activity for module operation is not found
        FileFinder.activity_finder_state = FileFinder.FILE_NOT_FOUND

        # reset activity index
        FileFinder.activity_index = 0

        # repeat as long as file is not found
        while FileFinder.activity_finder_state == FileFinder.FILE_NOT_FOUND:

            # if all activities have not been checked yet
            if FileFinder.activity_index < FileFinder.number_of_activity_files:
                # get activity source path
                activity_source_path = FileFinder.activity_source_path_list[FileFinder.activity_index]

                # open file and read content, then close file
                activity_file_disk = open(activity_source_path, "r")
                activity_file = activity_file_disk.readlines()
                activity_file = [line.strip() for line in activity_file]
                activity_file_disk.close()

                # increment activity index
                FileFinder.activity_index = FileFinder.activity_index + 1

                # check if activity file belongs to module with operation
                for i in range(0, len(activity_file)):

                    # if activity name if found
                    if ("<ID name=" in activity_file[i] and "mc=\"Standard.Activity\"" in activity_file[i] and
                            "<PID name=" in activity_file[i + 1] and
                            ("mc=\"Standard.Component\"" in activity_file[i+1] or
                             "mc=\"Standard.Package\"" in activity_file[i+1])):
                        # get activity name
                        FileFinder.activity_name = Supporter.get_name(activity_file[i], i+1)
                        # get activity uid
                        FileFinder.activity_uid = Supporter.get_uid(activity_file[i], i+1)
                        # get parent module name
                        parent_module_name = Supporter.get_name(activity_file[i+1], i+2)
                        # get parent module uid
                        parent_module_uid = Supporter.get_uid(activity_file[i+1], i+2)
                        # if there is name and uid compatibility
                        if FileFinder.module_name == parent_module_name and FileFinder.module_uid == parent_module_uid:
                            # store activity file
                            FileFinder.activity_file = activity_file
                            # set activity finder state
                            FileFinder.activity_finder_state = FileFinder.FILE_FOUND
                            # record info
                            Logger.save_in_log_file("FileFinder",
                                                    "Have found activity " + FileFinder.activity_name + " "
                                                    + FileFinder.activity_uid + ".exml file", False)
                            # exit 'for i in range' loop
                            break
            else:
                # all activities have been checked already
                FileFinder.activity_finder_state = FileFinder.NO_MORE_FILES
                # record info
                Logger.save_in_log_file("FileFinder", "No further .exml files have been found", False)

    # Description:
    # This method looks for set of .exml files, which describe entire content of one model element
    # (either component or package element), i.e. activity diagram and related interface elements.
    @staticmethod
    def find_files():

        # record info
        Logger.save_in_log_file("FileFinder", "Searching for set of .exml files that describe module details", True)

        # clear data before search
        FileFinder.clear_return_data()

        # find module file
        FileFinder.find_module_file()

        # only when module file has been found
        if FileFinder.module_finder_state == FileFinder.FILE_FOUND:
            # find activity file
            FileFinder.find_activity_file()

        # if module and activity files have been found
        if (FileFinder.module_finder_state == FileFinder.FILE_FOUND and
                FileFinder.activity_finder_state == FileFinder.FILE_FOUND):
            # set positive flag
            files_found = True

        else:
            # set negative flag
            files_found = False
            # clear again data before return
            FileFinder.clear_return_data()

        # append collected data to file finder list
        file_finder_list = []
        file_finder_list.insert(FileFinder.FILES_FOUND_INDEX, files_found)
        file_finder_list.insert(FileFinder.MODULE_FILE_INDEX, FileFinder.module_file)
        file_finder_list.insert(FileFinder.ACTIVITY_FILE_INDEX, FileFinder.activity_file)
        file_finder_list.insert(FileFinder.MODULE_NAME_INDEX, FileFinder.module_name)
        file_finder_list.insert(FileFinder.MODULE_UID_INDEX, FileFinder.module_uid)
        file_finder_list.insert(FileFinder.OPERATION_NAME_INDEX, FileFinder.operation_name)
        file_finder_list.insert(FileFinder.OPERATION_UID_INDEX, FileFinder.operation_uid)
        file_finder_list.insert(FileFinder.ACTIVITY_NAME_INDEX, FileFinder.activity_name)
        file_finder_list.insert(FileFinder.ACTIVITY_UID_INDEX, FileFinder.activity_uid)

        # return file finder list
        return file_finder_list
