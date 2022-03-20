#   FILE:           mcg_cgc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is
#       responsible for error recording, which may occur during run of MCG CGC.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           20 MAR 2022
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
    CHK_ERR_HEADER_EOF = 1
    CHK_ERR_HEADER_UN_LINE = 2
    CHK_ERR_DATA_OR_MOD_START_EOF = 3
    CHK_ERR_DATA_OR_MOD_START_UN_LINE = 4
    CHK_ERR_MOD_START_EOF = 5
    CHK_ERR_MOD_START_UN_LINE = 6
    CHK_ERR_COM_EOF = 7
    CHK_ERR_COM_SRC_UN_LINE = 8
    CHK_ERR_COM_NAM_UN_LINE = 9
    CHK_ERR_COM_IN_ST_UN_LINE = 10
    CHK_ERR_COM_IN_UN_LINE = 11
    CHK_ERR_COM_OUT_ST_UN_LINE = 12
    CHK_ERR_COM_OUT_UN_LINE = 13
    CHK_ERR_COM_LOC_ST_UN_LINE = 14
    CHK_ERR_COM_LOC_UN_LINE = 15
    CHK_ERR_COM_BOD_ST_UN_LINE = 16
    CHK_ERR_COM_BOD_UN_LINE = 17
    CHK_ERR_COM_END_UN_LINE = 18

    # Description:
    # This method records error (i.e. append error to error list), found during run of MCG CGC.
    @staticmethod
    def record_error(error_code, error_info1, error_info2):

        # CHECKER errors, range 1-100
        if error_code == ErrorHandler.CHK_ERR_HEADER_EOF:
            # set error notification
            error = "ERROR " + str(error_code) + ": End of the configuration file was reached at line " + \
                    str(error_info1) + " before config start was found"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_HEADER_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or config start"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_DATA_OR_MOD_START_EOF:
            # set error notification
            error = "ERROR " + str(error_code) + ": End of the configuration file was reached at line " + \
                    str(error_info1) + " before date or start of new module section was found"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_DATA_OR_MOD_START_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or date or start of new module section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_MOD_START_EOF:
            # set error notification
            error = "ERROR " + str(error_code) + ": End of the configuration file was reached at line " + \
                    str(error_info1) + " before start of new module section was found"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_MOD_START_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of new module section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_EOF:
            # set error notification
            error = "ERROR " + str(error_code) + ": End of the configuration file was reached at line " + \
                    str(error_info1) + " while checking component section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_SRC_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or component source info"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_NAM_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or component name info"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_IN_ST_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of input interface section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_IN_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or input data definition or end of input interface " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_OUT_ST_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of output interface section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_OUT_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or output data definition or end of output interface " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_LOC_ST_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of local data section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_LOC_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or local data definition or end of local data " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_BOD_ST_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or start of body section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_BOD_UN_LINE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Line " + str(error_info1) + " in the configuration file has " \
                    "unexpected content instead of empty line or body data definition or end of body data " \
                    "section"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.CHK_ERR_COM_END_UN_LINE:
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
