#   FILE:           mcg_cgc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is
#       responsible for error recording, which may occur during run of MCG CGC.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           9 APR 2022
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
    CHK_ERR_EOF = 1
    CHK_ERR_SKIPPED = 2
    CHK_ERR_FAULTY_HEADER = 10
    CHK_ERR_FAULTY_START = 20
    CHK_ERR_FAULTY_NAME = 21
    CHK_ERR_FAULTY_SOURCE = 22
    CHK_ERR_FAULTY_INPUT_INTERFACE = 23
    CHK_ERR_FAULTY_OUTPUT_INTERFACE = 24
    CHK_ERR_FAULTY_LOCAL_INTERFACE = 25
    CHK_ERR_FAULTY_BODY = 26
    CHK_ERR_FAULTY_END = 27
    CHK_ERR_FAULTY_FOOTER = 30
    CHK_ERR_DATA_AFTER_FOOTER = 31

    # Description:
    # This method records error (i.e. append error to error list), found during run of MCG CGC.
    @staticmethod
    def record_error(error_code, error_info1, error_info2):

        # CHECKER errors, range 1-100
        if error_code == ErrorHandler.CHK_ERR_EOF:
            # set error notification
            error = "ERROR " + str(error_code) + ": End of the configuration file was reached at line " + \
                    str(error_info1) + " before configuration check process was completed"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_SKIPPED:
            # set error notification
            error = "ERROR " + str(error_code) + ": Expected part of the configuration file was not found, " \
                    "therefore verification was skipped from line " + str(error_info1) + " to " + str(error_info2)
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_HEADER:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of config start maker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_START:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of module start maker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_NAME:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of module name or marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_SOURCE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of module source marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of input interface data or marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of output interface data or marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of local interface data or marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_BODY:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of body data or marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_END:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of module end maker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_FAULTY_FOOTER:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of config end maker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_DATA_AFTER_FOOTER:
            # set error notification
            error = "ERROR " + str(error_code) + ": Unexpected data appear at line " + str(error_info1) + \
                    " after end of the configuration file"
            # append error to error list
            ErrorHandler.error_list.append(error)

        else:
            # set error notification
            error = "UNKNOWN ERROR " + str(error_code) + ": Error code not recognized"
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
