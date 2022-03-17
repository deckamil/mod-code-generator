#   FILE:           mcg_cgc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is
#       responsible for error recording, which may occur during run of MCG CGC.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           17 MAR 2022
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


from mcg_cgc_logger import Logger


# Description:
# This class is responsible for error recording, which may occur during run of MCG CC.
class ErrorHandler(object):

    # error list
    error_list = []

    # CHECKER errors
    CHK_ERR_HEADER_UN_LINE = 1

    # Description:
    # This method records error (i.e. append error to error list), found during run of MCG CGC.
    @staticmethod
    def record_error(error_code, error_info1, error_info2):

        # CHECKER errors, range 1-100
        if error_code == ErrorHandler.CHK_ERR_HEADER_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or header start marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

    # Description:
    # This method checks if any error was recorded and if yes, then it ends run of MCG CGC.
    @staticmethod
    def check_errors():

        # if any error was recorded
        if len(ErrorHandler.error_list) > 0:
            # error handler
            Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
            Logger.save_in_log_file("*** ERRORS FOUND, Mod Code Generator (MCG) Code Generator Component (CGC) WILL EXIT")
            # display errors
            for error in ErrorHandler.error_list:
                Logger.save_in_log_file(error)

            # end of error handler
            Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF ERROR HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

            # exit MCG CGC.
            exit()
