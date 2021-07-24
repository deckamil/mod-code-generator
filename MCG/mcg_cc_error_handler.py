#   FILE:           mcg_cc_error_handler.py
#
#   DESCRIPTION:
#       This module is responsible for error recording, which may occur during
#       processing of Mod Code Generator (MCG) Converter Component (CC).
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           24 JUL 2021
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
def record_error(error_code, info):

    # for given error code
    if error_code == 1:
        # set error notification
        display = "ERROR 1: Action " + str(info) + " does not have target signal"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 2:
        # set error notification
        display = "ERROR 2: Signal " + str(info) + " has more than one source"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 3:
        # set error notification
        display = "ERROR 3: Action " + str(info) + " is not recognized as valid"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 4:
        # set error notification
        display = "ERROR 4: Could not find target signal with uid=" + str(info)
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 5:
        # set error notification
        display = "ERROR 5: Action " + str(info) + " has another action as target"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 6:
        # set error notification
        display = "ERROR 6: <name> element has not been found"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 7:
        # set error notification
        display = "ERROR 7: <uid> element has not been found"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 8:
        # set error notification
        display = "ERROR 8: Model element name or type has not been found"
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

    elif error_code == 9:
        # set error notification
        display = "ERROR 9: Could not find first input signal for action uid=" + str(info)
        # display error notification
        print(display)
        # append error to error list
        error_list.append(display)

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
def check_errors():

    # check errors
    print("******************************** ERROR CHECK *******************************")
    print()

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
