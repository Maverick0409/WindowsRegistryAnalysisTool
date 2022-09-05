########### Windows Registry Automated Analysis Tool ###########
#Author - Rashmi
#Student Id - 2154524
################################################################
import os
from tkinter.font import BOLD
from fpdf import FPDF
import subprocess
from tkinter import *
import win32com.client as win32
import tkinter as tk
from tkinter import ttk
import re
from tkinter import filedialog

import time

#This class is used to define the static variables used in the code
class staticVariables:
    softwareFilePath=""
    systemFilePath=""
    ntuserFilePath=""
    samFilePath=""
    softwareFilePathArray=[]
    systemFilePathArray=[]
    ntuserFilePathArray=[]
    samFilePathArray=[]
    selectedSamLocation=""
    selectedSoftwareLocation=""
    selectedSystemLocation=""
    selectedNtuserLocation=""
    regRipperPath="library\\readregistry.exe -r "
    usbData=[]
    winVerData=[]
    uninstallData=[]
    userData=[]
    networkCardsData=[]
    groupData=[]
    dhcpData=[]
    timezoneData=[]
    shutdownData=[]
    recentDocumentsData=[]
    recentAppsData=[]
    webUrlsData=[]
    subprocessWindowConfig=0x08000000

#This function sets chapter title for the PDF page for a section
def chapter_title_Pdf(pdfVar, num, label):
    pdfVar.set_font('Arial', '', 12)
    pdfVar.set_fill_color(200, 220, 255)
    pdfVar.set_text_color(0,0,0)
    pdfVar.cell(0, 6, 'Section %d : %s' % (num, label), 0, 1, 'L', 1)
    pdfVar.ln(4)

#This function writes the data for section using input data passed from parent function
def printPdfSectionContent(inputData,pdf,startY,cellWidth):
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial","",8)
    i=startY
    pdf.set_y=startY
    pdf.set_x=10
    for output in range(len(inputData)):
        if(inputData[output].count('#')==5):
            if(i>255):
                i=20
                pdf.add_page()
                #footer_Pdf(pdf)
                pdf.set_font("Arial","",8)
                pdf.set_text_color(0,0,0)
                pdf.rect(5, 5, 200, 287, 'S')
                pdf.set_x=10
                pdf.set_y=20
            pdf.cell(190,5,"---------------------------------------------------------------------------------------------------------------------------------------------------",0,1,'L',False)
            pdf.cell(190,5,inputData[output].replace("#",""),0,1,'L',False)
            pdf.cell(190,5,"---------------------------------------------------------------------------------------------------------------------------------------------------",0,1,'L',False)
            pdf.cell(190,5,"",0,1,'L',False)
            i=i+20
        elif(inputData[output].count('@')==5):
            outputSplit = inputData[output].partition('|')
            pdf.cell(190,5,"---------------------------------------------------------------------------------------------------------------------------------------------------",0,1,'L',False)
            pdf.cell(cellWidth[0],5,outputSplit[0].replace("@",""),0,0,'L',False)
            pdf.cell(cellWidth[1],5,outputSplit[2],0,1,'L',False)
            pdf.cell(190,5,"---------------------------------------------------------------------------------------------------------------------------------------------------",0,1,'L',False)
            pdf.cell(190,5,"",0,1,'L',False)
            i=i+20
        else:
            outputSplit = inputData[output].partition('|')
            pdf.cell(cellWidth[0],5,outputSplit[0].strip(),0,0,'L',False)
            #if(outputSplit[2].strip().len)
            pdf.cell(cellWidth[1],5,outputSplit[2].strip(),0,1,'L',False)
            i=i+5
            if(i>285 and output < len(inputData)-1):
                i=20
                pdf.add_page()
                #footer_Pdf(pdf)
                pdf.set_font("Arial","",8)
                pdf.set_text_color(0,0,0)
                pdf.rect(5, 5, 200, 287, 'S')
                pdf.set_x=10
                pdf.set_y=20
        
#This function creates the page with border,title and heading information of particular section
def printPdfSectionIntroduction(inputData,pdf,chapterNumber,description,link,cellWidth):
    pdf.add_page()
    chapter_title_Pdf(pdf, chapterNumber,description)

    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial","",9)
    pdf.set_link(link,10)
    pdf.rect(5, 5, 200, 287, 'S')
    pdf.set_y=25
    pdf.set_x=10
    i=25
    for output in range(len(inputData)):
        pdf.cell(cellWidth,5,inputData[output],0,1,'L',False)
        i=i+5
    pdf.cell(cellWidth,5,"",0,1,'L',False)
    i=i+5
    return i

#This function creates table of contents with hyperlinks to each section present in the pdf
def cellTableofContents(index,description,link,pdf,cellWidth):
    
    pdf.set_font("Arial","",10)
    pdf.set_text_color(0,0,0)
    pdf.set_x(20)
    pdf.cell(cellWidth[0],10,str(index),1,0,'L',False)
    pdf.cell(cellWidth[1],10,description,1,0,'L',False)
    pdf.set_font("Arial","U",10)
    pdf.set_text_color(0,0,255)
    pdf.cell(cellWidth[2],10,'Link',1,1,'L',False,link)
    

#This function is to generate pdf file to the path provided for the user
def pdfGenerator(fileName): 
    pdf = FPDF()
    pdf.add_page()
    pdf.rect(5, 5, 200, 287, 'S')
    pdf.set_font("Arial","B",20)
    pdf.set_text_color(0,0,255) 
    pdf.set_auto_page_break(True)
    pdf.text(40,100,"Forensic Report for Selected Artefacts")
    pdf.add_page()
    pdf.set_font("Arial","UB",16)
    pdf.set_text_color(0,0,0)
    pdf.text(20,20,"Table of Contents")
    cellWidth=[20,100,40]
    pdf.set_font("Arial","B",12)
    pdf.set_fill_color(193,229,252)
    pdf.set_y(30)
    pdf.set_x(20)
    pdf.cell(cellWidth[0],15,'Sr No.',1,0,'C',True)
    pdf.cell(cellWidth[1],15,'Description',1,0,'C',True)
    pdf.cell(cellWidth[2],15,'Location',1,1,'C',True)
    indexCounter=0
    linksArray=[]
    if staticVariables.usbData.count!=0 and usbCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'USB Devices',linksArray[-1],pdf,cellWidth)

    if staticVariables.winVerData.count!=0 and osCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Operating System',linksArray[-1],pdf,cellWidth)

    if staticVariables.networkCardsData.count!=0 and networkCardsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Network Cards',linksArray[-1],pdf,cellWidth)

    if staticVariables.uninstallData.count!=0 and installedApplicationsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Installed Softwares',linksArray[-1],pdf,cellWidth)

    if staticVariables.userData.count!=0 and userAccountsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'User Accounts',linksArray[-1],pdf,cellWidth)

    if staticVariables.groupData.count!=0 and userGroupsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'User Groups',linksArray[-1],pdf,cellWidth)

    if staticVariables.dhcpData.count!=0 and dhcpCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'DHCP',linksArray[-1],pdf,cellWidth)

    if staticVariables.timezoneData.count!=0 and timezoneCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Computer Timezone',linksArray[-1],pdf,cellWidth)

    if staticVariables.shutdownData.count!=0 and systemShutdownCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Shutdown Information',linksArray[-1],pdf,cellWidth)

    if staticVariables.recentDocumentsData.count!=0 and recentDocumentsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Recent Documents',linksArray[-1],pdf,cellWidth)

    if staticVariables.recentAppsData.count!=0 and recentAppsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Recent Applications',linksArray[-1],pdf,cellWidth)

    if staticVariables.webUrlsData.count!=0 and webUrlsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        linksArray.append(pdf.add_link())
        cellTableofContents(indexCounter,'Recent Web URLs',linksArray[-1],pdf,cellWidth)

    i=20
    indexCounter=0
    
    if staticVariables.usbData.count!=0 and usbCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("The information below shows the list of USB devices previously attached to the machine. Details are provided as below:")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'USB Devices',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.usbData,pdf,row+10,cellWidth1)

    if staticVariables.winVerData.count!=0 and osCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("The information below shows the Windows Operating system Product name, release version, Composition Edition Id which is the edition")
        inputData.append("upon which the current edition is derived from/based on, registered owner of the Operating system operational on the machine, and ")
        inputData.append("installation date and time of OS.")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Operating System',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.winVerData,pdf,row+10,cellWidth1)

    if staticVariables.networkCardsData.count!=0 and networkCardsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[90,150]
        inputData.append("The information below shows the network cards that were in use on this machine. The result can show two types of network cards; ")
        inputData.append("Ethernet (wired) or wireless interface. It also indicates the date and time when these cards were last used.")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Network Cards',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.networkCardsData,pdf,row+10,cellWidth1)

    if staticVariables.uninstallData.count!=0 and installedApplicationsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("List of software products installed on the machine are as follows according to date and time (latest first):")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Installed Softwares',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.uninstallData,pdf,row+10,cellWidth1)

    if staticVariables.userData.count!=0 and userAccountsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("The information below shows user accounts present on the machine. Details include:")
        inputData.append("")
        inputData.append("Username: This username is provided by Windows Operating System. Username is followed by number within square brackets such as")
        inputData.append("[501]. It denotes the Relative ID(RID). RID is a number that is generated to uniquely identify an account within a domain.")
        inputData.append("Any group or user created by Microsoft Windows Operating System will have RID less than 1000. Any group or user that the a Microsoft")
        inputData.append("Windows Operating System does not create, such as an account created by the end user has a RID of 1000 or greater by default.")
        inputData.append("")
        inputData.append("Full name : Full name as provided at the time of account creation.")
        inputData.append("")
        inputData.append("User Comment : Describes the access level and purpose of the user.")
        inputData.append("")
        inputData.append("Account created : Date and time when account had been created.")
        inputData.append("")
        inputData.append("Last Login Date: Last Login date will shows as 'Account used actively' if account is actively used by the user. The last login date")
        inputData.append("will have a time stamp only if the account has not been logged on since a while as in the case of 'Administrator' user.")
        inputData.append("")
        inputData.append("Password Reset Date : Date and time when account password was last reset.")
        inputData.append("")
        inputData.append("Password Setting : This setting shows if password is set to expire after a certain time period or not.")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'User Accounts',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.userData,pdf,row+10,cellWidth1)

    if staticVariables.groupData.count!=0 and userGroupsCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[25,165]
        inputData.append("The information below shows the list of user groups present on the machine. It provides details such as:")
        inputData.append("")
        inputData.append("Group Name: Name of the group.")
        inputData.append("")
        inputData.append("Last Updated: Demonstrates when the use group was last modified. For instance, additional or removal of users in the group will be ")
        inputData.append("considered as a modification to the group.")
        inputData.append("")
        inputData.append("Group Description: Describes the access level of the group.")
        inputData.append("")
        inputData.append("Users: The user SIDs or Security Identifiers for the user accounts are displayed under Users. When an account or group is established,")
        inputData.append("the system generates the SID that identifies that specific account or group. A Comprehensive list and descriptions of well-known SIDs can")
        inputData.append("be found here for further analysis-https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/security-identifiers.")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'User Groups',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.groupData,pdf,row+10,cellWidth1)

    if staticVariables.dhcpData.count!=0 and dhcpCheckboxInput.get()=="On":
        indexCounter=indexCounter+1
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("DHCP is the Dynamic Host Control Protocol that is responsible for allocating IP addresses to computers on a network. The information ")
        inputData.append("below explains the attributes associated with DHCP:")
        inputData.append("")
        inputData.append("Adapter: Windows provided unique ID every time DHCP assigns a new IP to the machine")
        inputData.append("")
        inputData.append("Last write time: This is the time when the DHCP allocated the Ip address to the machine")
        inputData.append("")
        inputData.append("DHCP IP address: IP address allocated to the machine")
        inputData.append("")
        inputData.append("DHCP subnet mask: The subnet mask divides the IP address into 2 parts; the host and network address. Thus, subnet mask defines")
        inputData.append("part of the IP address associated with the machine and part of IP address which is associated with the network.")
        inputData.append("")
        inputData.append("DHCP server IP: This provides the IP address of the server, which uses DHCP to dynamically issue IP addresses to networked devices.")
        inputData.append("enabling connectivity with another network.")
        inputData.append("")
        inputData.append("DHCP Lease Obtained Time: Time when DHCP lease was obtained.")
        inputData.append("")
        inputData.append("DHCP Terminate Time: Time when DHCP lease will expire.")
        inputData.append("")
        inputData.append("DHCP default gateway: The router's IP which was used to connect to outside networks such as the internet.")
        inputData.append("")
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'DHCP Information',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.dhcpData,pdf,row+10,cellWidth1)

    if staticVariables.timezoneData.count!=0 and timezoneCheckboxInput.get()=="On":
        inputData=[]
        cellWidth1=[40,150]
        inputData.append("Timezone defined for this machine is:")
        indexCounter=indexCounter+1
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Compute Timezone',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.timezoneData,pdf,row+10,cellWidth1)

    if staticVariables.shutdownData.count!=0 and systemShutdownCheckboxInput.get()=="On":
        inputData=[]
        cellWidth1=[40,150]        
        inputData.append("Last System shutdown time is as follows:")
        indexCounter=indexCounter+1
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Shutdown Details',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.shutdownData,pdf,row+10,cellWidth1)

    if staticVariables.recentDocumentsData.count!=0 and recentDocumentsCheckboxInput.get()=="On":
        inputData=[]
        cellWidth1=[40,150]        
        inputData.append("The information below shows list of documents recently accessed on the machine. The documents are divided into multiple categorises by")
        inputData.append("file type or extension. Last write time under each category of document showcases the last time that any document of that was modified.")
        indexCounter=indexCounter+1
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Recent Documents',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.recentDocumentsData,pdf,row+10,cellWidth1)

    if staticVariables.recentAppsData.count!=0 and recentAppsCheckboxInput.get()=="On":
        inputData=[]
        cellWidth1=[40,150]        
        inputData.append("The information below shows list of applications recently accessed on the machine. The documents are divided into multiple categorises")
        inputData.append("by file type or extension. Last access date time against each application showcases the last time application was used on the machine.")
        indexCounter=indexCounter+1
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Recent Applications',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.recentAppsData,pdf,row+10,cellWidth1)

    if staticVariables.webUrlsData.count!=0 and webUrlsCheckboxInput.get()=="On":
        inputData=[]
        cellWidth1=[40,150]        
        inputData.append("The information below shows web addresses that have been previously visited by the user. Last write time denotes the time when the")
        inputData.append("last visited url was typed.")
        indexCounter=indexCounter+1
        row=printPdfSectionIntroduction(inputData,pdf,indexCounter,'Recent Web URLS',linksArray[indexCounter-1],190)
        printPdfSectionContent(staticVariables.webUrlsData,pdf,row+10,cellWidth1)

    pdf.output(fileName)
    openPopup("PDF File Created","Report Generated Successfully","14","bold")

#This function is to trigger perl plugin to retrieve installed software list and print to result section 
def uninstallFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):

        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p installedapplications', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\nINSTALLED SOFTWARES \n")
        textarea.insert('end',"\nList of software products installed on the machine are as follows according to date and time (latest first):\n")

        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  INSTALL DATE TIME                   SOFTWARE                                                              \n")
                response.append("@@@@@INSTALL DATE TIME|SOFTWARE                                                              \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")


            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SOFTWARE HIVE FILE","SOFTWARE Hive File Not Found","14","bold")

    return response

#This function is to trigger perl plugin to retrieve usb devices connected to PC and print to result section 
def usbStoreFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p usbstorage', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)
        counter=1
        textarea.insert('end',"\nUSB DEVICES \n")
        textarea.insert('end',"\nThe information below shows the list of USB devices previously attached to the machine. Details are provided as below:\n")

        index=0
        for output in process.stdout.readlines():
        
            if(output.count('USB Device Name')>0):

                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"                          USB DEVICE - "+str(counter)+"\n")
                response.append("#####                                              USB DEVICE - "+str(counter)+"\n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                counter=counter + 1

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SYSTEM HIVE FILE","SYSTEM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve windows version and print to result section 
def winverFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p windowsversion', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        

        textarea.insert('end',"\nOPERATING SYSTEM \n")
        textarea.insert('end',"\nThe information below shows the Windows Operating system Product name, release version, Composition Edition Id which is the edition upon which the current edition is derived from/based on, registered owner of the Operating system operational on the machine, and installation date and time of OS.\n")

        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  PROPERTY                    DESCRIPTION                                                              \n")
                response.append("@@@@@PROPERTY|DESCRIPTION                                                              \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SOFTWARE HIVE FILE","SOFTWARE Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve list of Windows Users and print to result section 
def userFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p userdetails', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        counter=1
        textarea.insert('end',"\nUSER ACCOUNTS \n")
        textarea.insert('end',"\nThe information below shows user accounts present on the machine. Details include:\n")
        textarea.insert('end',"\nUsername : This username is provided by Windows Operating System.Username is followed by number within square brackets such as [501]. It denotes the Relative ID(RID). RID is a number that is generated to uniquely identify an account within a domain.\n")
        textarea.insert('end',"Any group or user created by Microsoft Windows Operating System will have RID less than 1000. Any group or user that the a Microsoft Windows Operating System does not create, such as an account created by the end user has a RID of 1000 or greater by default.\n")
        textarea.insert('end',"\nFull name : Full name as provided at the time of account creation.\n")
        textarea.insert('end',"\nUser Comment : Describes the access level and purpose of the user.\n")
        textarea.insert('end',"\nAccount created : Date and time when account had been created.\n")
        textarea.insert('end',"\nLast Login Date: Last Login date will shows as 'Account used actively' if account is actively used by the user. The last login date will have a time stamp only if the account has not been logged on since a while as in the case of 'Administrator' user.\n")
        textarea.insert('end',"\nPassword Reset Date : Date and time when account password was last reset.\n")
        textarea.insert('end',"\nPassword Setting : This setting shows if password is set to expire after a certain time period or not.\n")
        index=0
        for output in process.stdout.readlines():
            if(output.count('Username')>0):

                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"                          User Details - "+str(counter)+"\n")
                response.append("#####                                User Details - "+str(counter)+"\n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                counter=counter + 1

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SAM HIVE FILE","SAM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve network card details and print to result section 
def networkCardsFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p networkcards', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\nNETWORK CARDS \n")
        textarea.insert('end',"\nThe information below shows the network cards that were in use on this machine. The result can show two types of network cards; Ethernet (wired) or wireless interface. It also indicates the date and time when these cards were last used.\n")
        index=0
        for output in process.stdout.readlines(): 
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  NETWORK CARD NAME                                   LAST UPDATE DATE TIME                     \n")
                response.append("@@@@@NETWORK CARD NAME|LAST UPDATE DATE TIME                     \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

            textarea.insert('end',"  "+output.replace("|","  "))
            response.append(output)
            index=index+1
            
        if(index==0):

            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SOFTWARE HIVE FILE","SOFTWARE Hive File Not Found")
    return response

#This function is to trigger perl plugin to retrieve User Groups and print to result section 
def groupFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p usergroups', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)
        #output = process.stdout.readlines()
        counter=1
        textarea.insert('end',"\nUSER GROUPS \n")
        textarea.insert('end',"\nThe information below shows the list of user groups present on the machine. Details include:\n")
        textarea.insert('end',"\nGroup Name: Name of the group.\n")
        textarea.insert('end',"\nLast Updated: Demonstrates when the use group was last modified. For instance, additional or removal of users in the group will be considered as a modification to the group.\n")
        textarea.insert('end',"\nGroup Description: Describes the access level of the group.\n")
        textarea.insert('end',"\nUsers: The user SIDs or Security Identifiers for the user accounts are displayed under Users. When an account or group is established, the system generates the SID that identifies that specific account or group. A Comprehensive list and descriptions of well-known SIDs can be found here for further analysis - https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/security-identifiers.\n")
        index=0
        for output in process.stdout.readlines():
            if(output.count('Group Name')>0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")
                textarea.insert('end',"                          Group Details - "+str(counter)+"\n")
                response.append("#####                                  Group Details - "+str(counter)+"\n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")
                counter=counter + 1
            textarea.insert('end',"  "+output.replace("|"," : "))
            outputSplit = output.partition('|')
            if(len(outputSplit[2])>119):
                response.append(outputSplit[0]+outputSplit[1]+outputSplit[2][0:120])
                response.append(" |"+outputSplit[2][120:-1])
            else:
                response.append(output)
            index=index+1
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SAM HIVE FILE","SAM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve dhcp information and print to result section 
def dhcpFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p dhcpinformation', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        counter=1

        textarea.insert('end',"\nDHCP INFORMATION \n")
        textarea.insert('end',"\nDHCP is the Dynamic Host Control Protocol that is responsible for allocating IP addresses to computers on a network. The information below explains the attributes associated with DHCP:\n")
        textarea.insert('end',"\nAdapter: Windows provided unique ID every time DHCP assigns a new IP to the machine\n")
        textarea.insert('end',"\nLast write time: This is the time when the DHCP allocated the Ip address to the machine\n")
        textarea.insert('end',"\nDHCP IP address: IP address allocated to the machine\n")
        textarea.insert('end',"\nDHCP subnet mask: The subnet mask divides the IP address into 2 parts; the host and network address. Thus, subnet mask defines part of the IP address associated with the machine and part of IP address which is associated with the network.\n")
        textarea.insert('end',"\nDHCP server IP: This provides the IP address of the server, which uses DHCP to dynamically issue IP addresses to networked devices, enabling connectivity with another network.\n")
        textarea.insert('end',"\nDHCP Lease Obtained Time: Time when DHCP lease was obtained.\n")
        textarea.insert('end',"\nDHCP Terminate Time: Time when DHCP lease will expire.\n")
        textarea.insert('end',"\nDHCP default gateway: The router's IP which was used to connect to outside networks such as the internet.\n")
        
        index=0
        for output in process.stdout.readlines():
            if(output.count('Adapter')>0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"                          ADAPTER - "+str(counter)+"\n")
                response.append("#####                                 ADAPTER - "+str(counter)+"\n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                counter=counter + 1

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SYSTEM HIVE FILE","SYSTEM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve timezone set on device and print to result section 
def timezoneFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p timezonedetails', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\nCOMPUTER TIMEZONE \n")
        textarea.insert('end',"\nTimezone defined for this machine is:\n")

        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")
                textarea.insert('end',"  PROPERTY               DESCRIPTION                                                              \n")
                response.append("@@@@@PROPERTY|DESCRIPTION                                                              \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SYSTEM HIVE FILE","SYSTEM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to retrieve last shutdown time and print to result section 
def shutdownFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p shutdowndetails', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\nSHUTDOWN TIME \n")
        textarea.insert('end',"\nLast System shutdown time is as follows::\n")
        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  PROPERTY               DESCRIPTION                                                              \n")
                response.append("@@@@@PROPERTY|DESCRIPTION                                                              \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - SYSTEM HIVE FILE","SYSTEM Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to recent documents and print to result section 
def recentDocumentsFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p recentdocuments', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\nRECENT DOCUMENTS \n")
        textarea.insert('end',"\nThe information below shows list of documents recently accessed on the machine. The documents are divided into multiple categorises by file type or extension. Last write time under each category of document showcases the last time that any document of that was modified.\n")

        index=0
        for output in process.stdout.readlines():
            
            if(output.count('Type/Extension')>0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"                          Type/Extension - "+output.partition('|')[2])
                response.append("#####                             Type/Extension - "+output.partition('|')[2])
                textarea.insert('end',"--------------------------------------------------------------------------------\n")
            else:
                textarea.insert('end',"  "+output.replace("|"," : "))
                response.append(output)
            index=index+1
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - NTUSER.DAT HIVE FILE","NTUSER.DAT Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to recent Applciations and print to result section
def recentAppsFunction(hivePath):
    response=[]
    if(checkPath(hivePath)==TRUE):

        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p recentapplications', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\n RECENT APPLICATIONS \n")
        textarea.insert('end',"\nThe information below shows list of applications recently accessed on the machine. The documents are divided into multiple categorises by file type or extension. Last access date time against each application showcases the last time application was used on the machine.\n")

        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  LAST ACCESS DATE TIME                   APPLICATIONS                                                             \n")
                response.append("@@@@@LAST ACCESS DATE TIME|APPLICATIONS                                                             \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")
            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - NTUSER.DAT HIVE FILE","NTUSER.DAT Hive File Not Found","14","bold")
    return response

#This function is to trigger perl plugin to recent web urls and print to result section
def webUrlsFunction(hivePath):
    response=[]
    #print("WebHive Path"+hivePath)
    if(checkPath(hivePath)==TRUE):
        process = subprocess.Popen(staticVariables.regRipperPath+hivePath+' -p urlstyped', 
                               stdout=subprocess.PIPE,universal_newlines=True, stderr=subprocess.PIPE,creationflags=staticVariables.subprocessWindowConfig)

        textarea.insert('end',"\n RECENT WEB URLs \n")
        textarea.insert('end',"\nThe information below shows web addresses that have been previously visited by the user. Last write time denotes the time when the last visited url was typed.\n")
        index=0
        for output in process.stdout.readlines():
            if(index==0):
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

                textarea.insert('end',"  PROPERTY          DESCRIPTION                                                              \n")
                response.append("@@@@@PROPERTY|DESCRIPTION                                                              \n")
                textarea.insert('end',"--------------------------------------------------------------------------------\n")

            textarea.insert('end',"  "+output.replace("|"," : "))
            response.append(output)
            index=index+1
            
        if(index==0):
            textarea.insert('end',"\nNo information found.\n")
            textarea.insert('end',"\n================================================================================\n")
            response.append("No information found.|")
        else:
            textarea.insert('end',"\n================================================================================\n")
    else:
        openPopup("ERROR - NTUSER.DAT HIVE FILE","NTUSER.DAT Hive File Not Found","14","bold")
    return response

#Common Function is used to search for filename and return the directory path
def fileSearchFunction(rootPath,fileName):
    fileResearchResult = []
    for root, dirs, files in os.walk(rootPath):
        if fileName in files:
            #print(os.path.join(root))
            if(str(root).__contains__("System32\config") == FALSE):
                fileResearchResult.append(os.path.join(root,fileName))
        
    return fileResearchResult            

#Function is used to display browse folder for Hive Search Folder Path
def browse_dialogue():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    folderName = filedialog.askdirectory()
    folderName= folderName.replace("/","\\")

        
    if(str(folderName).__contains__("System32\config") == TRUE):
        openPopup("ERROR - Selected Live Hive Folder", "The tool does not operate on live registry hive files which are continuously updated. Please select another location.","9","bold")
    elif(str(folderName).__len__()!=0):
        registryPath_field.configure(state="normal")
        registryPath_field.delete(0,"end")
        registryPath_field.insert(0,folderName)
        registryPath_field.configure(state="readonly")
        staticVariables.softwareFilePathArray=fileSearchFunction(folderName,"SOFTWARE")
        staticVariables.systemFilePathArray=fileSearchFunction(folderName,"SYSTEM")
        staticVariables.samFilePathArray=fileSearchFunction(folderName,"SAM")
        staticVariables.ntuserFilePathArray=fileSearchFunction(folderName,"NTUSER.DAT")
        openPopupFiles(staticVariables.softwareFilePathArray,staticVariables.systemFilePathArray,staticVariables.samFilePathArray,staticVariables.ntuserFilePathArray)


def validateFilePath():
    initialiseForm()
    try:
        software_hive_output['text']=staticVariables.selectedSoftwareLocation.get()
        staticVariables.softwareFilePath=staticVariables.selectedSoftwareLocation.get()
    except:
        software_hive_output['text']=""
        staticVariables.softwareFilePath=""
    try:
        sam_hive_output['text']=staticVariables.selectedSamLocation.get()
        staticVariables.samFilePath=staticVariables.selectedSamLocation.get()
    except:
        sam_hive_output['text']=""
        staticVariables.samFilePath=""
    try:
        system_hive_output['text']=staticVariables.selectedSystemLocation.get()
        staticVariables.systemFilePath=staticVariables.selectedSystemLocation.get()
    except:
        system_hive_output['text']=""
        staticVariables.systemFilePath=""
    try:
        ntuser_hive_output['text']=staticVariables.selectedNtuserLocation.get()
        staticVariables.ntuserFilePath=staticVariables.selectedNtuserLocation.get()
    except:
        ntuser_hive_output['text']=""
        staticVariables.ntuserFilePath=""

    top.destroy()

#Function is used to display browse folder for Hive Search Folder Path
def fileDialogue():
    if len(textarea.get("1.0", "end-1c")) == 0:
        openPopup("ERROR - No Artefacts Selected", "No artefacts selected for report generation. Please select at least one artefact for report generation.","11","bold")
    else:
        root.filename =  filedialog.asksaveasfilename(initialdir = "./",title = "Save as PDF file",filetypes = [("pdf files", '*.pdf')], initialfile ="RegistryAnalysisReport_"+time.strftime('%Y%m%d-%H%M%S')+".pdf")
        if(len(root.filename)>0):
            pdfGenerator(root.filename)

#Function to display pop up window with list of hive files found as part of search and provide option for user to select and submit
def openPopupFiles(softwareFile,systemFile,samFile,ntuserFile):
   if(len(softwareFile)==0 & len(systemFile)==0 & len(samFile)==0 & len(ntuserFile)==0):
       openPopup("ERROR - No Hive Files Found", "No Windows registry hive files found in the input drive/folder. Please select another location.","11","bold")
   else:
       global top 
       top = Toplevel(root)
       top.geometry("650x800")
       top.title("Hive File Folder Locations")
       frame_header_software = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=105, pady=10)
       frame_header_software.place(relx=0.01, rely=0.01)
       heading_Select_Options = Label(frame_header_software, text="Software Hive File Locations on this machine")
       heading_Select_Options.grid(row=0, column=1)
       frame_software = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=105, pady=10)
       frame_software.place(relx=0.01, rely=0.08)

       if(len(softwareFile)!=0):
           staticVariables.selectedSoftwareLocation=StringVar()
           for index,softwareFileName in enumerate(softwareFile):
               if(index<4):
                   softwareRadio=Radiobutton(frame_software, bg="light blue", text=softwareFileName, variable=staticVariables.selectedSoftwareLocation, value=softwareFileName)         
                   softwareRadio.deselect()           
                   if(index==0):
                       softwareRadio.select()

                   softwareRadio.pack()
       if(len(softwareFile)<4):
           for i in range(1,4-len(softwareFile)):
               Label(frame_software, text="         ").pack()

       frame_header_system = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=110, pady=10)
       frame_header_system.place(relx=0.01, rely=0.24)
       heading_Select_Options = Label(frame_header_system, text="System Hive File Locations on this machine")
       heading_Select_Options.grid(row=0, column=1)
       frame_system = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=105, pady=10)
       frame_system.place(relx=0.01, rely=0.31)
       if(len(systemFile)!=0):
           staticVariables.selectedSystemLocation=StringVar()
           for index,systemFileName in enumerate(systemFile):
               if(index<4):
                   systemRadio = Radiobutton(frame_system, bg="light blue", text=systemFileName, variable=staticVariables.selectedSystemLocation, value=systemFileName)
                   systemRadio.deselect()
                   if(index==0):
                       systemRadio.select()
           
                   systemRadio.pack()
       if(len(systemFile)<4):
           for i in range(1,4-len(systemFile)):
               Label(frame_system, text="         ").pack()
       frame_header_sam = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=110, pady=10)
       frame_header_sam.place(relx=0.01, rely=0.48)
       heading_Select_Options = Label(frame_header_sam, text="Sam Hive File Locations on this machine     ")
       heading_Select_Options.grid(row=0, column=1)
       frame_sam = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=105, pady=10)
       frame_sam.place(relx=0.01, rely=0.55)
       if(len(samFile)!=0):
           staticVariables.selectedSamLocation=StringVar()
           for index, samFileName in enumerate(samFile):
               if(index<4):
                   samRadio=Radiobutton(frame_sam, bg="light blue", text=samFileName, variable=staticVariables.selectedSamLocation, value=samFileName)
                   samRadio.deselect()
                   if(index==0):
                       samRadio.select()
          
               
                   samRadio.pack()
       if(len(samFile)<4):
           for i in range(1,4-len(samFile)):
               Label(frame_sam, text="         ").pack()

       frame_header_ntuser = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=110, pady=10)
       frame_header_ntuser.place(relx=0.01, rely=0.72)
       heading_Select_Options = Label(frame_header_ntuser, text="NTUSER Hive File Locations on this machine")
       heading_Select_Options.grid(row=0, column=1)
       frame_ntuser = Frame(top, highlightbackground="dark grey", highlightthickness=10, padx=105, pady=10)
       frame_ntuser.place(relx=0.01, rely=0.79)
       if(len(ntuserFile)!=0):
           staticVariables.selectedNtuserLocation=StringVar()
           for index, ntuserFileName in enumerate(ntuserFile):
               if(index<4):
                   ntuserRadio=Radiobutton(frame_ntuser, bg="light blue", text=ntuserFileName, variable=staticVariables.selectedNtuserLocation, value=ntuserFileName)
                   ntuserRadio.deselect()
               if(index==0):
                   ntuserRadio.select()
               ntuserRadio.pack()
       if(len(ntuserFile)<4):
           for i in range(1,4-len(ntuserFile)):
               Label(frame_ntuser, text="         ").pack()
       
       frame_ok = Frame(top, highlightbackground="dark grey")
       frame_ok.place(relx=0.45, rely=0.97)
       buttonOk = Button(frame_ok, text="Submit", fg="Black",bg="Grey",font=("Calibri, 8"),command=validateFilePath)
       buttonOk.grid(row=0, column=2)

#Common Function to initialise form
def initialiseForm():
    usbCheckbox.deselect()
    osCheckbox.deselect()
    networkCardsCheckbox.deselect()
    installedApplicationsCheckbox.deselect()
    userAccountsCheckbox.deselect()
    userGroupsCheckbox.deselect()
    dhcpCheckbox.deselect()
    timezoneCheckbox.deselect()
    systemShutdownCheckbox.deselect()
    recentDocumentsCheckbox.deselect()
    recentAppsCheckbox.deselect()
    webUrlsCheckbox.deselect()
    selectallCheckbox.deselect()

def reportGenerator():
    printText=textarea.get("1.0",'end-1c')
    reportFilename = 'RegistryReport_'+time.strftime("%Y%m%d-%H%M%S")+".txt"
    with open(reportFilename,"a") as outf:
        outf.write(printText)
    openPopup("Report Generated Successfully","Registry Report - "+reportFilename+" created","14","bold")


#Common Function to check if path is valid
def checkPath(path):
    if not os.path.exists(path):
        return False
    else:
        return TRUE

#Common Function to display popup window for information or error
def openPopup(title,message,fontSize,fontStyle):
   top= Toplevel(root)
   top.geometry("650x200")
   top.title(title)
   Label(top, text=message, font=('Calibri '+fontSize+' '+fontStyle)).place(x=20,y=80)
   Button(top, text="OK", fg="Black",
                    bg="Grey",font=("Calibri, 14"),padx=10, command=top.destroy).place(x=280,y=150)


#Function triggered when users selects/deselects Select All Checkbox.
def selctAllControlMain():
    if(selectAllCheckboxInput.get()=="Off"):
        usbCheckbox.deselect()
        osCheckbox.deselect()
        networkCardsCheckbox.deselect()
        installedApplicationsCheckbox.deselect()
        userAccountsCheckbox.deselect()
        userGroupsCheckbox.deselect()
        dhcpCheckbox.deselect()
        timezoneCheckbox.deselect()
        systemShutdownCheckbox.deselect()
        recentDocumentsCheckbox.deselect()
        recentAppsCheckbox.deselect()
        webUrlsCheckbox.deselect()
        comboBoxControlMain()
    if(selectAllCheckboxInput.get()=="On"):
        usbCheckbox.select()
        osCheckbox.select()
        networkCardsCheckbox.select()
        installedApplicationsCheckbox.select()
        userAccountsCheckbox.select()
        userGroupsCheckbox.select()
        dhcpCheckbox.select()
        timezoneCheckbox.select()
        systemShutdownCheckbox.select()
        recentDocumentsCheckbox.select()
        recentAppsCheckbox.select()
        webUrlsCheckbox.select()
        comboBoxControlMain()

#Main Function triggered when checkboxes status changes and then trigger subfunctions to populate result section
def comboBoxControlMain():
    textarea.delete("1.0","end")


    if(checkPath(staticVariables.systemFilePath)==TRUE | checkPath(staticVariables.softwareFilePath)==TRUE | checkPath(staticVariables.samFilePath)==TRUE | checkPath(staticVariables.ntuserFilePath)==TRUE):

        if(usbCheckboxInput.get()=="On"):
            staticVariables.usbData=usbStoreFunction(staticVariables.systemFilePath)
        if(osCheckboxInput.get()=="On"):
            staticVariables.winVerData=winverFunction(staticVariables.softwareFilePath)
        if(networkCardsCheckboxInput.get()=="On"):
            staticVariables.networkCardsData=networkCardsFunction(staticVariables.softwareFilePath)
        if(installedApplicationsCheckboxInput.get()=="On"):
            staticVariables.uninstallData=uninstallFunction(staticVariables.softwareFilePath)
        if(userAccountsCheckboxInput.get()=="On"):
            staticVariables.userData=userFunction(staticVariables.samFilePath)
        
        if(userGroupsCheckboxInput.get()=="On"):
            staticVariables.groupData=groupFunction(staticVariables.samFilePath)
        if(dhcpCheckboxInput.get()=="On"):
            staticVariables.dhcpData=dhcpFunction(staticVariables.systemFilePath)
        if(timezoneCheckboxInput.get()=="On"):
           staticVariables.timezoneData= timezoneFunction(staticVariables.systemFilePath)
        if(systemShutdownCheckboxInput.get()=="On"):
            staticVariables.shutdownData=shutdownFunction(staticVariables.systemFilePath)
        if(recentDocumentsCheckboxInput.get()=="On"):
            staticVariables.recentDocumentsData=recentDocumentsFunction(staticVariables.ntuserFilePath)
        if(recentAppsCheckboxInput.get()=="On"):
            staticVariables.recentAppsData=recentAppsFunction(staticVariables.ntuserFilePath)
        if(webUrlsCheckboxInput.get()=="On"):
            staticVariables.webUrlsData=webUrlsFunction(staticVariables.ntuserFilePath)
        
            
        #Off Button    
        if(usbCheckboxInput.get()=="Off"):
            staticVariables.usbData.clear()
        if(osCheckboxInput.get()=="Off"):
            staticVariables.winVerData.clear()
        if(installedApplicationsCheckboxInput.get()=="Off"):
            staticVariables.uninstallData.clear()
        if(userAccountsCheckboxInput.get()=="Off"):
            staticVariables.userData.clear()
        if(networkCardsCheckboxInput.get()=="Off"):
            staticVariables.networkCardsData.clear()
        if(userGroupsCheckboxInput.get()=="Off"):
            staticVariables.groupData.clear()
        if(dhcpCheckboxInput.get()=="Off"):
            staticVariables.dhcpData.clear()
        if(timezoneCheckboxInput.get()=="Off"):
           staticVariables.timezoneData.clear()
        if(systemShutdownCheckboxInput.get()=="Off"):
            staticVariables.shutdownData.clear()
        if(recentDocumentsCheckboxInput.get()=="Off"):
            staticVariables.recentDocumentsData.clear()
        if(recentAppsCheckboxInput.get()=="Off"):
            staticVariables.recentAppsData.clear()
        if(webUrlsCheckboxInput.get()=="Off"):
            staticVariables.webUrlsData.clear()

    else:
        openPopup("ERROR - Registry Hive File Path","No Windows registry hive file path location provided. Please browse for drive/folder","11","bold")


if __name__ == "__main__":
    # create a GUI window
    root = Tk()
    
    # set the background colour of GUI window
    root.configure(background='light blue')

    # set the title of GUI window
    root.title("Windows Registry Analysis Tool")

    # set the configuration of GUI window
    root.geometry("1200x650")
    root.resizable(0,0)


    # create a Form label
    


    # User Input section where file location is taken as input
    frame_input = Frame(root, highlightbackground="dark grey", highlightthickness=2, padx=20, pady=20)
  
    registryPath = Label(frame_input, text="Registry Files Location", pady="5", bg="light blue")
    registryPath.grid(row=0, column=0)
    folder_path=""
    registryPath_field = Entry(frame_input,textvariable=folder_path)
    registryPath_field.configure(state="disabled")
    registryPath_field.grid(row=0, column=1, ipadx="80", ipady="5")
    browse_button = Button(frame_input, text="Browse", fg="Black",
                    bg="Grey",font=("Calibri, 8"), command=browse_dialogue)
    browse_button.grid(row=0, column=2, ipady="0")
    frame_input.place(relx=0.01, rely=0.01)
    
    #frame_filepath = Frame(root, highlightbackground="dark grey", 
    # highlightthickness=2, padx=0, pady=10)

    heading_Output_location = Label(frame_input, text="Selected Registry Hive File Paths (shows after selection)")
    heading_spacefiller = Label(frame_input, text="         ")
    heading_spacefiller1 = Label(frame_input, text="         ")
    heading_spacefiller2 = Label(frame_input, text="         ")
    heading_spacefiller3 = Label(frame_input, text="         ")
    heading_spacefiller.grid (row=3, column=1)
    heading_Output_location.grid(row=4, column=1)
    Software_hive = Label(frame_input, text="SOFTWARE hive : ", bg="light blue")
    System_hive = Label(frame_input, text="SYSTEM hive : ", bg="light blue")
    Sam_hive = Label(frame_input, text="SAM hive : ", bg="light blue")
    Ntuser_hive = Label(frame_input, text="NTUSER hive : ", bg="light blue")
    software_hive_output = Label(frame_input, text="",wraplength=300)
    system_hive_output = Label(frame_input, text="",wraplength=300)
    sam_hive_output = Label(frame_input, text="",wraplength=300)
    ntuser_hive_output = Label(frame_input, text="",wraplength=300)
    Software_hive.grid(row=6, column=0)
    heading_spacefiller1.grid(row=5, column=0)
    System_hive.grid(row=7, column=0)
    Sam_hive.grid(row=9, column=0)
    Ntuser_hive.grid(row=11, column=0)
    software_hive_output.grid(row=6, column=1)
    system_hive_output.grid(row=7, column=1)
    sam_hive_output.grid(row=9, column=1)
    ntuser_hive_output.grid(row=11, column=1)



    frame_checkbox = Frame(root, highlightbackground="dark grey", 
    highlightthickness=2, padx=105, pady=2)
    frame_checkbox.place(relx=0.01, rely=0.425)
    heading_Select_Options = Label(frame_checkbox, text="Select Pre-defined Extracts")
    spacefiller1 = Label(frame_checkbox, text="       ")
    usbLabel = Label(frame_checkbox, text="USB Devices", bg="light blue")
    osLabel = Label(frame_checkbox, text="Operating System", bg="light blue")
    networkCardsLabel = Label(frame_checkbox, text="Network Cards", bg="light blue")
    accessPointsLabel = Label(frame_checkbox, text="Installed Softwares", bg="light blue")
    userAccountsLabel = Label(frame_checkbox, text="User Accounts", bg="light blue")
    userGroupsLabel = Label(frame_checkbox, text="User Groups", bg="light blue")
    dhcpLabel = Label(frame_checkbox, text="DHCP", bg="light blue")
    timezoneLabel= Label(frame_checkbox, text="Computer Timezone", bg="light blue")
    systemShutdownLabel = Label(frame_checkbox, text="Last Shutdown Time", bg="light blue")
    recentDocumentsLabel= Label(frame_checkbox, text="Recent Documents", bg="light blue")
    recentAppsLabel = Label(frame_checkbox, text="Recent Applications", bg="light blue")
    webUrlsLabel = Label(frame_checkbox, text="Recent Web URLs", bg="light blue")
    selectall = Label(frame_checkbox, text="Select All", bg="light blue")


    usbCheckboxInput = StringVar()
    osCheckboxInput = StringVar()
    networkCardsCheckboxInput = StringVar()
    installedApplicationsCheckboxInput = StringVar()
    userAccountsCheckboxInput = StringVar()
    userGroupsCheckboxInput = StringVar()
    dhcpCheckboxInput = StringVar()
    timezoneCheckboxInput = StringVar()
    systemShutdownCheckboxInput = StringVar()
    recentDocumentsCheckboxInput = StringVar()
    webUrlsCheckboxInput= StringVar()
    recentAppsCheckboxInput = StringVar()
    selectAllCheckboxInput = StringVar()
    usbCheckbox = Checkbutton(frame_checkbox,variable=usbCheckboxInput,onvalue="On",offvalue="Off", bg="light blue" ,command=comboBoxControlMain)
    usbCheckbox.deselect()
    osCheckbox = Checkbutton(frame_checkbox,variable=osCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    osCheckbox.deselect()
    networkCardsCheckbox = Checkbutton(frame_checkbox,variable=networkCardsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    networkCardsCheckbox.deselect()
    installedApplicationsCheckbox = Checkbutton(frame_checkbox,variable=installedApplicationsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    installedApplicationsCheckbox.deselect()
    userAccountsCheckbox = Checkbutton(frame_checkbox,variable=userAccountsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    userAccountsCheckbox.deselect()
    userGroupsCheckbox = Checkbutton(frame_checkbox,variable=userGroupsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    userGroupsCheckbox.deselect()
    dhcpCheckbox = Checkbutton(frame_checkbox,variable=dhcpCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    dhcpCheckbox.deselect()
    timezoneCheckbox = Checkbutton(frame_checkbox,variable=timezoneCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    timezoneCheckbox.deselect()
    systemShutdownCheckbox = Checkbutton(frame_checkbox,variable=systemShutdownCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    systemShutdownCheckbox.deselect()
    recentDocumentsCheckbox = Checkbutton(frame_checkbox,variable=recentDocumentsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    recentDocumentsCheckbox.deselect()
    recentAppsCheckbox = Checkbutton(frame_checkbox,variable=recentAppsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    recentAppsCheckbox.deselect()
    webUrlsCheckbox = Checkbutton(frame_checkbox,variable=webUrlsCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=comboBoxControlMain)
    webUrlsCheckbox.deselect()
    selectallCheckbox = Checkbutton(frame_checkbox,variable=selectAllCheckboxInput,onvalue="On",offvalue="Off", bg="light blue",command=selctAllControlMain)
    selectallCheckbox.deselect()

    
    frame_result = Frame(root, width=480, height=500, highlightbackground="dark grey", highlightthickness=2, padx=5, pady=5)
    resultsLabel = Label(frame_result, text="RESULTS",font=("Calibri","16"))
    resultsLabel.pack()


    frame_result.place(relx=0.42, rely=0.01)

    v=Scrollbar(frame_result, orient='vertical')
    v.pack(side=RIGHT, fill='y')


    textarea=Text(frame_result, yscrollcommand=v.set,height=31)

    
    v.config(command=textarea.yview)
    textarea.pack()

  
    heading_Select_Options.grid(row=5, column=3)
    usbCheckbox.grid(row=10,column=7)
    osCheckbox.grid(row=11,column=7)
    networkCardsCheckbox.grid(row=12,column=7)
    installedApplicationsCheckbox.grid(row=13,column=7)
    userAccountsCheckbox.grid(row=14,column=7)
    userGroupsCheckbox.grid(row=15,column=7)
    dhcpCheckbox.grid(row=16,column=7)
    timezoneCheckbox.grid(row=17,column=7)
    systemShutdownCheckbox.grid(row=18,column=7)
    recentDocumentsCheckbox.grid(row=19,column=7)
    recentAppsCheckbox.grid(row=20,column=7)
    webUrlsCheckbox.grid(row=21,column=7)
    selectallCheckbox.grid(row=22,column=7)

    usbLabel.grid(row=10,column=0)
    osLabel.grid(row=11,column=0)
    networkCardsLabel.grid(row=12,column=0)
    accessPointsLabel.grid(row=13,column=0)
    userAccountsLabel.grid(row=14,column=0)
    userGroupsLabel.grid(row=15,column=0)
    dhcpLabel.grid(row=16,column=0)
    timezoneLabel.grid(row=17,column=0)
    systemShutdownLabel.grid(row=18,column=0)
    recentDocumentsLabel.grid(row=19,column=0)
    recentAppsLabel.grid(row=20,column=0)
    webUrlsLabel.grid(row=21,column=0)
    selectall.grid(row=22,column=0)

    frame_report = Frame(root, highlightbackground="dark grey", 
    highlightthickness=2, padx=156, pady=12.5)
    frame_report.place(relx=0.42, rely=0.85)
    submit = Button(frame_report, text="Generate Report", fg="Black",
                    bg="Grey",font=("Calibri, 18"),padx=80, command=fileDialogue)
    submit.grid(row=0, column=1)

    # start the GUI
    root.mainloop()