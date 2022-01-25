import os
import hashlib
import xml.etree.ElementTree as ET
import csv
import datetime
import shutil
import copy
import uuid
import time
import random
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import threading
from threading import Event
import multiprocessing
from multiprocessing import Process, Queue
import tkinter.ttk as ttk
from tkinter.ttk import *
from multiprocessing import freeze_support
import pandas as pd
from tkinter import messagebox
import re



# log writing function
def log(text,logFilePath):
    flog = open(logFilePath,"a")
    flog.write(str(datetime.datetime.now())+ ":" + " " + text + "\n")
    flog.close

def no_time_log(text,logFilePath):
    flog = open(logFilePath,"a")
    flog.write("    "+ text + "\n")
    flog.close

# def data_frame_log(dataFrame, logFilePath):
#     dataFrame.to_cvs(logFilePath)

# def copyFolder1(source,destination):
#
#     rootOfSource = source.replace(os.path.basename(source), "")
#
#     for (folderPaths, subdirs, files) in os.walk(source):
#         newFolder = os.path.join(destination, folderPaths.replace(rootOfSource, ""))
#         os.makedirs(newFolder, exist_ok=True)
#         for file in files:
#
#             srcFile = os.path.join(folderPaths, file)
#             desFile = os.path.join(newFolder, file)
#
#             shutil.copyfile(srcFile, desFile)


# Copy folder from source folder to destination
def copyFolder(source,destination,Q, rcpCreatorLog):


    rootOfSource = source.replace(os.path.basename(source), "")
    try:
        if os.path.isdir(source) == True:
            for (folderPaths, subdirs, files) in os.walk(source):
                newFolder = os.path.join(destination, folderPaths.replace(rootOfSource, ""))
                os.makedirs(newFolder, exist_ok=True)
                for file in files:

                    srcFile = os.path.join(folderPaths, file)
                    desFile = os.path.join(newFolder, file)

                    if os.path.isfile(srcFile) == True:

                        log("Copying: " + srcFile + " To: " + desFile, rcpCreatorLog)
                        shutil.copyfile(srcFile, desFile)
                        log("Copying: " +srcFile + " To: " + desFile + " [COMPLETED]", rcpCreatorLog)
                        Q.put(True)
                    else:
                        log("Copying: " + srcFile + " To: " + desFile + " [FALIED]", rcpCreatorLog)
                        Q.put(False)
        else:
            Q.put(False)
    except Exception as error:
        print(str(error))
        log("Copying: " + source + " To: " + destination + " [FALIED]", rcpCreatorLog)
        no_time_log(str(error), rcpCreatorLog)

# path format

def path_format(path):
    return path.replace("/","\\")
def remove_double_backslash(path):
    return path.replace("\\\\","\\")

# read configuration xml file function
# return: reading result (True, False), TemplateFolder, NetworkDrive, NetworkFolder. RecipeList
def configuration_read():

    #print("Reading RecipeCreatorConfig.Xml ....")
    log("Reading RecipeCreatorConfig.Xml ....", recipeCreatorLog)
    templateFolderExist = False
    networkDriveExist = False
    networkFolderExist = False
    recipeCopyTimeoutExist = False
    HCGoldenFilePathExist = False
    DefaultGoldenFileExist = False


    templPath = ""
    netDrive = ""
    netFolder = ""
    rcpCopyTimeout = ""
    HCGoldenFilePath = ""
    DefaultGoldenFileList =[]
    EnableVersionCheck = "True"
    EnableValueCheckOnly = "False"

    try:
        configPath = os.path.join(os.getcwd(), "RecipeCreatorConfig.Xml")
        if os.path.isfile(configPath):
            configXml = ET.parse(configPath)
            configXmlRoot = configXml.getroot()

            no_time_log("RecipeCreatorConfig.Xml", recipeCreatorLog)
            no_time_log(ET.tostring(configXmlRoot, encoding='utf-8').decode('utf-8'), recipeCreatorLog)
            # #print(ET.tostring(configXmlRoot, encoding='utf-8').decode('utf-8'))

            for x in configXmlRoot:

                if x.tag == "TemplateFolder":
                    templateFolderExist = True
                    templPath = x.text.strip()

                if x.tag == "NetworkDrive":
                    networkDriveExist = True
                    netDrive = x.text.strip()

                if x.tag == "NetworkFolder":
                    networkFolderExist = True
                    netFolder = x.text.strip()

                if x.tag == "RecipeCopyTimeout":
                    recipeCopyTimeoutExist = True
                    rcpCopyTimeout = x.text.strip()

                if x.tag == "HCGoldenFilePath":
                    HCGoldenFilePathExist = True
                    if x.text:

                        HCGoldenFilePath = x.text.strip()

                if x.tag == "DefaultGoldenFile":
                    DefaultGoldenFileExist = True

                    if x.text:
                        DefaultGoldenFileList = x.text.strip().split(',')
                
                if x.tag == "EnableVersionCheck":
                    # DefaultGoldenFileExist = True
                    EnableVersionCheck = x.text.strip()
                
                if x.tag == "EnableValueCheckOnly":
                    # DefaultGoldenFileExist = True
                    EnableValueCheckOnly = x.text.strip()

            if templateFolderExist == False or networkDriveExist == False or networkFolderExist == False or recipeCopyTimeoutExist == False or HCGoldenFilePathExist == False or DefaultGoldenFileExist ==False:

                if templateFolderExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have TemplateFolder configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have TemplateFolder configuration. Recipe conversion is terminated",
                        summaryLog)

                if networkDriveExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have NetworkDrive configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have NetworkDrive configuration. Recipe conversion is terminated",
                        summaryLog)

                if networkFolderExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have networkFolder configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have networkFolder configuration. Recipe conversion is terminated",
                        summaryLog)

                if recipeCopyTimeoutExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have RecipeCopyTimeout configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have RecipeCopyTimeout configuration. Recipe conversion is terminated",
                        summaryLog)

                if HCGoldenFilePathExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have HCGoldenFilePath configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have HCGoldenFilePath configuration. Recipe conversion is terminated",
                        summaryLog)

                if DefaultGoldenFileExist == False:
                    log("Error: RecipeCreatorConfig.Xml does not have DefaultGoldenFileExist configuration", recipeCreatorLog)
                    no_time_log(
                        "Error: RecipeCreatorConfig.Xml does not have DefaultGoldenFileExist configuration. Recipe conversion is terminated",
                        summaryLog)

                #print("Reading RecipeCreatorConfig.Xml [FAILED]")
                #print("Recipe conversion is terminated with NO recipe converted.")

                return False
            else:

                log("Reading RecipeCreatorConfig.Xml [COMPLETED]", recipeCreatorLog)
                #print("Reading RecipeCreatorConfig.Xml [COMPLETED]")

                return True, templPath, netDrive, netFolder, rcpCopyTimeout, HCGoldenFilePath, DefaultGoldenFileList, EnableVersionCheck,EnableValueCheckOnly
            #print(" Error: The file at:[" + configPath + "] is not found")
            log(" Error: The file at:[" + configPath + "] is not found", recipeCreatorLog)
            no_time_log(" Error: The file at:[" + configPath + "] is not found", summaryLog)

            return False, templPath, netDrive, netFolder , rcpCopyTimeout, HCGoldenFilePath, DefaultGoldenFileList, EnableVersionCheck,EnableValueCheckOnly

    except Exception as error:

        log("Error: Cannot process RecipeCreatorConfig.Xml", recipeCreatorLog)
        no_time_log("Error: Cannot process RecipeCreatorConfig.Xml. Recipe conversion is terminated", summaryLog)
        no_time_log(str(error), recipeCreatorLog)
        #print("Error during reading RecipeCreatorConfig.Xml. Recipe conversion is terminated")

        return False, templPath, netDrive, netFolder, rcpCopyTimeout,HCGoldenFilePath,DefaultGoldenFileList,EnableVersionCheck,EnableValueCheckOnly

# sdtc type template update function
def sdtc_type_template_update(templFilePath,toUpdateFilePath, templateLine):
    log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath, recipeCreatorLog )
    try:

        templateXml = ET.parse(templFilePath)
        templateXmlRoot = templateXml.getroot()

        retry = 0

        while os.path.isfile(toUpdateFilePath) == False and retry <=10:
            retry = retry + 1
            log("Retry[" + str(retry) +"] for checking:" + os.path.isfile(toUpdateFilePath), recipeCreatorLog)
            time.sleep(1)

        toUpdateFileXml = ET.parse(toUpdateFilePath)
        # toUpdateFileXmlRoot = toUpdateFileXml.getroot()

        if templateLine == "Add":
            templateXmlRoot.insert(2, toUpdateFileXml.find("Template"))
        elif templateLine =="Remove":
            templateXmlRoot.remove(templateXml.find("Template"))

        # To match RMT format, if units ="" -> remove
        # Move units to the end of the parameter dictionary
        # If the units value is not empty, move the unites to the end of parameter line
        for tplMenu in templateXmlRoot.findall("Menu"):
            for tplItem in tplMenu.findall('Item'):
                if "units" in tplItem.attrib:
                    if tplItem.get('units') == "":
                        tplItem.attrib.pop("units")
                    else:
                        # Store the value of units
                        unitValue = tplItem.get('units')
                        # remove the units attribute
                        tplItem.attrib.pop("units")
                        # Add units attribute back. It will add to the end
                        tplItem.set('units', str(unitValue))

        for tplMenu in templateXmlRoot.findall("Menu"):

            # Find in the toUpdateFile, a menu having the same name with the template menu tplMenu.get('name')
            rcpMenu = toUpdateFileXml.find("Menu[@name = " + "'" + tplMenu.get('name') + "'" + "]")

            if not(rcpMenu is None):

                for tplItem in tplMenu:

                    # Find in rcpMenu, parameter having the same name with the template parameter tplItem.get('name')
                    rcpItem = rcpMenu.find("Item[@name = " + "'" + tplItem.get('name') + "'" + "]")

                    if not (rcpItem is None):
                        # Always update the template with the current recipe value except:
                        # - Value list is different and the current value does not exist in the template list
                        # (Remove this logic). User will need to update using specific parameter file

                        # if not (rcpItem.get('valuelist') != tplItem.get('valuelist') and tplItem.get('valuelist').find(rcpItem.get('value')) == -1):
                        # =================== This is to match BLiT creation ================
                        # Check: If the value does not exist (there are some un-used parameters which has no value attribute after appling rmt. HC convert tool keeps them as value = ""
                        # if it does not, set value ="". Do not leave it as the template value which could be anything
                        # key = 'value'
                        # if key not in rcpItem.attrib:
                        #     tplItem.attrib.pop('value', "")
                        # else:
                        #     tplItem.set('value', str(rcpItem.get('value')))

                        # ===================== This is to match RMT ========================
                        # Remove value attribute if it does not exist in the recipe
                        key = 'value'
                        if key not in rcpItem.attrib:
                            tplItem.attrib.pop("value")
                        else:
                            tplItem.set('value', str(rcpItem.get('value')))

        # writing updated template xml to the toUpdateFile
        templateXml.write(toUpdateFilePath)
        log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath + "[COMPLETED]", recipeCreatorLog)
        return True
    except Exception as error:
        log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

# manifest type template update function
def manifest_type_template_update(templFilePath,toUpdateFilePath):
    log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath, recipeCreatorLog)
    try:
        templateXml = ET.parse(templFilePath)
        templateXmlRoot = templateXml.getroot()
        toUpdateFileXml = ET.parse(toUpdateFilePath)

        for tpl in templateXmlRoot:

            compRecipePara = toUpdateFileXml.find("ComponentRecipe[@type = " + "'" + str(tpl.get('type')) + "'" + "]")
            if not (compRecipePara is None):
                tpl.find('SourcePath').text = compRecipePara.find('SourcePath').text

        # writing updated template xml to the toUpdateFile
        templateXml.write(toUpdateFilePath)
        log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath + "[COMPLETED]", recipeCreatorLog)
        return  True
    except Exception as error:
        log("Updating: " + toUpdateFilePath + "To the template: " + templFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

# Update Identity line for .xml files function

def identity_update(toUpdateFilePath):
    log("Updating Identity line for: " + toUpdateFilePath, recipeCreatorLog)
    try:

        toUpdateFileXml = ET.parse(toUpdateFilePath)
        toUpdateFileXmlRoot = toUpdateFileXml.getroot()

        sub = toUpdateFileXmlRoot.find("Identity")

        if not (sub is None):
            sub.set('name', os.path.basename(toUpdateFilePath).split('.')[0])
            sub.set('id', str(uuid.uuid4()).upper())
            sub.set('asof', datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))

            # writing updated template xml to the toUpdateFile
            toUpdateFileXml.write(toUpdateFilePath)
            log("Updating Identity line for: " + toUpdateFilePath + "[COMPLETED]", recipeCreatorLog)
            return True
        else:
            return False
    except Exception as error:
        log("Updating Identity line for: " + toUpdateFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def mas_file_parameter_update(toUpdateFilePath):
    log("Updating values of mas.xml file: " + toUpdateFilePath, recipeCreatorLog)
    try:

        toUpdateFileXml = ET.parse(toUpdateFilePath)
        toUpdateFileXmlRoot = toUpdateFileXml.getroot()
        for sub in toUpdateFileXmlRoot:
            if sub.tag == "Menu" and sub.get('name') == "HC Master":
                for item in sub:
                    if item.get('name') == "SDTC_Recipe":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".mas.xml")
                    else:
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".xml")

            if sub.tag == "Menu" and sub.get('name') == "SDTC Master":
                for item in sub:
                    if item.get('name') == "SDTC_Recipe_Parameter" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".xml")
                    if item.get('name') == "SDTC_Probe_Pattern" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".ptn")
                    if item.get('name') == "SDTC_Unit_Pattern" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".utn")
                    if item.get('name') == "SDTC_Probe_Parameter" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".prb")
                    if item.get('name') == "SDTC_Unit_Parameter" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".unt")
                    if item.get('name') == "SDTC_BVIU_Parameter" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".rcp")
                    if item.get('name') == "SDTC_Contact_Parameter" and item.get('value') != "":
                        item.set('value', str(os.path.basename(toUpdateFilePath).split('.')[0]) + ".cnt")

        # writing updated template xml to the toUpdateFile
        toUpdateFileXml.write(toUpdateFilePath)
        log("Updating values of mas.xml file: " + toUpdateFilePath + "[COMPLETED]", recipeCreatorLog)
        return True
    except Exception as error:
        log("Updating values of mas.xml file: " + toUpdateFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def specific_para_file_update(recipePath, specificParaFilePath):
    try:
        log("Updating the recipe: " + recipePath + "with the specific parameter file: " + specificParaFilePath, recipeCreatorLog)


        paraFileXml = ET.parse(specificParaFilePath)

        paraFileXmlRoot = paraFileXml.getroot()

        no_time_log(ET.tostring(paraFileXmlRoot, encoding='utf-8').decode('utf-8'), recipeCreatorLog)
        toUpdateFilePath = ""

        for paraComp in paraFileXmlRoot:
            # The xml file in the created recipe is indentified from combination of ComponentRecipe + recipe name
            for paraFileInfo in paraComp:
                if paraFileInfo.get("name") == "xml":
                    # Read xml file in recipe
                    toUpdateFilePath = os.path.join(recipePath, paraComp.get('name'), os.path.basename(recipePath) + ".xml")
                    toUpdateFileXml = ET.parse(toUpdateFilePath)

                if paraFileInfo.get("name") == "mas.xml":
                    # Read mas xml file in recipe
                    toUpdateFilePath = os.path.join(recipePath, paraComp.get('name'), os.path.basename(recipePath) + ".mas.xml")
                    toUpdateFileXml = ET.parse(toUpdateFilePath)

                # Find in the toUpdateFile, menu having the same name with the template menu paraMenu.get('name')
                for paraMenu in paraFileInfo.findall("Menu"):

                    rcpMenu = toUpdateFileXml.find("Menu[@name = " + "'" + paraMenu.get('name') + "'" + "]")

                    if not (rcpMenu is None):

                        #  find in recipe Menu , item having the same name with the parameter Item paraItem.get('name')
                        for paraItem in paraMenu:
                            rcpItem = rcpMenu.find("Item[@name = " + "'" + paraItem.get('name') + "'" + "]")
                            if not (rcpItem is None):
                                rcpItem.set('value', str(paraItem.get('value')))
                            else:
                                log("Cannot find Item:[" + str(paraItem.get('name')) + "] in the Menu: [" + str(paraMenu.get('name')) + "] in the file:" + toUpdateFilePath,recipeCreatorLog)
                                return False

                    else:
                        log("Cannot find Menu:[" + str(paraMenu.get('name')) + "]in the file: " + toUpdateFilePath,recipeCreatorLog)
                        return False

                toUpdateFileXml.write(toUpdateFilePath)

    # log("Updating the recipe: " + recipePath + "with the specific parameter file: " + specificParaFilePath + "[COMPLETED]",recipeCreatorLog)

        return True
    except Exception as error:
        log("Updating the recipe: " + recipePath + "with the specific parameter file: " + specificParaFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False


def network_folder_manifest_file_update(recipePath, absNetworkFolder, networkFolder, networkDrive):
    log("Updating network folder for: " + recipePath, recipeCreatorLog)
    try:

        # Check if asbNetworkFolder includes networkFolder


        if str(absNetworkFolder.find(networkFolder)) == "-1":

            log("Requested new recipe path:[" + absNetworkFolder + "] does NOT exist in the networkFolder configuration:[" + networkFolder + "]",recipeCreatorLog )
            return  False
        else:
            rcpNetworkPlace = absNetworkFolder.replace(networkFolder, networkDrive)

            recipeName = os.path.basename(recipePath)
            toUpdateFilePath = os.path.join(recipePath, "Manifest", recipeName + ".xml")

            toUpdateFileXml = ET.parse(toUpdateFilePath)
            toUpdateFileXmlRoot = toUpdateFileXml.getroot()

            for compRcp in toUpdateFileXmlRoot:
                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "HCRecipeMaster":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "HC", recipeName + ".mas.xml" )

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "HC_Recipe Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "HC", recipeName + ".xml" )

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "IOM_Recipe":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "IOM", recipeName + ".xml" )

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTCRecipeMaster":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".mas.xml" )

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Recipe_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".xml" )

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Unit_Pattern":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".utn")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".utn" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Probe_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".prb")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".prb" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Unit_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".unt")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".unt" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Probe_Pattern":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".ptn")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".ptn" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_Contact_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".cnt")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".cnt" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_BVIU_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + ".rcp")) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + ".rcp" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

                if compRcp.tag =="ComponentRecipe" and compRcp.get('type') == "SDTC_BVIU_R_Parameter":
                    for srcPath in compRcp:
                        if srcPath.tag =="SourcePath":
                            if os.path.isfile(os.path.join(recipePath, "SDTC", recipeName + "_R.rcp" )) == True:
                                srcPath.text = os.path.join(rcpNetworkPlace, recipeName, "SDTC", recipeName + "_R.rcp" )
                            else:
                                toUpdateFileXmlRoot.remove(compRcp)

            # writing updated template xml to the toUpdateFile
            toUpdateFileXml.write(toUpdateFilePath)
            log("Updating network folder for: " + recipePath + "[COMPLETED]", recipeCreatorLog)
            return True
    except Exception as error:
        log("Updating network folder for: " + recipePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def manifest_file_update(recipePath):
    log("Updating manifest file for: " + recipePath, recipeCreatorLog)
    try:
        recipeName = os.path.basename(recipePath)
        toUpdateFilePath = os.path.join(recipePath, "Manifest", recipeName + ".xml")

        toUpdateFileXml = ET.parse(toUpdateFilePath)
        toUpdateFileXmlRoot = toUpdateFileXml.getroot()

        sdtcXml = ET.parse(os.path.join(recipePath, "SDTC", recipeName + ".xml"))
        sdtcXmlRoot = sdtcXml.getroot()
        sdtcMasXml = ET.parse(os.path.join(recipePath, "SDTC", recipeName + ".mas.xml"))
        sdtcMasXmlRoot =sdtcMasXml.getroot()
        hCXml = ET.parse(os.path.join(recipePath, "HC", recipeName + ".xml"))
        hCXmlRoot = hCXml.getroot()
        hCMasXml = ET.parse(os.path.join(recipePath, "HC", recipeName + ".mas.xml"))
        hCMasXmlRoot = hCMasXml.getroot()
        iOMXml = ET.parse(os.path.join(recipePath, "IOM", recipeName + ".xml"))
        iOMXmlRoot = iOMXml.getroot()

        randomNumber = random.random()


        # result = True
        for compRcp in toUpdateFileXmlRoot:

            if compRcp.tag == "ComponentRecipe" and compRcp.get('type') == "HCRecipeMaster":

                compRcp.set('id', str(hCMasXml.find("Identity").get('id')))
                compRcp.set('version', str(hCMasXml.find("Identity").get('version')))
                compRcp.set('chksum', str(hCMasXmlRoot.get('checksum')))

            elif compRcp.tag == "ComponentRecipe" and compRcp.get('type') == "HC_Recipe Parameter":
                compRcp.set('id', str(hCXml.find("Identity").get('id')))
                compRcp.set('version', str(hCXml.find("Identity").get('version')))
                compRcp.set('chksum', str(hCXmlRoot.get('checksum')))


            elif compRcp.tag == "ComponentRecipe" and compRcp.get('type') == "IOM_Recipe":
                compRcp.set('id', str(iOMXml.find("Identity").get('id')))
                compRcp.set('version', str(iOMXml.find("Identity").get('version')))
                compRcp.set('chksum', str(iOMXmlRoot.get('checksum')))

            elif compRcp.tag == "ComponentRecipe" and compRcp.get('type') == "SDTCRecipeMaster":
                compRcp.set('id', str(sdtcMasXml.find("Identity").get('id')))
                compRcp.set('version', str(sdtcMasXml.find("Identity").get('version')))
                compRcp.set('chksum', str(sdtcMasXmlRoot.get('checksum')))


            elif compRcp.tag == "ComponentRecipe" and compRcp.get('type') == "SDTC_Recipe_Parameter":
                compRcp.set('id', str(sdtcXml.find("Identity").get('id')))
                compRcp.set('version', str(sdtcXml.find("Identity").get('version')))
                compRcp.set('chksum', str(sdtcXmlRoot.get('checksum')))

            elif compRcp.tag == "ComponentRecipe":
                compRcp.set('id', str(uuid.uuid4()).upper())
                checksum = hashlib.md5()
                checksum.update(str(randomNumber).encode('utf-8'))
                compRcp.set('chksum', str(checksum.hexdigest()))

        # writing updated template xml to the toUpdateFile
        toUpdateFileXml.write(toUpdateFilePath)
        log("Updating manifest file for: " + recipePath + "[COMPLETED]", recipeCreatorLog)
        return True
    except Exception as error:
        log("Updating manifest file for: " + recipePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def checksum_creator(toUpdateFilePath):
    log("Creating checksum for: " + toUpdateFilePath, recipeCreatorLog)
    try:

        binaryFile = open(toUpdateFilePath, "rb")
        readBinaryFile = binaryFile.read()
        binaryFile.close()

        ChecksumStartPostion = readBinaryFile.find("<BeginChecksum />".encode('utf-8')) + len("<BeginChecksum />".encode('utf-8'))

        readBinaryFileChecksumPart = readBinaryFile[ChecksumStartPostion:]

        checksum = hashlib.md5()
        checksum.update(readBinaryFileChecksumPart)

        chksString = str(checksum.hexdigest())
        # #print(checksum.hexdigest())

        toUpdateFileXml = ET.parse(toUpdateFilePath)
        toUpdateFileXmlRoot = toUpdateFileXml.getroot()

        if "checksum" in toUpdateFileXmlRoot.attrib:
            toUpdateFileXmlRoot.set('checksum', chksString)
            # writing updated template xml to the toUpdateFile
            toUpdateFileXml.write(toUpdateFilePath)
            log("Creating checksum for: " + toUpdateFilePath + "[COMPLETED]", recipeCreatorLog)
            return True
        else:
            log("Creating checksum for: " + toUpdateFilePath + "[FAILED] - [checksum] attribute does not exist", recipeCreatorLog)
            return False

    except Exception as error:
        log("Creating checksum for: " + toUpdateFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def new_recipe_name_validation(currentRecipe, recipeList):

    log("Verifying the recipe name:" + currentRecipe, recipeCreatorLog)

    validateResult = True
    if currentRecipe.strip() == "":

        validateResult = False
        log("Verifying the recipe name:" + currentRecipe + " [FAILED] - The recipe name is EMPTY", recipeCreatorLog)
        #print("Verifying the recipe name:" + currentRecipe + " [FAILED]")

    else:
        if str(currentRecipe.find(" ")) != "-1":
            validateResult = False
            log("Verifying the recipe name:" + currentRecipe + " [FAILED] - The recipe new name has Whitespace", recipeCreatorLog)
        else:
            count = 0
            for rcp in recipeList:
                if rcp == currentRecipe:
                    count = count + 1
            if count > 1:
                validateResult = False
                log("Verifying the recipe name:" + currentRecipe + " [FAILED] - The recipe new name is DUPLICATED", recipeCreatorLog)

    if validateResult == True:
        log("Verifying the recipe name:" + currentRecipe + " [SUCCESSFUL]", recipeCreatorLog)
        return True
    else:
        return False

def final_recipe_validation(recipePath, specificParaFilePath):
#     Read all xml and make sure it is successfull
#     If the new recipe parameter file exist, check parameter matching
    log("Final verifying for: " + recipePath, recipeCreatorLog)
    isRecipeValid = True
    try:
        recipeName = os.path.basename(recipePath)

        filePath = os.path.join(recipePath, "Manifest", recipeName + ".xml")



        filePath = os.path.join(recipePath, "IOM", recipeName + ".xml")
        iOMXml = ET.parse(filePath)


        filePath = os.path.join(recipePath, "SDTC", recipeName + ".xml")
        sDTCXml = ET.parse(filePath)


        filePath = os.path.join(recipePath, "SDTC", recipeName + ".mas.xml")
        sDTCMasXml = ET.parse(filePath)


        filePath = os.path.join(recipePath, "HC", recipeName + ".mas.xml")
        hCMasXml = ET.parse(filePath)


        filePath = os.path.join(recipePath, "HC", recipeName + ".xml")
        hCXml = ET.parse(filePath)



        if specificParaFilePath.strip() != "":

            paraFileXml = ET.parse(specificParaFilePath)
            paraFileXmlRoot = paraFileXml.getroot()

            for paraComp in paraFileXmlRoot:
                # The xml file in the created recipe is indentified from combination of ComponentRecipe + recipe name
                for paraFileInfo in paraComp:
                    if paraFileInfo.get("name") == "xml":
                        # Read xml file in recipe
                        recipeFilePath = os.path.join(recipePath, paraComp.get('name'),
                                                        os.path.basename(recipePath) + ".xml")
                        recipeFileXml = ET.parse(recipeFilePath)

                    if paraFileInfo.get("name") == "mas.xml":
                        # Read mas xml file in recipe
                        recipeFilePath = os.path.join(recipePath, paraComp.get('name'),
                                                        os.path.basename(recipePath) + ".mas.xml")
                        recipeFileXml = ET.parse(recipeFilePath)

                    # Find in the toUpdateFile, menu having the same name with the template menu paraMenu.get('name')
                    for paraMenu in paraFileInfo.findall("Menu"):

                        rcpMenu = recipeFileXml.find("Menu[@name = " + "'" + paraMenu.get('name') + "'" + "]")

                        if not (rcpMenu is None):

                            #  find in recipe Menu , item having the same name with the parameter Item paraItem.get('name')
                            for paraItem in paraMenu:
                                rcpItem = rcpMenu.find("Item[@name = " + "'" + paraItem.get('name') + "'" + "]")

                                if not (rcpItem is None):

                                    # log(rcpItem.get('name'),recipeCreatorLog)

                                    if str(rcpItem.get('value')) != str(paraItem.get('value')):
                                        isRecipeValid = False
                                        log("Final verifying MISMATCHED for: " + "[" + rcpItem.get('name') + "] of recipe:" + recipeFilePath, recipeCreatorLog)
                                    else:
                                        log("Final verifying MATCHED for: " + "[" + rcpItem.get('name') + "=" + rcpItem.get('value') + "] of recipe:" + recipeFilePath, recipeCreatorLog)
                                else:
                                    isRecipeValid = False
                                    log("Final verifying for: " + recipeFilePath + "[FAILED]" + " :Parameter:" + "[" + rcpItem.get('name') + "] NOT FOUND", recipeCreatorLog)
                        else:
                            isRecipeValid = False
                            log("Final verifying for: " + recipeFilePath + "[FAILED]" + " :Menu:"+ "[" + paraItem.get('name') + "] NOT FOUND", recipeCreatorLog)
    except Exception as error:
        log("Final verifying for: " + recipePath + "[FAILED]" + " Exception during reading xml files", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        isRecipeValid = False
        pass

    return isRecipeValid

def template_validation(tplPath):

    templ1 = os.path.join(tplPath,"HCRecipe_template.xml")
    templ2 = os.path.join(tplPath, "HCRecipeMaster_template.mas.xml")
    templ3 = os.path.join(tplPath, "IOMRecipe_template.xml")
    templ4 = os.path.join(tplPath, "Manifest_template.xml")
    templ5 = os.path.join(tplPath, "SDTCRecipe_template.xml")
    templ6 = os.path.join(tplPath, "SDTCRecipeMaster_template.xml")

    if os.path.isfile(templ1) == False or os.path.isfile(templ2) == False or os.path.isfile(templ3) == False or os.path.isfile(templ4) == False or os.path.isfile(templ5) == False or os.path.isfile(templ6) == False:
        return False
    else:

        try:
            templ1Xml = ET.parse(templ1)
            templ2Xml = ET.parse(templ2)
            templ3Xml = ET.parse(templ3)
            templ4Xml = ET.parse(templ4)
            templ5Xml = ET.parse(templ5)
            templ6Xml = ET.parse(templ6)

            return True

        except Exception as error:
            no_time_log("Exception: " + str(error), recipeCreatorLog)
            return False

# Main multiple recipe creation function
def main(selRecipeListPath, selTemplatePath):

    global summaryLog
    summaryLog = os.path.join(os.getcwd(), "logs", str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + "RecipeCreatorLogSummary.txt")

    log("The template is used:[" + selTemplatePath + "]", recipeCreatorLog)
    log("The recipe list is used:[" + selRecipeListPath + "]", recipeCreatorLog)

    global templatePath
    templatePath = selTemplatePath

    global recipeListPath
    recipeListPath = selRecipeListPath

    if recipeListPath == "" or templatePath == "":



        if recipeListPath == "" and templatePath != "":

            alarmText = "Please select a recipe list!"

        elif recipeListPath != "" and templatePath == "":

            alarmText = "Please select a recipe template!"

        else:

            alarmText = "Please select a recipe template AND a recipe list!"

        AlarmGui(alarmText)

        # if templatePath == "":
        #     Alarm.alarm.set("No template is selected!")
    else:

        app.runButton.config(state = tk.DISABLED)
        app.rcpListButtton.config(state = tk.DISABLED)
        app.rcpTemplateEntry.config(state = tk.DISABLED)
        app.rcpTemplateButton.config(state = tk.DISABLED)
        app.rcpListPathEntry.config(state=tk.DISABLED)
        app.templateFolderCheckbutton.config(state=tk.DISABLED)
        app.rcpCountResult.set("0/0")

        app.stopButton.config(state=tk.NORMAL)


        def callback():

            try:

                # If declare progress at __Main__ function, the progress gui will open automatically
                # progress = ProgressGui()
                # progress.progressMaster.mainloop()

                if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
                    os.makedirs(os.path.join(os.getcwd(), "logs"))

                # global recipeCreatorLog
                # recipeCreatorLog = os.path.join(os.getcwd(), "logs", str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + "RecipeCreatorLog.txt")
                # summaryLog = os.path.join(os.getcwd(), "logs", str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + "RecipeCreatorLogSummary.txt")
                no_time_log("Summary for a job run at: [" + str(datetime.datetime.now()) + "]", summaryLog)
                no_time_log("Recipe template: "+ templatePath, summaryLog)
                no_time_log("Recipe list: "+ recipeListPath, summaryLog)

                #print("=== HCRecipeCreator [Version 2.0]\n"
                      # "=== Created on 03/29/2020 by trong.tong@intel.com\n"
                      # "=== This program is used to convert existing Handler Controller recipes to new ones\n"
                      # "=== Package requirements:\n"
                      # "         - HCRecipeCreator.exe\n"
                      # "         - RecipeCreatorConfig.Xml [File name must be exact]\n"
                      # "         - Handler Controller recipe template folder [Folder name is configurable in the RecipeCreatorConfig.xml]\n"
                      # "         - RecipeList.csv [File name and path are configurable in the RecipeCreatorConfig.xml]\n"
                      # "         - SpecificParameter.xml [File name and path are configurable in RecipeList.csv]\n"
                      # "=== Successfully converted recipes are in RecipeConvert folder\n"
                      # "=== Result of recipe conversion is reported in a summary log in the logs folder\n"
                      # "=== See full logs in the logs folder for more detail\n")

                log("STARTING TO CONVERT RECIPES", recipeCreatorLog)
                #print("STARTING TO CONVERT RECIPES")

                # get current directory
                scriptDir = os.getcwd()

                # Delete ConvertRecipe and SourceAlignmentRecipes folde
                # if os.path.isdir(os.path.join(scriptDir,newRcpDir)):
                #     for dir in os.listdir(os.path.join(scriptDir,newRcpDir)):
                #         if os.path.isdir(dir):
                #             #print(dir)


                global verifyFlag
                global newRcpDir
                newRcpDir = "Recipe_"+str(datetime.datetime.now().strftime("%m%d_%H%M%S"))
                newRcpDirPath = os.path.join(scriptDir, newRcpDir)
                verifyFlag = True
                # = Old design ========================
                # Delete folders inside newRcpDir (ConvertRecipes) folder
                # All previously created recipes will be deleted
                # if verifyFlag == True:
                #     try:
                #
                #         newRcpDirPath = os.path.join(scriptDir, newRcpDir)
                #         # #print(newRcpDirPath)
                #
                #         if os.path.isdir(newRcpDirPath):
                #
                #             for dir in os.listdir(newRcpDirPath):
                #                 subDirPath = os.path.join(newRcpDirPath,dir)
                #                 if os.path.isdir(subDirPath):
                #                     shutil.rmtree(subDirPath)
                #
                #     except Exception as error:
                #         verifyFlag = False
                #         #print("Cannot delete: " + os.path.join(scriptDir,newRcpDir))
                #         #print("The process is terminated!")
                #         log("Cannot delete: " + os.path.join(scriptDir,newRcpDir), recipeCreatorLog)
                #         log("The process is terminated!", recipeCreatorLog)
                #         no_time_log(str(error),recipeCreatorLog)
                #
                #         app.progress.set("The recipe creation process is terminated! [Error: Deleting the local recipe folder]")
                #
                # # ==== Old design=======================
                #
                # Creating a new folder to store recipes

                # newRcpDir = str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + "_ConvertedRecipes"



                # Read and verify RecipeCreatorConfig.xml

                global networkDrive
                global networkFolder

                recipeFileList = str(recipeListPath)

                # if verifyFlag == True:
                #
                #     # verifyFlag, templatePath, networkDrive, networkFolder, recipeFileList = configuration_read()
                #
                #     verifyFlag, templatePath, networkDrive, networkFolder, recipeCopyTimeout = configuration_read()


                # Read Recipe List

                recipeListFields =[]
                recipeListRows = []
                recipeNewNameList =[]
                srcRecipeNameList = []
                if verifyFlag == True:
                    # lists of fields and rows of RecipeList

                    # Read RecipeList.csv
                    log("Reading:" + recipeFileList,recipeCreatorLog)
                    #print("Reading:" + recipeFileList)
                    if os.path.isfile(recipeFileList):
                        try:
                            with open(recipeFileList,'r') as csvfile:
                                csvreader = csv.reader(csvfile)

                                # extract field names via first row
                                recipeListFields= next(csvreader)
                                no_time_log("|  |".join(recipeListFields), recipeCreatorLog)

                                # extract row data
                                for row in csvreader:
                                    recipeListRows.append(row)
                                    recipeNewNameList.append(row[3])
                                    srcRecipeNameList.append(row[0])
                                    # join all column strings intro a string with |***| in between each string of column
                                    no_time_log("|  |".join(row), recipeCreatorLog)

                                log("Reading:" + recipeFileList + " [COMPLETED]",recipeCreatorLog)
                                #print("Reading:" + recipeFileList + " [COMPLETED]")
                        except Exception as error:
                            verifyFlag = False
                            log("Reading:" + recipeFileList + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Reading:" + recipeFileList + " [FAILED]")
                            no_time_log("Error occured during reading the recile list. No recipe is converted",summaryLog)
                            app.progress.set("The recipe creation process is terminated! [Error: Read recipe list]")
                    else:
                        #print("Error: The file at:[" + recipeFileList + "] is not found" )
                        #print("Reading:" + recipeFileList + " [FAILED]")

                        log("Reading:" + recipeFileList + " [FAILED]", recipeCreatorLog)
                        log("Error: The file at:[" + recipeFileList + "] is not found", recipeCreatorLog)

                        no_time_log("Error occured during reading the recile list. No recipe is converted", summaryLog)
                        app.progress.set("The recipe creation process is terminated! [Error: Read recipe list]")
                        verifyFlag = False


                # Column numbers of SourceRecipe, SourceAlignmentRecipe, NewRecipeLocation, NewRecipeName, SpecificParameterUpdateFile


                # Verifying recipeList

                if verifyFlag == True:

                    log("Verifying:"+recipeFileList,recipeCreatorLog)
                    i = 1
                    for field in recipeListFields:

                        if i == 1:
                            no_time_log("Expected column name = [SourceRecipe]",recipeCreatorLog)
                            no_time_log("Current column name in RecipeList = [" + field +']',recipeCreatorLog)
                            verifyFlag = verifyFlag and (field =="SourceRecipe")
                            if field =="SourceRecipe":
                                no_time_log("-----------SoureRcipe column name is MATCHED-----------",recipeCreatorLog)
                            else:
                                no_time_log("-----------SoureRcipe column name is MISMATCHED-----------",recipeCreatorLog)
                        elif i == 2:
                            no_time_log("Expected column name = [SourceAlignmentRecipe]",recipeCreatorLog)
                            no_time_log("Current column name in RecipeList = [" + field +']',recipeCreatorLog)
                            verifyFlag = verifyFlag and (field =="SourceAlignmentRecipe")
                            if field =="SourceAlignmentRecipe":
                                no_time_log("-----------SourceAlignmentRecipe column name is MATCHED-----------",recipeCreatorLog)
                            else:
                                no_time_log("-----------SourceAlignmentRecipe column name is MISMATCHED-----------",recipeCreatorLog)

                        elif i == 3:
                            no_time_log("Expected column name = [NewRecipeLocation]", recipeCreatorLog)
                            no_time_log("Current column name in RecipeList = [" + field + ']', recipeCreatorLog)
                            verifyFlag = verifyFlag and (field =="NewRecipeLocation")
                            if field =="NewRecipeLocation":
                                no_time_log("-----------NewRecipeLocation column name is MATCHED-----------",recipeCreatorLog)
                            else:
                                no_time_log("-----------NewRecipeLocation column name is MISMATCHED-----------",recipeCreatorLog)
                        elif i == 4:
                            no_time_log("Expected column name = [NewRecipeName]", recipeCreatorLog)
                            no_time_log("Current column name in RecipeList = [" + field + ']', recipeCreatorLog)
                            verifyFlag = verifyFlag and (field =="NewRecipeName")
                            if field =="NewRecipeName":
                                no_time_log("-----------NewRecipeName column name is MATCHED-----------",recipeCreatorLog)
                            else:
                                no_time_log("-----------NewRecipeName column name is MISMATCHED-----------",recipeCreatorLog)
                        elif i == 5:
                            no_time_log("Expected column name = [SourceAlignmentRecipe]", recipeCreatorLog)
                            no_time_log("Current column name in RecipeList = [" + field + ']', recipeCreatorLog)
                            verifyFlag = verifyFlag and (field =="SpecificParameterUpdateFile")
                            if field =="SpecificParameterUpdateFile":
                                no_time_log("-----------SpecificParameterUpdateFile column name is MATCHED-----------",recipeCreatorLog)
                            else:
                                no_time_log("-----------SpecificParameterUpdateFile column name is MISMATCHED-----------",recipeCreatorLog)
                        i = i+1

                    if verifyFlag:
                        log("Final result of RecipeList verification: VALID",recipeCreatorLog)
                    else:
                        log("Final result of RecipeList verification: INVALID",recipeCreatorLog)
                        log("Recipe conversion is terminated - Name of RecipeList.csv's columns are incorrect", recipeCreatorLog)
                        no_time_log("Final result of RecipeList verification: INVALID. Recipe conversion is terminated - Name of RecipeList.csv's columns are incorrect", summaryLog)
                        app.progress.set("The recipe creation process is terminated! [Error: Recipe list is INVALID]")

                # Varifying the template
                if verifyFlag == True:

                    log("Validating the template: " + templatePath, recipeCreatorLog)

                    verifyFlag = template_validation(templatePath)

                    if verifyFlag == True:
                        log("Validation succeeded for: " + templatePath, recipeCreatorLog)

                    else:

                        #print("Validation failed for: "+ templatePath)
                        #print("The process is terminated!")
                        log("Validation failed for: "+ templatePath, recipeCreatorLog)
                        log("The process is terminated!", recipeCreatorLog)
                        app.progress.set("The recipe creation process is terminated! [Error: Templates are INVALID]")


                # ======================================================================================
                # START RECIPE CONVERSION
                convertedRcpList =[]
                failedRcpList = []

                processFlag =""
                if verifyFlag == True:



                    newRcpDirPath = os.path.join(scriptDir, newRcpDir)

                    # srcAlignRcpDirPath = os.path.join(scriptDir, srcAlignRcpDir)

                    srcRcpColIndex = 0
                    srcAlignRcpColIndex = 1
                    newRcpLocColIndex = 2
                    newRcpNameColIndex = 3
                    spfParUpdFileColIndex = 4
                    prcRcpNameColIndex = 5

                    # list to store recipes which are copied to SourceAlignmentRecipes
                    srcAlignRcpCopiedList = []

                    #Flag to add a recipe to processing list
                    # Loop through all recipes need to be converted in the list and convert the recipe
                    # At the end of a loop, a recipe conversion will be completed
                    contProcessFlag = True
                    cvtRcpPath =""
                    row =""


                    rowIndex =0

                    # MAIN LOOP TO CONVERT RECIPE LIST
                    rcpProcessedCount = 0
                    app.progressBar["value"] = 0
                    rcpNeedToCreateCount = len(recipeListRows)

                    app.progressBar["maximum"] = rcpNeedToCreateCount

                    # Event object used to send signals from one thread to another
                    global stop_event
                    stop_event = Event()

                    app.progress.set("Recipe creation is in progress...")


                    stopFlag = False
                    for row in recipeListRows:
                        # Number of recipe has been processed
                        # Update progress bar status
                        rcpProcessedCount = rcpProcessedCount + 1
                        app.progressBar["value"] = rcpProcessedCount
                        processStatusStr = str(rcpProcessedCount) + "/" + str(len(recipeListRows))
                        app.processedCount.set(processStatusStr)

                        app.rcpCountResult.set(str(len(convertedRcpList)) + "/" + str(len(failedRcpList)))

                        contProcessFlag = True
                        source = row[srcRcpColIndex]
                        srcRcpName = os.path.basename(source)
                        cvtRcpPath = os.path.join(newRcpDirPath, "temp", srcRcpName)
                        cvtRcppathRoot = os.path.join(newRcpDirPath, "temp")

                        # Delete temp if it exist
                        if os.path.isdir(cvtRcppathRoot):
                            for dir in os.listdir(cvtRcppathRoot):
                                if os.path.isdir(os.path.join(cvtRcppathRoot,dir)):

                                    shutil.rmtree(os.path.join(cvtRcppathRoot,dir))


                        # no_time_log("\n",recipeCreatorLog)
                        no_time_log("*******************************************************************************************", recipeCreatorLog)
                        # log("Start to process the recipe:" + source, recipeCreatorLog)
                        # #print("\nStart to process the recipe:" + source)

                        rowIndex = rowIndex + 1
                        # Validate recipe new name
                        if contProcessFlag == True:

                            log("Start to process the recipe:" + source, recipeCreatorLog)
                            #print("\nStart to process the recipe:" + source)
                            check = new_recipe_name_validation(row[newRcpNameColIndex], recipeNewNameList)

                            if check == True:
                                contProcessFlag = True
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0,"Failed to validate recipe name: " + row[newRcpNameColIndex])
                                tempRow.insert(0,str(rowIndex))

                                failedRcpList.append(tempRow)

                        #  copy the recipe from the source
                        if contProcessFlag == True:
                            # no_time_log("\n", recipeCreatorLog)
                            log("Copying:"+source, recipeCreatorLog)
                            #print("Copying:"+source)
                            # try:

                            # Using copytree method to copy folder
                            # shutil.copytree(source, cvtRcpPath, dirs_exist_ok=True)

                            # using copyFolder function - which use shutil.copyfile
                            # Set timeout for recipe

                            # Create a Process

                            # global Q
                            Q = Queue()
                            recipe_copy_process = Process(target= copyFolder, args=(source, cvtRcppathRoot,Q,recipeCreatorLog))

                            # Start the process and we block for X seconds.
                            try:
                                recipe_copy_process.start()
                                if Q.get() == False:


                                    contProcessFlag = False

                                    log("Copying:" + source + " [FAILED]", recipeCreatorLog)

                                    #print("Copying:" + source + " [FAILED]")

                                    log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    tempRow = row
                                    tempRow.insert(0,"Failed to copy the recipe from the source: " + source + ". Possible reasons: The source recipe does not exist. The recipe is corrupted. Access perssion issue. The recipe has been existed on the recipe converted folder")
                                    tempRow.insert(0, str(rowIndex))

                                    failedRcpList.append(tempRow)

                                    # Deleted the corrupted folder from the Converted recipe folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)

                                    # continue


                            except Exception as error:

                                contProcessFlag = False

                                log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                                no_time_log(str(error), recipeCreatorLog)
                                #print("Copying:" + source + " [FAILED]")

                                log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                tempRow = row
                                tempRow.insert(0,"Failed to copy the recipe from the source: " + source + ". Possible reasons: The source recipe does not exist. The recipe is corrupted. Access perssion issue. The recipe has been existed on the recipe converted folder")
                                tempRow.insert(0,str(rowIndex))

                                failedRcpList.append(tempRow)

                                # Deleted the corrupted folder from the Converted recipe folder

                                if os.path.isdir(cvtRcpPath):
                                    shutil.rmtree(cvtRcpPath)

                                # continue

                            # Wait for 10 second even the recipe_copy_process is running.

                            if contProcessFlag == True:
                                recipe_copy_process.join(timeout=float(recipeCopyTimeout))

                                # Check if the thread is still alive
                                if recipe_copy_process.is_alive() is True:
                                    # terminate the thread
                                    recipe_copy_process.terminate()

                                    contProcessFlag = False
                                    log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                                    no_time_log("Timeout = " + recipeCopyTimeout + "for copying:", recipeCreatorLog)
                                    #print("Copying:" + source + " [FAILED]")

                                    log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    tempRow = row
                                    tempRow.insert(0,"Failed (Timeout for:" + recipeCopyTimeout + ") to copy the recipe from the source: " + source)
                                    tempRow.insert(0, str(rowIndex))

                                    failedRcpList.append(tempRow)

                                    # Deleted the corrupted folder from the Converted recipe folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                            # else:
                            #
                            #     log("Copying:" + source + " [COMPLETED]", recipeCreatorLog)
                            #     #print("Copying:" + source + " [COMPLETED]")

                                # update modified time of cvtRcpPath folder
                                # os.utime(cvtRcpPath)
                                # for (paths, subdirs, files) in os.walk(cvtRcpPath):
                                #     os.utime(paths)
                                #     for file in files:
                                #         os.utime(os.path.join(paths, file))

                            # except Exception as error:
                            #     contProcessFlag = False
                            #     log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                            #     no_time_log(str(error), recipeCreatorLog)
                            #     #print("Copying:" + source + " [FAILED]")
                            #
                            #     log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #     #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                            #
                            #     tempRow = row
                            #     tempRow.insert(0,"Failed to copy the recipe from the source: " + source + ". Possible reasons: The source recipe does not exist. The recipe is corrupted. Access perssion issue. The recipe has been existed on the recipe converted folder")
                            #     tempRow.insert(0,str(rowIndex))
                            #
                            #     failedRcpList.append(tempRow)
                            #
                            #     # Deleted the corrupted folder from the Converted recipe folder
                            #     shutil.rmtree(cvtRcpPath, ignore_errors=True)
                            #
                            #     continue

                        #  alignment file update
                        if contProcessFlag == True:
                            srcAlignRcpPath = row[srcAlignRcpColIndex]
                            srcAlignRcpName = os.path.basename(srcAlignRcpPath)

                            # Process the alignment recipe update IF the alignment recipe exists AND the alignment recipe is different from the source recipe on the RecipeList.csv


                            if srcAlignRcpPath != "" and srcAlignRcpPath != row[srcRcpColIndex]:


                                probeAlignPTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPTN_FileExt)
                                probeAlignPRB_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPRB_FileExt)

                                unitAlignUTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUTN_FileExt)
                                unitAlignUNT_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUNT_FileExt)


                                try:
                                    # Delete current probe and unit alignment files
                                    log("Deleting probe alignment file:" + probeAlignPTN_File, recipeCreatorLog)
                                    os.remove(probeAlignPTN_File)
                                    log("Deleting probe alignment file:" + probeAlignPTN_File + " [COMPLETED]", recipeCreatorLog)


                                    log("Deleting probe alignment file:" + probeAlignPRB_File, recipeCreatorLog)
                                    os.remove(probeAlignPRB_File)
                                    log("Deleting probe alignment file:" + probeAlignPRB_File + " [COMPLETED]", recipeCreatorLog)

                                    log("Deleting unit alignment file:" + unitAlignUTN_File, recipeCreatorLog)
                                    os.remove(unitAlignUTN_File)
                                    log("Deleting unit alignment file:" + unitAlignUTN_File + " [COMPLETED]", recipeCreatorLog)

                                    log("Deleting unit alignment file:" + unitAlignUNT_File, recipeCreatorLog)
                                    os.remove(unitAlignUNT_File)
                                    log("Deleting unit alignment file:" + unitAlignUNT_File + " [COMPLETED]", recipeCreatorLog)


                                    srcFiles = os.listdir(os.path.join(srcAlignRcpPath,"SDTC"))
                                    dstDir = os.path.join(cvtRcpPath,"SDTC")

                                    # Looking into SDTC folder of the source recipe for alignment files
                                    for f in srcFiles:
                                        fileName = os.path.basename(f)

                                        srcSDTCFile = os.path.join(srcAlignRcpPath, "SDTC", fileName)

                                        # Copy alignment files from source alignment recipe and rename the files to the source recipe name
                                        # Find the file with extension '.ptn'
                                        if fileName.split('.')[len(fileName.split('.'))-1] == probeAlignPTN_FileExt:
                                            log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                            # shutil.copy2(srcSDTCFile, dstDir)

                                            dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt)
                                            shutil.copyfile(srcSDTCFile, dstFile)

                                            log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]", recipeCreatorLog)

                                            # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt), recipeCreatorLog)
                                            # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))
                                            # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt) + " [COMPLETED]", recipeCreatorLog)
                                            #
                                            # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))

                                        # Find the file with extension '.prb'
                                        if fileName.split('.')[len(fileName.split('.'))-1] == probeAlignPRB_FileExt:
                                            log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                            # shutil.copy2(srcSDTCFile, dstDir)

                                            dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt)
                                            shutil.copyfile(srcSDTCFile, dstFile)

                                            log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]", recipeCreatorLog)

                                            # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt), recipeCreatorLog)
                                            # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                                            # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt) + " [COMPLETED]", recipeCreatorLog)

                                            # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                                        # Find the file with extension '.utn'
                                        if fileName.split('.')[len(fileName.split('.'))-1] == unitAlignUTN_FileExt:
                                            log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                            # shutil.copy2(srcSDTCFile, dstDir)

                                            dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt)
                                            shutil.copyfile(srcSDTCFile, dstFile)

                                            log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]", recipeCreatorLog)

                                            # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt), recipeCreatorLog)
                                            # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                                            # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt) + " [COMPLETED]", recipeCreatorLog)

                                            # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                                        # Find the file with extension '.unt'
                                        if fileName.split('.')[len(fileName.split('.'))-1] == unitAlignUNT_FileExt:
                                            log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                            # shutil.copy2(srcSDTCFile, dstDir)

                                            dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt)
                                            shutil.copyfile(srcSDTCFile, dstFile)

                                            log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]", recipeCreatorLog)

                                            # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt), recipeCreatorLog)
                                            # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))
                                            # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt) + " [COMPLETED]", recipeCreatorLog)
                                            #
                                            # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))




                                    # Update the probe alignment and unit alignment box size for SDTC.xml

                                    alignSrcRcpSdtcXmlPath = os.path.join(srcAlignRcpPath, "SDTC", srcAlignRcpName + ".xml")
                                    dstRcpSdtcXmlPath = os.path.join(cvtRcpPath, "SDTC", srcRcpName + ".xml")
                                    tempAlignSrcRcpSdtcXmlPath = os.path.join(scriptDir, newRcpDir,"tempAlign\\sdtc.xml")

                                    if not os.path.exists(os.path.join(scriptDir, newRcpDir,"tempAlign")):
                                        os.mkdir(os.path.join(scriptDir, newRcpDir,"tempAlign"))
                                    shutil.copy2(alignSrcRcpSdtcXmlPath,tempAlignSrcRcpSdtcXmlPath)

                                    sdtcAlignSrcRcpXml = ET.parse(tempAlignSrcRcpSdtcXmlPath)
                                    sdtcAlignSrcRcpXmlRoot = sdtcAlignSrcRcpXml.getroot()


                                    sdtcDstRcpXml = ET.parse(dstRcpSdtcXmlPath)
                                    sdtcDstRcpXmlRoot = sdtcDstRcpXml.getroot()

                                    log("Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath,recipeCreatorLog)
                                    prbP1W = ""
                                    prbP1H = ""
                                    prbP2W = ""
                                    prbP2H = ""
                                    prbP3W = ""
                                    prbP3H = ""
                                    prbP4W = ""
                                    prbP4H = ""

                                    prbP1Wexist = False
                                    prbP1Hexist = False
                                    prbP2Wexist = False
                                    prbP2Hexist = False
                                    prbP3Wexist = False
                                    prbP3Hexist = False
                                    prbP4Wexist = False
                                    prbP4Hexist = False

                                    untP1W = ""
                                    untP1H = ""
                                    untP2W = ""
                                    untP2H = ""

                                    untP1Wexist = False
                                    untP1Hexist = False
                                    untP2Wexist = False
                                    untP2Hexist = False

                                    for sdtcAlignSrcRcpXmlSubRoot in sdtcAlignSrcRcpXmlRoot:
                                        if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Probe":
                                            for x in sdtcAlignSrcRcpXmlSubRoot:
                                                if x.get('name') == "Pattern1_Wide":
                                                    prbP1W = x.get('value')
                                                    prbP1Wexist = True
                                                if x.get('name') == "Pattern1_Height":
                                                    prbP1H = x.get('value')
                                                    prbP1Hexist = True
                                                if x.get('name') == "Pattern2_Wide":
                                                    prbP2W = x.get('value')
                                                    prbP2Wexist = True
                                                if x.get('name') == "Pattern2_Height":
                                                    prbP2H = x.get('value')
                                                    prbP2Hexist = True
                                                if x.get('name') == "Pattern3_Wide":
                                                    prbP3W = x.get('value')
                                                    prbP3Wexist = True
                                                if x.get('name') == "Pattern3_Height":
                                                    prbP3H = x.get('value')
                                                    prbP3Hexist = True
                                                if x.get('name') == "Pattern4_Wide":
                                                    prbP4W = x.get('value')
                                                    prbP4Wexist = True
                                                if x.get('name') == "Pattern4_Height":
                                                    prbP4H = x.get('value')
                                                    prbP4Hexist = True


                                        if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Unit Alignment":
                                            for x in sdtcAlignSrcRcpXmlSubRoot:
                                                if x.get('name') == "Pattern1_Wide":
                                                    untP1W = x.get('value')
                                                    untP1Wexist = True
                                                if x.get('name') == "Pattern1_Height":
                                                    untP1H = x.get('value')
                                                    untP1Hexist = True
                                                if x.get('name') == "Pattern2_Wide":
                                                    untP2W = x.get('value')
                                                    untP2Wexist = True
                                                if x.get('name') == "Pattern2_Height":
                                                    untP2H = x.get('value')
                                                    untP2Hexist = True


                                    for sdtcDstRcpXmlSubRoot in sdtcDstRcpXmlRoot:
                                        if sdtcDstRcpXmlSubRoot.get('name') == "Probe":
                                            for x in sdtcDstRcpXmlSubRoot:
                                                if x.get('name') == "Pattern1_Wide" and prbP1Wexist ==True:
                                                    x.set('value', prbP1W)
                                                if x.get('name') == "Pattern1_Height" and prbP1Hexist ==True:
                                                    x.set('value', prbP1H)
                                                if x.get('name') == "Pattern2_Wide" and prbP2Wexist ==True:
                                                    x.set('value', prbP2W)
                                                if x.get('name') == "Pattern2_Height" and prbP2Hexist ==True:
                                                    x.set('value', prbP2H)
                                                if x.get('name') == "Pattern3_Wide" and prbP3Wexist ==True:
                                                    x.set('value', prbP3W)
                                                if x.get('name') == "Pattern3_Height" and prbP3Hexist ==True:
                                                    x.set('value', prbP3H)
                                                if x.get('name') == "Pattern4_Wide" and prbP4Wexist ==True:
                                                    x.set('value', prbP4W)
                                                if x.get('name') == "Pattern4_Height" and prbP4Hexist ==True:
                                                    x.set('value', prbP4H)


                                        if sdtcDstRcpXmlSubRoot.get('name') == "Unit Alignment":
                                            for x in sdtcDstRcpXmlSubRoot:
                                                if x.get('name') == "Pattern1_Wide" and untP1Wexist == True:
                                                    x.set('value', untP1W)
                                                if x.get('name') == "Pattern1_Height" and untP1Hexist == True:
                                                    x.set('value', untP1H)
                                                if x.get('name') == "Pattern2_Wide" and untP2Wexist == True:
                                                    x.set('value', untP2W)
                                                if x.get('name') == "Pattern2_Height" and untP2Hexist == True:
                                                    x.set('value', untP2H)


                                    sdtcDstRcpXml.write(dstRcpSdtcXmlPath)
                                    # Delete ConvertRecipe\\tempAlign
                                    shutil.rmtree(os.path.join(scriptDir, newRcpDir,"tempAlign"))
                                    log("Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath + " [COMPLETED]",recipeCreatorLog)

                                except Exception as error:
                                    contProcessFlag = False
                                    log("Updating alignment files for:" + cvtRcpPath + " [FAILED]", recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    #print("Updating alignment files for:" + cvtRcpPath + " [FAILED]")
                                    log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    tempRow = row
                                    tempRow.insert(0,"Failed to process the alignment file update")
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                                    # continue


                        # Rename files in each recipe
                        if contProcessFlag == True:

                            #print("The recipe conversion is in progress...")
                            log("Starting to rename the recipe", recipeCreatorLog)
                            log("Renaming:"+cvtRcpPath, recipeCreatorLog)

                            # get recipe new name
                            newRcpName = row[newRcpNameColIndex]

                            # Renaming files HC folder
                            folderPath = os.path.join(cvtRcpPath, "HC")
                            files = os.listdir(folderPath)

                            for f in files:
                                src = ""
                                dst = ""
                                fileName = os.path.basename(f)
                                try:
                                    if fileName.find('mas') != -1:
                                        newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.'))-1]
                                        src= os.path.join(folderPath,f)
                                        dst= os.path.join(folderPath,newFileName)
                                        log("Renaming:" + src,recipeCreatorLog)
                                        os.rename(src,dst)
                                        log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                                    else:
                                        newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.'))-1]
                                        src= os.path.join(folderPath,f)
                                        dst= os.path.join(folderPath,newFileName)
                                        log("Renaming:" + src, recipeCreatorLog)
                                        os.rename(src,dst)
                                        log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                                except Exception as error:

                                    contProcessFlag = False

                                    tempRow = row
                                    tempRow.insert(0,"Failed to rename the file:" + f)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    log("Renaming:" + src + " [FAILED]",recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    #print("Renaming:" + src + " [FAILED]")
                                    # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                                    # continue


                            #Renaming file in IOM folder

                            folderPath = os.path.join(cvtRcpPath, "IOM")
                            files = os.listdir(folderPath)

                            for f in files:
                                src = ""
                                dst = ""
                                fileName = os.path.basename(f)
                                try:

                                    newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                    src = os.path.join(folderPath, f)
                                    dst = os.path.join(folderPath, newFileName)
                                    log("Renaming:" + src, recipeCreatorLog)
                                    os.rename(src, dst)
                                    log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                                except Exception as error:

                                    contProcessFlag = False

                                    tempRow = row
                                    tempRow.insert(0,"Failed to rename the file:" + f)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    #print("Renaming:" + src + " [FAILED]")
                                    # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                                    # continue


                            # Renaming file in Manifest folder

                            folderPath = os.path.join(cvtRcpPath, "Manifest")
                            files = os.listdir(folderPath)

                            for f in files:
                                src = ""
                                dst = ""
                                fileName = os.path.basename(f)
                                try:

                                    newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                    src = os.path.join(folderPath, f)
                                    dst = os.path.join(folderPath, newFileName)
                                    log("Renaming:" + src, recipeCreatorLog)
                                    os.rename(src, dst)
                                    log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                                except Exception as error:

                                    contProcessFlag = False

                                    tempRow = row
                                    tempRow.insert(0,"Failed to rename the file:" + f)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    #print("Renaming:" + src + " [FAILED]")
                                    # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                                    # continue


                            # Renaming files in SDTC folder
                            folderPath = os.path.join(cvtRcpPath, "SDTC")
                            files = os.listdir(folderPath)

                            for f in files:
                                src = ""
                                dst = ""
                                fileName = os.path.basename(f)
                                try:
                                    if fileName.find('mas') != -1:
                                        newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                        src = os.path.join(folderPath, f)
                                        dst = os.path.join(folderPath, newFileName)
                                        log("Renaming:" + src, recipeCreatorLog)
                                        os.rename(src, dst)
                                        log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                                    elif fileName.find('_R.rcp') != -1:
                                        newFileName = newRcpName + "_R" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                        src = os.path.join(folderPath, f)
                                        dst = os.path.join(folderPath, newFileName)
                                        log("Renaming:" + src, recipeCreatorLog)
                                        os.rename(src, dst)
                                        log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                                    else:
                                        newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                        src = os.path.join(folderPath, f)
                                        dst = os.path.join(folderPath, newFileName)
                                        log("Renaming:" + src, recipeCreatorLog)
                                        os.rename(src, dst)
                                        log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                                except Exception as error:

                                    contProcessFlag = False

                                    tempRow = row
                                    tempRow.insert(0,"Failed to rename the file:" + f)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    #print("Renaming:" + src + " [FAILED]")
                                    # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)
                                    # continue



                            # Renaming the root recipe folder
                            # Wait 2 seconds before remaing the root folder to make sure all fies are updated
                            # time.sleep(1)
                            if contProcessFlag == True:
                                src =""
                                dst =""

                                try:
                                    src = cvtRcpPath
                                    dst = os.path.join(newRcpDirPath,newRcpName)
                                    # copyFolder1(src,dst)
                                    shutil.copytree(src,dst)
                                    log("Copy and change name of the recipe folder: " + src + " TO: " + dst + " [COMPLETED]", recipeCreatorLog)
                                except Exception as error:
                                    contProcessFlag = False

                                    tempRow = row
                                    tempRow.insert(0, "Failed to Copy and change name of the folder:" + src + " To:" + dst)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    log("Copy and change name of folder: " + src + " TO: " + dst + " [FAILED]", recipeCreatorLog)
                                    no_time_log(str(error), recipeCreatorLog)
                                    log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                                    #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)


                                    # Remove the corrupted folder
                                    if os.path.isdir(cvtRcpPath) == True:
                                        shutil.rmtree(cvtRcpPath)

                                    if os.path.isdir(dst) == True:
                                        shutil.rmtree(dst)
                                    # continue



                        # Updating the recipe to the template

                        if contProcessFlag == True:

                            newRcpName = row[newRcpNameColIndex]
                            newRcpPath = os.path.join(newRcpDirPath, newRcpName)

                            log("Updating:" + newRcpPath + "To the templates:" + templatePath, recipeCreatorLog)
                            check1 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipe_template.xml"), os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"), templateLine= "Add")
                            check2 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipeMaster_template.xml"), os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"), templateLine= "Add")
                            check3 = sdtc_type_template_update(os.path.join(templatePath, "IOMRecipe_template.xml"), os.path.join(newRcpPath, "IOM", newRcpName + ".xml"), templateLine= "Add")
                            check4 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipe_template.xml"), os.path.join(newRcpPath, "HC", newRcpName + ".xml"), templateLine = "" )
                            check5 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipeMaster_template.mas.xml"), os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"), templateLine= "Remove")

                            check6 = manifest_type_template_update(os.path.join(templatePath, "Manifest_template.xml"), os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                            if check1 and check2 and check3 and check4 and check5 and check6:
                                contProcessFlag = True
                                log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "Failed to update the recipe to the templates:" + templatePath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)

                                log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [FAILED]", recipeCreatorLog)

                        # Update Identity line for xml files
                        if contProcessFlag == True:

                            log("Updating identity line for:" + newRcpPath, recipeCreatorLog)
                            check1 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                            check2 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                            check3 = identity_update(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                            check4 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                            check5 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                            check6 = identity_update(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                            if check1 and check2 and check3 and check4 and check5 and check6:
                                contProcessFlag = True
                                log("Updating identity line for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0,"Failed to update Identity line for:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)

                                log("Updating identity line for:" + newRcpPath + " [FAILED]", recipeCreatorLog)


                        # Update value of mas xml files
                        if contProcessFlag == True:

                            log("Updating value of mas.xml files for:" + newRcpPath, recipeCreatorLog)

                            check1 = mas_file_parameter_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                            check2 = mas_file_parameter_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))

                            if check1 and check2:
                                contProcessFlag = True
                                log("Updating value of mas.xml files for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "Failed to update value of mas.xml files for:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)

                                log("Updating value of mas.xml files for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                        #  Update specific parameter
                        #  If there is no specific parameter link -> DO nothing and Continue

                        if contProcessFlag == True:

                            specificParaFilePath = row[spfParUpdFileColIndex]
                            if specificParaFilePath.strip() != "":
                                if os.path.isfile(specificParaFilePath.strip()):

                                    log("Updating specific parameters for:" + newRcpPath + "Using:" + specificParaFilePath,
                                        recipeCreatorLog)

                                    check = specific_para_file_update(newRcpPath, specificParaFilePath)

                                    if check == True:
                                        contProcessFlag = True
                                        log(
                                            "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]",
                                            recipeCreatorLog)
                                    else:
                                        contProcessFlag = False
                                        tempRow = row
                                        tempRow.insert(0, "Failed to update specific parameters for:" + newRcpPath)
                                        tempRow.insert(0, str(rowIndex))
                                        failedRcpList.append(tempRow)

                                        # Remove the corrupted folder
                                        if os.path.isdir(newRcpPath) == True:
                                            shutil.rmtree(newRcpPath)
                                        log(
                                            "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                            recipeCreatorLog)
                                else:
                                    contProcessFlag = False
                                    tempRow = row
                                    tempRow.insert(0, "Failed to update specific parameters for:" + newRcpPath)
                                    tempRow.insert(0, str(rowIndex))
                                    failedRcpList.append(tempRow)

                                    # Remove the corrupted folder
                                    if os.path.isdir(newRcpPath) == True:
                                        shutil.rmtree(newRcpPath)
                                    log(
                                        "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                        recipeCreatorLog)
                                    no_time_log("The parameter file at:[" + specificParaFilePath.strip() + "] could not be found", recipeCreatorLog)

                            else:
                                log("There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                                    recipeCreatorLog)

                        # Test new way to catch exception
                        # if contProcessFlag == True:
                        #
                        #     specificParaFilePath = row[spfParUpdFileColIndex]
                        #     if specificParaFilePath.strip() != "":
                        #
                        #         log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath,
                        #             recipeCreatorLog)
                        #         try:
                        #             specific_para_file_update(newRcpPath, specificParaFilePath)
                        #             contProcessFlag = True
                        #             log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]", recipeCreatorLog)
                        #         except Exception:
                        #
                        #             contProcessFlag = False
                        #
                        #             tempRow = row
                        #             tempRow.insert(0, "Failed to update specific parameters for:" + newRcpPath)
                        #             tempRow.insert(0, str(rowIndex))
                        #             failedRcpList.append(tempRow)
                        #
                        #             log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                        #             #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                        #
                        #             # Remove the corrupted folder
                        #             shutil.rmtree(cvtRcpPath, ignore_errors=True)
                        #             continue
                        #     else:
                        #         log("There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                        #             recipeCreatorLog)

                        # Update network folder for Manifest.xml
                        if contProcessFlag == True:
                            # templatePath = ""
                            # networkDrive = ""
                            # networkFolder = ""
                            # recipeFileList = ""

                            log("Updating network folder for:" + newRcpPath, recipeCreatorLog)

                            absNetworkFolder = row[newRcpLocColIndex]
                            check = network_folder_manifest_file_update(newRcpPath, absNetworkFolder, networkFolder, networkDrive)

                            if check == True:
                                contProcessFlag = True
                                log("Updating network folder for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "Failed to update network folder for:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)


                                log("Updating network folder for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                        # Update main checksum of all xml except manifest xml
                        if contProcessFlag == True:

                            log("Updating checksum for:" + newRcpPath, recipeCreatorLog)
                            check1 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                            check2 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                            check3 = checksum_creator(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                            check4 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                            check5 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                            # check6 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                            if check1 and check2 and check3 and check4 and check5:
                                contProcessFlag = True
                                log("Updating checksum for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "Failed to update checksum for:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)

                                log("Updating checksum for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                        # Update manifest file for checksum and other
                        if contProcessFlag == True:

                            check = manifest_file_update(newRcpPath)
                            check1 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                            if check == True and check1 == True:
                                contProcessFlag = True
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "Failed to update manifest file for:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)


                        # Final recipe verification

                        if contProcessFlag == True:

                            specificParaFilePath = row[spfParUpdFileColIndex]

                            check = final_recipe_validation(newRcpPath, specificParaFilePath)

                            if check == True:
                                contProcessFlag = True
                                log("Final verifying for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                tempRow = row
                                tempRow.insert(0, "The recipe failed for final verification - Look at the main log for more detail:" + newRcpPath)
                                tempRow.insert(0, str(rowIndex))
                                failedRcpList.append(tempRow)

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)
                                log("Final verifying for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                        # Adding the successfullly created to the convertedRcpList
                        if contProcessFlag == True:

                            tempRow = row
                            tempRow.insert(0, newRcpName)
                            tempRow.insert(0, str(rowIndex))
                            convertedRcpList.append(tempRow)

                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)


                            log("[SUCCESSFULL]: The recipe conversion for: " + source, recipeCreatorLog)
                            #print("[SUCCESSFULL]: The recipe conversion for: " + source)
                        else:
                            log("[FAILED]: The recipe conversion for: " + source, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + source)

                        # app.rcpCountResult.set(str(len(convertedRcpList)) + "/" + str(len(failedRcpList)))


                        # Here we make the check if the other thread sent a signal to stop execution.
                        if stop_event.is_set():

                            stopFlag = True
                            break

                    if stopFlag == True:
                        processFlag = "Abort"
                    else:
                        processFlag = "Complete"
                    app.rcpCountResult.set(str(len(convertedRcpList)) + "/" + str(len(failedRcpList)))


                #
                try:
                    if os.path.isdir(os.path.join(newRcpDirPath, "temp")):
                        shutil.rmtree(os.path.join(newRcpDirPath, "temp"))
                except Exception as error:
                    #print("Warning: All recipes have been processed but cannot delete: " + os.path.join(newRcpDirPath, "temp"))
                    log("All recipes have been processed but cannot delete: " + os.path.join(newRcpDirPath, "temp"), recipeCreatorLog)
                    no_time_log(str(error),recipeCreatorLog)


                # Print out summary

                #print("\n=======SUMMARY=======")
                #print("SUCCESSFULLY converted recipe count: " + str(len(convertedRcpList)))
                #print("FAILED converted recipe count: " + str(len(failedRcpList)))

                no_time_log("\nFAILED CONVERTED RECIPES - TOTAL: " + str(len(failedRcpList)), summaryLog)
                i = 0
                for rcp in failedRcpList:
                    i = i + 1
                    no_time_log("Recipe #" + str(i) + ":", summaryLog)
                    no_time_log("   - Index in the recipe file list: " + rcp[0], summaryLog)
                    no_time_log("   - Source recipe: " + rcp[2], summaryLog)
                    no_time_log("   - Source alignment recipe: " + rcp[3], summaryLog)
                    no_time_log("   - New Network folder: " + rcp[4], summaryLog)
                    no_time_log("   - New recipe name: " + rcp[5], summaryLog)
                    no_time_log("   - SpecificParameterFile:" + rcp[6], summaryLog)
                    no_time_log("   - ERROR: " + rcp[1], summaryLog)

                no_time_log("\nSUCCESSFULLY CONVERTED RECIPES - TOTAL: " + str(len(convertedRcpList)), summaryLog)
                i = 0
                for rcp in convertedRcpList:
                    i = i + 1
                    no_time_log("Recipe #" + str(i) + ":", summaryLog)
                    no_time_log("   - Index in the recipe file list: " + rcp[0], summaryLog)
                    no_time_log("   - Source recipe: " + rcp[2], summaryLog)
                    no_time_log("   - Source alignment recipe: " + rcp[3], summaryLog)
                    no_time_log("   - New Network folder: " + rcp[4], summaryLog)
                    no_time_log("   - New recipe name: " + rcp[5], summaryLog)
                    no_time_log("   - SpecificParameterFile:" + rcp[6], summaryLog)

                if processFlag == "Complete":

                    app.progress.set("Recipe creation is COMPLETED!")
                    app.stopButton.config(state=tk.DISABLED)

                elif processFlag == "Abort":
                    app.progress.set("Recipe creation is ABORTED!")


            except Exception as error:
                app.progress.set("Recipe creation is terminated ABNORMALLY!")
                no_time_log(str(error), recipeCreatorLog)
                #print("The process is terminated due to an exception:\n")
                #print(str(error))


            # Enable buttons and Entry text after done with recipe conversion
            app.runButton.config(state = tk.NORMAL)
            app.rcpListButtton.config(state = tk.NORMAL)
            app.rcpListPathEntry.config(state=tk.NORMAL)
            app.templateFolderCheckbutton.config(state=tk.NORMAL)
            if app.templateFolderChkbValue.get() == "NO":
                app.rcpTemplateEntry.config(state = tk.NORMAL)
                app.rcpTemplateButton.config(state = tk.NORMAL)


        # Start main() thread
        global mainTask

        mainTask = threading.Thread(target=callback)
        mainTask.start()

# ==========================
def stop():
    app.stopButton.config(state=tk.DISABLED)
    if mainTask.is_alive() is True:
        stop_event.set()

def single_recipe_main(selectedTemplatePath,sourceRecipePath,newRecipeName,sourceAlignRecipePath,specificParameterFilePath, newRecipeLocationPath):

    newRcpDirName = "Recipe_" + str(datetime.datetime.now().strftime("%m%d_%H%M%S"))

    newRcpDirPath = os.path.join(os.getcwd(), newRcpDirName)
    def callback():
        if sourceRecipePath =="":
            AlarmGui("Please select a source recipe")
        else:
            try:

                log("Inputs from user:",recipeCreatorLog)
                no_time_log("Template is used: " + selectedTemplatePath, recipeCreatorLog)
                no_time_log("Source recipe: " + sourceRecipePath, recipeCreatorLog)
                no_time_log("New recipe name: " + newRecipeName, recipeCreatorLog)
                no_time_log("Source alignment recipe: " + sourceAlignRecipePath, recipeCreatorLog)
                no_time_log("Specific parameter file: " + specificParameterFilePath, recipeCreatorLog)
                no_time_log("Netapp location of the new recipe: " + newRecipeLocationPath, recipeCreatorLog)


                scriptDir = os.getcwd()
                templatePath = selectedTemplatePath

                singleRecipeCreationMessage = "Recipe creation is in progress..."

                single_creation_gui.runButton.config(state = tk.DISABLED)
                single_creation_gui.newRecipeLocationButton.config(state = tk.DISABLED)
                single_creation_gui.sourceRecipeButton.config(state = tk.DISABLED)
                single_creation_gui.specificParameterFileButton.config(state = tk.DISABLED)
                single_creation_gui.recipeTemplateButton.config(state=tk.DISABLED)
                single_creation_gui.sourceAlignRecipeButton.config(state=tk.DISABLED)

                single_creation_gui.recipeTemplateEntry.config(state=tk.DISABLED)
                single_creation_gui.sourceRecipeEntry.config(state=tk.DISABLED)
                single_creation_gui.newRecipeNameEntry.config(state=tk.DISABLED)
                single_creation_gui.newRecipeLocationEntry.config(state=tk.DISABLED)
                single_creation_gui.specificParameterFileEntry.config(state=tk.DISABLED)
                single_creation_gui.sourceAlignRecipeEntry.config(state=tk.DISABLED)

                single_creation_gui.recipeTemplateCheckbutton.config(state = tk.DISABLED)
                single_creation_gui.newRcipeLocationCheckbutton.config(state = tk.DISABLED)
                single_creation_gui.sourceAlignRecipeCheckbutton.config(state = tk.DISABLED)
                single_creation_gui.newRecipeNameCheckbutton.config(state = tk.DISABLED)




                single_creation_gui.messageLableValue.set(singleRecipeCreationMessage)

                # Failure message

                contProcessFlag = True
                singleRecipeCreationMessage = ""
                source = sourceRecipePath
                srcRcpName = os.path.basename(source)
                cvtRcpPath = os.path.join(newRcpDirPath, "temp", srcRcpName)
                cvtRcppathRoot = os.path.join(newRcpDirPath, "temp")
                # try:
                #
                #     if os.path.isdir(newRcpDirPath):
                #         for dir in os.listdir(newRcpDirPath):
                #             if os.path.isdir(os.path.join(newRcpDirPath, dir)):
                #                 shutil.rmtree(os.path.join(newRcpDirPath, dir))
                # except Exception as error:
                #     contProcessFlag = False
                #     singleRecipeCreationMessage = "Cannot delete subfolder of:" + newRcpDirPath + "!"
                #     no_time_log(str(error), recipeCreatorLog)


                # # Delete temp if it exist
                # if os.path.isdir(cvtRcppathRoot):
                #     for dir in os.listdir(cvtRcppathRoot):
                #         if os.path.isdir(os.path.join(cvtRcppathRoot, dir)):
                #             shutil.rmtree(os.path.join(cvtRcppathRoot, dir))

                no_time_log("\n", recipeCreatorLog)
                no_time_log("*******************************************************************************************",
                            recipeCreatorLog)
                # log("Start to process the recipe:" + source, recipeCreatorLog)
                # #print("\nStart to process the recipe:" + source)





                if contProcessFlag == True:

                    log("Start to process the recipe:" + source, recipeCreatorLog)
                    #print("\nStart to process the recipe:" + source)

                # Validate template
                if contProcessFlag == True:
                    log("Validating the template: " + templatePath, recipeCreatorLog)

                    contProcessFlag = template_validation(templatePath)

                    if contProcessFlag == True:
                        log("Validation succeeded for: " + templatePath, recipeCreatorLog)

                    else:

                        #print("Validation failed for: " + templatePath)
                        #print("The process is terminated!")
                        log("Validation failed for: " + templatePath, recipeCreatorLog)
                        log("The process is terminated!", recipeCreatorLog)
                        singleRecipeCreationMessage = "The process is terminated. Template is INVALID!"

                # Check Whitespace in the recipe name
                if contProcessFlag == True:
                    if str(newRecipeName.find(" ")) != "-1":
                        contProcessFlag = False
                        log("Verifying the recipe name:" + newRecipeName + " [FAILED] - The recipe new name has Whitespace",
                            recipeCreatorLog)
                        singleRecipeCreationMessage = "The process is terminated. New recipe name has whitespace!"


                #  copy the recipe from the source
                if contProcessFlag == True:
                    # no_time_log("\n", recipeCreatorLog)
                    log("Copying:" + source, recipeCreatorLog)
                    #print("Copying:" + source)
                    # try:

                    # Using copytree method to copy folder
                    # shutil.copytree(source, cvtRcpPath, dirs_exist_ok=True)

                    # using copyFolder function - which use shutil.copyfile
                    # Set timeout for recipe

                    # Create a Process

                    # global Q
                    Q = Queue()
                    recipe_copy_process = Process(target=copyFolder, args=(source, cvtRcppathRoot, Q, recipeCreatorLog))

                    # Start the process and we block for X seconds.
                    try:
                        recipe_copy_process.start()
                        if Q.get() == False:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Copy the source recipe has an exception!"

                            log("Copying:" + source + " [FAILED]", recipeCreatorLog)

                            #print("Copying:" + source + " [FAILED]")

                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)


                            # Deleted the corrupted folder from the Converted recipe folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)

                            # continue

                    except Exception as error:

                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Copy the source recipe has an exception!"

                        log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                        no_time_log(str(error), recipeCreatorLog)
                        #print("Copying:" + source + " [FAILED]")

                        log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                        #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                        # Deleted the corrupted folder from the Converted recipe folder

                        if os.path.isdir(cvtRcpPath):
                            shutil.rmtree(cvtRcpPath)

                        # continue

                    # Wait for 10 second even the recipe_copy_process is running.

                    if contProcessFlag == True:
                        recipe_copy_process.join(timeout=float(recipeCopyTimeout))

                        # Check if the thread is still alive
                        if recipe_copy_process.is_alive() is True:
                            # terminate the thread
                            recipe_copy_process.terminate()

                            contProcessFlag = False
                            log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                            no_time_log("Timeout = " + recipeCopyTimeout + "for copying:", recipeCreatorLog)
                            #print("Copying:" + source + " [FAILED]")

                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Deleted the corrupted folder from the Converted recipe folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                    # else:
                    #
                    #     log("Copying:" + source + " [COMPLETED]", recipeCreatorLog)
                    #     #print("Copying:" + source + " [COMPLETED]")

                    # update modified time of cvtRcpPath folder
                    # os.utime(cvtRcpPath)
                    # for (paths, subdirs, files) in os.walk(cvtRcpPath):
                    #     os.utime(paths)
                    #     for file in files:
                    #         os.utime(os.path.join(paths, file))

                    # except Exception as error:
                    #     contProcessFlag = False
                    #     log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                    #     no_time_log(str(error), recipeCreatorLog)
                    #     #print("Copying:" + source + " [FAILED]")
                    #
                    #     log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                    #     #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                    #
                    #     tempRow = row
                    #     tempRow.insert(0,"Failed to copy the recipe from the source: " + source + ". Possible reasons: The source recipe does not exist. The recipe is corrupted. Access perssion issue. The recipe has been existed on the recipe converted folder")
                    #     tempRow.insert(0,str(rowIndex))
                    #
                    #     failedRcpList.append(tempRow)
                    #
                    #     # Deleted the corrupted folder from the Converted recipe folder
                    #     shutil.rmtree(cvtRcpPath, ignore_errors=True)
                    #
                    #     continue

                #  alignment file update
                if contProcessFlag == True:
                    srcAlignRcpPath = sourceAlignRecipePath
                    srcAlignRcpName = os.path.basename(srcAlignRcpPath)

                    # Process the alignment recipe update IF the alignment recipe exists AND the alignment recipe is different from the source recipe on the RecipeList.csv

                    if srcAlignRcpPath != "" and srcAlignRcpPath != sourceRecipePath:

                        probeAlignPTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPTN_FileExt)
                        probeAlignPRB_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPRB_FileExt)

                        unitAlignUTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUTN_FileExt)
                        unitAlignUNT_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUNT_FileExt)

                        try:
                            # Delete current probe and unit alignment files
                            log("Deleting probe alignment file:" + probeAlignPTN_File, recipeCreatorLog)
                            os.remove(probeAlignPTN_File)
                            log("Deleting probe alignment file:" + probeAlignPTN_File + " [COMPLETED]", recipeCreatorLog)

                            log("Deleting probe alignment file:" + probeAlignPRB_File, recipeCreatorLog)
                            os.remove(probeAlignPRB_File)
                            log("Deleting probe alignment file:" + probeAlignPRB_File + " [COMPLETED]", recipeCreatorLog)

                            log("Deleting unit alignment file:" + unitAlignUTN_File, recipeCreatorLog)
                            os.remove(unitAlignUTN_File)
                            log("Deleting unit alignment file:" + unitAlignUTN_File + " [COMPLETED]", recipeCreatorLog)

                            log("Deleting unit alignment file:" + unitAlignUNT_File, recipeCreatorLog)
                            os.remove(unitAlignUNT_File)
                            log("Deleting unit alignment file:" + unitAlignUNT_File + " [COMPLETED]", recipeCreatorLog)

                            srcFiles = os.listdir(os.path.join(srcAlignRcpPath, "SDTC"))
                            dstDir = os.path.join(cvtRcpPath, "SDTC")

                            # Looking into SDTC folder of the source recipe for alignment files
                            for f in srcFiles:
                                fileName = os.path.basename(f)

                                srcSDTCFile = os.path.join(srcAlignRcpPath, "SDTC", fileName)

                                # Copy alignment files from source alignment recipe and rename the files to the source recipe name
                                # Find the file with extension '.ptn'
                                if fileName.split('.')[len(fileName.split('.')) - 1] == probeAlignPTN_FileExt:
                                    log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir,
                                        recipeCreatorLog)
                                    # shutil.copy2(srcSDTCFile, dstDir)

                                    dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt)
                                    shutil.copyfile(srcSDTCFile, dstFile)

                                    log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                                        recipeCreatorLog)

                                    # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt), recipeCreatorLog)
                                    # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))
                                    # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt) + " [COMPLETED]", recipeCreatorLog)
                                    #
                                    # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))

                                # Find the file with extension '.prb'
                                if fileName.split('.')[len(fileName.split('.')) - 1] == probeAlignPRB_FileExt:
                                    log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir,
                                        recipeCreatorLog)
                                    # shutil.copy2(srcSDTCFile, dstDir)

                                    dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt)
                                    shutil.copyfile(srcSDTCFile, dstFile)

                                    log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                                        recipeCreatorLog)

                                    # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt), recipeCreatorLog)
                                    # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                                    # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt) + " [COMPLETED]", recipeCreatorLog)

                                    # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                                # Find the file with extension '.utn'
                                if fileName.split('.')[len(fileName.split('.')) - 1] == unitAlignUTN_FileExt:
                                    log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                    # shutil.copy2(srcSDTCFile, dstDir)

                                    dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt)
                                    shutil.copyfile(srcSDTCFile, dstFile)

                                    log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                                        recipeCreatorLog)

                                    # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt), recipeCreatorLog)
                                    # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                                    # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt) + " [COMPLETED]", recipeCreatorLog)

                                    # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                                # Find the file with extension '.unt'
                                if fileName.split('.')[len(fileName.split('.')) - 1] == unitAlignUNT_FileExt:
                                    log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                                    # shutil.copy2(srcSDTCFile, dstDir)

                                    dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt)
                                    shutil.copyfile(srcSDTCFile, dstFile)

                                    log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                                        recipeCreatorLog)

                                    # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt), recipeCreatorLog)
                                    # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))
                                    # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt) + " [COMPLETED]", recipeCreatorLog)
                                    #
                                    # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))

                            # Update the probe alignment and unit alignment box size for SDTC.xml



                            alignSrcRcpSdtcXmlPath = os.path.join(srcAlignRcpPath, "SDTC", srcAlignRcpName + ".xml")
                            dstRcpSdtcXmlPath = os.path.join(cvtRcpPath, "SDTC", srcRcpName + ".xml")
                            tempAlignSrcRcpSdtcXmlPath = os.path.join(scriptDir, newRcpDirName, "tempAlign\\sdtc.xml")

                            if not os.path.exists(os.path.join(scriptDir, newRcpDirName,"tempAlign")):
                                os.mkdir(os.path.join(scriptDir, newRcpDirName, "tempAlign"))
                            shutil.copy2(alignSrcRcpSdtcXmlPath, tempAlignSrcRcpSdtcXmlPath)

                            sdtcAlignSrcRcpXml = ET.parse(tempAlignSrcRcpSdtcXmlPath)
                            sdtcAlignSrcRcpXmlRoot = sdtcAlignSrcRcpXml.getroot()

                            sdtcDstRcpXml = ET.parse(dstRcpSdtcXmlPath)
                            sdtcDstRcpXmlRoot = sdtcDstRcpXml.getroot()

                            log(
                                "Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath,
                                recipeCreatorLog)
                            prbP1W = ""
                            prbP1H = ""
                            prbP2W = ""
                            prbP2H = ""
                            prbP3W = ""
                            prbP3H = ""
                            prbP4W = ""
                            prbP4H = ""

                            prbP1Wexist = False
                            prbP1Hexist = False
                            prbP2Wexist = False
                            prbP2Hexist = False
                            prbP3Wexist = False
                            prbP3Hexist = False
                            prbP4Wexist = False
                            prbP4Hexist = False

                            untP1W = ""
                            untP1H = ""
                            untP2W = ""
                            untP2H = ""

                            untP1Wexist = False
                            untP1Hexist = False
                            untP2Wexist = False
                            untP2Hexist = False

                            for sdtcAlignSrcRcpXmlSubRoot in sdtcAlignSrcRcpXmlRoot:
                                if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Probe":
                                    for x in sdtcAlignSrcRcpXmlSubRoot:
                                        if x.get('name') == "Pattern1_Wide":
                                            prbP1W = x.get('value')
                                            prbP1Wexist = True
                                        if x.get('name') == "Pattern1_Height":
                                            prbP1H = x.get('value')
                                            prbP1Hexist = True
                                        if x.get('name') == "Pattern2_Wide":
                                            prbP2W = x.get('value')
                                            prbP2Wexist = True
                                        if x.get('name') == "Pattern2_Height":
                                            prbP2H = x.get('value')
                                            prbP2Hexist = True
                                        if x.get('name') == "Pattern3_Wide":
                                            prbP3W = x.get('value')
                                            prbP3Wexist = True
                                        if x.get('name') == "Pattern3_Height":
                                            prbP3H = x.get('value')
                                            prbP3Hexist = True
                                        if x.get('name') == "Pattern4_Wide":
                                            prbP4W = x.get('value')
                                            prbP4Wexist = True
                                        if x.get('name') == "Pattern4_Height":
                                            prbP4H = x.get('value')
                                            prbP4Hexist = True

                                if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Unit Alignment":
                                    for x in sdtcAlignSrcRcpXmlSubRoot:
                                        if x.get('name') == "Pattern1_Wide":
                                            untP1W = x.get('value')
                                            untP1Wexist = True
                                        if x.get('name') == "Pattern1_Height":
                                            untP1H = x.get('value')
                                            untP1Hexist = True
                                        if x.get('name') == "Pattern2_Wide":
                                            untP2W = x.get('value')
                                            untP2Wexist = True
                                        if x.get('name') == "Pattern2_Height":
                                            untP2H = x.get('value')
                                            untP2Hexist = True

                            for sdtcDstRcpXmlSubRoot in sdtcDstRcpXmlRoot:
                                if sdtcDstRcpXmlSubRoot.get('name') == "Probe":
                                    for x in sdtcDstRcpXmlSubRoot:
                                        if x.get('name') == "Pattern1_Wide" and prbP1Wexist == True:
                                            x.set('value', prbP1W)
                                        if x.get('name') == "Pattern1_Height" and prbP1Hexist == True:
                                            x.set('value', prbP1H)
                                        if x.get('name') == "Pattern2_Wide" and prbP2Wexist == True:
                                            x.set('value', prbP2W)
                                        if x.get('name') == "Pattern2_Height" and prbP2Hexist == True:
                                            x.set('value', prbP2H)
                                        if x.get('name') == "Pattern3_Wide" and prbP3Wexist == True:
                                            x.set('value', prbP3W)
                                        if x.get('name') == "Pattern3_Height" and prbP3Hexist == True:
                                            x.set('value', prbP3H)
                                        if x.get('name') == "Pattern4_Wide" and prbP4Wexist == True:
                                            x.set('value', prbP4W)
                                        if x.get('name') == "Pattern4_Height" and prbP4Hexist == True:
                                            x.set('value', prbP4H)

                                if sdtcDstRcpXmlSubRoot.get('name') == "Unit Alignment":
                                    for x in sdtcDstRcpXmlSubRoot:
                                        if x.get('name') == "Pattern1_Wide" and untP1Wexist == True:
                                            x.set('value', untP1W)
                                        if x.get('name') == "Pattern1_Height" and untP1Hexist == True:
                                            x.set('value', untP1H)
                                        if x.get('name') == "Pattern2_Wide" and untP2Wexist == True:
                                            x.set('value', untP2W)
                                        if x.get('name') == "Pattern2_Height" and untP2Hexist == True:
                                            x.set('value', untP2H)


                            sdtcDstRcpXml.write(dstRcpSdtcXmlPath)
                            # Delete ConvertRecipe\\tempAlign
                            shutil.rmtree(os.path.join(scriptDir,newRcpDirName, "tempAlign"))
                            log(
                                "Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath + " [COMPLETED]",
                                recipeCreatorLog)

                        except Exception as error:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Update alignment to the source alignment recipe failed!"

                            log("Updating alignment files for:" + cvtRcpPath + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Updating alignment files for:" + cvtRcpPath + " [FAILED]")
                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)



                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                # Rename files in each recipe
                if contProcessFlag == True:

                    #print("The recipe conversion is in progress...")
                    log("Starting to rename the recipe", recipeCreatorLog)
                    log("Renaming:" + cvtRcpPath, recipeCreatorLog)

                    # get recipe new name
                    newRcpName = newRecipeName

                    # Renaming files HC folder
                    folderPath = os.path.join(cvtRcpPath, "HC")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:
                            if fileName.find('mas') != -1:
                                newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                            else:
                                newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in HC folder to new recipe name!"


                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming file in IOM folder

                    folderPath = os.path.join(cvtRcpPath, "IOM")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:

                            newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                            src = os.path.join(folderPath, f)
                            dst = os.path.join(folderPath, newFileName)
                            log("Renaming:" + src, recipeCreatorLog)
                            os.rename(src, dst)
                            log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in IOM folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming file in Manifest folder

                    folderPath = os.path.join(cvtRcpPath, "Manifest")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:

                            newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                            src = os.path.join(folderPath, f)
                            dst = os.path.join(folderPath, newFileName)
                            log("Renaming:" + src, recipeCreatorLog)
                            os.rename(src, dst)
                            log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in Manifest folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming files in SDTC folder
                    folderPath = os.path.join(cvtRcpPath, "SDTC")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:
                            if fileName.find('mas') != -1:
                                newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                            elif fileName.find('_R.rcp') != -1:
                                newFileName = newRcpName + "_R" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                            else:
                                newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in SDTC folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming the root recipe folder
                    # Wait 2 seconds before remaing the root folder to make sure all fies are updated
                    # time.sleep(1)
                    if contProcessFlag == True:
                        src = ""
                        dst = ""

                        try:
                            src = cvtRcpPath
                            dst = os.path.join(newRcpDirPath, newRcpName)
                            # copyFolder1(src,dst)
                            shutil.copytree(src, dst)
                            log("Copy and change name of the recipe folder: " + src + " TO: " + dst + " [COMPLETED]",
                                recipeCreatorLog)
                        except Exception as error:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update the new recipe root folder name!"

                            log("Copy and change name of folder: " + src + " TO: " + dst + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)

                            if os.path.isdir(dst) == True:
                                shutil.rmtree(dst)
                            # continue

                # Updating the recipe to the template

                if contProcessFlag == True:

                    newRcpName = newRecipeName
                    newRcpPath = os.path.join(newRcpDirPath, newRcpName)

                    log("Updating:" + newRcpPath + "To the templates:" + templatePath, recipeCreatorLog)
                    check1 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"),
                                                       templateLine="Add")
                    check2 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipeMaster_template.xml"),
                                                       os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"),
                                                       templateLine="Add")
                    check3 = sdtc_type_template_update(os.path.join(templatePath, "IOMRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "IOM", newRcpName + ".xml"), templateLine="Add")
                    check4 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "HC", newRcpName + ".xml"), templateLine="")
                    check5 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipeMaster_template.mas.xml"),
                                                       os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"),
                                                       templateLine="Remove")

                    check6 = manifest_type_template_update(os.path.join(templatePath, "Manifest_template.xml"),
                                                           os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5 and check6:
                        contProcessFlag = True
                        log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update to new recipe template failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [FAILED]", recipeCreatorLog)

                # Update Identity line for xml files
                if contProcessFlag == True:

                    log("Updating identity line for:" + newRcpPath, recipeCreatorLog)
                    check1 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                    check2 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check3 = identity_update(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                    check4 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                    check5 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                    check6 = identity_update(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5 and check6:
                        contProcessFlag = True
                        log("Updating identity line for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update recipe files failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating identity line for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update value of mas xml files
                if contProcessFlag == True:

                    log("Updating value of mas.xml files for:" + newRcpPath, recipeCreatorLog)

                    check1 = mas_file_parameter_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check2 = mas_file_parameter_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))

                    if check1 and check2:
                        contProcessFlag = True
                        log("Updating value of mas.xml files for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update recipe files failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating value of mas.xml files for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                #  Update specific parameter
                #  If there is no specific parameter link -> DO nothing and Continue

                if contProcessFlag == True:

                    specificParaFilePath = specificParameterFilePath
                    if specificParaFilePath.strip() != "":
                        if os.path.isfile(specificParaFilePath.strip()):

                            log("Updating specific parameters for:" + newRcpPath + "Using:" + specificParaFilePath,
                                recipeCreatorLog)

                            check = specific_para_file_update(newRcpPath, specificParaFilePath)

                            if check == True:
                                contProcessFlag = True
                                log(
                                    "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]",
                                    recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                singleRecipeCreationMessage = "The process is terminated. Update specific parameters failed!"

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)
                                log(
                                    "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                    recipeCreatorLog)
                        else:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Update specific parameters failed. File could not be found!"
                            # Remove the corrupted folder
                            if os.path.isdir(newRcpPath) == True:
                                shutil.rmtree(newRcpPath)
                            log(
                                "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                recipeCreatorLog)
                            no_time_log("The parameter file at:[" + specificParaFilePath.strip() + "] could not be found",
                                        recipeCreatorLog)

                    else:
                        log("There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                            recipeCreatorLog)

                # Test new way to catch exception
                # if contProcessFlag == True:
                #
                #     specificParaFilePath = row[spfParUpdFileColIndex]
                #     if specificParaFilePath.strip() != "":
                #
                #         log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath,
                #             recipeCreatorLog)
                #         try:
                #             specific_para_file_update(newRcpPath, specificParaFilePath)
                #             contProcessFlag = True
                #             log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]", recipeCreatorLog)
                #         except Exception:
                #
                #             contProcessFlag = False
                #
                #             tempRow = row
                #             tempRow.insert(0, "Failed to update specific parameters for:" + newRcpPath)
                #             tempRow.insert(0, str(rowIndex))
                #             failedRcpList.append(tempRow)
                #
                #             log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                #             #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                #
                #             # Remove the corrupted folder
                #             shutil.rmtree(cvtRcpPath, ignore_errors=True)
                #             continue
                #     else:
                #         log("There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                #             recipeCreatorLog)

                # Update network folder for Manifest.xml
                if contProcessFlag == True:
                    # templatePath = ""
                    # networkDrive = ""
                    # networkFolder = ""
                    # recipeFileList = ""

                    log("Updating network folder for:" + newRcpPath, recipeCreatorLog)

                    absNetworkFolder = newRecipeLocationPath
                    check = network_folder_manifest_file_update(newRcpPath, absNetworkFolder, networkFolder, networkDrive)

                    if check == True:
                        contProcessFlag = True
                        log("Updating network folder for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False

                        singleRecipeCreationMessage = "The process is terminated. Update network path in the manifest file failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating network folder for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update main checksum of all xml except manifest xml
                if contProcessFlag == True:

                    log("Updating checksum for:" + newRcpPath, recipeCreatorLog)
                    check1 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                    check2 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check3 = checksum_creator(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                    check4 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                    check5 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                    # check6 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5:
                        contProcessFlag = True
                        log("Updating checksum for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update checksum for xml files (except manifest .xml) failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating checksum for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update manifest file for checksum and other
                if contProcessFlag == True:

                    check = manifest_file_update(newRcpPath)
                    check1 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check == True and check1 == True:
                        contProcessFlag = True
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update checksum for manifest file failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                # Final recipe verification

                if contProcessFlag == True:

                    specificParaFilePath = specificParameterFilePath

                    check = final_recipe_validation(newRcpPath, specificParaFilePath)

                    if check == True:
                        contProcessFlag = True
                        log("Final verifying for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Final verification failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)
                        log("Final verifying for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Remove the temp folder cvtRcppathRoot = ...\ConvertRecipe\Temp
                if contProcessFlag == True:

                    singleRecipeCreationMessage = "Recipe creation COMPLETED!"

                    if os.path.isdir(cvtRcppathRoot) == True:
                        shutil.rmtree(cvtRcppathRoot)

                    log("[SUCCESSFULL]: The recipe conversion for: " + source, recipeCreatorLog)
                    #print("[SUCCESSFULL]: The recipe conversion for: " + source)
                else:
                    log("[FAILED]: The recipe conversion for: " + source, recipeCreatorLog)
                    #print("[FAILED]: The recipe conversion for: " + source)


                # Pop up result message

                single_creation_gui.messageLableValue.set(singleRecipeCreationMessage)

                # Setup state for widgets
                single_creation_gui.recipeTemplateCheckbutton.config(state=tk.NORMAL)
                single_creation_gui.newRcipeLocationCheckbutton.config(state=tk.NORMAL)
                single_creation_gui.sourceAlignRecipeCheckbutton.config(state=tk.NORMAL)
                single_creation_gui.newRecipeNameCheckbutton.config(state=tk.NORMAL)

                if single_creation_gui.rcpTemplateCheckbuttonValue.get() == "NO":
                    single_creation_gui.recipeTemplateEntry.config(state=tk.NORMAL)
                    single_creation_gui.recipeTemplateButton.config(state=tk.NORMAL)
                single_creation_gui.runButton.config(state=tk.NORMAL)

                if single_creation_gui.newRcpLocCheckbuttonValue.get() == "NO":
                    single_creation_gui.newRecipeLocationButton.config(state=tk.NORMAL)
                    single_creation_gui.newRecipeLocationEntry.config(state=tk.NORMAL)

                if single_creation_gui.srcAlignRecipeCheckbuttonValue.get() == "NO":
                    single_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)
                    single_creation_gui.sourceAlignRecipeEntry.config(state=tk.NORMAL)

                single_creation_gui.sourceRecipeEntry.config(state=tk.NORMAL)
                single_creation_gui.sourceRecipeButton.config(state=tk.NORMAL)

                if single_creation_gui.newRcpNameCheckbuttonValue.get() == "NO":
                    single_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)
                    single_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)

                single_creation_gui.specificParameterFileEntry.config(state=tk.NORMAL)
                single_creation_gui.specificParameterFileButton.config(state=tk.NORMAL)

                single_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)


            except Exception as error:

                cvtRcppathRoot = os.path.join(newRcpDirPath, "temp")
                singleRecipeCreationMessage = "Recipe creation FAILED!"
                single_creation_gui.messageLableValue.set(singleRecipeCreationMessage)
                if os.path.isdir(cvtRcppathRoot) == True:
                    shutil.rmtree(cvtRcppathRoot)

                no_time_log(str(error),recipeCreatorLog)

                # Setup state for widgets
                single_creation_gui.recipeTemplateCheckbutton.config(state = tk.NORMAL)
                single_creation_gui.newRcipeLocationCheckbutton.config(state = tk.NORMAL)
                single_creation_gui.sourceAlignRecipeCheckbutton.config(state = tk.NORMAL)
                single_creation_gui.newRecipeNameCheckbutton.config(state = tk.NORMAL)


                if single_creation_gui.rcpTemplateCheckbuttonValue.get() == "NO":
                    single_creation_gui.recipeTemplateEntry.config(state = tk.NORMAL)
                    single_creation_gui.recipeTemplateButton.config(state=tk.NORMAL)
                single_creation_gui.runButton.config(state = tk.NORMAL)

                if single_creation_gui.newRcpLocCheckbuttonValue.get() == "NO":
                    single_creation_gui.newRecipeLocationButton.config(state = tk.NORMAL)
                    single_creation_gui.newRecipeLocationEntry.config(state = tk.NORMAL)


                if single_creation_gui.srcAlignRecipeCheckbuttonValue.get() == "NO":
                    single_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)
                    single_creation_gui.sourceAlignRecipeEntry.config(state = tk.NORMAL)


                single_creation_gui.sourceRecipeEntry.config(state=tk.NORMAL)
                single_creation_gui.sourceRecipeButton.config(state=tk.NORMAL)

                if single_creation_gui.newRcpNameCheckbuttonValue.get() == "NO":
                    single_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)
                    single_creation_gui.newRecipeNameEntry.config(state = tk.NORMAL)


                single_creation_gui.specificParameterFileEntry.config(state=tk.NORMAL)
                single_creation_gui.specificParameterFileButton.config(state=tk.NORMAL)
            

    global singleRecipeTask

    singleRecipeTask = threading.Thread(target=callback)
    singleRecipeTask.start()


    # app.rcpCountResult.set(str(len(convertedRcpList)) + "/" + str(len(failedRcpList)))

def check_parameter_coexist_in_parameter_file(parameterFileList):
    allParameterList = []
    duplicatedParameterList =[]

    try:
        for filePath in parameterFileList:

            paraFileXml = ET.parse(filePath)
            paraFileXmlRoot = paraFileXml.getroot()
            for paraComp in paraFileXmlRoot:
                for paraFileInfo in paraComp:
                    for menu in paraFileInfo:
                        for item in menu:
                            parameter = paraComp.get('name') + paraFileInfo.get('name') + '>' + menu.get('name') + '>' + item.get('name')
                            allParameterList.append(parameter)
        print(allParameterList)
        for i in range(len(allParameterList)):
            if allParameterList[i] not in duplicatedParameterList:
                for j in range(i+1,len(allParameterList)):
                    if allParameterList[i] == allParameterList[j]:
                        duplicatedParameterList.append(allParameterList[i])
        print(duplicatedParameterList)
        if len(duplicatedParameterList) == 0:

            return True,duplicatedParameterList
        else:
            log("There are parameters existing in multiple parameter files. The process will be terminated.", recipeCreatorLog)
            no_time_log("Duplicated parameters:",recipeCreatorLog)
            for para in duplicatedParameterList:
                no_time_log(para,recipeCreatorLog)
            return False, duplicatedParameterList
    except Exception as error:
        log("Failed to check integrity of parameter files: ", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False, duplicatedParameterList



def NPI_recipe_main(selectedTemplatePath,sourceRecipePath,newRecipeName,specificParameterFilePath,goldenFileList, newRecipeLocationPath):

    newRcpDirName = "Recipe_" + str(datetime.datetime.now().strftime("%m%d_%H%M%S"))

    newRcpDirPath = os.path.join(os.getcwd(), newRcpDirName)


    def callback():

        if sourceRecipePath =="":
            AlarmGui("Please select a source recipe")

        else:
            try:

                log("Inputs from user:",recipeCreatorLog)
                no_time_log("Template is used: " + selectedTemplatePath, recipeCreatorLog)
                no_time_log("Source recipe: " + sourceRecipePath, recipeCreatorLog)
                no_time_log("New recipe name: " + newRecipeName, recipeCreatorLog)
                # no_time_log("Source alignment recipe: " + sourceAlignRecipePath, recipeCreatorLog)

                no_time_log("Specific parameter file: " + specificParameterFilePath, recipeCreatorLog)
                for goldenFile in goldenFileList:

                    no_time_log("Golden parameter file: " + goldenFile , recipeCreatorLog)

                no_time_log("Netapp location of the new recipe: " + newRecipeLocationPath, recipeCreatorLog)


                scriptDir = os.getcwd()
                templatePath = selectedTemplatePath

                singleRecipeCreationMessage = "Recipe creation is in progress..."

                NPI_creation_gui.runButton.config(state = tk.DISABLED)
                NPI_creation_gui.newRecipeLocationButton.config(state = tk.DISABLED)
                NPI_creation_gui.sourceRecipeButton.config(state = tk.DISABLED)
                NPI_creation_gui.specificParameterFileButton.config(state = tk.DISABLED)
                NPI_creation_gui.recipeTemplateButton.config(state=tk.DISABLED)
                # NPI_creation_gui.sourceAlignRecipeButton.config(state=tk.DISABLED)

                NPI_creation_gui.recipeTemplateEntry.config(state=tk.DISABLED)
                NPI_creation_gui.sourceRecipeEntry.config(state=tk.DISABLED)
                NPI_creation_gui.newRecipeNameEntry.config(state=tk.DISABLED)
                NPI_creation_gui.newRecipeLocationEntry.config(state=tk.DISABLED)
                NPI_creation_gui.specificParameterFileEntry.config(state=tk.DISABLED)
                # NPI_creation_gui.sourceAlignRecipeEntry.config(state=tk.DISABLED)

                NPI_creation_gui.recipeTemplateCheckbutton.config(state = tk.DISABLED)
                NPI_creation_gui.newRcipeLocationCheckbutton.config(state = tk.DISABLED)
                # NPI_creation_gui.sourceAlignRecipeCheckbutton.config(state = tk.DISABLED)
                NPI_creation_gui.newRecipeNameCheckbutton.config(state = tk.DISABLED)




                NPI_creation_gui.messageLableValue.set(singleRecipeCreationMessage)

                # Failure message

                contProcessFlag = True
                singleRecipeCreationMessage = ""
                source = sourceRecipePath
                srcRcpName = os.path.basename(source)
                cvtRcpPath = os.path.join(newRcpDirPath, "temp", srcRcpName)
                cvtRcppathRoot = os.path.join(newRcpDirPath, "temp")
                # try:
                #
                #     if os.path.isdir(newRcpDirPath):
                #         for dir in os.listdir(newRcpDirPath):
                #             if os.path.isdir(os.path.join(newRcpDirPath, dir)):
                #                 shutil.rmtree(os.path.join(newRcpDirPath, dir))
                # except Exception as error:
                #     contProcessFlag = False
                #     singleRecipeCreationMessage = "Cannot delete subfolder of:" + newRcpDirPath + "!"
                #     no_time_log(str(error), recipeCreatorLog)


                # # Delete temp if it exist
                # if os.path.isdir(cvtRcppathRoot):
                #     for dir in os.listdir(cvtRcppathRoot):
                #         if os.path.isdir(os.path.join(cvtRcppathRoot, dir)):
                #             shutil.rmtree(os.path.join(cvtRcppathRoot, dir))

                no_time_log("\n", recipeCreatorLog)
                no_time_log("*******************************************************************************************",
                            recipeCreatorLog)
                # log("Start to process the recipe:" + source, recipeCreatorLog)
                # #print("\nStart to process the recipe:" + source)


                # Validate parameter files for parameter integrity


                if contProcessFlag == True:
                    log("Validating parameter files for parameter integrity...", recipeCreatorLog)

                    parameterFileList = goldenFileList.copy()

                    if specificParameterFilePath!= "":

                        parameterFileList.append(specificParameterFilePath)

                    contProcessFlag,duplicatedParameterList = check_parameter_coexist_in_parameter_file(parameterFileList)

                    if contProcessFlag == True:
                        log("Validating parameter files for parameter integrity [SUCCESSFUL]", recipeCreatorLog)
                    else:
                        singleRecipeCreationMessage = "The process is terminated. Parameter files are INVALID with duplicated parameters!"

                if contProcessFlag == True:

                    log("Start to process the recipe:" + source, recipeCreatorLog)
                    #print("\nStart to process the recipe:" + source)

                # Validate template
                if contProcessFlag == True:
                    log("Validating the template: " + templatePath, recipeCreatorLog)

                    contProcessFlag = template_validation(templatePath)

                    if contProcessFlag == True:
                        log("Validation succeeded for: " + templatePath, recipeCreatorLog)

                    else:

                        #print("Validation failed for: " + templatePath)
                        #print("The process is terminated!")
                        log("Validation failed for: " + templatePath, recipeCreatorLog)
                        log("The process is terminated!", recipeCreatorLog)
                        singleRecipeCreationMessage = "The process is terminated. Template is INVALID!"

                # Check Whitespace in the recipe name
                if contProcessFlag == True:
                    if str(newRecipeName.find(" ")) != "-1":
                        contProcessFlag = False
                        log("Verifying the recipe name:" + newRecipeName + " [FAILED] - The recipe new name has Whitespace",
                            recipeCreatorLog)
                        singleRecipeCreationMessage = "The process is terminated. New recipe name has whitespace!"


                #  copy the recipe from the source
                if contProcessFlag == True:
                    # no_time_log("\n", recipeCreatorLog)
                    log("Copying:" + source, recipeCreatorLog)
                    #print("Copying:" + source)
                    # try:

                    # Using copytree method to copy folder
                    # shutil.copytree(source, cvtRcpPath, dirs_exist_ok=True)

                    # using copyFolder function - which use shutil.copyfile
                    # Set timeout for recipe

                    # Create a Process

                    # global Q
                    Q = Queue()
                    recipe_copy_process = Process(target=copyFolder, args=(source, cvtRcppathRoot, Q, recipeCreatorLog))

                    # Start the process and we block for X seconds.
                    try:
                        recipe_copy_process.start()
                        if Q.get() == False:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Copy the source recipe has an exception!"

                            log("Copying:" + source + " [FAILED]", recipeCreatorLog)

                            #print("Copying:" + source + " [FAILED]")

                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)


                            # Deleted the corrupted folder from the Converted recipe folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)

                            # continue

                    except Exception as error:

                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Copy the source recipe has an exception!"

                        log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                        no_time_log(str(error), recipeCreatorLog)
                        #print("Copying:" + source + " [FAILED]")

                        log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                        #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                        # Deleted the corrupted folder from the Converted recipe folder

                        if os.path.isdir(cvtRcpPath):
                            shutil.rmtree(cvtRcpPath)

                        # continue

                    # Wait for 10 second even the recipe_copy_process is running.

                    if contProcessFlag == True:
                        recipe_copy_process.join(timeout=float(recipeCopyTimeout))

                        # Check if the thread is still alive
                        if recipe_copy_process.is_alive() is True:
                            # terminate the thread
                            recipe_copy_process.terminate()

                            contProcessFlag = False
                            log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                            no_time_log("Timeout = " + recipeCopyTimeout + "for copying:", recipeCreatorLog)
                            #print("Copying:" + source + " [FAILED]")

                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Deleted the corrupted folder from the Converted recipe folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                    # else:
                    #
                    #     log("Copying:" + source + " [COMPLETED]", recipeCreatorLog)
                    #     #print("Copying:" + source + " [COMPLETED]")

                    # update modified time of cvtRcpPath folder
                    # os.utime(cvtRcpPath)
                    # for (paths, subdirs, files) in os.walk(cvtRcpPath):
                    #     os.utime(paths)
                    #     for file in files:
                    #         os.utime(os.path.join(paths, file))

                    # except Exception as error:
                    #     contProcessFlag = False
                    #     log("Copying:" + source + " [FAILED]", recipeCreatorLog)
                    #     no_time_log(str(error), recipeCreatorLog)
                    #     #print("Copying:" + source + " [FAILED]")
                    #
                    #     log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                    #     #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                    #
                    #     tempRow = row
                    #     tempRow.insert(0,"Failed to copy the recipe from the source: " + source + ". Possible reasons: The source recipe does not exist. The recipe is corrupted. Access perssion issue. The recipe has been existed on the recipe converted folder")
                    #     tempRow.insert(0,str(rowIndex))
                    #
                    #     failedRcpList.append(tempRow)
                    #
                    #     # Deleted the corrupted folder from the Converted recipe folder
                    #     shutil.rmtree(cvtRcpPath, ignore_errors=True)
                    #
                    #     continue

                #  alignment file update
                # if contProcessFlag == True:
                #     srcAlignRcpPath = sourceAlignRecipePath
                #     srcAlignRcpName = os.path.basename(srcAlignRcpPath)
                #
                #     # Process the alignment recipe update IF the alignment recipe exists AND the alignment recipe is different from the source recipe on the RecipeList.csv
                #
                #     if srcAlignRcpPath != "" and srcAlignRcpPath != sourceRecipePath:
                #
                #         probeAlignPTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPTN_FileExt)
                #         probeAlignPRB_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + probeAlignPRB_FileExt)
                #
                #         unitAlignUTN_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUTN_FileExt)
                #         unitAlignUNT_File = os.path.join(cvtRcpPath, "SDTC", srcRcpName + "." + unitAlignUNT_FileExt)
                #
                #         try:
                #             # Delete current probe and unit alignment files
                #             log("Deleting probe alignment file:" + probeAlignPTN_File, recipeCreatorLog)
                #             os.remove(probeAlignPTN_File)
                #             log("Deleting probe alignment file:" + probeAlignPTN_File + " [COMPLETED]", recipeCreatorLog)
                #
                #             log("Deleting probe alignment file:" + probeAlignPRB_File, recipeCreatorLog)
                #             os.remove(probeAlignPRB_File)
                #             log("Deleting probe alignment file:" + probeAlignPRB_File + " [COMPLETED]", recipeCreatorLog)
                #
                #             log("Deleting unit alignment file:" + unitAlignUTN_File, recipeCreatorLog)
                #             os.remove(unitAlignUTN_File)
                #             log("Deleting unit alignment file:" + unitAlignUTN_File + " [COMPLETED]", recipeCreatorLog)
                #
                #             log("Deleting unit alignment file:" + unitAlignUNT_File, recipeCreatorLog)
                #             os.remove(unitAlignUNT_File)
                #             log("Deleting unit alignment file:" + unitAlignUNT_File + " [COMPLETED]", recipeCreatorLog)
                #
                #             srcFiles = os.listdir(os.path.join(srcAlignRcpPath, "SDTC"))
                #             dstDir = os.path.join(cvtRcpPath, "SDTC")
                #
                #             # Looking into SDTC folder of the source recipe for alignment files
                #             for f in srcFiles:
                #                 fileName = os.path.basename(f)
                #
                #                 srcSDTCFile = os.path.join(srcAlignRcpPath, "SDTC", fileName)
                #
                #                 # Copy alignment files from source alignment recipe and rename the files to the source recipe name
                #                 # Find the file with extension '.ptn'
                #                 if fileName.split('.')[len(fileName.split('.')) - 1] == probeAlignPTN_FileExt:
                #                     log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir,
                #                         recipeCreatorLog)
                #                     # shutil.copy2(srcSDTCFile, dstDir)
                #
                #                     dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt)
                #                     shutil.copyfile(srcSDTCFile, dstFile)
                #
                #                     log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                #                         recipeCreatorLog)
                #
                #                     # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt), recipeCreatorLog)
                #                     # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))
                #                     # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt) + " [COMPLETED]", recipeCreatorLog)
                #                     #
                #                     # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPTN_FileExt))
                #
                #                 # Find the file with extension '.prb'
                #                 if fileName.split('.')[len(fileName.split('.')) - 1] == probeAlignPRB_FileExt:
                #                     log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir,
                #                         recipeCreatorLog)
                #                     # shutil.copy2(srcSDTCFile, dstDir)
                #
                #                     dstFile = os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt)
                #                     shutil.copyfile(srcSDTCFile, dstFile)
                #
                #                     log("Copying probe alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                #                         recipeCreatorLog)
                #
                #                     # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt), recipeCreatorLog)
                #                     # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                #                     # log("Renaming probe alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt) + " [COMPLETED]", recipeCreatorLog)
                #
                #                     # os.utime(os.path.join(dstDir, srcRcpName + "." + probeAlignPRB_FileExt))
                #                 # Find the file with extension '.utn'
                #                 if fileName.split('.')[len(fileName.split('.')) - 1] == unitAlignUTN_FileExt:
                #                     log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                #                     # shutil.copy2(srcSDTCFile, dstDir)
                #
                #                     dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt)
                #                     shutil.copyfile(srcSDTCFile, dstFile)
                #
                #                     log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                #                         recipeCreatorLog)
                #
                #                     # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt), recipeCreatorLog)
                #                     # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                #                     # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt) + " [COMPLETED]", recipeCreatorLog)
                #
                #                     # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUTN_FileExt))
                #                 # Find the file with extension '.unt'
                #                 if fileName.split('.')[len(fileName.split('.')) - 1] == unitAlignUNT_FileExt:
                #                     log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir, recipeCreatorLog)
                #                     # shutil.copy2(srcSDTCFile, dstDir)
                #
                #                     dstFile = os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt)
                #                     shutil.copyfile(srcSDTCFile, dstFile)
                #
                #                     log("Copying unit alignment file from: " + srcSDTCFile + " to: " + dstDir + " [COMPLETED]",
                #                         recipeCreatorLog)
                #
                #                     # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt), recipeCreatorLog)
                #                     # os.rename(os.path.join(dstDir, fileName), os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))
                #                     # log("Renaming unit alignment file:" + os.path.join(dstDir, fileName) + "to: " + os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt) + " [COMPLETED]", recipeCreatorLog)
                #                     #
                #                     # os.utime(os.path.join(dstDir, srcRcpName + "." + unitAlignUNT_FileExt))
                #
                #             # Update the probe alignment and unit alignment box size for SDTC.xml
                #
                #
                #
                #             alignSrcRcpSdtcXmlPath = os.path.join(srcAlignRcpPath, "SDTC", srcAlignRcpName + ".xml")
                #             dstRcpSdtcXmlPath = os.path.join(cvtRcpPath, "SDTC", srcRcpName + ".xml")
                #             tempAlignSrcRcpSdtcXmlPath = os.path.join(scriptDir, newRcpDirName, "tempAlign\\sdtc.xml")
                #
                #             if not os.path.exists(os.path.join(scriptDir, newRcpDirName,"tempAlign")):
                #                 os.mkdir(os.path.join(scriptDir, newRcpDirName, "tempAlign"))
                #             shutil.copy2(alignSrcRcpSdtcXmlPath, tempAlignSrcRcpSdtcXmlPath)
                #
                #             sdtcAlignSrcRcpXml = ET.parse(tempAlignSrcRcpSdtcXmlPath)
                #             sdtcAlignSrcRcpXmlRoot = sdtcAlignSrcRcpXml.getroot()
                #
                #             sdtcDstRcpXml = ET.parse(dstRcpSdtcXmlPath)
                #             sdtcDstRcpXmlRoot = sdtcDstRcpXml.getroot()
                #
                #             log(
                #                 "Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath,
                #                 recipeCreatorLog)
                #             prbP1W = ""
                #             prbP1H = ""
                #             prbP2W = ""
                #             prbP2H = ""
                #             prbP3W = ""
                #             prbP3H = ""
                #             prbP4W = ""
                #             prbP4H = ""
                #
                #             prbP1Wexist = False
                #             prbP1Hexist = False
                #             prbP2Wexist = False
                #             prbP2Hexist = False
                #             prbP3Wexist = False
                #             prbP3Hexist = False
                #             prbP4Wexist = False
                #             prbP4Hexist = False
                #
                #             untP1W = ""
                #             untP1H = ""
                #             untP2W = ""
                #             untP2H = ""
                #
                #             untP1Wexist = False
                #             untP1Hexist = False
                #             untP2Wexist = False
                #             untP2Hexist = False
                #
                #             for sdtcAlignSrcRcpXmlSubRoot in sdtcAlignSrcRcpXmlRoot:
                #                 if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Probe":
                #                     for x in sdtcAlignSrcRcpXmlSubRoot:
                #                         if x.get('name') == "Pattern1_Wide":
                #                             prbP1W = x.get('value')
                #                             prbP1Wexist = True
                #                         if x.get('name') == "Pattern1_Height":
                #                             prbP1H = x.get('value')
                #                             prbP1Hexist = True
                #                         if x.get('name') == "Pattern2_Wide":
                #                             prbP2W = x.get('value')
                #                             prbP2Wexist = True
                #                         if x.get('name') == "Pattern2_Height":
                #                             prbP2H = x.get('value')
                #                             prbP2Hexist = True
                #                         if x.get('name') == "Pattern3_Wide":
                #                             prbP3W = x.get('value')
                #                             prbP3Wexist = True
                #                         if x.get('name') == "Pattern3_Height":
                #                             prbP3H = x.get('value')
                #                             prbP3Hexist = True
                #                         if x.get('name') == "Pattern4_Wide":
                #                             prbP4W = x.get('value')
                #                             prbP4Wexist = True
                #                         if x.get('name') == "Pattern4_Height":
                #                             prbP4H = x.get('value')
                #                             prbP4Hexist = True
                #
                #                 if sdtcAlignSrcRcpXmlSubRoot.get('name') == "Unit Alignment":
                #                     for x in sdtcAlignSrcRcpXmlSubRoot:
                #                         if x.get('name') == "Pattern1_Wide":
                #                             untP1W = x.get('value')
                #                             untP1Wexist = True
                #                         if x.get('name') == "Pattern1_Height":
                #                             untP1H = x.get('value')
                #                             untP1Hexist = True
                #                         if x.get('name') == "Pattern2_Wide":
                #                             untP2W = x.get('value')
                #                             untP2Wexist = True
                #                         if x.get('name') == "Pattern2_Height":
                #                             untP2H = x.get('value')
                #                             untP2Hexist = True
                #
                #             for sdtcDstRcpXmlSubRoot in sdtcDstRcpXmlRoot:
                #                 if sdtcDstRcpXmlSubRoot.get('name') == "Probe":
                #                     for x in sdtcDstRcpXmlSubRoot:
                #                         if x.get('name') == "Pattern1_Wide" and prbP1Wexist == True:
                #                             x.set('value', prbP1W)
                #                         if x.get('name') == "Pattern1_Height" and prbP1Hexist == True:
                #                             x.set('value', prbP1H)
                #                         if x.get('name') == "Pattern2_Wide" and prbP2Wexist == True:
                #                             x.set('value', prbP2W)
                #                         if x.get('name') == "Pattern2_Height" and prbP2Hexist == True:
                #                             x.set('value', prbP2H)
                #                         if x.get('name') == "Pattern3_Wide" and prbP3Wexist == True:
                #                             x.set('value', prbP3W)
                #                         if x.get('name') == "Pattern3_Height" and prbP3Hexist == True:
                #                             x.set('value', prbP3H)
                #                         if x.get('name') == "Pattern4_Wide" and prbP4Wexist == True:
                #                             x.set('value', prbP4W)
                #                         if x.get('name') == "Pattern4_Height" and prbP4Hexist == True:
                #                             x.set('value', prbP4H)
                #
                #                 if sdtcDstRcpXmlSubRoot.get('name') == "Unit Alignment":
                #                     for x in sdtcDstRcpXmlSubRoot:
                #                         if x.get('name') == "Pattern1_Wide" and untP1Wexist == True:
                #                             x.set('value', untP1W)
                #                         if x.get('name') == "Pattern1_Height" and untP1Hexist == True:
                #                             x.set('value', untP1H)
                #                         if x.get('name') == "Pattern2_Wide" and untP2Wexist == True:
                #                             x.set('value', untP2W)
                #                         if x.get('name') == "Pattern2_Height" and untP2Hexist == True:
                #                             x.set('value', untP2H)
                #
                #
                #             sdtcDstRcpXml.write(dstRcpSdtcXmlPath)
                #             # Delete ConvertRecipe\\tempAlign
                #             shutil.rmtree(os.path.join(scriptDir,newRcpDirName, "tempAlign"))
                #             log(
                #                 "Updating Pattern Wide/Height of Probe and Unit Alignment of: " + dstRcpSdtcXmlPath + " To match one of: " + alignSrcRcpSdtcXmlPath + " [COMPLETED]",
                #                 recipeCreatorLog)
                #
                #         except Exception as error:
                #             contProcessFlag = False
                #             singleRecipeCreationMessage = "The process is terminated. Update alignment to the source alignment recipe failed!"
                #
                #             log("Updating alignment files for:" + cvtRcpPath + " [FAILED]", recipeCreatorLog)
                #             no_time_log(str(error), recipeCreatorLog)
                #             #print("Updating alignment files for:" + cvtRcpPath + " [FAILED]")
                #             log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                #             #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                #
                #
                #
                #             # Remove the corrupted folder
                #             if os.path.isdir(cvtRcpPath) == True:
                #                 shutil.rmtree(cvtRcpPath)
                #             # continue

                # Rename files in each recipe
                if contProcessFlag == True:

                    #print("The recipe conversion is in progress...")
                    log("Starting to rename the recipe", recipeCreatorLog)
                    log("Renaming:" + cvtRcpPath, recipeCreatorLog)

                    # get recipe new name
                    newRcpName = newRecipeName

                    # Renaming files HC folder
                    folderPath = os.path.join(cvtRcpPath, "HC")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:
                            if fileName.find('mas') != -1:
                                newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                            else:
                                newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in HC folder to new recipe name!"


                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming file in IOM folder

                    folderPath = os.path.join(cvtRcpPath, "IOM")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:

                            newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                            src = os.path.join(folderPath, f)
                            dst = os.path.join(folderPath, newFileName)
                            log("Renaming:" + src, recipeCreatorLog)
                            os.rename(src, dst)
                            log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in IOM folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming file in Manifest folder

                    folderPath = os.path.join(cvtRcpPath, "Manifest")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:

                            newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                            src = os.path.join(folderPath, f)
                            dst = os.path.join(folderPath, newFileName)
                            log("Renaming:" + src, recipeCreatorLog)
                            os.rename(src, dst)
                            log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in Manifest folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming files in SDTC folder
                    folderPath = os.path.join(cvtRcpPath, "SDTC")
                    files = os.listdir(folderPath)

                    for f in files:
                        src = ""
                        dst = ""
                        fileName = os.path.basename(f)
                        try:
                            if fileName.find('mas') != -1:
                                newFileName = newRcpName + ".mas" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                            elif fileName.find('_R.rcp') != -1:
                                newFileName = newRcpName + "_R" + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)

                            else:
                                newFileName = newRcpName + "." + fileName.split('.')[len(fileName.split('.')) - 1]
                                src = os.path.join(folderPath, f)
                                dst = os.path.join(folderPath, newFileName)
                                log("Renaming:" + src, recipeCreatorLog)
                                os.rename(src, dst)
                                log("Renaming:" + src + "to:" + dst + " [COMPLETED]", recipeCreatorLog)
                        except Exception as error:

                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update files in SDTC folder to new recipe name!"

                            log("Renaming:" + src + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            #print("Renaming:" + src + " [FAILED]")
                            # log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            # #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)
                            # continue

                    # Renaming the root recipe folder
                    # Wait 2 seconds before remaing the root folder to make sure all fies are updated
                    # time.sleep(1)
                    if contProcessFlag == True:
                        src = ""
                        dst = ""

                        try:
                            src = cvtRcpPath
                            dst = os.path.join(newRcpDirPath, newRcpName)
                            # copyFolder1(src,dst)
                            shutil.copytree(src, dst)
                            log("Copy and change name of the recipe folder: " + src + " TO: " + dst + " [COMPLETED]",
                                recipeCreatorLog)
                        except Exception as error:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Cannot update the new recipe root folder name!"

                            log("Copy and change name of folder: " + src + " TO: " + dst + " [FAILED]", recipeCreatorLog)
                            no_time_log(str(error), recipeCreatorLog)
                            log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                            #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)

                            # Remove the corrupted folder
                            if os.path.isdir(cvtRcpPath) == True:
                                shutil.rmtree(cvtRcpPath)

                            if os.path.isdir(dst) == True:
                                shutil.rmtree(dst)
                            # continue

                # Updating the recipe to the template

                if contProcessFlag == True:

                    newRcpName = newRecipeName
                    newRcpPath = os.path.join(newRcpDirPath, newRcpName)

                    log("Updating:" + newRcpPath + "To the templates:" + templatePath, recipeCreatorLog)
                    check1 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"),
                                                       templateLine="Add")
                    check2 = sdtc_type_template_update(os.path.join(templatePath, "SDTCRecipeMaster_template.xml"),
                                                       os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"),
                                                       templateLine="Add")
                    check3 = sdtc_type_template_update(os.path.join(templatePath, "IOMRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "IOM", newRcpName + ".xml"), templateLine="Add")
                    check4 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipe_template.xml"),
                                                       os.path.join(newRcpPath, "HC", newRcpName + ".xml"), templateLine="")
                    check5 = sdtc_type_template_update(os.path.join(templatePath, "HCRecipeMaster_template.mas.xml"),
                                                       os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"),
                                                       templateLine="Remove")

                    check6 = manifest_type_template_update(os.path.join(templatePath, "Manifest_template.xml"),
                                                           os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5 and check6:
                        contProcessFlag = True
                        log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update to new recipe template failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating:" + newRcpPath + "To the templates:" + templatePath + " [FAILED]", recipeCreatorLog)

                # Update Identity line for xml files
                if contProcessFlag == True:

                    log("Updating identity line for:" + newRcpPath, recipeCreatorLog)
                    check1 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                    check2 = identity_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check3 = identity_update(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                    check4 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                    check5 = identity_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                    check6 = identity_update(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5 and check6:
                        contProcessFlag = True
                        log("Updating identity line for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update recipe files failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating identity line for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update value of mas xml files
                if contProcessFlag == True:

                    log("Updating value of mas.xml files for:" + newRcpPath, recipeCreatorLog)

                    check1 = mas_file_parameter_update(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check2 = mas_file_parameter_update(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))

                    if check1 and check2:
                        contProcessFlag = True
                        log("Updating value of mas.xml files for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update recipe files failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating value of mas.xml files for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                #  Update specific parameter
                #  If there is no specific parameter link -> DO nothing and Continue

                if contProcessFlag == True:

                    specificParaFilePath = specificParameterFilePath
                    if specificParaFilePath.strip() != "":
                        if os.path.isfile(specificParaFilePath.strip()):

                            log("Updating specific parameters for:" + newRcpPath + "Using:" + specificParaFilePath,
                                recipeCreatorLog)

                            check = specific_para_file_update(newRcpPath, specificParaFilePath)

                            if check == True:
                                contProcessFlag = True
                                log(
                                    "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]",
                                    recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                singleRecipeCreationMessage = "The process is terminated. Update specific parameters failed!"

                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)
                                log(
                                    "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                    recipeCreatorLog)
                        else:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Update specific parameters failed. File could not be found!"
                            # Remove the corrupted folder
                            if os.path.isdir(newRcpPath) == True:
                                shutil.rmtree(newRcpPath)
                            log(
                                "Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                recipeCreatorLog)
                            no_time_log(
                                "The parameter file at:[" + specificParaFilePath.strip() + "] could not be found",
                                recipeCreatorLog)

                    else:
                        log(
                            "There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                            recipeCreatorLog)

                #  Update golden parameter
                #  If there is no specific parameter link -> DO nothing and Continue

                if contProcessFlag == True:

                    for goldenFilePath in goldenFileList:

                        specificParaFilePath = goldenFilePath
                        if specificParaFilePath.strip() != "":
                            if os.path.isfile(specificParaFilePath.strip()):

                                log("Updating golden parameters for:" + newRcpPath + "Using:" + specificParaFilePath,
                                    recipeCreatorLog)

                                check = specific_para_file_update(newRcpPath, specificParaFilePath)

                                if check == True:
                                    contProcessFlag = True
                                    log(
                                        "Updating golden parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]",
                                        recipeCreatorLog)
                                else:
                                    contProcessFlag = False
                                    singleRecipeCreationMessage = "The process is terminated. Update golden parameters failed!"

                                    # Remove the corrupted folder
                                    if os.path.isdir(newRcpPath) == True:
                                        shutil.rmtree(newRcpPath)
                                    log(
                                        "Updating golden parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                        recipeCreatorLog)
                            else:
                                contProcessFlag = False
                                singleRecipeCreationMessage = "The process is terminated. Update golden parameters failed. File could not be found!"
                                # Remove the corrupted folder
                                if os.path.isdir(newRcpPath) == True:
                                    shutil.rmtree(newRcpPath)
                                log(
                                    "Updating golden parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [FAILED]",
                                    recipeCreatorLog)
                                no_time_log("The parameter file at:[" + specificParaFilePath.strip() + "] could not be found",
                                            recipeCreatorLog)

                        else:
                            log("There is EMPTY link for the golden parameter file. No change to the recipe:" + newRcpPath,
                                recipeCreatorLog)

                # Test new way to catch exception
                # if contProcessFlag == True:
                #
                #     specificParaFilePath = row[spfParUpdFileColIndex]
                #     if specificParaFilePath.strip() != "":
                #
                #         log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath,
                #             recipeCreatorLog)
                #         try:
                #             specific_para_file_update(newRcpPath, specificParaFilePath)
                #             contProcessFlag = True
                #             log("Updating specific parameters for:" + newRcpPath + " Using:" + specificParaFilePath + " [COMPLETED]", recipeCreatorLog)
                #         except Exception:
                #
                #             contProcessFlag = False
                #
                #             tempRow = row
                #             tempRow.insert(0, "Failed to update specific parameters for:" + newRcpPath)
                #             tempRow.insert(0, str(rowIndex))
                #             failedRcpList.append(tempRow)
                #
                #             log("[FAILED]: The recipe conversion for: " + cvtRcpPath, recipeCreatorLog)
                #             #print("[FAILED]: The recipe conversion for: " + cvtRcpPath)
                #
                #             # Remove the corrupted folder
                #             shutil.rmtree(cvtRcpPath, ignore_errors=True)
                #             continue
                #     else:
                #         log("There is EMPTY link for the specific parameter file. No change to the recipe:" + newRcpPath,
                #             recipeCreatorLog)

                # Update network folder for Manifest.xml
                if contProcessFlag == True:
                    # templatePath = ""
                    # networkDrive = ""
                    # networkFolder = ""
                    # recipeFileList = ""

                    log("Updating network folder for:" + newRcpPath, recipeCreatorLog)

                    absNetworkFolder = newRecipeLocationPath
                    check = network_folder_manifest_file_update(newRcpPath, absNetworkFolder, networkFolder, networkDrive)

                    if check == True:
                        contProcessFlag = True
                        log("Updating network folder for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False

                        singleRecipeCreationMessage = "The process is terminated. Update network path in the manifest file failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating network folder for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update main checksum of all xml except manifest xml
                if contProcessFlag == True:

                    log("Updating checksum for:" + newRcpPath, recipeCreatorLog)
                    check1 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".xml"))
                    check2 = checksum_creator(os.path.join(newRcpPath, "SDTC", newRcpName + ".mas.xml"))
                    check3 = checksum_creator(os.path.join(newRcpPath, "IOM", newRcpName + ".xml"))
                    check4 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".xml"))
                    check5 = checksum_creator(os.path.join(newRcpPath, "HC", newRcpName + ".mas.xml"))
                    # check6 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check1 and check2 and check3 and check4 and check5:
                        contProcessFlag = True
                        log("Updating checksum for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update checksum for xml files (except manifest .xml) failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                        log("Updating checksum for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Update manifest file for checksum and other
                if contProcessFlag == True:

                    check = manifest_file_update(newRcpPath)
                    check1 = checksum_creator(os.path.join(newRcpPath, "Manifest", newRcpName + ".xml"))

                    if check == True and check1 == True:
                        contProcessFlag = True
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Update checksum for manifest file failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)

                # Final specific parameter verification

                if contProcessFlag == True:

                    specificParaFilePath = specificParameterFilePath

                    check = final_recipe_validation(newRcpPath, specificParaFilePath)

                    if check == True:
                        contProcessFlag = True
                        log("Final verifying for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                    else:
                        contProcessFlag = False
                        singleRecipeCreationMessage = "The process is terminated. Final verification failed!"

                        # Remove the corrupted folder
                        if os.path.isdir(newRcpPath) == True:
                            shutil.rmtree(newRcpPath)
                        log("Final verifying for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Golden parameter final verification

                if contProcessFlag == True:

                    for goldenFilePath in goldenFileList:
                        specificParaFilePath = goldenFilePath

                        check = final_recipe_validation(newRcpPath, specificParaFilePath)

                        if check == True:
                            contProcessFlag = True
                            log("Final verifying for:" + newRcpPath + " [COMPLETED]", recipeCreatorLog)
                        else:
                            contProcessFlag = False
                            singleRecipeCreationMessage = "The process is terminated. Final verification failed!"

                            # Remove the corrupted folder
                            if os.path.isdir(newRcpPath) == True:
                                shutil.rmtree(newRcpPath)
                            log("Final verifying for:" + newRcpPath + " [FAILED]", recipeCreatorLog)

                # Remove the temp folder cvtRcppathRoot = ...\ConvertRecipe\Temp
                if contProcessFlag == True:

                    singleRecipeCreationMessage = "Recipe creation COMPLETED!"

                    if os.path.isdir(cvtRcppathRoot) == True:
                        shutil.rmtree(cvtRcppathRoot)

                    log("[SUCCESSFULL]: The recipe conversion for: " + source, recipeCreatorLog)
                    #print("[SUCCESSFULL]: The recipe conversion for: " + source)
                else:
                    log("[FAILED]: The recipe conversion for: " + source, recipeCreatorLog)
                    #print("[FAILED]: The recipe conversion for: " + source)


                # Pop up result message

                NPI_creation_gui.messageLableValue.set(singleRecipeCreationMessage)

                # Setup state for widgets
                NPI_creation_gui.recipeTemplateCheckbutton.config(state=tk.NORMAL)
                NPI_creation_gui.newRcipeLocationCheckbutton.config(state=tk.NORMAL)
                # NPI_creation_gui.sourceAlignRecipeCheckbutton.config(state=tk.NORMAL)
                NPI_creation_gui.newRecipeNameCheckbutton.config(state=tk.NORMAL)

                if NPI_creation_gui.rcpTemplateCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.recipeTemplateEntry.config(state=tk.NORMAL)
                    NPI_creation_gui.recipeTemplateButton.config(state=tk.NORMAL)
                NPI_creation_gui.runButton.config(state=tk.NORMAL)

                if NPI_creation_gui.newRcpLocCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.newRecipeLocationButton.config(state=tk.NORMAL)
                    NPI_creation_gui.newRecipeLocationEntry.config(state=tk.NORMAL)

                # if NPI_creation_gui.srcAlignRecipeCheckbuttonValue.get() == "NO":
                #     NPI_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)
                #     NPI_creation_gui.sourceAlignRecipeEntry.config(state=tk.NORMAL)

                NPI_creation_gui.sourceRecipeEntry.config(state=tk.NORMAL)
                NPI_creation_gui.sourceRecipeButton.config(state=tk.NORMAL)

                if NPI_creation_gui.newRcpNameCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)
                    NPI_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)

                NPI_creation_gui.specificParameterFileEntry.config(state=tk.NORMAL)
                NPI_creation_gui.specificParameterFileButton.config(state=tk.NORMAL)

                # NPI_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)


            except Exception as error:

                cvtRcppathRoot = os.path.join(newRcpDirPath, "temp")
                singleRecipeCreationMessage = "Recipe creation FAILED!"
                NPI_creation_gui.messageLableValue.set(singleRecipeCreationMessage)
                if os.path.isdir(cvtRcppathRoot) == True:
                    shutil.rmtree(cvtRcppathRoot)

                no_time_log(str(error),recipeCreatorLog)

                # Setup state for widgets
                NPI_creation_gui.recipeTemplateCheckbutton.config(state = tk.NORMAL)
                NPI_creation_gui.newRcipeLocationCheckbutton.config(state = tk.NORMAL)
                # NPI_creation_gui.sourceAlignRecipeCheckbutton.config(state = tk.NORMAL)
                NPI_creation_gui.newRecipeNameCheckbutton.config(state = tk.NORMAL)


                if NPI_creation_gui.rcpTemplateCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.recipeTemplateEntry.config(state = tk.NORMAL)
                    NPI_creation_gui.recipeTemplateButton.config(state=tk.NORMAL)
                NPI_creation_gui.runButton.config(state = tk.NORMAL)

                if NPI_creation_gui.newRcpLocCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.newRecipeLocationButton.config(state = tk.NORMAL)
                    NPI_creation_gui.newRecipeLocationEntry.config(state = tk.NORMAL)


                # if NPI_creation_gui.srcAlignRecipeCheckbuttonValue.get() == "NO":
                #     NPI_creation_gui.sourceAlignRecipeButton.config(state=tk.NORMAL)
                #     NPI_creation_gui.sourceAlignRecipeEntry.config(state = tk.NORMAL)


                NPI_creation_gui.sourceRecipeEntry.config(state=tk.NORMAL)
                NPI_creation_gui.sourceRecipeButton.config(state=tk.NORMAL)

                if NPI_creation_gui.newRcpNameCheckbuttonValue.get() == "NO":
                    NPI_creation_gui.newRecipeNameEntry.config(state=tk.NORMAL)
                    NPI_creation_gui.newRecipeNameEntry.config(state = tk.NORMAL)


                NPI_creation_gui.specificParameterFileEntry.config(state=tk.NORMAL)
                NPI_creation_gui.specificParameterFileButton.config(state=tk.NORMAL)


    global singleRecipeTask

    singleRecipeTask = threading.Thread(target=callback)
    singleRecipeTask.start()


    # app.rcpCountResult.set(str(len(convertedRcpList)) + "/" + str(len(failedRcpList)))

def version_verification(recipePath,TemplatePath):

    try:
        log("Checking the recipe: " + recipePath + " VS the template version: " + TemplatePath, recipeCreatorLog)

        compareResult = True

        for file in os.listdir(TemplatePath):
            recipeFilePath =""
            templateFilePath = os.path.join(TemplatePath,file)
            templateFileXml = ET.parse(templateFilePath)
            templateVersion = templateFileXml.find("Identity").get('version')

            if templateFileXml.find("Identity").get('name') == "HCRecipeMaster_template":
                recipeFilePath = os.path.join(recipePath,"HC",os.path.basename(recipePath)+ ".mas.xml" )
            if templateFileXml.find("Identity").get('name') == "HCRecipe_template":
                recipeFilePath = os.path.join(recipePath,"HC",os.path.basename(recipePath)+ ".xml" )
            if templateFileXml.find("Identity").get('name') == "IOMRecipe":
                recipeFilePath = os.path.join(recipePath,"IOM",os.path.basename(recipePath)+ ".xml" )
            if templateFileXml.find("Identity").get('name') == "Manifest_template":
                recipeFilePath = os.path.join(recipePath,"Manifest",os.path.basename(recipePath)+ ".xml" )
            if templateFileXml.find("Identity").get('name') == "SDTCRecipe":
                recipeFilePath = os.path.join(recipePath,"SDTC",os.path.basename(recipePath)+ ".xml" )
            if templateFileXml.find("Identity").get('name') == "SDTCRecipeMas":
                recipeFilePath = os.path.join(recipePath,"SDTC",os.path.basename(recipePath)+ ".mas.xml" )

            recipeFileXml = ET.parse(recipeFilePath)
            recipeVersion = recipeFileXml.find("Identity").get('version')

            if templateVersion!= recipeVersion:
                RGC_gui.mismatchedRecipeReportList.append(recipePath)
                RGC_gui.mismatchedRecipeFileReportList.append(recipeFilePath)
                RGC_gui.mismatchedParameterList.append(recipeVersion)
                RGC_gui.mismatchedGoldenFileReportList.append(templateFilePath)
                RGC_gui.mismatchedGoldenParameterList.append(templateVersion)

                compareResult = False
                log(f"Checking recipe version: {recipeFilePath}  VS template version: {templateFilePath} - Result = FAILED", recipeCreatorLog)


        return compareResult
    except Exception as error:
        RGC_gui.mismatchedRecipeReportList.append(recipePath)
        RGC_gui.mismatchedRecipeFileReportList.append(repr(error))
        RGC_gui.mismatchedParameterList.append(repr(error))
        RGC_gui.mismatchedGoldenFileReportList.append(repr(error))
        RGC_gui.mismatchedGoldenParameterList.append(repr(error))
        log(f"Checking recipe version: {recipePath}  VS template version: {TemplatePath} - Result = FAILED", recipeCreatorLog)
        no_time_log(repr(error), recipeCreatorLog)
        return False


def specific_golden_file_vefication(recipePath, specificGoldenFilePath):
    try:
        log("==================================================================================", recipeCreatorLog)
        log("Checking the recipe: " + recipePath + " VS the golden file: " + specificGoldenFilePath, recipeCreatorLog)

        compareResult = True

        paraFileXml = ET.parse(specificGoldenFilePath)

        paraFileXmlRoot = paraFileXml.getroot()

        # no_time_log(ET.tostring(paraFileXmlRoot, encoding='utf-8').decode('utf-8'), recipeCreatorLog)
        toUpdateFilePath = ""

        for paraComp in paraFileXmlRoot:
            # The xml file in the created recipe is indentified from combination of ComponentRecipe + recipe name
            for paraFileInfo in paraComp:
                if paraFileInfo.get("name") == "xml":
                    # Read xml file in recipe
                    toUpdateFilePath = os.path.join(recipePath, paraComp.get('name'), os.path.basename(recipePath) + ".xml")
                    toUpdateFileXml = ET.parse(toUpdateFilePath)

                # if paraFileInfo.get("name") == "mas.xml":
                #     # Read mas xml file in recipe
                #     toUpdateFilePath = os.path.join(recipePath, paraComp.get('name'), os.path.basename(recipePath) + ".mas.xml")
                #     toUpdateFileXml = ET.parse(toUpdateFilePath)

                # Find in the toUpdateFile the menu having the same name with the paraMenu.get('name') in the golden file
                for paraMenu in paraFileInfo.findall("Menu"):

                    # Read Supported XPath syntax for ElementTree xml
                    # [@attrib='value'] Selects all elements for which the given attribute has the given value. The value cannot contain quotes.

                    rcpMenu = toUpdateFileXml.find("Menu[@name = " + "'" + paraMenu.get('name') + "'" + "]")

                    if not (rcpMenu is None):

                        #  find in recipe Menu , item having the same name with the parameter Item paraItem.get('name')
                        for paraItem in paraMenu:
                            rcpItem = rcpMenu.find("Item[@name = " + "'" + paraItem.get('name') + "'" + "]")
                            # print(paraItem.attrib)

                            if not (rcpItem is None):
                                log(f"Checking Recipe parameter: {str(rcpItem.attrib)}  VS Golden parameter: {paraItem.attrib}", recipeCreatorLog)
                                if EnableValueCheckOnly == "False":
                                    if rcpItem.attrib!=paraItem.attrib:
                                        RGC_gui.mismatchedRecipeReportList.append(recipePath)
                                        RGC_gui.mismatchedRecipeFileReportList.append(os.path.join(paraComp.get('name'), os.path.basename(recipePath) + ".xml"))
                                        RGC_gui.mismatchedParameterList.append(f"{rcpMenu.get('name')} >> {rcpItem.attrib}")
                                        RGC_gui.mismatchedGoldenFileReportList.append(specificGoldenFilePath)
                                        RGC_gui.mismatchedGoldenParameterList.append(f"{paraMenu.get('name')} >> {paraItem.attrib}")

                                        compareResult = False
                                        log(f"Checking Recipe parameter: {str(rcpItem.attrib)}  VS Golden parameter: {paraItem.attrib} - Result = FAILED", recipeCreatorLog)
                                    else:
                                        log(f"Checking Recipe parameter: {str(rcpItem.attrib)}  VS Golden parameter: {paraItem.attrib} - Result = PASSED",recipeCreatorLog)
                                else:
                                    if rcpItem.get('value') !=paraItem.get('value'):
                                        RGC_gui.mismatchedRecipeReportList.append(recipePath)
                                        RGC_gui.mismatchedRecipeFileReportList.append(os.path.join(paraComp.get('name'), os.path.basename(recipePath) + ".xml"))
                                        RGC_gui.mismatchedParameterList.append(f"{rcpMenu.get('name')} >> {rcpItem.attrib}")
                                        RGC_gui.mismatchedGoldenFileReportList.append(specificGoldenFilePath)
                                        RGC_gui.mismatchedGoldenParameterList.append(f"{paraMenu.get('name')} >> {paraItem.attrib}")

                                        compareResult = False
                                        log(f"Checking Recipe parameter: {str(rcpItem.attrib)}  VS Golden parameter: {paraItem.attrib} - Result = FAILED", recipeCreatorLog)
                                    else:
                                        log(f"Checking Recipe parameter: {str(rcpItem.attrib)}  VS Golden parameter: {paraItem.attrib} - Result = PASSED",recipeCreatorLog)
                                    # rcpItem.set('value', str(paraItem.get('value')))

                            else:

                                RGC_gui.mismatchedRecipeReportList.append(recipePath)
                                RGC_gui.mismatchedRecipeFileReportList.append(os.path.join(paraComp.get('name'), os.path.basename(recipePath) + ".xml"))
                                RGC_gui.mismatchedParameterList.append(f"{rcpMenu.get('name')} >> Parameter does not exist")
                                RGC_gui.mismatchedGoldenFileReportList.append(specificGoldenFilePath)
                                RGC_gui.mismatchedGoldenParameterList.append(f"{paraMenu.get('name')} >> {paraItem.attrib}")


                                log("Cannot find Item:[" + str(paraItem.get('name')) + "] in the Menu: [" + str(paraMenu.get('name')) + "] in the file:" + toUpdateFilePath,recipeCreatorLog)
                                log(f"Checking Recipe parameter: Not Exist  VS Golden parameter: {paraItem.attrib} - Result = FAILED",recipeCreatorLog)
                                compareResult = False


                    else:

                        RGC_gui.mismatchedRecipeReportList.append(recipePath)
                        RGC_gui.mismatchedRecipeFileReportList.append(os.path.join(paraComp.get('name'), os.path.basename(recipePath) + ".xml"))
                        RGC_gui.mismatchedParameterList.append("Menu does not exist")
                        RGC_gui.mismatchedGoldenFileReportList.append(specificGoldenFilePath)
                        RGC_gui.mismatchedGoldenParameterList.append(f"{paraMenu.get('name')}")

                        log("Cannot find Menu:[" + str(paraMenu.get('name')) + "]in the file: " + toUpdateFilePath,recipeCreatorLog)
                        log(f"Checking Recipe Menu: Not Exist  VS Golden File Menu: {str(paraMenu.get('name'))} - Result = FAILED",recipeCreatorLog)
                        compareResult = False


        log("Checking the recipe: " + recipePath + "against the golden file: " + specificGoldenFilePath + "[COMPLETED]", recipeCreatorLog)

        return compareResult
    except Exception as error:
        RGC_gui.mismatchedRecipeReportList.append(recipePath)
        RGC_gui.mismatchedRecipeFileReportList.append(str(error))
        RGC_gui.mismatchedParameterList.append(str(error))
        RGC_gui.mismatchedGoldenFileReportList.append(specificGoldenFilePath)
        RGC_gui.mismatchedGoldenParameterList.append(str(error))

        log("Checking the recipe: " + recipePath + "against the golden file: " + specificGoldenFilePath + "[FAILED]", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def auto_export_to_csv(dictionary,name):

    try:


        csvFilePath = os.path.join(os.getcwd(), str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + name)

        if csvFilePath is not None:

            log("Exporting the selected recipe list to: [" + csvFilePath +"]", recipeCreatorLog)

            df = pd.DataFrame(dictionary)
            df.to_csv(csvFilePath, index = False)
            # df.to_csv(recipeCreatorLog, sep='\t',mode = 'a')

            log("Exporting the selected recipe list to: [" + csvFilePath + "] - [COMPLETED]", recipeCreatorLog)

    except Exception as error:

        no_time_log(str(error),recipeCreatorLog)

def recipe_gold_check_main(confTemplatePath,selectedRecipeList,goldenFileList):

    def callback():
#     Verify against golden files
#         Reset mismatched list
        global EnableVersionCheck

        try:
            del RGC_gui.mismatchedRecipeList[:]

            del RGC_gui.mismatchedRecipeReportList[:]
            del RGC_gui.mismatchedRecipeFileReportList[:]
            del RGC_gui.mismatchedParameterList[:]
            del RGC_gui.mismatchedGoldenFileReportList[:]
            del RGC_gui.mismatchedGoldenParameterList[:]

            RGC_gui.mismatchedRecipeListbox.delete(0,'end')
            RGC_gui.goldCheckProgressBar["value"] =0


            totalRecipeCount = len(selectedRecipeList)
            RGC_gui.goldCheckProgressBar["maximum"] = totalRecipeCount

            RGC_gui.rcpGoldCheckResult.set("0/0")

            #Disable buttons to prevent muliple run
            RGC_gui.runGoldCheckButton.config(state=DISABLED)
            RGC_gui.goldenFileSelectionDefaultCheckbutton.config(state=DISABLED)
            RGC_gui.removeButton.config(state=DISABLED)
            RGC_gui.addButton.config(state=DISABLED)
            RGC_gui.sourceRecipeLocationButton.config(state=DISABLED)

            RGC_gui.progressMessage.set("Recipe verification is in progress...")
            # Executing gold check function

            processedRecipeCount = 0
            passedRecipeCount = 0
            for recipe in selectedRecipeList:
                processedRecipeCount = processedRecipeCount +1
                goldCheckResult = True

                if EnableVersionCheck == "True":
                    tempResult = version_verification(recipe,app.rcpTemplate.get())
                    goldCheckResult = goldCheckResult and tempResult

                for goldenFile in goldenFileList:

                    tempResult = specific_golden_file_vefication(recipe, goldenFile)
                    goldCheckResult = goldCheckResult and tempResult


                if goldCheckResult == False:
                    RGC_gui.mismatchedRecipeList.append(recipe)
                    RGC_gui.mismatchedRecipeListbox.insert(END,recipe)
                else:
                    passedRecipeCount = passedRecipeCount +1

                # Update progess bar
                RGC_gui.goldCheckProgressBar["value"] = processedRecipeCount
                RGC_gui.rcpGoldCheckResult.set(f"{str(processedRecipeCount)}/{str(passedRecipeCount)}")


            auto_export_to_csv(RGC_gui.mismatchedRecipeResultDict,"MismatchedRecipeDetailReport.csv")
            auto_export_to_csv(RGC_gui.mismatchedRecipeListDict,"MismatchedRecipeList.csv")


            #Enable buttons after gold check completed or CANCEL button is press
            RGC_gui.runGoldCheckButton.config(state=NORMAL)
            RGC_gui.goldenFileSelectionDefaultCheckbutton.config(state=NORMAL)
            RGC_gui.removeButton.config(state=NORMAL)
            RGC_gui.addButton.config(state=NORMAL)
            RGC_gui.sourceRecipeLocationButton.config(state=NORMAL)

            RGC_gui.progressMessage.set("Recipe verification is completed!")

        except Exception as error:

            log(str(error), recipeCreatorLog)
            RGC_gui.progressMessage.set("Recipe verification is terminated abnormally!")

    global singleRecipeTask

    singleRecipeTask = threading.Thread(target=callback)
    singleRecipeTask.start()



def single_creation():
    global single_creation_gui
    single_creation_gui = singleRecipeConvertGUI()
    # Set templatePath to the config value
    single_creation_gui.rcpTemplatePath.set(configTemplatePath)

def recipe_list_creation():
    global recipe_list_creation_gui
    recipe_list_creation_gui = recipeListCreationGui()


def checksum_validate(toCheckFilePath):

    try:

        binaryFile = open(toCheckFilePath, "rb")
        readBinaryFile = binaryFile.read()
        binaryFile.close()

        ChecksumStartPostion = readBinaryFile.find("<BeginChecksum />".encode('utf-8')) + len("<BeginChecksum />".encode('utf-8'))

        readBinaryFileChecksumPart = readBinaryFile[ChecksumStartPostion:]

        checksum = hashlib.md5()
        checksum.update(readBinaryFileChecksumPart)

        chksString = str(checksum.hexdigest())
        # #print(checksum.hexdigest())

        toCheckFileXml = ET.parse(toCheckFilePath)
        toCheckFileXmlRoot = toCheckFileXml.getroot()

        if toCheckFileXmlRoot.get('checksum') == chksString:
            return True
        else:
            return False


    except Exception as error:
        log("Exception occured during checksum varification!", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False


def checksum_creator_and_verification(toCheckpathPath):

    try:
        toCheckpathXml = ET.parse(toCheckpathPath)
        toCheckpathXmlRoot = toCheckpathXml.getroot()

        if "checksum" in toCheckpathXmlRoot.attrib:

            for sub in toCheckpathXmlRoot:
                if sub.tag == "Identity":
                    sub.set('name', os.path.basename(toCheckpathPath).split('.')[0])
                    sub.set('id', str(uuid.uuid4()).upper())
                    sub.set('asof', datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))

            # Update the file before creating checksum
            toCheckpathXml.write(toCheckpathPath)


            # Create checksume
            binaryFile = open(toCheckpathPath, "rb")
            readBinaryFile = binaryFile.read()
            binaryFile.close()

            ChecksumStartPostion = readBinaryFile.find("<BeginChecksum />".encode('utf-8')) + len("<BeginChecksum />".encode('utf-8'))

            readBinaryFileChecksumPart = readBinaryFile[ChecksumStartPostion:]

            checksum = hashlib.md5()
            checksum.update(readBinaryFileChecksumPart)

            chksString = str(checksum.hexdigest())
            toCheckpathXmlRoot.set('checksum', chksString)

            # Write xml file
            toCheckpathXml.write(toCheckpathPath)

        #     Verify checksum again

            binarypath = open(toCheckpathPath, "rb")
            readBinarypath = binarypath.read()
            binarypath.close()

            ChecksumStartPostion = readBinarypath.find("<BeginChecksum />".encode('utf-8')) + len("<BeginChecksum />".encode('utf-8'))

            readBinarypathChecksumPart = readBinarypath[ChecksumStartPostion:]

            checksum = hashlib.md5()
            checksum.update(readBinarypathChecksumPart)

            chksString = str(checksum.hexdigest())

            toCheckpathXml = ET.parse(toCheckpathPath)
            toCheckpathXmlRoot = toCheckpathXml.getroot()

            if toCheckpathXmlRoot.get('checksum') == chksString:

                return True
            else:
                log("Checksum is updated but failed during re-verification", recipeCreatorLog)
                return False
        else:
            no_time_log("[checksum] attribute does not exist", recipeCreatorLog)
            return False

    except Exception as error:
        log("Exception occured during checksum creation!", recipeCreatorLog)
        no_time_log(str(error), recipeCreatorLog)
        return False

def NPI_creation():
    global NPI_creation_gui
    NPI_creation_gui = NPIRecipeConvertGUI()
    # Set templatePath to the config value
    NPI_creation_gui.rcpTemplatePath.set(configTemplatePath)

def RGC():
    global RGC_gui
    RGC_gui = recipeGoldCheckGui()


class MainGui:
    def __init__(self):
        px = 10
        ipy= 5
        # Init master gui
        self.master = tk.Tk()
        self.master.title('BLiTS Recipe Creator 3.0.1 - INTEL CONFIDENTIAL')
        self.master.resizable(1, 0)
        if os.path.isfile("icons\\brick.png") == True:
            self.p1 = PhotoImage(file='icons\\brick.png')

            # Setting icon of master window
            self.master.iconphoto(True, self.p1)

        # Positions the window
        self.master.geometry("+100+100")

        # init recipe file name path
        self.rcpListPath = tk.StringVar()
        self.rcpTemplate = tk.StringVar()
        self.rcpNetDrive = tk.StringVar()
        self.rcpNetFolder = tk.StringVar()
        self.templateFolderChkbValue = tk.StringVar()
        self.rcpCountResult = tk.StringVar()
        self.rcpCountResult.set("0/0")
        self.successRcpCount = tk.StringVar()
        self.processedCount = tk.StringVar()
        self.processedCount.set("0/0")

        self.progress = tk.StringVar()
        self.progress.set("")
        # self.rcpListPath = ""

        # menu = Menu(self.master)
        # self.master.config(menu=menu)
        #
        # fileMenu = Menu(menu)
        # fileMenu.add_command(label="Item")
        # # fileMenu.add_command(label="Exit", command=self.exitProgram)
        # menu.add_cascade(label="File", menu=fileMenu)
        #
        # editMenu = Menu(menu)
        # editMenu.add_command(label="Undo")
        # editMenu.add_command(label="Redo")
        # menu.add_cascade(label="Edit", menu=editMenu)

        self.master.columnconfigure(0, weight=1)


        # Adding utility buttons
        self.utilitiesFrame = tk.LabelFrame(self.master, text = 'Utilities', font=("TkTextFont", 14), fg = "blue", width = 1230, height = 100)

        self.rcpListCreateButton = tk.Button(self.utilitiesFrame, text='Recipe List Creation', command=recipe_list_creation, font=('TkTextFont	', 14))
        self.rcpChecksumCreationButton = tk.Button(self.utilitiesFrame, text='Checksum Validation', command=self.checksum_creation, font=('TkTextFont	', 14))
        self.rcpSingleCreationButton = tk.Button(self.utilitiesFrame, text='Single Creation', command=single_creation, font=('TkTextFont	', 14))
        self.rcpNPIButton = tk.Button(self.utilitiesFrame, text='NPI Creation', command=NPI_creation, font=('TkTextFont	', 14))
        self.rcpGCButton = tk.Button(self.utilitiesFrame, text='RGC', command=RGC, font=('TkTextFont	', 14))

        self.utilitiesFrame.grid(row=0, column=0, padx=10, pady=0, sticky=tk.W+tk.E)
        # self.utilitiesFrame.grid_propagate(False)
        self.rcpListCreateButton.grid(row=0, column=0, padx=px, pady=10, sticky=tk.E)
        self.rcpChecksumCreationButton.grid(row=0, column=1, padx=px, pady=10, sticky=tk.E)
        self.rcpSingleCreationButton.grid(row=0, column=2, padx=px, pady=10, sticky=tk.E)
        self.rcpNPIButton.grid(row=0, column=3, padx=px, pady=10, sticky=tk.E)
        self.rcpGCButton.grid(row=0, column=4, padx=px, pady=10, sticky=tk.E)

        # ===========================================================
        # Config frame
        self.configFrame = tk.LabelFrame(self.master, text = 'Configuration', font=("TkTextFont", 14), fg = "blue", width = 1230, height = 160)
        # Template Config label
        self.rcpTemplateLabel = tk.Label(self.configFrame, text=' Recipe Template', font=("TkTextFont", 14))
        self.rcpTemplateEntry = tk.Entry(self.configFrame, textvariable = self.rcpTemplate, width = 105, font=('TkTextFont	', 12))

        self.rcpNetworkDriveLabel = tk.Label(self.configFrame, text='  Network Drive', font=('TkTextFont', 14))
        self.rcpNetworkDriveEntry = tk.Entry(self.configFrame, textvariable=self.rcpNetDrive,width = 10, font=('TkTextFont	', 14))

        self.rcpNetworkFolderLabel = tk.Label(self.configFrame, text=' Network Folder', font=('TkTextFont	', 14))
        self.rcpNetworkFolderEntry = tk.Entry(self.configFrame, textvariable=self.rcpNetFolder,width=59, font=('TkTextFont	', 14))

        self.templateFolderCheckbutton  = tk.Checkbutton(self.configFrame,  text = 'Set as configuration', variable = self.templateFolderChkbValue, onvalue = "YES", offvalue = "NO", font=('TkTextFont', 14), command = self.tongle)
        self.rcpTemplateButton = tk.Button(self.configFrame, text='>>>', command=self.get_template_path, font=('TkTextFont	', 14))

        # Organize widgets for config frame


        self.configFrame.grid(row=1, column=0, padx = 10, pady=50, sticky = tk.W+tk.E)
        # self.configFrame.grid_propagate(False)
        self.configFrame.columnconfigure(1,weight=1)
        self.configFrame.columnconfigure(3, weight=1)

        self.rcpNetworkDriveLabel.grid(row=0, column=0, padx=px, pady=10, sticky = tk.E)
        self.rcpNetworkDriveEntry.grid(row=0, column=1, padx=px, ipady=ipy, sticky=tk.W)
        self.rcpNetworkFolderLabel.grid(row=0, column=2, padx=px, pady=10, sticky = tk.E)
        self.rcpNetworkFolderEntry.grid(row=0, column=3, padx=px, ipady=ipy, sticky=tk.E+tk.W)

        self.rcpTemplateLabel.grid(row=2, column=0, padx=px, pady=10, sticky=tk.W)

        self.rcpTemplateEntry.grid(row=2, column=1, padx=px, ipady = ipy, sticky = tk.W +tk.E, columnspan = 3)
        self.rcpTemplateButton.grid(row=2, column=4, padx=px, sticky = tk.E)
        self.templateFolderCheckbutton.grid(row=3, column = 3,sticky=tk.E )


        # ============================================================
        # Add Run Frame
        self.runFrame = tk.LabelFrame(self.master, text ='Recipe Create',font=("TkTextFont", 14), fg = "blue", width = 1230, height = 200)
        self.rcpListButtton = tk.Button(self.runFrame, text='>>>', command=self.get_recipe_list_path, font=('TkTextFont	', 14))
        self.rcpListPathEntry = tk.Entry(self.runFrame, textvariable=self.rcpListPath, width=105, font=('TkTextFont', 12))
        self.rcpListPathLabel = tk.Label(self.runFrame, text='Recipe List', font=('TkTextFont', 14))


        # self.runFrame.columnconfigure(0,weight=1)
        self.runFrame.columnconfigure(1, weight=1)
        # self.runFrame.columnconfigure(2, weight=1)
        self.runFrame.grid(row=2, column=0, padx = 10, pady = 10, sticky = tk.W+tk.E)
        # self.runFrame.grid_propagate(False)
        self.rcpListPathLabel.grid(row=0, column=0, padx=px, pady=10, sticky = tk.E)
        self.rcpListPathEntry.grid(row=0, column=1, padx=px, ipady=ipy, sticky = tk.W +tk.E)
        self.rcpListButtton.grid(row=0, column=2, padx =px, sticky = tk.E)


        self.progressBar = ttk.Progressbar(self.runFrame, length = 950, mode="determinate")

        self.rcpProcessedCountLabel = tk.Label(self.runFrame,textvariable=self.processedCount , font=('TkTextFont', 14))

        self.rcpCountResultLabel = tk.Label(self.runFrame, text='N [Created/Failed]', font=('TkTextFont', 14))
        self.rcpCountResultLbl = tk.Label(self.runFrame, textvariable=self.rcpCountResult, font=('TkTextFont', 14))

        self.stopRunFrame = tk.Frame(self.runFrame)
        self.runButton = tk.Button(self.stopRunFrame, text='Create', command= lambda: main(self.rcpListPath.get(), self.rcpTemplate.get()), font=('TkTextFont', 14))
        self.stopButton = tk.Button(self.stopRunFrame, text='Stop', command= lambda: stop(), font=('TkTextFont', 14))

        self.progressLabel = tk.Label(self.runFrame,textvariable=self.progress , font=('TkTextFont', 14))


        self.progressBar.grid(row=1, column=1, padx=px, pady=10, ipady=8 , sticky=tk.W+tk.E)
        self.rcpProcessedCountLabel.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W + tk.E)
        self.progressLabel.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)


        self.rcpCountResultLabel.grid(row=2, column=0, padx=px, pady=10, sticky=tk.E)
        self.rcpCountResultLbl.grid(row=2, column=1, padx=px, ipady=ipy, ipadx = 30, sticky=tk.W)

        self.stopRunFrame.grid(row=1, column=0, sticky = tk.E+tk.W)
        self.runButton.grid(row=0, column=0, padx=px, pady = 5, sticky = tk.E)
        self.stopButton.grid(row=0, column=1, padx=px, pady=5, sticky=tk.E)

        # self.master.update()
        # windowWidth = self.master.winfo_width()
        # windowHeight = self.master.winfo_height()
        #
        # # Gets both half the screen width/height and window width/height
        # positionRight = int(self.master.winfo_screenwidth() / 2 - windowWidth / 2)
        # positionDown = int(self.master.winfo_screenheight() / 2 - windowHeight / 2)
        #
        # # Positions the window in the center of the page.
        # self.master.geometry("+%d+%d" % (positionRight, positionDown))





    def get_recipe_list_path(self):

        self.processedCount.set("0/0")
        self.rcpCountResult.set("0/0")
        self.progressBar["value"] = 0

        # self.rcpListPathEntry.insert(0, self.rcpListPath)

        previousSelection = self.rcpListPath.get()

        self.rcpListPath.set(filedialog.askopenfilename())
        self.rcpListPath.set(path_format(self.rcpListPath.get()))

        if self.rcpListPath.get() != "":
            log("User selected a recipe list:[" + self.rcpListPath.get() + "]", recipeCreatorLog)

        else:
            self.rcpListPath.set(previousSelection)

        # self.rcpListPathEntry.config(state = DISABLED)


    def get_template_path(self):

        self.processedCount.set("0/0")
        self.rcpCountResult.set("0/0")
        self.progressBar["value"] = 0

        previousSelection = self.rcpTemplate.get()
        self.rcpTemplate.set(filedialog.askdirectory())
        self.rcpTemplate.set(path_format(self.rcpTemplate.get()))

        if self.rcpTemplate.get() != "":
            log("User selected a template:[" + self.rcpTemplate.get() + "]", recipeCreatorLog)
        else:
            self.rcpTemplate.set(previousSelection)

    def tongle(self):

        self.processedCount.set("0/0")
        self.rcpCountResult.set("0/0")
        self.progressBar["value"] = 0

        if self.templateFolderChkbValue.get() == "YES":
            # global templatePath
            self.rcpTemplate.set(configTemplatePath)
            self.rcpTemplateEntry.config(state=tk.DISABLED)
            self.rcpTemplateButton.config(state=tk.DISABLED)
        else:
            self.rcpTemplateEntry.config(state=tk.NORMAL)
            self.rcpTemplateButton.config(state=tk.NORMAL)

    def checksum_creation(self):

        fileType = [('xml files', '*.xml')]
        self.fileToVerify = path_format(filedialog.askopenfilename(filetypes=fileType, defaultextension=fileType))

        if os.path.isfile(self.fileToVerify):
            log("Starting verification for:[" + self.fileToVerify + "]", recipeCreatorLog)
            if checksum_validate(self.fileToVerify) == True:
                # AlarmGui("Checksum is CORRECT!")
                messagebox.showinfo("Checksum verification", "Checksum is CORRECT!" )
                log("Checksum verification for:[" + self.fileToVerify + "] is SUCCESSFUL ", recipeCreatorLog)
            else:
                MsgBox = tk.messagebox.askquestion('Checksum verification', 'Checksum is INCORRECT! Do you want to fix?',icon='warning')
                log("Checksum verification for:[" + self.fileToVerify + "] is FAILED ", recipeCreatorLog)
                if MsgBox == 'yes':
                    log("User decided to fix the checksum for :[" + self.fileToVerify + "] ", recipeCreatorLog)
                    checksumCreationResult = checksum_creator_and_verification(self.fileToVerify)

                    if checksumCreationResult == True:
                        messagebox.showinfo("Checksum creation", "Checksum is successful created and verified!")
                        log("Checksum creation for:[" + self.fileToVerify + "] is SUCCESSFUL ", recipeCreatorLog)
                    else:
                        messagebox.showerror("Checksum creation", "Cannot fix checksum!")
                        log("Checksum creation for:[" + self.fileToVerify + "] is FAILED ", recipeCreatorLog)
                else:
                    log("User decided to NOT fix the checksum for :[" + self.fileToVerify + "] ", recipeCreatorLog)


class AlarmGui:
    def __init__(self, displayText):
        px = 10
        ipy= 6
        # Init master gui
        self.alarmMaster = tk.Toplevel()
        self.alarmMaster.grab_set()

        self.alarmMaster.title('Message')

        self.alarmMaster.resizable(0, 0)
        self.alarmMaster.columnconfigure(0, weight=1)

        self.alarmLabel = tk.Label(self.alarmMaster, text = displayText, font=('TkTextFont', 16, 'bold'))
        self.oKButton = tk.Button(self.alarmMaster, text='OK', command= self.alarmMaster.destroy, font=('TkTextFont', 14))

        self.alarmLabel.grid(row=0,column=0, pady=20, padx = 20, sticky = tk.E +tk.W + tk.S + tk.N)
        self.oKButton.grid(row=1, column=0, pady=20, padx=20, sticky = tk.N + tk.S)

        # Update drawing before calling getting width and height
        # It is important to pass displayText to alarmLabel so width and height will be updated accordingly to text
        self.alarmMaster.update()

        self.windowWidth = self.alarmMaster.winfo_width()

        self.windowHeight = self.alarmMaster.winfo_height()

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.alarmMaster.winfo_screenwidth() / 2 - self.windowWidth / 2)
        positionDown = int(self.alarmMaster.winfo_screenheight() / 2 - self.windowHeight / 2)

        # Positions the window in the center of the page.

        self.alarmMaster.geometry("+%d+%d" % (positionRight, positionDown))


class singleRecipeConvertGUI:

    def __init__(self):
        px = 10
        ipy= 5
        # Init master gui
        self.master = tk.Toplevel()
        self.master.grab_set()
        self.master.title('Single Recipe Creator')

        self.master.geometry("+200+200")
        self.master.resizable(0, 0)

        self.srcRcpPath = tk.StringVar()
        self.newRcpLocationPath = tk.StringVar()
        self.newRcpName = tk.StringVar()
        self.srcAlignRecipePath = tk.StringVar()
        self.rcpTemplatePath = tk.StringVar()
        self.specificParameterFilePath = tk.StringVar()

        self.rcpTemplateCheckbuttonValue = tk.StringVar(value = "YES")

        self.newRcpLocCheckbuttonValue = tk.StringVar(value ="YES")
        self.newRcpNameCheckbuttonValue=tk.StringVar(value ="YES")
        self.srcAlignRecipeCheckbuttonValue = tk.StringVar(value = "YES")
        self.messageLableValue = tk.StringVar(value = "")


        self.recipeTemplateLabel = tk.Label(self.master, text='Recipe Template', font=('TkTextFont', 14))
        self.recipeTemplateEntry = tk.Entry(self.master, textvariable=self.rcpTemplatePath, width=105, font=('TkTextFont', 12))
        self.recipeTemplateButton = tk.Button(self.master, text='>>>', command=self.get_template, font=('TkTextFont	', 14))
        self.recipeTemplateCheckbutton = tk.Checkbutton(self.master, text='Set as configuration',
                                                          variable=self.rcpTemplateCheckbuttonValue, onvalue="YES",
                                                          offvalue="NO", font=('TkTextFont', 14),
                                                          command=self.recipe_template_checkbutton)


        self.sourceRecipeEntry = tk.Entry(self.master, textvariable=self.srcRcpPath, width=105,font=('TkTextFont', 12))
        self.sourceRecipeLabel = tk.Label(self.master, text='Source recipe', font=('TkTextFont', 14))
        self.sourceRecipeButton = tk.Button(self.master, text='>>>', command=self.get_source_recipe_path, font=('TkTextFont	', 14))

        self.newRecipeLocationEntry = tk.Entry(self.master, textvariable=self.newRcpLocationPath, width=105,font=('TkTextFont', 12))
        self.newRecipeLocationLabel = tk.Label(self.master, text='Recipe location', font=('TkTextFont', 14))
        self.newRecipeLocationButton = tk.Button(self.master, text='>>>', command=self.get_new_recipe_location_path, font=('TkTextFont	', 14))
        self.newRcipeLocationCheckbutton  = tk.Checkbutton(self.master,  text = 'Set as source recipe', variable = self.newRcpLocCheckbuttonValue, onvalue = "YES", offvalue = "NO", font=('TkTextFont', 14), command = self.new_recipe_location_tongle)

        self.newRecipeNameEntry = tk.Entry(self.master, textvariable=self.newRcpName, width=105,font=('TkTextFont', 12))
        self.newRecipeNameLabel = tk.Label(self.master, text='Recipe name', font=('TkTextFont', 14))
        self.newRecipeNameCheckbutton  = tk.Checkbutton(self.master,  text = 'Set as source recipe', variable = self.newRcpNameCheckbuttonValue, onvalue = "YES", offvalue = "NO", font=('TkTextFont', 14), command = self.new_recipe_name_tongle)

        self.sourceAlignRecipeEntry = tk.Entry(self.master, textvariable=self.srcAlignRecipePath, width=105,font=('TkTextFont', 12))
        self.sourceAlignRecipeLabel = tk.Label(self.master, text='Source alignment recipe', font=('TkTextFont', 14))
        self.sourceAlignRecipeButton = tk.Button(self.master, text='>>>', command=self.get_source_align_recipe_location_path, font=('TkTextFont	', 14))
        self.sourceAlignRecipeCheckbutton  = tk.Checkbutton(self.master,  text = 'Set as source recipe', variable = self.srcAlignRecipeCheckbuttonValue, onvalue = "YES", offvalue = "NO", font=('TkTextFont', 14), command = self.source_align_recipe_tongle)

        self.specificParameterFileEntry = tk.Entry(self.master, textvariable=self.specificParameterFilePath, width=105,
                                               font=('TkTextFont', 12))
        self.specificParameterFileLabel = tk.Label(self.master, text='Parameter file', font=('TkTextFont', 14))
        self.specificParameterFileButton = tk.Button(self.master, text='>>>',
                                                 command=self.get_specific_parameter_file_path,
                                                 font=('TkTextFont	', 14))


        self.runFrame = tk.Frame(self.master)
        self.runButton = tk.Button(self.runFrame, text='Create',
                                   command=lambda: single_recipe_main(self.rcpTemplatePath.get(),
                                                                      self.srcRcpPath.get(),
                                                                      self.newRcpName.get(),
                                                                      self.srcAlignRecipePath.get(),
                                                                      self.specificParameterFilePath.get(),
                                                                      self.newRcpLocationPath.get()),
                                   font=('TkTextFont', 18))

        self.messageLabel = tk.Label(self.runFrame, textvariable = self.messageLableValue, font=('TkTextFont', 14, 'bold'))

        # Organize widgets

        self.recipeTemplateEntry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.recipeTemplateLabel.grid(row=0, column=0, padx=10, sticky=tk.E)
        self.recipeTemplateButton.grid(row=0, column=2, padx=10, sticky=tk.E)
        self.recipeTemplateCheckbutton.grid(row=1, column=1, padx=10, sticky=tk.E)

        self.sourceRecipeEntry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.sourceRecipeLabel.grid(row=2, column=0, padx=10, sticky=tk.E)
        self.sourceRecipeButton.grid(row=2, column=2, padx=10, sticky=tk.E)


        self.newRecipeLocationEntry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.newRecipeLocationLabel.grid(row=3, column=0, padx=10, sticky=tk.E)
        self.newRecipeLocationButton.grid(row=3, column=2, padx=10, sticky=tk.E)
        self.newRcipeLocationCheckbutton.grid(row=4, column=1, padx=10, sticky=tk.E)

        self.newRecipeNameEntry.grid(row=5, column=1, padx=10, pady=10,sticky=tk.W)
        self.newRecipeNameLabel.grid(row=5, column=0, padx=10, sticky=tk.E)
        self.newRecipeNameCheckbutton.grid(row=6, column=1, padx=10, sticky=tk.E)


        self.specificParameterFileEntry.grid(row=7, column=1, padx=10, pady=10, sticky=tk.W)
        self.specificParameterFileLabel.grid(row=7, column=0, padx=10, sticky=tk.E)
        self.specificParameterFileButton.grid(row=7, column=2, padx=10, sticky=tk.E)

        self.sourceAlignRecipeEntry.grid(row=8, column=1, padx=10, pady=10, sticky=tk.W)
        self.sourceAlignRecipeLabel.grid(row=8, column=0, padx=10, sticky=tk.E)
        self.sourceAlignRecipeButton.grid(row=8, column=2, padx=10, sticky=tk.E)
        self.sourceAlignRecipeCheckbutton.grid(row=9, column=1, padx=10, sticky=tk.E)

        self.runFrame.grid(row=10, column=1, sticky=tk.E)
        self.messageLabel.grid(row=0, column=0, padx=10, sticky=tk.W)
        self.runButton.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

        # self.master.update()
        # windowWidth = self.master.winfo_width()
        # windowHeight = self.master.winfo_height()
        #
        # # Gets both half the screen width/height and window width/height
        # positionRight = int(self.master.winfo_screenwidth() / 2 - windowWidth / 2)
        # positionDown = int(self.master.winfo_screenheight() / 2 - windowHeight / 2)
        #
        # # Positions the window in the center of the page.
        # self.master.geometry("+%d+%d" % (positionRight, positionDown))

    #     Initiation
        self.recipeTemplateButton.config(state = tk.DISABLED)
        self.recipeTemplateEntry.config(state = tk.DISABLED)
        self.newRecipeLocationEntry.config(state =tk.DISABLED)
        self.newRecipeNameEntry.config(state=tk.DISABLED)
        self.sourceAlignRecipeEntry.config(state =tk.DISABLED)
        self.sourceAlignRecipeButton.config(state = tk.DISABLED)
        


    def get_template(self):

        previousSelection = self.rcpTemplatePath.get()

        self.rcpTemplatePath.set(filedialog.askdirectory())
        self.rcpTemplatePath.set(path_format(self.rcpTemplatePath.get()))
        if self.rcpTemplatePath.get() !="":
            log("User selected a recipe template:[" + self.rcpTemplatePath.get() + "]", recipeCreatorLog)
        else:
            self.rcpTemplatePath.set(previousSelection)


    def recipe_template_checkbutton(self):
        if self.rcpTemplateCheckbuttonValue.get() == "YES":

            self.rcpTemplatePath.set(configTemplatePath)
            self.recipeTemplateEntry.config(state = tk.DISABLED)
            self.recipeTemplateButton.config(state = tk.DISABLED)

        else:
            self.recipeTemplateEntry.config(state=tk.NORMAL)
            self.recipeTemplateButton.config(state=tk.NORMAL)

    def get_source_recipe_path(self):

        previousSelection = self.srcRcpPath.get()

        # self.rcpListPathEntry.insert(0, self.rcpListPath)
        self.srcRcpPath.set(filedialog.askdirectory())
        self.srcRcpPath.set(path_format(self.srcRcpPath.get()))

        if self.srcRcpPath.get() != "":

            # Populate new name with the source one
            self.newRcpName.set(os.path.basename(self.srcRcpPath.get()))
            self.newRecipeNameEntry.config(state=tk.DISABLED)
            self.newRecipeNameCheckbutton.select()

            self.newRcpLocationPath.set(self.srcRcpPath.get().replace(os.path.basename(self.srcRcpPath.get()),"")[:-1])
            self.newRecipeLocationEntry.config(state = tk.DISABLED)
            self.newRcpLocCheckbuttonValue.set("YES")
            # Can use below way
            # self.newRcipeLocationCheckbutton.select()

            self.newRecipeLocationButton.config(state = tk.DISABLED)
            self.sourceAlignRecipeButton.config(state = tk.DISABLED)

            log("User selected a source recipe:[" + self.srcRcpPath.get() + "]", recipeCreatorLog)
        else:
            self.srcRcpPath.set(previousSelection)



    def get_new_recipe_location_path(self):

        previousSelection = self.newRcpLocationPath.get()

        self.newRcpLocationPath.set(filedialog.askdirectory())
        self.newRcpLocationPath.set(path_format(self.newRcpLocationPath.get()))
        if self.newRcpLocationPath.get() !="":

            log("User selected a new recipe location:[" + self.newRcpLocationPath.get() + "]", recipeCreatorLog)
        else:
            self.newRcpLocationPath.set(previousSelection)



    def get_source_align_recipe_location_path(self):

        previousSelection = self.srcAlignRecipePath.get()

        self.srcAlignRecipePath.set(filedialog.askdirectory())
        self.srcAlignRecipePath.set(path_format(self.srcAlignRecipePath.get()))

        if self.srcAlignRecipePath.get() !="":

            log("User selected a source alignment recipe:[" + self.srcAlignRecipePath.get() + "]", recipeCreatorLog)
        else:
            self.srcAlignRecipePath.set(previousSelection)

    def get_specific_parameter_file_path(self):

        previousSelection = self.specificParameterFilePath.get()

        self.specificParameterFilePath.set(filedialog.askopenfilename())
        self.specificParameterFilePath.set(path_format(self.specificParameterFilePath.get()))

        if self.specificParameterFilePath.get() !="":
            log("User selected a specific parameter file:[" + self.specificParameterFilePath.get() + "]", recipeCreatorLog)
        else:
            self.specificParameterFilePath.set(previousSelection)

    def new_recipe_location_tongle(self):

        if self.newRcpLocCheckbuttonValue.get() == "YES":
            self.newRcpLocationPath.set(self.srcRcpPath.get().replace(os.path.basename(self.srcRcpPath.get()),"")[:-1])
            self.newRecipeLocationEntry.config(state = tk.DISABLED)
            self.newRecipeLocationButton.config(state = tk.DISABLED)

        else:
            self.newRecipeLocationEntry.config(state=tk.NORMAL)
            self.newRecipeLocationButton.config(state=tk.NORMAL)



    def new_recipe_name_tongle(self):

        if self.newRcpNameCheckbuttonValue.get() == "YES":
            # global templatePath

            self.newRcpName.set(os.path.basename(self.srcRcpPath.get()))
            self.newRecipeNameEntry.config(state=tk.DISABLED)
        else:
            self.newRecipeNameEntry.config(state=tk.NORMAL)


    def source_align_recipe_tongle(self):

        if self.srcAlignRecipeCheckbuttonValue.get() == "YES":

            self.srcAlignRecipePath.set("")
            self.sourceAlignRecipeEntry.config(state=tk.DISABLED)
            self.sourceAlignRecipeButton.config(state=tk.DISABLED)

        else:
            self.sourceAlignRecipeEntry.config(state=tk.NORMAL)
            self.sourceAlignRecipeButton.config(state=tk.NORMAL)


class NPIRecipeConvertGUI:

    def __init__(self):
        px = 10
        ipy = 5
        # Init master gui
        self.master = tk.Toplevel()
        self.master.grab_set()
        self.master.title('NPI Recipe Creator')

        self.master.geometry("+200+200")
        self.master.resizable(1, 1)

        self.srcRcpPath = tk.StringVar()
        self.newRcpLocationPath = tk.StringVar()
        self.newRcpName = tk.StringVar()
        # self.srcAlignRecipePath = tk.StringVar()
        self.rcpTemplatePath = tk.StringVar()
        self.specificParameterFilePath = tk.StringVar()

        self.rcpTemplateCheckbuttonValue = tk.StringVar(value="YES")

        self.newRcpLocCheckbuttonValue = tk.StringVar(value="YES")
        self.newRcpNameCheckbuttonValue = tk.StringVar(value="YES")
        # self.srcAlignRecipeCheckbuttonValue = tk.StringVar(value="YES")
        self.goldenFileSelectionDefaultCheckbuttonValue = tk.StringVar(value="YES")

        self.messageLableValue = tk.StringVar(value="")

        self.goldenFileList = []



        # Create labels, buttons, lists ...
        self.recipeTemplateLabel = tk.Label(self.master, text='Recipe Template', font=('TkTextFont', 14))
        self.recipeTemplateEntry = tk.Entry(self.master, textvariable=self.rcpTemplatePath, width=105,
                                            font=('TkTextFont', 12))
        self.recipeTemplateButton = tk.Button(self.master, text='>>>', command=self.get_template,
                                              font=('TkTextFont	', 14))
        self.recipeTemplateCheckbutton = tk.Checkbutton(self.master, text='Set as configuration',
                                                        variable=self.rcpTemplateCheckbuttonValue, onvalue="YES",
                                                        offvalue="NO", font=('TkTextFont', 14),
                                                        command=self.recipe_template_checkbutton)

        self.sourceRecipeEntry = tk.Entry(self.master, textvariable=self.srcRcpPath, width=105, font=('TkTextFont', 12))
        self.sourceRecipeLabel = tk.Label(self.master, text='Source recipe', font=('TkTextFont', 14))
        self.sourceRecipeButton = tk.Button(self.master, text='>>>', command=self.get_source_recipe_path,
                                            font=('TkTextFont	', 14))

        self.newRecipeLocationEntry = tk.Entry(self.master, textvariable=self.newRcpLocationPath, width=105,
                                               font=('TkTextFont', 12))
        self.newRecipeLocationLabel = tk.Label(self.master, text='Recipe location', font=('TkTextFont', 14))
        self.newRecipeLocationButton = tk.Button(self.master, text='>>>', command=self.get_new_recipe_location_path,
                                                 font=('TkTextFont	', 14))
        self.newRcipeLocationCheckbutton = tk.Checkbutton(self.master, text='Set as source recipe',
                                                          variable=self.newRcpLocCheckbuttonValue, onvalue="YES",
                                                          offvalue="NO", font=('TkTextFont', 14),
                                                          command=self.new_recipe_location_tongle)

        self.newRecipeNameEntry = tk.Entry(self.master, textvariable=self.newRcpName, width=105,
                                           font=('TkTextFont', 12))
        self.newRecipeNameLabel = tk.Label(self.master, text='Recipe name', font=('TkTextFont', 14))
        self.newRecipeNameCheckbutton = tk.Checkbutton(self.master, text='Set as source recipe',
                                                       variable=self.newRcpNameCheckbuttonValue, onvalue="YES",
                                                       offvalue="NO", font=('TkTextFont', 14),
                                                       command=self.new_recipe_name_tongle)



        self.specificParameterFileEntry = tk.Entry(self.master, textvariable=self.specificParameterFilePath, width=105,
                                                   font=('TkTextFont', 12))
        self.specificParameterFileLabel = tk.Label(self.master, text='Parameter file', font=('TkTextFont', 14))
        self.specificParameterFileButton = tk.Button(self.master, text='>>>',
                                                     command=self.get_specific_parameter_file_path,
                                                     font=('TkTextFont	', 14))

        self.runFrame = tk.Frame(self.master)
        self.runButton = tk.Button(self.runFrame, text='Create',
                                   command=lambda: NPI_recipe_main(self.rcpTemplatePath.get(),
                                                                      self.srcRcpPath.get(),
                                                                      self.newRcpName.get(),
                                                                      # self.srcAlignRecipePath.get(),
                                                                      self.specificParameterFilePath.get(),
                                                                      self.goldenFileList,
                                                                      self.newRcpLocationPath.get()),
                                   font=('TkTextFont', 18))

        self.messageLabel = tk.Label(self.runFrame, textvariable=self.messageLableValue,
                                     font=('TkTextFont', 14, 'bold'))


        # Add golden file list and selected golden file list and buttons

        self.goldenFileSelectionFrame = tk.LabelFrame(self.master, text="", fg="Blue",
                                                    font=('TkTextFont', 12))
        self.goldenFileListboxFrame = tk.LabelFrame(self.goldenFileSelectionFrame, text="Golden Files", fg="Blue",
                                                      font=('TkTextFont', 12))
        self.goldenFileScrollbar = tk.Scrollbar(self.goldenFileListboxFrame)
        self.goldenFileListbox = tk.Listbox(self.goldenFileListboxFrame, width=51, height=10,
                                              font=('TkTextFont', 10), yscrollcommand=self.goldenFileScrollbar.set,
                                              activestyle='dotbox',selectmode=EXTENDED)

        self.selectedGoldenFileListboxFrame = tk.LabelFrame(self.goldenFileSelectionFrame, text="Selected Golden Files", fg="Blue",
                                                   font=('TkTextFont', 12))
        self.selectedGoldenFileScrollbar = tk.Scrollbar(self.selectedGoldenFileListboxFrame)
        self.selectedGoldenFileListbox = tk.Listbox(self.selectedGoldenFileListboxFrame, width=51, height=10,
                                            font=('TkTextFont', 10), yscrollcommand=self.selectedGoldenFileScrollbar.set,
                                            activestyle='dotbox',selectmode=EXTENDED)

        self.goldenFileButtonFrame = tk.LabelFrame(self.goldenFileSelectionFrame, text="Action", fg="Blue",
                                                    font=('TkTextFont', 12))
        self.goldenFileAddButton = tk.Button(self.goldenFileButtonFrame, text='Add',
                                                 command=self.add_golden_files,
                                                 font=('TkTextFont	', 14))

        self.goldenFileRemoveButton = tk.Button(self.goldenFileButtonFrame, text='Remove',
                                                 command=self.remove_golden_files,
                                                 font=('TkTextFont	', 14))
        self.goldenFileSelectionDefaultCheckbutton = tk.Checkbutton(self.goldenFileButtonFrame, text='Default',
                                                        variable=self.goldenFileSelectionDefaultCheckbuttonValue, onvalue="YES",
                                                        offvalue="NO", font=('TkTextFont', 14),
                                                        command=self.golden_File_Selection_Default_Checkbutton)

        # Organize widgets

        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(8, weight=1)



        self.recipeTemplateEntry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
        self.recipeTemplateLabel.grid(row=0, column=0, padx=10, sticky=tk.E)
        self.recipeTemplateButton.grid(row=0, column=2, padx=10, sticky=tk.E)
        self.recipeTemplateCheckbutton.grid(row=1, column=1, padx=10, sticky=tk.E)



        self.sourceRecipeEntry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
        self.sourceRecipeLabel.grid(row=2, column=0, padx=10, sticky=tk.E)
        self.sourceRecipeButton.grid(row=2, column=2, padx=10, sticky=tk.E)

        self.newRecipeLocationEntry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
        self.newRecipeLocationLabel.grid(row=3, column=0, padx=10, sticky=tk.E)
        self.newRecipeLocationButton.grid(row=3, column=2, padx=10, sticky=tk.E)
        self.newRcipeLocationCheckbutton.grid(row=4, column=1, padx=10, sticky=tk.E)

        self.newRecipeNameEntry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
        self.newRecipeNameLabel.grid(row=5, column=0, padx=10, sticky=tk.E)
        self.newRecipeNameCheckbutton.grid(row=6, column=1, padx=10, sticky=tk.E)

        self.specificParameterFileEntry.grid(row=7, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
        self.specificParameterFileLabel.grid(row=7, column=0, padx=10, sticky=tk.E)
        self.specificParameterFileButton.grid(row=7, column=2, padx=10, sticky=tk.E)



        self.goldenFileSelectionFrame.grid(row=8, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        self.goldenFileSelectionFrame.columnconfigure(0, weight=1)
        self.goldenFileSelectionFrame.columnconfigure(2, weight=1)
        self.goldenFileSelectionFrame.rowconfigure(0, weight=1)


        self.goldenFileListboxFrame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.goldenFileScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileScrollbar.config(command=self.goldenFileListbox.yview)

        self.goldenFileListboxFrame.columnconfigure(0, weight = 1)
        self.goldenFileListboxFrame.rowconfigure(0, weight=1)


        self.goldenFileButtonFrame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileSelectionDefaultCheckbutton.grid(row=0, column=0, padx=10, sticky=tk.E)
        self.goldenFileAddButton.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.goldenFileRemoveButton.grid(row=2, column=0, padx=10,pady =10, sticky=tk.E)


        self.selectedGoldenFileListboxFrame.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedGoldenFileListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.selectedGoldenFileScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedGoldenFileScrollbar.config(command=self.selectedGoldenFileListbox.yview)

        self.selectedGoldenFileListboxFrame.columnconfigure(0, weight=1)
        self.selectedGoldenFileListboxFrame.rowconfigure(0, weight=1)





        self.runFrame.grid(row=10, column=1, sticky=tk.E)
        self.messageLabel.grid(row=0, column=0, padx=10, sticky=tk.W)
        self.runButton.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)



        #     Initiation
        self.recipeTemplateButton.config(state=tk.DISABLED)
        self.recipeTemplateEntry.config(state=tk.DISABLED)
        self.newRecipeLocationEntry.config(state=tk.DISABLED)
        self.newRecipeNameEntry.config(state=tk.DISABLED)


        # The listbox needs to be ENABLE to add a item
        self.display_default_golden_file_to_golden_file_listbox()
        self.goldenFileAddButton.config(state=tk.DISABLED)
        self.goldenFileRemoveButton.config(state=tk.DISABLED)

        self.goldenFileListbox.config(state =tk.DISABLED)
        self.selectedGoldenFileListbox.config(state=tk.DISABLED)



    def get_template(self):

        previousSelection = self.rcpTemplatePath.get()

        self.rcpTemplatePath.set(filedialog.askdirectory())
        self.rcpTemplatePath.set(path_format(self.rcpTemplatePath.get()))
        if self.rcpTemplatePath.get() != "":
            log("User selected a recipe template:[" + self.rcpTemplatePath.get() + "]", recipeCreatorLog)
        else:
            self.rcpTemplatePath.set(previousSelection)

    def recipe_template_checkbutton(self):
        if self.rcpTemplateCheckbuttonValue.get() == "YES":

            self.rcpTemplatePath.set(configTemplatePath)
            self.recipeTemplateEntry.config(state=tk.DISABLED)
            self.recipeTemplateButton.config(state=tk.DISABLED)

        else:
            self.recipeTemplateEntry.config(state=tk.NORMAL)
            self.recipeTemplateButton.config(state=tk.NORMAL)

    def get_source_recipe_path(self):

        previousSelection = self.srcRcpPath.get()


        # self.rcpListPathEntry.insert(0, self.rcpListPath)
        self.srcRcpPath.set(filedialog.askdirectory())
        self.srcRcpPath.set(path_format(self.srcRcpPath.get()))

        if self.srcRcpPath.get() != "":

            # Populate new name with the source one
            self.newRcpName.set(os.path.basename(self.srcRcpPath.get()))
            self.newRecipeNameEntry.config(state=tk.DISABLED)
            self.newRecipeNameCheckbutton.select()

            self.newRcpLocationPath.set(self.srcRcpPath.get().replace(os.path.basename(self.srcRcpPath.get()), "")[:-1])
            self.newRecipeLocationEntry.config(state=tk.DISABLED)
            self.newRcpLocCheckbuttonValue.set("YES")
            # Can use below way
            # self.newRcipeLocationCheckbutton.select()

            self.newRecipeLocationButton.config(state=tk.DISABLED)
            # self.sourceAlignRecipeButton.config(state=tk.DISABLED)

            log("User selected a source recipe:[" + self.srcRcpPath.get() + "]", recipeCreatorLog)
        else:
            self.srcRcpPath.set(previousSelection)

    def get_new_recipe_location_path(self):

        previousSelection = self.newRcpLocationPath.get()

        self.newRcpLocationPath.set(filedialog.askdirectory())
        self.newRcpLocationPath.set(path_format(self.newRcpLocationPath.get()))
        if self.newRcpLocationPath.get() != "":

            log("User selected a new recipe location:[" + self.newRcpLocationPath.get() + "]", recipeCreatorLog)
        else:
            self.newRcpLocationPath.set(previousSelection)



    def get_specific_parameter_file_path(self):

        previousSelection = self.specificParameterFilePath.get()

        self.specificParameterFilePath.set(filedialog.askopenfilename())
        self.specificParameterFilePath.set(path_format(self.specificParameterFilePath.get()))

        if self.specificParameterFilePath.get() != "":
            log("User selected a specific parameter file:[" + self.specificParameterFilePath.get() + "]",
                recipeCreatorLog)
        else:
            self.specificParameterFilePath.set(previousSelection)

    def new_recipe_location_tongle(self):

        if self.newRcpLocCheckbuttonValue.get() == "YES":
            self.newRcpLocationPath.set(self.srcRcpPath.get().replace(os.path.basename(self.srcRcpPath.get()), "")[:-1])
            self.newRecipeLocationEntry.config(state=tk.DISABLED)
            self.newRecipeLocationButton.config(state=tk.DISABLED)

        else:
            self.newRecipeLocationEntry.config(state=tk.NORMAL)
            self.newRecipeLocationButton.config(state=tk.NORMAL)

    def new_recipe_name_tongle(self):

        if self.newRcpNameCheckbuttonValue.get() == "YES":
            # global templatePath

            self.newRcpName.set(os.path.basename(self.srcRcpPath.get()))
            self.newRecipeNameEntry.config(state=tk.DISABLED)
        else:
            self.newRecipeNameEntry.config(state=tk.NORMAL)


    def display_default_golden_file_to_golden_file_listbox(self):
        # clear the list box
        self.goldenFileListbox.delete(0, self.goldenFileListbox.size())
        self.selectedGoldenFileListbox.delete(0, self.selectedGoldenFileListbox.size())
        # Check if the list is empty
        if DefaultGoldenFileList:

            for file in DefaultGoldenFileList:
                if HCGoldenFilePath:
                    filePath = os.path.join(HCGoldenFilePath, file)
                    self.goldenFileListbox.insert(END, file)
                    self.selectedGoldenFileListbox.insert(END, file)

                    self.goldenFileList.append(filePath)



    def display_golden_file_to_golden_file_listbox(self):
        try:

            # clear the list box
            self.goldenFileListbox.delete(0, self.goldenFileListbox.size())
            self.selectedGoldenFileListbox.delete(0, self.selectedGoldenFileListbox.size())
            # Check if the list is empty
            if HCGoldenFilePath:
                for file in os.listdir(HCGoldenFilePath):
                    self.goldenFileListbox.insert(END, file)
        except Exception as error:
            AlarmGui(str(error))
            no_time_log(str(error),recipeCreatorLog)

    def add_golden_files(self):
        for goldenFileIndex in self.goldenFileListbox.curselection():

            if HCGoldenFilePath:
                filePath = os.path.join(HCGoldenFilePath, self.goldenFileListbox.get(goldenFileIndex))
                # Check if the file has been added to the selected golden file list box
                if filePath not in self.goldenFileList:
                    self.selectedGoldenFileListbox.insert(END, self.goldenFileListbox.get(goldenFileIndex))
                    # Add the selected golden file path to goldenFileList
                    self.goldenFileList.append(filePath)


    def remove_golden_files(self):
        for goldenFileIndex in self.selectedGoldenFileListbox.curselection()[::-1]:
            self.selectedGoldenFileListbox.delete(goldenFileIndex)
            self.goldenFileList.pop(goldenFileIndex)


    def golden_File_Selection_Default_Checkbutton(self):
        
        if self.goldenFileSelectionDefaultCheckbuttonValue.get() == "YES":

            self.display_default_golden_file_to_golden_file_listbox()

            self.goldenFileAddButton.config(state=tk.DISABLED)
            self.goldenFileRemoveButton.config(state=tk.DISABLED)

            self.goldenFileListbox.config(state=tk.DISABLED)
            self.selectedGoldenFileListbox.config(state=tk.DISABLED)



        else:
            self.goldenFileAddButton.config(state=tk.NORMAL)
            self.goldenFileRemoveButton.config(state=tk.NORMAL)

            self.goldenFileListbox.config(state=tk.NORMAL)
            self.selectedGoldenFileListbox.config(state=tk.NORMAL)
            self.display_golden_file_to_golden_file_listbox()
            self.goldenFileList = []


class recipeListCreationGui:

    def __init__(self):
        px = 10
        ipy= 5
        # Init master gui
        self.master = tk.Toplevel()
        self.master.grab_set()
        self.master.title('Recipe List Creator')


        self.master.geometry("+0+200")
        self.master.resizable(1, 1)

        self.sourceRecipeLocation = tk.StringVar()
        self.selectionModeText = tk.StringVar(value = "Drag")

        self.newNameSearchTextEntryVar = tk.StringVar()
        self.newNameReplaceTextEntryVar = tk.StringVar()
        self.selectedRecipeCountVar = tk.StringVar(value = "0")

        self.selectedRecipeCount = 0
        self.selectedRecipeList =[]
        self.sourceAlignmentRecipeList =[]
        self.newRecipeLocationList = []
        self.newRecipeNameList = []
        self.specificParameterUpdateFileList = []

        self.recipeListDict = {'SourceRecipe': self.selectedRecipeList,
                               'SourceAlignmentRecipe': self.sourceAlignmentRecipeList,
                               'NewRecipeLocation': self.newRecipeLocationList,
                               'NewRecipeName': self.newRecipeNameList,
                               'SpecificParameterUpdateFile': self.specificParameterUpdateFileList}

        # Source recipe frame
        self.soureRecipeLocationFrame = tk.LabelFrame(self.master, text = "Source recipe network folder", fg = "Blue", font=('TkTextFont', 12))
        self.sourceRecipeLocationEntry = tk.Entry(self.soureRecipeLocationFrame, textvariable=self.sourceRecipeLocation, width=60, font=('TkTextFont', 9))
        self.sourceRecipeLocationButton = tk.Button(self.soureRecipeLocationFrame, text='>>>', command=self.get_source_recipe_location, font=('TkTextFont	', 12))


        self.sourceRecipeListboxFrame = tk.LabelFrame(self.master, text = "Source recipe", fg = "Blue", font=('TkTextFont', 12))
        self.sourceRecipeScrollbar = tk.Scrollbar(self.sourceRecipeListboxFrame)
        self.sourceRecipeListbox = tk.Listbox(self.sourceRecipeListboxFrame, width = 70, height = 30, font =('TkTextFont',10),yscrollcommand = self.sourceRecipeScrollbar.set, activestyle='dotbox')

        # Functional button frame
        self.selectionButtonFrame = tk.LabelFrame(self.master, text = 'Action', fg = 'Blue', font=('TkTextFont', 12))
        self.addButton = tk.Button(self.selectionButtonFrame, text='Add', command=self.add_to_recipe_list, font=('TkTextFont	', 12))
        self.removeButton = tk.Button(self.selectionButtonFrame, text='Remove', command=self.remove_from_recipe_list, font=('TkTextFont	', 12))
        self.exportButton = tk.Button(self.selectionButtonFrame, text='Export', command=self.export_to_csv, font=('TkTextFont	', 12))

        self.selectionModeFrame = tk.LabelFrame(self.master, text="Select mode", fg="Blue", font=('TkTextFont', 12))
        self.selectionModeToggleButton = tk.Button(self.selectionModeFrame, textvariable = self.selectionModeText, command=self.selection_mode_toggle, font=('TkTextFont	', 12))

        # Selected recipe frame

        self.selectedRecipeCountFrame = tk.LabelFrame(self.master, text = "Selected recipe count", fg = "Blue", font=('TkTextFont', 12))
        self.selectedRecipeCountEntry = tk.Entry(self.selectedRecipeCountFrame, textvariable=self.selectedRecipeCountVar, width=10, font=('TkTextFont', 12))

        self.selectedRecipeLocationFrame = tk.LabelFrame(self.master, text = "Selected recipe", fg = "Blue", font=('TkTextFont', 12))

        self.selectedRecipeScrollbar = tk.Scrollbar(self.selectedRecipeLocationFrame)
        self.selectedRecipeListbox = tk.Listbox(self.selectedRecipeLocationFrame, width = 70, height =30, font =('TkTextFont',10),yscrollcommand = self.selectedRecipeScrollbar.set, activestyle='dotbox')

        # naming recipe frame

        self.newNameRecipeFrame = tk.LabelFrame(self.master, text = "New recipe name", fg = "Blue", font=('TkTextFont', 12))

        self.newNameRecipeScrollbar = tk.Scrollbar(self.newNameRecipeFrame)
        self.newNameRecipeListbox = tk.Listbox(self.newNameRecipeFrame, width = 70, height =30, font =('TkTextFont',10),yscrollcommand = self.newNameRecipeScrollbar.set, activestyle='dotbox')

        self.newNameRecipeReplaceResetFrame = tk.Frame(self.master)
        self.newNameReplaceFrame = tk.LabelFrame(self.newNameRecipeReplaceResetFrame,text = "Recipe name change - RegEx", fg = "Blue", font=('TkTextFont', 12))
        self.replaceButton = tk.Button(self.newNameReplaceFrame, text='Replace by', command=self.new_name_replace, font=('TkTextFont	', 12))
        self.newNameSearchTextEntry = tk.Entry(self.newNameReplaceFrame, text ='Search', textvariable=self.newNameSearchTextEntryVar, width=25, font=('TkTextFont', 12))
        self.newNameReplaceTextEntry = tk.Entry(self.newNameReplaceFrame, textvariable=self.newNameReplaceTextEntryVar, width=25, font=('TkTextFont', 12))

        self.newNameRecipeResetFrame = tk.Frame(self.newNameRecipeReplaceResetFrame)
        self.newNameResetButton = tk.Button(self.newNameRecipeResetFrame, text='Reset', command=self.new_name_reset, font=('TkTextFont	', 12))




        # Layout the GUI


        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(1, weight=1)

        # Source recipe frame
        self.soureRecipeLocationFrame.grid(row=0, column=0, padx=10, ipady=5, sticky=tk.W + tk.E +tk.N)
        self.sourceRecipeLocationEntry.grid(row=0, column=0, padx=10, pady=5, ipady=2, sticky=tk.W + tk.E + tk.N + tk.S)
        self.sourceRecipeLocationButton.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E)


        # self.soureRecipeLocationFrame.rowconfigure(0, weight=1)
        self.soureRecipeLocationFrame.columnconfigure(0, weight=1)
        self.sourceRecipeLocationEntry.columnconfigure(0, weight=1)

        self.sourceRecipeListboxFrame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E+tk.N+tk.S)
        self.sourceRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W +tk.N + tk.S)

        self.sourceRecipeScrollbar.grid(row=0, column=1, sticky = tk.W+ tk.E + tk.N + tk.S)
        self.sourceRecipeScrollbar.config(command=self.sourceRecipeListbox.yview)


        self.sourceRecipeListboxFrame.rowconfigure(0, weight=1)
        self.sourceRecipeListboxFrame.columnconfigure(0, weight=1)
        self.sourceRecipeLocationEntry.columnconfigure(0,weight=1)

        # Button frames
        self.selectionButtonFrame.columnconfigure(0,weight =1)
        self.selectionModeFrame.columnconfigure(0, weight=1)
        self.selectionButtonFrame.grid(row =1, column = 1, padx=0, pady=10, sticky=tk.W + tk.E + tk.N)
        self.selectionModeFrame.grid(row=1, column=1, padx = 0, pady=10, sticky = tk.W + tk.E + tk.S )


        self.addButton.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.removeButton.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.exportButton.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        self.selectionModeToggleButton.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        # select recipe Frame

        self.selectedRecipeCountFrame.grid(row =0, column = 2, padx=10, ipady = 5,sticky=tk.W + tk.N)
        self.selectedRecipeCountEntry.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.selectedRecipeLocationFrame.grid(row =1, column = 2, padx=10, pady=10, sticky=tk.W + tk.E+tk.N+tk.S)
        self.selectedRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.selectedRecipeScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedRecipeScrollbar.config(command=self.selectedRecipeListbox.yview)

        self.selectedRecipeLocationFrame.rowconfigure(0, weight=1)
        self.selectedRecipeLocationFrame.columnconfigure(0, weight=1)


        # new name recipe Frame

        self.newNameRecipeReplaceResetFrame.grid(row=0, column=3, padx=10,ipady = 0, sticky=tk.W + tk.N)
        self.newNameReplaceFrame.grid(row=0, column=0, padx=10, pady=5, ipady = 0, sticky=tk.W + tk.S + tk.N)
        self.newNameSearchTextEntry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W + tk.E)
        self.replaceButton.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W + tk.E)
        self.newNameReplaceTextEntry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W + tk.E)

        self.newNameRecipeResetFrame.grid(row=0, column=1, padx=10, pady=5, ipady = 0, sticky=tk.E + tk.S)
        self.newNameResetButton.grid(row=0,column=0, padx=10, pady=5, sticky=tk.W + tk.E + tk.S)

        self.newNameRecipeFrame.grid(row=1, column=3, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.newNameRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.newNameRecipeScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.newNameRecipeScrollbar.config(command=self.newNameRecipeListbox.yview)

        self.newNameRecipeFrame.rowconfigure(0, weight=1)
        self.newNameRecipeFrame.columnconfigure(0, weight=1)


        self.sourceRecipeListbox.config(selectmode=EXTENDED)
        self.selectedRecipeListbox.config(selectmode=EXTENDED)
        self.newNameRecipeListbox.config(selectmode=EXTENDED)

        # self.master.update()
        #
        # windowWidth = self.master.winfo_width()
        # windowHeight = self.master.winfo_height()
        #
        # # Gets both half the screen width/height and window width/height
        # positionRight = int(self.master.winfo_screenwidth() / 2 - windowWidth / 2)
        # positionDown = int(self.master.winfo_screenheight() / 2 - windowHeight / 2)
        #
        # # Positions the window in the center of the page.
        # self.master.geometry("+%d+%d" % (positionRight, positionDown))

    #

    #     Keyboard binding

        self.sourceRecipeLocationEntry.bind('<Return>',self.source_recipe_location_enter)
        self.newNameRecipeListbox.bind('<Control-c>', self.listbox_copy)

    # Class functions

    def listbox_copy(self,event):
        self.master.clipboard_clear()
        for recipeIndex in self.newNameRecipeListbox.curselection():
            self.master.clipboard_append(self.newNameRecipeListbox.get(recipeIndex))

    
    def source_recipe_location_enter(self, event):

        try:

            if self.sourceRecipeLocation.get() != "":
                log("User selected a source recipe location:[" + self.sourceRecipeLocation.get() + "]", recipeCreatorLog)

                # clear the list box
                self.sourceRecipeListbox.delete(0, self.sourceRecipeListbox.size())
                for dir in os.listdir(self.sourceRecipeLocation.get()):
                    # if os.path.isdir(dir):
                    self.sourceRecipeListbox.insert(END, dir)
        except Exception as error:
            AlarmGui(str(error))
            no_time_log(str(error),recipeCreatorLog)


    def new_name_replace(self):
        if self.newNameSearchTextEntryVar.get()!="":
            for recipeIndex in self.newNameRecipeListbox.curselection():
                newName = re.sub(self.newNameSearchTextEntryVar.get(), self.newNameReplaceTextEntryVar.get(), self.newNameRecipeListbox.get(recipeIndex))
                self.newNameRecipeListbox.delete(recipeIndex)
                self.newNameRecipeListbox.insert(recipeIndex,newName)

                self.newRecipeNameList.pop(recipeIndex)
                self.newRecipeNameList.insert(recipeIndex, newName)

    def new_name_reset(self):
        for recipeIndex in self.newNameRecipeListbox.curselection():
            self.newNameRecipeListbox.delete(recipeIndex)
            self.newNameRecipeListbox.insert(recipeIndex,self.selectedRecipeListbox.get(recipeIndex))

            self.newRecipeNameList.pop(recipeIndex)
            self.newRecipeNameList.insert(recipeIndex, self.selectedRecipeListbox.get(recipeIndex))

    def add_to_recipe_list(self):
        for recipeIndex in self.sourceRecipeListbox.curselection():
            self.selectedRecipeListbox.insert(END, self.sourceRecipeListbox.get(recipeIndex))
            self.newNameRecipeListbox.insert(END, self.sourceRecipeListbox.get(recipeIndex))

            # Add selected recipe to self.selectedRecipeList
            self.selectedRecipeList.append(os.path.join(self.sourceRecipeLocation.get(), self.sourceRecipeListbox.get(recipeIndex)) )

            # Add new location to self.newRecipeLocationList
            self.newRecipeLocationList.append(self.sourceRecipeLocation.get())

            # Add to self.newRecipeNameList
            self.newRecipeNameList.append(self.sourceRecipeListbox.get(recipeIndex))

            # Add to self.specificParameterUpdateFileList
            self.specificParameterUpdateFileList.append("")

            # Add to self.sourceAlignmentRecipeList
            self.sourceAlignmentRecipeList.append("")

            # Update selected recipe count
            self.selectedRecipeCount = self.selectedRecipeCount + 1
            self.selectedRecipeCountVar.set(str(self.selectedRecipeCount))


    def remove_from_recipe_list(self):
        for recipeIndex in self.selectedRecipeListbox.curselection()[::-1]:

            self.selectedRecipeListbox.delete(recipeIndex)
            self.newNameRecipeListbox.delete(recipeIndex)

            # Remove selected recipe to self.selectedRecipeList
            self.selectedRecipeList.pop(recipeIndex)

            # Remove new location to self.newRecipeLocationList
            self.newRecipeLocationList.pop(recipeIndex)

            # Remove to self.newRecipeNameList
            self.newRecipeNameList.pop(recipeIndex)

            # Remove to self.specificParameterUpdateFileList
            self.specificParameterUpdateFileList.pop(recipeIndex)

            # Remove to self.sourceAlignmentRecipeList
            self.sourceAlignmentRecipeList.pop(recipeIndex)

            # Update selected recipe count
            self.selectedRecipeCount = self.selectedRecipeCount - 1
            self.selectedRecipeCountVar.set(str(self.selectedRecipeCount))

    def selection_mode_toggle(self):
        if self.selectionModeText.get() == "Drag":
            self.sourceRecipeListbox.config(selectmode=MULTIPLE)
            self.selectionModeText.set("Multi")
        else:
            self.sourceRecipeListbox.config(selectmode=EXTENDED)
            self.selectionModeText.set("Drag")

    def export_to_csv(self):

        try:

            fileType = [('csv files', '*.csv')]
            selectedRecipeCsvFile = filedialog.asksaveasfile(filetypes=fileType, defaultextension=fileType)

            if selectedRecipeCsvFile is not None:

                log("Exporting the selected recipe list to: [" + selectedRecipeCsvFile.name +"]", recipeCreatorLog)

                df = pd.DataFrame(self.recipeListDict)
                df.to_csv(selectedRecipeCsvFile.name, index = False)
                df.to_csv(recipeCreatorLog, sep='\t',mode = 'a')

                log("Exporting the selected recipe list to: [" + selectedRecipeCsvFile.name + "] - [COMPLETED]", recipeCreatorLog)
                AlarmGui("The recipe list has been sucesssfully created!")

        except Exception as error:

            AlarmGui(str(error))
            no_time_log(str(error),recipeCreatorLog)



    def get_source_recipe_location(self):

        previousSelectedRecipeLocation = self.sourceRecipeLocation.get()
        self.sourceRecipeLocation.set(filedialog.askdirectory())
        self.sourceRecipeLocation.set(path_format(self.sourceRecipeLocation.get()))

        if self.sourceRecipeLocation.get() != "":
            log("User selected a source recipe location:[" + self.sourceRecipeLocation.get() + "]", recipeCreatorLog)

            # clear the list box
            self.sourceRecipeListbox.delete(0,self.sourceRecipeListbox.size())
            for dir in next(os.walk(self.sourceRecipeLocation.get()))[1]:
                # if os.path.isdir(dir):
                self.sourceRecipeListbox.insert(END, dir)
        else:
            self.sourceRecipeLocation.set(previousSelectedRecipeLocation)


class recipeGoldCheckGui:

    def __init__(self):
        px = 10
        ipy = 5
        # Init master gui
        self.master = tk.Toplevel()
        self.master.grab_set()
        self.master.title('Recipe Gold Check - RGC')

        self.master.geometry("+0+200")
        self.master.resizable(1, 1)

        self.sourceRecipeLocation = tk.StringVar()
        self.selectionModeText = tk.StringVar(value="Drag")
        self.selectedRecipeCountVar = tk.StringVar(value="0")

        self.selectedRecipeCount = 0
        self.selectedRecipeList = []

        self.mismatchedRecipeList = []
        self.mismatchedRecipeReportList = []
        self.mismatchedRecipeFileReportList = []
        self.mismatchedParameterList = []
        self.mismatchedGoldenFileReportList = []
        self.mismatchedGoldenParameterList = []

        self.goldenFileSelectionDefaultCheckbuttonValue = tk.StringVar(value="YES")
        self.goldenFileList = []

        self.rcpGoldCheckResult = tk.StringVar(value="0/0")

        self.progressMessage = tk.StringVar(value="")

        self.mismatchedRecipeResultDict = {'Recipe': self.mismatchedRecipeReportList,
                                           'RecipeFile': self.mismatchedRecipeFileReportList,
                                           'Parameter': self.mismatchedParameterList,
                                           'GoldenFile': self.mismatchedGoldenFileReportList,
                                           'GoldenParameter': self.mismatchedGoldenParameterList}

        self.mismatchedRecipeListDict = {'Recipe': self.mismatchedRecipeList}

        # Source recipe frame
        self.soureRecipeLocationFrame = tk.LabelFrame(self.master, text="Source recipe network folder", fg="Blue",
                                                      font=('TkTextFont', 12))
        self.sourceRecipeLocationEntry = tk.Entry(self.soureRecipeLocationFrame, textvariable=self.sourceRecipeLocation,
                                                  width=60, font=('TkTextFont', 9))
        self.sourceRecipeLocationButton = tk.Button(self.soureRecipeLocationFrame, text='>>>',
                                                    command=self.get_source_recipe_location,
                                                    font=('TkTextFont	', 12))

        self.sourceRecipeListboxFrame = tk.LabelFrame(self.master, text="Source recipe", fg="Blue",
                                                      font=('TkTextFont', 12))
        self.sourceRecipeScrollbar = tk.Scrollbar(self.sourceRecipeListboxFrame)
        self.sourceRecipeListbox = tk.Listbox(self.sourceRecipeListboxFrame, width=70, height=30,
                                              font=('TkTextFont', 10), yscrollcommand=self.sourceRecipeScrollbar.set,
                                              activestyle='dotbox')

        # Functional button frame
        self.selectionButtonFrame = tk.LabelFrame(self.master, text='Action', fg='Blue', font=('TkTextFont', 12))
        self.addButton = tk.Button(self.selectionButtonFrame, text='Add', command=self.add_to_recipe_list,
                                   font=('TkTextFont	', 12))
        self.removeButton = tk.Button(self.selectionButtonFrame, text='Remove', command=self.remove_from_recipe_list,
                                      font=('TkTextFont	', 12))
        self.runGoldCheckButton = tk.Button(self.selectionButtonFrame, text='RGC', command=lambda: recipe_gold_check_main(configTemplatePath,
                                                                                                                          self.selectedRecipeList,
                                                                                                                          self.goldenFileList),
                                            font=('TkTextFont	', 12))

        self.selectionModeFrame = tk.LabelFrame(self.master, text="Select mode", fg="Blue", font=('TkTextFont', 12))
        self.selectionModeToggleButton = tk.Button(self.selectionModeFrame, textvariable=self.selectionModeText,
                                                   command=self.selection_mode_toggle, font=('TkTextFont	', 12))

        # Selected recipe frame

        self.selectedRecipeCountFrame = tk.LabelFrame(self.master, text="Selected recipe count", fg="Blue",
                                                      font=('TkTextFont', 12))
        self.selectedRecipeCountEntry = tk.Entry(self.selectedRecipeCountFrame,
                                                 textvariable=self.selectedRecipeCountVar, width=10,
                                                 font=('TkTextFont', 12))

        self.selectedRecipeLocationFrame = tk.LabelFrame(self.master, text="Selected recipe", fg="Blue",
                                                         font=('TkTextFont', 12))

        self.selectedRecipeScrollbar = tk.Scrollbar(self.selectedRecipeLocationFrame)
        self.selectedRecipeListbox = tk.Listbox(self.selectedRecipeLocationFrame, width=70, height=30,
                                                font=('TkTextFont', 10),
                                                yscrollcommand=self.selectedRecipeScrollbar.set, activestyle='dotbox')

        # mismatched recipe frame

        self.mismatchedRecipeFrame = tk.LabelFrame(self.master, text="Mismatched Recipe", fg="Blue", font=('TkTextFont', 12))

        self.mismatchedRecipeScrollbar = tk.Scrollbar(self.mismatchedRecipeFrame)
        self.mismatchedRecipeScrollbarX = tk.Scrollbar(self.mismatchedRecipeFrame,orient='horizontal' )
        self.mismatchedRecipeListbox = tk.Listbox(self.mismatchedRecipeFrame, width=70, height=30, font=('TkTextFont', 10),
                                               yscrollcommand=self.mismatchedRecipeScrollbar.set, xscrollcommand=self.mismatchedRecipeScrollbarX.set, activestyle='dotbox')

        # Golden file selection frame
        # self.goldenFileSelectionFrame = tk.LabelFrame(self.master, text="", fg="Blue",
        #                                             font=('TkTextFont', 12))
        self.goldenFileListboxFrame = tk.LabelFrame(self.master, text="Golden Files", fg="Blue",
                                                      font=('TkTextFont', 12))
        self.goldenFileScrollbar = tk.Scrollbar(self.goldenFileListboxFrame)
        self.goldenFileListbox = tk.Listbox(self.goldenFileListboxFrame, width=70, height=10,
                                              font=('TkTextFont', 10), yscrollcommand=self.goldenFileScrollbar.set,
                                              activestyle='dotbox',selectmode=EXTENDED)

        self.selectedGoldenFileListboxFrame = tk.LabelFrame(self.master, text="Selected Golden Files", fg="Blue",
                                                   font=('TkTextFont', 12))
        self.selectedGoldenFileScrollbar = tk.Scrollbar(self.selectedGoldenFileListboxFrame)
        self.selectedGoldenFileListbox = tk.Listbox(self.selectedGoldenFileListboxFrame, width=70, height=10,
                                            font=('TkTextFont', 10), yscrollcommand=self.selectedGoldenFileScrollbar.set,
                                            activestyle='dotbox',selectmode=EXTENDED)

        self.goldenFileButtonFrame = tk.LabelFrame(self.master, text="Action", fg="Blue",
                                                    font=('TkTextFont', 12))
        self.goldenFileAddButton = tk.Button(self.goldenFileButtonFrame, text='Add',
                                                 command=self.add_golden_files,
                                                 font=('TkTextFont	', 14))

        self.goldenFileRemoveButton = tk.Button(self.goldenFileButtonFrame, text='Remove',
                                                 command=self.remove_golden_files,
                                                 font=('TkTextFont	', 14))
        self.goldenFileSelectionDefaultCheckbutton = tk.Checkbutton(self.goldenFileButtonFrame, text='Default',
                                                        variable=self.goldenFileSelectionDefaultCheckbuttonValue, onvalue="YES",
                                                        offvalue="NO", font=('TkTextFont', 14),
                                                        command=self.golden_File_Selection_Default_Checkbutton)


        # Progess bar frame
        self.goldCheckProgressBarFrame = tk.LabelFrame(self.master, text="Progess", fg="Blue",font=('TkTextFont', 12))
        self.goldCheckProgressBar = ttk.Progressbar(self.goldCheckProgressBarFrame, length=500, mode="determinate")

        # self.rcpGoldCheckProcessedCountLabel = tk.Label(self.progressBarFrame, textvariable=self.processedGoldCheckCount, font=('TkTextFont', 14))

        self.rcpGoldCheckResultLabel = tk.Label(self.goldCheckProgressBarFrame, text='N [Checked/Passed]', font=('TkTextFont', 14))
        self.rcpGoldCheckResultLbl = tk.Label(self.goldCheckProgressBarFrame, textvariable=self.rcpGoldCheckResult, font=('TkTextFont', 14))

        self.progressMessageLabel = tk.Label(self.goldCheckProgressBarFrame, textvariable=self.progressMessage, font=('TkTextFont', 14))

        # Layout the GUI

        # Config for column to be able to expand - By default weight = 0 which means no expand. Just need to give a non-zero value to set it able to expand
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)

        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)

        # Source recipe frame
        self.soureRecipeLocationFrame.grid(row=0, column=0, padx=10, ipady=5, sticky=tk.W + tk.E + tk.N)
        self.sourceRecipeLocationEntry.grid(row=0, column=0, padx=10, pady=5, ipady=2, sticky=tk.W + tk.E + tk.N + tk.S)
        self.sourceRecipeLocationButton.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E)


        # self.soureRecipeLocationFrame.rowconfigure(0, weight=1)
        self.soureRecipeLocationFrame.columnconfigure(0, weight=1)
        self.sourceRecipeLocationEntry.columnconfigure(0, weight=1)

        self.sourceRecipeListboxFrame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.sourceRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

        self.sourceRecipeScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.sourceRecipeScrollbar.config(command=self.sourceRecipeListbox.yview)

        self.sourceRecipeListboxFrame.rowconfigure(0, weight=1)
        self.sourceRecipeListboxFrame.columnconfigure(0, weight=1)
        self.sourceRecipeLocationEntry.columnconfigure(0, weight=1)


        # Button frames
        self.selectionButtonFrame.columnconfigure(0, weight=1)
        self.selectionModeFrame.columnconfigure(0, weight=1)
        self.selectionButtonFrame.grid(row=1, column=1, padx=0, pady=10, sticky=tk.W + tk.E + tk.N)
        self.selectionModeFrame.grid(row=1, column=1, padx=0, pady=10, sticky=tk.W + tk.E + tk.S)

        self.addButton.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.removeButton.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.runGoldCheckButton.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        self.selectionModeToggleButton.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        # select recipe Frame

        self.selectedRecipeCountFrame.grid(row=0, column=2, padx=10, ipady=5, sticky=tk.W + tk.N)
        self.selectedRecipeCountEntry.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.selectedRecipeLocationFrame.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.selectedRecipeScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedRecipeScrollbar.config(command=self.selectedRecipeListbox.yview)

        self.selectedRecipeLocationFrame.rowconfigure(0, weight=1)
        self.selectedRecipeLocationFrame.columnconfigure(0, weight=1)

        self.mismatchedRecipeFrame.grid(row=1, column=3, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.mismatchedRecipeListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.mismatchedRecipeScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.mismatchedRecipeScrollbar.config(command=self.mismatchedRecipeListbox.yview)
        self.mismatchedRecipeScrollbarX.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.mismatchedRecipeScrollbarX.config(command=self.mismatchedRecipeListbox.xview)


        self.mismatchedRecipeFrame.rowconfigure(0, weight=1)
        self.mismatchedRecipeFrame.columnconfigure(0, weight=1)

        self.sourceRecipeListbox.config(selectmode=EXTENDED)
        self.selectedRecipeListbox.config(selectmode=EXTENDED)
        self.mismatchedRecipeListbox.config(selectmode=EXTENDED)

        # Golden file selection Frame

        # self.goldenFileSelectionFrame.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S, columnspan =3)

        self.goldenFileListboxFrame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.goldenFileScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileScrollbar.config(command=self.goldenFileListbox.yview)

        self.goldenFileListboxFrame.rowconfigure(0, weight=1)
        self.goldenFileListboxFrame.columnconfigure(0, weight=1)

        self.goldenFileButtonFrame.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.goldenFileSelectionDefaultCheckbutton.grid(row=0, column=0, padx=10, sticky=tk.E)
        self.goldenFileAddButton.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.goldenFileRemoveButton.grid(row=2, column=0, padx=10,pady =10, sticky=tk.E)


        self.selectedGoldenFileListboxFrame.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedGoldenFileListbox.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.selectedGoldenFileScrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.selectedGoldenFileScrollbar.config(command=self.selectedGoldenFileListbox.yview)

        self.selectedGoldenFileListboxFrame.rowconfigure(0, weight=1)
        self.selectedGoldenFileListboxFrame.columnconfigure(0, weight=1)



        # Progess bar frame
        self.goldCheckProgressBarFrame.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        # Allow items in the frame to be able to expand
        self.goldCheckProgressBarFrame.columnconfigure(0, weight=1)
        self.goldCheckProgressBarFrame.columnconfigure(1, weight=1)

        self.goldCheckProgressBar.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S,columnspan=2)
        self.rcpGoldCheckResultLabel.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S)
        self.rcpGoldCheckResultLbl.grid(row=1, column=1, sticky=tk.W + tk.N + tk.S)
        self.progressMessageLabel.grid(row=3, column=0, sticky=tk.W + tk.N + tk.S,columnspan=2)



        # Display golden file to the golden file listbox
        self.display_default_golden_file_to_golden_file_listbox()
        self.goldenFileAddButton.config(state=tk.DISABLED)
        self.goldenFileRemoveButton.config(state=tk.DISABLED)
        self.goldenFileListbox.config(state=tk.DISABLED)
        self.selectedGoldenFileListbox.config(state=tk.DISABLED)


        #     Keyboard binding

        self.sourceRecipeLocationEntry.bind('<Return>', self.source_recipe_location_enter)
        self.mismatchedRecipeListbox.bind('<Control-c>', self.listbox_copy)



    # Class functions

    def listbox_copy(self, event):
        self.master.clipboard_clear()
        for recipeIndex in self.mismatchedRecipeListbox.curselection():
            self.master.clipboard_append(self.mismatchedRecipeListbox.get(recipeIndex))

    def source_recipe_location_enter(self, event):

        try:

            if self.sourceRecipeLocation.get() != "":
                log("User selected a source recipe location:[" + self.sourceRecipeLocation.get() + "]",
                    recipeCreatorLog)

                # clear the list box
                self.sourceRecipeListbox.delete(0, self.sourceRecipeListbox.size())
                for dir in os.listdir(self.sourceRecipeLocation.get()):
                    # if os.path.isdir(dir):
                    self.sourceRecipeListbox.insert(END, dir)
        except Exception as error:
            AlarmGui(str(error))
            no_time_log(str(error), recipeCreatorLog)

    def add_to_recipe_list(self):
        for recipeIndex in self.sourceRecipeListbox.curselection():

            recipePath = os.path.join(self.sourceRecipeLocation.get(), self.sourceRecipeListbox.get(recipeIndex))
            # Check if the recipe has been added to the selected golden file list box. Will NOT add the recipe has been added
            if recipePath not in self.selectedRecipeList:

                self.selectedRecipeListbox.insert(END, self.sourceRecipeListbox.get(recipeIndex))
                # self.mismatchedRecipeListbox.insert(END, self.sourceRecipeListbox.get(recipeIndex))

                # Add selected recipe to self.selectedRecipeList
                self.selectedRecipeList.append(
                    os.path.join(self.sourceRecipeLocation.get(), self.sourceRecipeListbox.get(recipeIndex)))

                # # Add new location to self.newRecipeLocationList
                # self.newRecipeLocationList.append(self.sourceRecipeLocation.get())
                #
                # # Add to self.newRecipeNameList
                # self.newRecipeNameList.append(self.sourceRecipeListbox.get(recipeIndex))
                #
                # # Add to self.specificParameterUpdateFileList
                # self.specificParameterUpdateFileList.append("")
                #
                # # Add to self.sourceAlignmentRecipeList
                # self.sourceAlignmentRecipeList.append("")

                # Update selected recipe count
                self.selectedRecipeCount = self.selectedRecipeCount + 1
                self.selectedRecipeCountVar.set(str(self.selectedRecipeCount))

    def remove_from_recipe_list(self):
        for recipeIndex in self.selectedRecipeListbox.curselection()[::-1]:
            self.selectedRecipeListbox.delete(recipeIndex)
            # self.mismatchedRecipeListbox.delete(recipeIndex)

            # Remove selected recipe to self.selectedRecipeList
            self.selectedRecipeList.pop(recipeIndex)

            # # Remove new location to self.newRecipeLocationList
            # self.newRecipeLocationList.pop(recipeIndex)
            #
            # # Remove to self.newRecipeNameList
            # self.newRecipeNameList.pop(recipeIndex)
            #
            # # Remove to self.specificParameterUpdateFileList
            # self.specificParameterUpdateFileList.pop(recipeIndex)
            #
            # # Remove to self.sourceAlignmentRecipeList
            # self.sourceAlignmentRecipeList.pop(recipeIndex)

            # Update selected recipe count
            self.selectedRecipeCount = self.selectedRecipeCount - 1
            self.selectedRecipeCountVar.set(str(self.selectedRecipeCount))

    def selection_mode_toggle(self):
        if self.selectionModeText.get() == "Drag":
            self.sourceRecipeListbox.config(selectmode=MULTIPLE)
            self.selectionModeText.set("Multi")
        else:
            self.sourceRecipeListbox.config(selectmode=EXTENDED)
            self.selectionModeText.set("Drag")

    # def run_gold_check(self):
    #     print(self.selectedRecipeList)


    def get_source_recipe_location(self):

        previousSelectedRecipeLocation = self.sourceRecipeLocation.get()
        self.sourceRecipeLocation.set(filedialog.askdirectory())
        self.sourceRecipeLocation.set(path_format(self.sourceRecipeLocation.get()))

        if self.sourceRecipeLocation.get() != "":
            log("User selected a source recipe location:[" + self.sourceRecipeLocation.get() + "]", recipeCreatorLog)

            # clear the list box
            self.sourceRecipeListbox.delete(0, self.sourceRecipeListbox.size())
            for dir in next(os.walk(self.sourceRecipeLocation.get()))[1]:
                # if os.path.isdir(dir):
                self.sourceRecipeListbox.insert(END, dir)
        else:
            self.sourceRecipeLocation.set(previousSelectedRecipeLocation)

    def display_default_golden_file_to_golden_file_listbox(self):
        # clear the list box
        self.goldenFileListbox.delete(0, self.goldenFileListbox.size())
        self.selectedGoldenFileListbox.delete(0, self.selectedGoldenFileListbox.size())

        if DefaultGoldenFileList:
            for file in DefaultGoldenFileList:
                if HCGoldenFilePath:
                    filePath = os.path.join(HCGoldenFilePath, file)
                    self.goldenFileListbox.insert(END, file)
                    self.selectedGoldenFileListbox.insert(END, file)

                    self.goldenFileList.append(filePath)

    def display_golden_file_to_golden_file_listbox(self):
        try:

            # clear the list box
            self.goldenFileListbox.delete(0, self.goldenFileListbox.size())
            self.selectedGoldenFileListbox.delete(0, self.selectedGoldenFileListbox.size())
            if HCGoldenFilePath:
                for file in os.listdir(HCGoldenFilePath):
                    self.goldenFileListbox.insert(END, file)
        except Exception as error:
            AlarmGui(str(error))
            no_time_log(str(error), recipeCreatorLog)

    def add_golden_files(self):
        for goldenFileIndex in self.goldenFileListbox.curselection():

            if HCGoldenFilePath:
                filePath = os.path.join(HCGoldenFilePath, self.goldenFileListbox.get(goldenFileIndex))
                # Check if the file has been added to the selected golden file list box
                if filePath not in self.goldenFileList:
                    self.selectedGoldenFileListbox.insert(END, self.goldenFileListbox.get(goldenFileIndex))
                    # Add the selected golden file path to goldenFileList
                    self.goldenFileList.append(filePath)

    def remove_golden_files(self):
        for goldenFileIndex in self.selectedGoldenFileListbox.curselection()[::-1]:
            self.selectedGoldenFileListbox.delete(goldenFileIndex)
            self.goldenFileList.pop(goldenFileIndex)

    def golden_File_Selection_Default_Checkbutton(self):

        if self.goldenFileSelectionDefaultCheckbuttonValue.get() == "YES":

            self.display_default_golden_file_to_golden_file_listbox()

            self.goldenFileAddButton.config(state=tk.DISABLED)
            self.goldenFileRemoveButton.config(state=tk.DISABLED)

            self.goldenFileListbox.config(state=tk.DISABLED)
            self.selectedGoldenFileListbox.config(state=tk.DISABLED)



        else:
            self.goldenFileAddButton.config(state=tk.NORMAL)
            self.goldenFileRemoveButton.config(state=tk.NORMAL)

            self.goldenFileListbox.config(state=tk.NORMAL)
            self.selectedGoldenFileListbox.config(state=tk.NORMAL)
            self.display_golden_file_to_golden_file_listbox()
            self.goldenFileList = []

# =========================START MAIN FUNCTION==========================================================================
# Global variables

# newRcpDir = "ConvertRecipe"
# srcAlignRcpDir = "SourceAlignmentRecipes"
probeAlignPTN_FileExt = "ptn"
probeAlignPRB_FileExt = "prb"
unitAlignUTN_FileExt = "utn"
unitAlignUNT_FileExt = "unt"

verifyFlag = True
templatePath= ""
networkDrive= ""
networkFolder= ""
recipeCopyTimeout= ""
configTemplatePath =""
HCGoldenFilePath = ""
DefaultGoldenFileList =[]
EnableVersionCheck = ""
EnableValueCheckOnly = ""
summaryLog =""


# main program
if __name__ == '__main__':

    # freeze_support is to suppress calling new gui when running multiple processing
    freeze_support()
    recipeCreatorLog = os.path.join(os.getcwd(), "logs", str(datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")) + "RecipeCreatorLog.txt")

    # Create logs folder

    if os.path.isdir(os.path.join(os.getcwd(),"logs")) == False:
        os.mkdir(os.path.join(os.getcwd(),"logs"))
    # Reading configuration
    verifyFlag, configTemplatePath, networkDrive, networkFolder, recipeCopyTimeout, HCGoldenFilePath, DefaultGoldenFileList,EnableVersionCheck,EnableValueCheckOnly = configuration_read()


    # Check configuration reading

    if verifyFlag == False:

        alarmText = "Failed to read the configuration!"
        AlarmGui(alarmText)

        configAlarm.alarmMaster.mainloop()

    else:

        app = MainGui()
        templatePath = configTemplatePath
        app.rcpTemplate.set(templatePath)
        app.rcpNetDrive.set(networkDrive)
        app.rcpNetFolder.set(networkFolder)

        app.rcpNetworkDriveEntry.config(state = tk.DISABLED)
        app.rcpNetworkFolderEntry.config(state = tk.DISABLED)
        app.rcpTemplateEntry.config(state = tk.DISABLED)
        app.rcpTemplateButton.config(state = tk.DISABLED)
        app.stopButton.config(state = tk.DISABLED)

        app.master.mainloop()



# =================Version 3.0 change ============================================
# Check if a parameter in the SPU file or the folden files exist in the template. Not sure this is implemented in 2.X version. - It has been implemented in 2.X version -DONE
# Copy the PatMax value from the source alignment recipe to the new one
# Add NPI creation function - Done
# Add gold check function - DONE
#   Add parameter duplicated check - Make sure there is no recipe duplicated in two golden file and in one file
#   Add gold check for binary file
#   Add Cancel button to gold check menu
#   Add detail of mismatch column to report
#   Add checksum check
# Remove GUI size lock  -DONE
# SPU file can be selected in Recipe List Creation
# Clear Selected and Naming list box when loading a new source recipe folder

# ================= Notes ========================================================
#             Save recipe to new folder for each run: Having issue with a long recipe name
#                   - Possible solution: Change name while copying from netapp -> Do not need to move the whole recipe from temp to convertRecipe folder one more time
#             Timeout function -Timeout for the whole convert process for a recipe

#             Using os.utime() to update metadata of folder. DONE. -> No need anymore after using copyfile which automatically update file metadata
#             Put logic to check if the new name is empty -> Fail the recipe. DONE
#             Add a new column named "Failure reason" to failedRcpList. Then update a reason everytime a new recipe is added. DONE
#             Update box size of unit and probe alignment in SDTC .xml. Consider in the future we need to remove the box size: DONE
#             Update file name of all folder DONE
#             Verify the uniqueness of new recipe name: DONE
#             Verify new recipe name has no space: DONE
#
#             Update content of all .xml:
#               - Name of file in each .xml: DONE
#               - GUI and date DONE
#               - New recipe cvtRcpPath path: DONE
#               - Update HC, SDTC mas for value: DONE
#               - Update specific parameters: DONE
#               - Check if specific parameter file path exist or not. If not exist. Do nothing. DONE
#               - Update new recipe path place in manifest.xml. If path empty, will FAIL the recipe. This is to force user to input right folder. DONE
#               - Finally apply checksum: DONE
#               - Update summary log: DONE
#              Update .xml with template. DONE
#              Add to config.xml mapping configuration DONE
#              Add to config.xml option to select SW verion. DONE
#              Verify specific parameter update after completion:DONE

#              Separated log for each coversion: DONE

#              Make recipe list location configurable: DONE
#              Add continue after calling function to continue process: IMPORTANT. For example, specific para file is a wrong format which causes the app to crash. DONE
#              Failed updating specific if the file format is wrong: DONE
#              Does not #print [FAILED] when it failed to rename a recipe: Priority Medium. DONE
#              Randomly failed to rename recipe. IMPORTANT - Added 2 seconds delay before renaming the folder. DONE
#              Add option to force the value is within the range and check for accuracy of int or double value
#              Print csv file nicer. No need
#


