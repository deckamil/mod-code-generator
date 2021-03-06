#   FILE:           mcg_cc_error_handler.py
#
#   DESCRIPTION:
#       This module contains definition of ErrorHandler class, which is responsible
#       for error recording, which may occur during run of Mod Code Generator (MCG)
#       Converter Component (CC).
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           19 JAN 2022
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


# Class:
# ErrorHandler()
#
# Description:
# This is base class responsible for error recording, which may occur during run of MCG CC.
class ErrorHandler(object):

    # error list
    error_list = []

    # SIGNAL errors
    SIG_ERR_MORE_INPUTS = 1
    SIG_ERR_NO_SIG_UID_TARGET = 20

    # ACTION errors
    ACT_ERR_ACT_NOT_ALLOWED = 51
    ACT_ERR_NO_TARGET = 70
    ACT_ERR_NO_SIG_UID_TARGET = 71
    ACT_ERR_NO_FIRST_INPUT = 72
    ACT_ERR_ACT_IS_TARGET = 73

    # STRUCTURE errors
    STR_ERR_MORE_INPUTS = 101
    STR_ERR_NO_COM_STR_UID_TARGET = 120

    # COMPONENT errors
    COM_ERR_NO_TARGET = 170
    COM_ERR_NO_STR_UID_TARGET = 171

    # INTERFACE errors
    INT_ERR_NO_INP_INT_IN_COM = 201
    INT_ERR_NO_OUT_INT_IN_COM = 202
    INT_ERR_NO_LOC_DAT_IN_COM = 203
    INT_ERR_NO_INP_INT_IN_PAC = 204
    INT_ERR_NO_OUT_INT_IN_PAC = 205
    INT_ERR_NO_LOC_DAT_IN_PAC = 206
    INT_ERR_SIG_NOT_IN_INT = 210
    INT_ERR_STR_NOT_IN_INT = 211
    INT_ERR_INC_INP_INT_TYPE_IN_COM = 212
    INT_ERR_INC_OUT_INT_TYPE_IN_COM = 213
    INT_ERR_INC_LOC_DAT_TYPE_IN_COM = 214
    INT_ERR_INC_INP_INT_TYPE_IN_PAC = 215
    INT_ERR_INC_OUT_INT_TYPE_IN_PAC = 216
    INT_ERR_INC_LOC_DAT_TYPE_IN_PAC = 217
    INT_ERR_INP_INT_SIG_IS_TAR_IN_COM = 220
    INT_ERR_OUT_INT_SIG_IS_SRC_IN_COM = 221
    INT_ERR_INP_INT_STR_IS_TAR_IN_PAC = 222
    INT_ERR_OUT_INT_STR_IS_SRC_IN_PAC = 223

    # GENERAL errors
    GEN_ERR_NO_NAME_ELEMENT = 270
    GEN_ERR_NO_UID_ELEMENT = 271
    GEN_ERR_NO_COM_PAC_ACTIVITY = 272
    GEN_ERR_NO_COM_PAC_INTERFACE = 273

    # Method:
    # record_error()
    #
    # Description:
    # This method records error (i.e. append error to error list), found during run of MCG CC.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def record_error(error_code, error_info1, error_info2):

        # SIGNAL errors, range 1-50
        if error_code == ErrorHandler.SIG_ERR_MORE_INPUTS:
            # set error notification
            error = "ERROR " + str(error_code) + ": Signal " + str(error_info1) + \
                    " has more than one input connection (source) within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.SIG_ERR_NO_SIG_UID_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find target signal with uid=" + str(error_info1) + \
                    " for signal " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # ACTIONS errors, range 51-100
        elif error_code == ErrorHandler.ACT_ERR_ACT_NOT_ALLOWED:
            # set error notification
            error = "ERROR " + str(error_code) + ": Action " + str(error_info1) + \
                    " has invalid type within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.ACT_ERR_NO_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find any target for action " + \
                    str(error_info1) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.ACT_ERR_NO_SIG_UID_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find target signal with uid=" + str(error_info1) + \
                    " for action " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.ACT_ERR_NO_FIRST_INPUT:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find first input signal for action " + \
                    str(error_info1) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.ACT_ERR_ACT_IS_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Another action is target of action " + \
                    str(error_info1) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # STRUCTURE errors, range 101-150
        elif error_code == ErrorHandler.STR_ERR_MORE_INPUTS:
            # set error notification
            error = "ERROR " + str(error_code) + ": Structure " + str(error_info1) + \
                    " has more than one input connection (source) within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.STR_ERR_NO_COM_STR_UID_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find target component or structure with uid=" + \
                    str(error_info1) + " for structure " + str(error_info2) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # COMPONENT errors, range 151-200
        elif error_code == ErrorHandler.COM_ERR_NO_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find any target for component " + \
                    str(error_info1) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.COM_ERR_NO_STR_UID_TARGET:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find target structure with uid=" + \
                    str(error_info1) + " for component " + str(error_info2) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # INTERFACE errors, range 201-250
        elif error_code == ErrorHandler.INT_ERR_NO_INP_INT_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Input Interface element within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_NO_OUT_INT_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Output Interface element within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_NO_LOC_DAT_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Local Data element within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_NO_INP_INT_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Input Interface element within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_NO_OUT_INT_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Output Interface element within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_NO_LOC_DAT_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find Local Data element within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_SIG_NOT_IN_INT:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find " + str(error_info1) + \
                    " signal within component interface"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_STR_NOT_IN_INT:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find " + str(error_info1) + \
                    " structure within package interface"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_INP_INT_TYPE_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Input Interface signal " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_OUT_INT_TYPE_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Output Interface signal " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_LOC_DAT_TYPE_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Local Data signal " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_INP_INT_TYPE_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Input Interface signal " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_OUT_INT_TYPE_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Output Interface signal " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INC_LOC_DAT_TYPE_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Local Data structure " + str(error_info1) + \
                    " has invalid type " + str(error_info2) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INP_INT_SIG_IS_TAR_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Input Interface signal " + str(error_info1) + \
                    " is connected as output (target) of " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_OUT_INT_SIG_IS_SRC_IN_COM:
            # set error notification
            error = "ERROR " + str(error_code) + ": Output Interface signal " + str(error_info1) + \
                    " is connected as input (source) of " + str(error_info2) + " within component content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_INP_INT_STR_IS_TAR_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Input Interface structure is connected as output (target) of " \
                    + str(error_info1) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.INT_ERR_OUT_INT_STR_IS_SRC_IN_PAC:
            # set error notification
            error = "ERROR " + str(error_code) + ": Output Interface structure is connected as input (source) of " \
                    + str(error_info1) + " within package content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        # GENERAL errors, range 251-300
        elif error_code == ErrorHandler.GEN_ERR_NO_NAME_ELEMENT:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find <name> element at line " + \
                    str(error_info1) + " within file content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.GEN_ERR_NO_UID_ELEMENT:
            # set error notification
            error = "ERROR " + str(error_code) + ": Could not find <uid> element at line " + \
                    str(error_info1) + " within file content"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.GEN_ERR_NO_COM_PAC_ACTIVITY:
            # set error notification
            error = "ERROR " + str(error_code) + ": Activity file does not belong to component or package"
            # append error to error list
            ErrorHandler.error_list.append(error)

        elif error_code == ErrorHandler.GEN_ERR_NO_COM_PAC_INTERFACE:
            # set error notification
            error = "ERROR " + str(error_code) + ": Interface file does not belong to component or package"
            # append error to error list
            ErrorHandler.error_list.append(error)

        else:
            # set error notification
            error = "UNKNOWN ERROR " + str(error_code) + ": Error code not recognized"
            # append error to error list
            ErrorHandler.error_list.append(error)

    # Method:
    # check_errors()
    #
    # Description:
    # This method checks if any error was recorded and if yes, then it ends run of MCG CC.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def check_errors(model_element_name, activity_source, model_element_type):

        # if any error was recorded
        if len(ErrorHandler.error_list) > 0:
            # error handler
            Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

            # print model element details
            Logger.save_in_log_file("Model Element Name:      " + str(model_element_name))
            Logger.save_in_log_file("Model Element Source:    " + str(activity_source))
            Logger.save_in_log_file("Model Element Type:      " + str(model_element_type))
            Logger.save_in_log_file("*** ERRORS FOUND, Mod Code Generator (MCG) Converter Component (CC) WILL EXIT")
            # display errors
            for error in ErrorHandler.error_list:
                Logger.save_in_log_file(error)

            # end of error handler
            Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF ERROR HANDLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

            # exit MCG CC.
            exit()
