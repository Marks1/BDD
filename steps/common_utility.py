__author__ = 'Marks Shen'

import os
import shutil
import time
import subprocess
import sys
sys.path.append("..\..\..\libs")
import conf

class common_utility():

    def __init__(self,context):
        self.context = context

    def createPDFbyURL(self, htmlTemp, url, pdfFile):
        try:
            self.ftemp = open(htmlTemp, 'r')
            self.mailcontent = self.ftemp.read()
            self.ftemp.close()

        except:
            raise AssertionError("Cannot find html template for pdf generation! %s" % htmlTemp)

        try:
            srcHtml = "%s\\mail_sample\\srcHtml.html" % os.getcwd()
            print "html = %s" % srcHtml
            self.pdf = open(srcHtml, 'wb')
            self.pdf.write(self.mailcontent.replace('DDEI_TEST_URL', url))
            self.pdf.close()
        except:
            raise AssertionError("Cannot create html sample for url[%s]! " % url)

        #generate pdf
        cmd = "%s\\steps\\PDF\\runner.exe pdf %s %s" % (os.getcwd(), srcHtml, pdfFile)
        os.system(cmd)

        print("sample PDF is created successfully at %s" % pdfFile)

    def createOfficebyURL(self, docType, targetDoc, url):
       #revise the copy as affected document
        #print "URL for doc generation  = [%s]" % url
        if docType in ['docx', 'pptx', 'xlsx']:
            #create a copy of docTemp
            try:
                shutil.copyfile("%s\\steps\\PDF\\template.%s" % (os.getcwd(), docType.strip()), targetDoc)
            except:
                raise AssertionError("Cannot find template.%s template for doc generation!" % docType)
            cmd = "%s\\steps\\PDF\\runner.exe %s %s %s \"%s\"" % (os.getcwd(), docType, targetDoc, 'DDEI_TEST_URL', url)
            os.system(cmd)
        elif docType in ['doc', 'ppt', 'xls']:
            try:
                shutil.copyfile("%s\\steps\\PDF\\template.%s" % (os.getcwd(), docType.strip()), targetDoc)
            except:
                raise AssertionError("Cannot find template.%s template for doc generation!" % docType)
        else:
            raise AssertionError("[createOfficebyURL] unsupported file type")
        print("sample is created successfully at %s" % targetDoc)

    def getFileType(self, fileName):
        fileName, fileExtension = os.path.splitext(fileName)
        return fileExtension.strip('.')


    def sendMailwithAttachment(self, mail_from, to, smtp_server, mail_path, mail_attachment):
        work_dir = os.path.dirname(mail_path)
        att_str = ''
        for singleAttachment in mail_attachment:
            print "singleAttachment is %s" % singleAttachment
            att_str = att_str + singleAttachment + ';'

        print "attachment is [%s]" % att_str.strip(';')
        send_parameters = ' -PORT=25 -FROM=%s -TO=%s -SMTP=%s %s -Attach=%s' % (mail_from, to, smtp_server, mail_path, att_str.strip(';'))
        send_cmd = conf.TEMAIL_BIN + send_parameters

        save_dir = os.path.abspath(os.curdir)

        os.chdir(work_dir)
        subprocess.Popen(send_cmd, shell = True)

        #time.sleep(10)
        os.chdir(save_dir)


    def createMailbyURL(self,template, destMail, url):
        try:
            #self.ftemp = open(template, 'wb')
            self.ftemp = open(template, 'r')
            self.mailcontent = self.ftemp.read()
            self.ftemp.close()

        except:
            raise AssertionError("Cannot find mail template for testing! %s" % template)

        try:
            self.mail = open(destMail, 'wb')
            self.mail.write(self.mailcontent.replace('TESTURL', url))
            self.mail.close()
        except:
            raise AssertionError("Cannot create mail sample for url[%s]! " % url)

        print("sample mail is created successfully at %s" % destMail)

    def removeMail(self, mailpath):
        try:
            os.remove(mailpath)
        except:
            raise AssertionError("remove temp mail sample fail")


#os.chdir('C:\BVT\TestDDEI\BDD\DDEI')
#aa = 'a'
#tool = common_utility(aa)
#tool.sendMailwithAttachment('marks@test.com', 'marks@get.com', '10.204.253.158', "%s\\mail_sample\\mailTemp.txt" % os.getcwd(), "%s\\mail_sample\\%s" % (os.getcwd(), 'PdfWithbedURL.pdf'))
#targetFile = "C:\BVT\TestDDEI\BDD\DDEI\mail_sample\out.pdf"

#tool.createOfficebyURL('docx', targetFile, 'www.baidu.com')
#htmlTemp = "C:\\BVT\\TestDDEI\\BDD\\DDEI\\steps\\PDF\\pdf_temp.html"
#tool.createPDFbyURL(htmlTemp, 'baidu.com', targetFile)