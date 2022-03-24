#   FILE:           mcg_cgc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is
#       responsible for error recording, which may occur during run of MCG CGC.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           24 MAR 2022
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
    CHK_ERR_HEAD_ST_UN = 3
    CHK_ERR_HEAD_DA_UN = 4
    CHK_ERR_MOD_ST_UN = 5
    CHK_ERR_COM_SRC_UN = 6
    CHK_ERR_COM_NAM_UN = 7
    CHK_ERR_COM_IN_ST_UN = 8
    CHK_ERR_COM_IN_UN = 9
    CHK_ERR_COM_OUT_ST_UN = 10
    CHK_ERR_COM_OUT_UN = 11
    CHK_ERR_COM_LOC_ST_UN = 12
    CHK_ERR_COM_LOC_UN = 13
    CHK_ERR_COM_BOD_ST_UN = 14
    CHK_ERR_COM_BOD_UN = 15
    CHK_ERR_COM_END_UN = 16

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
            error = "ERROR " + str(error_code) + ": Expected section of the configuration file was not found, " \
                    "therefore verification was skipped from line " + str(error_info1) + " to " + str(error_info2)
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_HEAD_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or header start marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_HEAD_DA_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or header date marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_MOD_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of new module section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_SRC_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or component source marker"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_NAM_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or component name"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_IN_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of input interface section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_IN_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or input data definition or end of input interface " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_OUT_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of output interface section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_OUT_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or output data definition or end of output interface " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_LOC_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of local data section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_LOC_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or local data definition or end of local data " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_BOD_ST_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of body section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_BOD_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or body data definition or end of body data " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_END_UN:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or end of component section"
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
