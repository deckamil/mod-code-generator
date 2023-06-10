#   FILE:           mcg_cc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is
#       responsible for error recording, which may occur during run of MCG CC.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           7 JUN 2023
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


from mcg_cc_logger import Logger


# Description:
# This class is responsible for error recording, which may occur during run of MCG CC.
class ErrorHandler(object):

    # error list
    error_list = []

    # CONNECTION errors
    CON_ERR_INVALID_ACTION_TYPE = 1

    # INTERFACE errors
    INT_ERR_INVALID_INTERFACE_ELEMENT_TYPE = 51

    # Description:
    # This method records error (i.e. append error to error list), found during run of MCG CC.
    @staticmethod
    def record_error(error_code, error_info1, error_info2):

        # CONNECTION errors, range 1-50
        if error_code == ErrorHandler.CON_ERR_INVALID_ACTION_TYPE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Invalid action type was found in " + str(error_info1) + \
                    " connection"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # INTERFACE errors, range 51-100
        elif error_code == ErrorHandler.INT_ERR_INVALID_INTERFACE_ELEMENT_TYPE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Invalid interface element type was found in " + str(error_info1) + \
                    " interface element"
            # append error to error list
            ErrorHandler.error_list.append(error)

    # Description:
    # This method checks if any error was recorded and if yes, then it ends run of MCG CC.
    @staticmethod
    def check_errors():

        # if any error was recorded
        if len(ErrorHandler.error_list) > 0:
            # error handler
            Logger.save_in_log_file("ErrorHandler",
                                    "ERRORS FOUND, Mod Code Generator (MCG) Converter Component (CC) WILL EXIT",
                                    True)
            # display errors
            for error in ErrorHandler.error_list:
                Logger.save_in_log_file("ErrorHandler", error, False)

            # save log file footer
            Logger.save_log_file_footer()

            # exit MCG CGC.
            exit()
