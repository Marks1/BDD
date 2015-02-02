__author__ = 'Marks Shen'


from behave import *
import time
import os
import shutil
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.by import By
#from common_utility import common_utility
import sys
sys.path.append("..\..\..\libs")
import conf


@given('malicious {URL} in a {file}')
def step_impl(context, URL, file):
    fileExt= context.tool.getFileType(file.strip()).lower()

    print "fileExt = %s" % fileExt
    #create the doc sample
    targetFile = "%s\\mail_sample\\%s" % (os.getcwd(), file)
    print "PDF file = %s" % targetFile
    if fileExt != 'pdf':
        context.tool.createOfficebyURL(fileExt, targetFile, URL)
    if fileExt == 'pdf':
        htmlTemp = "%s\\steps\\PDF\\pdf_temp.html" % os.getcwd()
        context.tool.createPDFbyURL(htmlTemp, URL, targetFile)

    context.targetDoc.append(targetFile)

    context.mail_path = "%s\\mail_sample\\mailTemp.txt" % os.getcwd()

@given('unrated {URL} in a {file}')
def step_impl(context, URL, file):
    context.execute_steps(u'''
        given malicious %s in a %s
    ''' % (URL, file))

@given('{num} URLs in mail body')
def step_impl(context, num):
    #modify the mailtemp.txt
    temp = "%s\\mail_sample\\mailTemp2.txt" % os.getcwd()
    shutil.copyfile(context.mail_path, temp)

    URL = ''
    for i in range(50, 50+int(num)):
        URL = URL + 'http://wrs%s.winshipway.com;\n' % i
    print "%s" % URL

    context.tool.createMailbyURL(context.mail_path, temp, URL)

    context.mail_path = temp



@when('This file is attached in mail and going through DDEI')
def step_impl(context):
    #context.keyword.wait_until_usandbox_is_ready()
    context.tool.sendMailwithAttachment('marks@sender.com', conf.MAIL_TO, conf.SMTP_SERVER, context.mail_path, context.targetDoc)

@then('This mail should be detected out by {who}')
def step_impl(context, who):
    #check if the sample is detected out
    sleep_time = 300
    temp_timeout_cnt = 10
    while True:
        cmd = "%s 'select %s from %s'" % (conf.PSQL_EXE,'overall_severity','tb_policy_event_total')
        value = context.keyword.ssh_conn.execute_command(cmd)
        value = value.strip()
        if not value:
            time.sleep(5)
            temp_timeout_cnt -= 1
            if temp_timeout_cnt <=0:
                raise  AssertionError("Timeout for waiting policy event record generation")
            continue
        if value != '4' or sleep_time <= 0:
            break
        time.sleep(5)
        sleep_time -= 5
    print "value = %s" % value
    #raise AssertionError("Cannot wait for VA analysis, it takes too long")

    if sleep_time <=0:
        raise AssertionError("Cannot wait for VA analysis, it takes too long")

    cmd = "%s 'select %s from %s'" % (conf.PSQL_EXE,'threat_type','tb_policy_event_total')
    threat_type = context.keyword.ssh_conn.execute_command(cmd)
    print("overall_secrity = %s; threat_type = %s" % (value, threat_type.strip()))

    if who is 'WRS' and threat_type.strip() != '3':
        raise AssertionError("This detection is not detected by WRS!")
    if who is 'VA' and threat_type.strip() != '5':
        raise AssertionError("This detection is not detected by VA!")


@then('This URL should be extracted and sent to VA for analysis')
def step_impl(context):
    context.execute_steps(u'''
        Then The file dropped from URL will be submitted to VA
    ''')

@given('Total {num} URLs in a {file}')
def step_impl(context, num, file):
    URL = ''
    fileExt= context.tool.getFileType(file.strip()).lower()
    print "!!!!!file type = %s" % fileExt
    for i in range(21, 21+int(num)):
        if fileExt == 'pdf':
            print "!!!!!file type PDF"
            URL = URL + 'http://wrs%s.winshipway.com;<br />' % i
        else:
            URL = URL + 'http://wrs%s.winshipway.com;                ' % i
    print "%s" % URL

    context.execute_steps(u'''
        given malicious %s in a %s
    ''' % (URL, file))


@then('Only {num} URLs are sent to scan')
def step_impl(context, num):
    #get WRS score list in DB
    wait = 10
    while True:
        cmd = "%s 'select %s from %s'" % (conf.PSQL_EXE,'wrs_score_list','tb_policy_event_total')
        value = context.keyword.ssh_conn.execute_command(cmd)
        print "wrs_score_list = [%s]" % value
        value = value.strip()
        if not value:
            time.sleep(2)
            wait -= 1
            if wait <=0:
                raise  AssertionError("Timeout for waiting policy event record generation")
            continue
        else:
            break

    actual_url_num = len(value.strip().split('|'))

    if int(num) != int(actual_url_num):
        raise AssertionError("actual URLs number[%s] from mail is not as expected[%s]" % (actual_url_num, num))


@given('enable Doc_extracted_URL_scan function')
def step_impl(context):
    context.execute_steps(u'''
        Given    i have login DDEI hidden page
        When    switch to "URL Extraction Setting" tab
    ''')

    if not context.browser.find_element_by_id("docurl_enable").is_selected():
        context.browser.find_element_by_id("docurl_enable").click()
        context.browser.find_element_by_id("btn_save_docurl").click()
        WebDriverWait(context.browser, 40).until(EC.text_to_be_present_in_element((By.ID, "flag_docurl"), "Saved OK."))

@then('URL from document check box should be disabled by default')
def step_impl(context):
    if context.browser.find_element_by_id("docurl_enable").is_selected():
        raise AssertionError('doc embeded URL scanning should be disabled by default')

@then('malicious URL in doc should not be detected')
def step_impl(context):
    context.execute_steps(u'''
        Given   malicious %s in a %s
        When    This file is attached in mail and going through DDEI
        Then    This mail should not be detected out by WRS
    ''' % ('http://wrs21.winshipway.com', 'Doc2007WithbedURL.docx'))

@then('This mail should not be detected out by WRS')
def step_impl(context):
    #check if the sample is detected out
    temp_timeout_cnt = 5
    value = ''
    while temp_timeout_cnt >=0 or value == '':
        cmd = "%s 'select count(*) from %s where %s'" % (conf.PSQL_EXE,'tb_policy_event_total', 'threat_type=3')
        value = context.keyword.ssh_conn.execute_command(cmd)
        time.sleep(3)
        temp_timeout_cnt -= 1

    #print "value is [%s]" % value.strip()
    if int(value) != 0:
        raise AssertionError("this sample should not be detected by WRS")

@given('Set max-URL count to {num} on hidden page')
def step_impl(context, num):
    context.execute_steps(u'''
        Given    i have login DDEI hidden page
        When    switch to "URL Extraction Setting" tab
    ''')

    context.browser.find_element_by_id('max_count').clear()
    context.browser.find_element_by_id('max_count').send_keys(num)
    context.browser.find_element_by_id('btn_save_extraction').click()
    result = context.browser.find_element_by_id("flag_docurl").text
    WebDriverWait(context.browser, 40).until(EC.text_to_be_present_in_element((By.ID, "flag_extraction"), "Saved OK."))
