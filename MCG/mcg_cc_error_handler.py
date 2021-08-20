#   FILE:           mcg_cc_error_handler.py
#
#   DESCRIPTION:
#       This module is responsible for error recording, which may occur during
#       processing of Mod Code Generator (MCG) Converter Component (CC).
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           20 AUG 2021
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


# empty list placeholder
error_list = []


# Function:
# record_error()
#
# Description:
# This function record error (i.e. append error to error list) found
# during processing of converter module.
#
# Returns:
# This function does not return anything.
def record_error(error_code, info1, info2):

    # SIGNAL errors, range 1-50
    if error_code == 1:
        # set error notification
        error = "ERROR " + str(error_code) + ": Signal " + str(info1) + " has more than one source within " \
                                                                        "component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 20:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find target signal with uid=" + str(info1) + \
                " for signal " + str(info2) + " within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 21:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find target signal with uid=" + str(info1) + \
                " for action " + str(info2) + " within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 22:
        # set error notification
        display = "ERROR " + str(error_code) + ": Could not find first input signal for action with uid=" + \
                  str(info1) + " within component content"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    # ACTIONS errors, range 51-100
    elif error_code == 51:
        # set error notification
        error = "ERROR " + str(error_code) + ": Action " + str(info1) + " is not recognized as valid one within " \
                                                                        "component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 70:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find any target for action " + \
                str(info1) + " within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 80:
        # set error notification
        error = "ERROR " + str(error_code) + ": Another action is target of action " + \
                str(info1) + " within component content"
        # append error to error list
        error_list.append(error)

    # INTERFACE errors, range 101-150
    elif error_code == 120:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find Input Interface within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 121:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find Output Interface within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 122:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find Local Parameters within component content"
        # append error to error list
        error_list.append(error)

    elif error_code == 123:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find Input Interface within package content"
        # append error to error list
        error_list.append(error)

    elif error_code == 124:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find Output Interface within package content"
        # append error to error list
        error_list.append(error)

    # COMPONENT errors, range 151-200
    elif error_code == 170:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find any target for component " + \
                str(info1) + " within package content"
        # append error to error list
        error_list.append(error)

    elif error_code == 171:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find target element with uid=" + str(info1) + \
                " for component " + str(info2) + " within package content"
        # append error to error list
        error_list.append(error)

    elif error_code == 172:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find target component with uid=" + str(info1) + \
                " for interface " + str(info2) + " within package content"
        # append error to error list
        error_list.append(error)

    # PACKAGE errors, range 201-250

    # GENERAL errors, range 251-300
    elif error_code == 270:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find component or package content within file content"
        # append error to error list
        error_list.append(error)

    elif error_code == 271:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find <name> element at line " + \
                str(info1) + " within file content"
        # append error to error list
        error_list.append(error)

    elif error_code == 272:
        # set error notification
        error = "ERROR " + str(error_code) + ": Could not find <uid> element at line " + \
                str(info1) + " within file content"
        # append error to error list
        error_list.append(error)

    else:
        # display error notification
        print("UNKNOWN ERROR: Error code not recognized")
        # append error to error list
        error_list.append(-1)


# Function:
# check_errors()
#
# Description:
# This function checks if any error was recorded and if yes, then it ends processing
# of Mod Code Generator (MCG) Converter Component (CC).
#
# Returns:
# This function does not return anything.
def check_errors(model_element_source, model_element_name):

    # check errors
    print("******************************** ERROR CHECK *******************************")
    print()

    # print model element details
    print("Component Source:    " + str(model_element_source))
    print("Component Name:      " + str(model_element_name))

    # if any error was recorded
    print("*** CHECK ERRORS ***")
    if len(error_list) > 0:
        print("*** ERRORS FOUND, Mod Code Generator (MCG) Converter Component (CC) WILL EXIT")
        # display errors
        for error in error_list:
            print(error)
        # exit Mod Code Generator (MCG) Converter Component (CC).
        exit()

    # no errors found, keep processing
    print("*** NO ERRORS FOUND ***")
    print()

    print("**************************** END OF ERROR CHECK ****************************")
    print()
