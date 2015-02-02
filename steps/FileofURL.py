__author__ = 'Marks Shen'


from behave import *
import time
import string
import os
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.by import By
from common_utility import common_utility

import sys
sys.path.append("..\..\..\libs")
import conf


@given('{urls} in mail could possibly drop a {malicious} file')
def step_impl(context, urls, malicious):
    tool = common_utility(context)
    print "CWD = %s" % os.getcwd()
    context.tempmail = '%s\\mail_sample\\mailTemp.txt' % os.getcwd()
    context.mailsample = '%s\\mail_sample\\urldirectedfile.eml' % os.getcwd()
    context.targetURL = urls.strip()
    tool.createMailbyURL(context.tempmail,context.mailsample,context.targetURL)


@given('Set VA customize file type to default')
def step_impl(context):
    #WIN_EXE only by default
    context.keyword.clear_custom_file_type()
    context.keyword.add_custom_file_type(conf.VA_FILE_TYPE_EXE)

@given('A {save_urls} in mail that is not possible to drop a malicious file')
def step_impl(context, save_urls):
    tool = common_utility(context)
    context.tempmail = '%s\\mail_sample\\mailTemp.txt' % os.getcwd()
    context.mailsample = '%s\\mail_sample\\urldirectedfile.eml' % os.getcwd()
    context.targetURL = save_urls.strip()
    tool.createMailbyURL(context.tempmail,context.mailsample,context.targetURL)

@given('switch to "{hidden_tab}" tab')
def step_impl(context, hidden_tab):
    print "@@@@%s" % hidden_tab
    if hidden_tab == 'URL Filter Setting':
        print "aaa"
        try:
            context.browser.switch_to_default_content()
            context.browser.switch_to_frame("left")
            context.browser.find_element_by_id("url_filter").click()
            context.browser.switch_to_default_content()
            context.browser.switch_to_frame("right")
            time.sleep(2)
        except:
            context.browser.quit()

@given('The time to download the file exceeds the "{conn_timeout_value}" and "{timeout_value}"')
def step_impl(context, conn_timeout_value, timeout_value):
    context.execute_steps(u'''
        Given    i have login DDEI hidden page
        And    switch to "URL Filter Setting" tab
        when Set connection Timeout setting value to "%s"
        when set download Timeout setting value to "%s"
        when Set File size setting value to "4"
        Then    New value should be accepted by UI and saved
    ''' % (conn_timeout_value, timeout_value))


@given('The dropped file size exceeds the "{Max_filesize_value}"')
def step_impl(context, Max_filesize_value):
    context.execute_steps(u'''
        Given    i have login DDEI hidden page
        And    switch to "URL Filter Setting" tab
        when Set connection Timeout setting value to "20"
        when set download Timeout setting value to "100"
        when Set File size setting value to "%s"
        Then    New value should be accepted by UI and saved
    ''' % Max_filesize_value)

@given('Dropped file "{filetype}" is configured to {whether} forcedly submitted to VA')
def step_impl(context, filetype, whether):
    print "@@@@@@@@@@@@@@@@@@ %s" % filetype
    if whether.strip() == 'be':
        context.keyword.clear_custom_file_type()
        if filetype.strip() == 'PDF':
            context.keyword.add_custom_file_type(conf.VA_FILE_TYPE_PDF)
        if filetype.strip() == 'EXE':
            context.keyword.add_custom_file_type(conf.VA_FILE_TYPE_EXE)
    elif whether.strip() == 'be not':
        context.keyword.clear_custom_file_type()
    else:
        raise AssertionError("incorrect feature description!")

    NOTIFY_CMD="kill -HUP $( cat /opt/trend/ddei/bin/task_processor.pid )"

    context.keyword.exec_command_on_DDEI(NOTIFY_CMD)


@when('This URL is included in mail and going through DDEI')
def step_impl(context):
    #context.keyword.wait_until_usandbox_is_ready()
    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, context.mailsample, 'marks@sender.com')


@when('Set connection Timeout setting value to "{conn_timeout_value}"')
def step_impl(context, conn_timeout_value):
    print("value=%s" % conn_timeout_value)
    context.conn_time = conn_timeout_value


    context.browser.find_element_by_id("timeout_conn").clear()
    if conn_timeout_value.strip() != 'null':
        context.browser.find_element_by_id("timeout_conn").send_keys(conn_timeout_value)

@when('set download Timeout setting value to "{download_timeout_value}"')
def step_impl(context, download_timeout_value):
    print("value=%s" % download_timeout_value)
    context.download_time = download_timeout_value

    context.browser.find_element_by_id("timeout_download").clear()
    if download_timeout_value.strip() != 'null':
        context.browser.find_element_by_id("timeout_download").send_keys(download_timeout_value)


@when('Set File size setting value to "{Max_filesize_value}"')
def step_impl(context, Max_filesize_value):
    print("value=%s" % Max_filesize_value)
    context.file_size = Max_filesize_value
    #enable the function first

    context.browser.find_element_by_id("timeout_size").clear()
    if Max_filesize_value.strip() != 'null':
        context.browser.find_element_by_id("timeout_size").send_keys(Max_filesize_value)


#unused
@then('Content of this URL will {option} be downloaded')
def step_impl(context, option):
    print "option = %s" % option
    if option == '':
        #method to check the dowload actitivy will be determined later
        date_str = time.strftime('%Y%m%d',time.localtime(time.time()))
        policy_eventlog = '/opt/trend/ddei/log/polevt.imss.%s.0001' % date_str
        shell_cmd = "tail -n 1 %s | awk '{print $4}'" % policy_eventlog
        UUID = context.keyword.exec_command_on_DDEI(shell_cmd)
        print "UUID = %s" % UUID

        #check file under /var/app_data/ddei/queue/sandbox_suspicious/UUID
        filename = 'urldoenload'
        download_filename = '/var/app_data/ddei/queue/sandbox_suspicious/%s/%s' % (UUID, filename)

        if os.path.isfile(download_filename):
            #check content
            print "downloaded"
        else:
            raise AssertionError("File is not downloaded for url[%s]! " % context.targetURL)

@then('New value should {whether} accepted by UI and saved')
def step_impl(context, whether):

    #context.browser.find_element_by_xpath("//li[@id='btn_save']/span").click()
    context.browser.find_element_by_id("btn_save_timeout").click()
    time.sleep(1)
    if whether.strip() == 'be':
        result = context.browser.find_element_by_id("flag_timeout").text
        max_wait = 10
        while 'Saving' in result and max_wait >=0:
            time.sleep(5)
            max_wait -= 1
            result = context.browser.find_element_by_id("flag_timeout").text
        if 'Saved OK.' != result.strip():
            raise AssertionError('Timeout/File size setting information (%s) is not as expected' % result)
        #check value on UI after refresh the page
        context.execute_steps(u'''
            given switch to "URL Filter Setting" tab
        ''')
        if context.conn_time != context.browser.find_element_by_id("timeout_conn").get_attribute("value") \
                or context.download_time != context.browser.find_element_by_id("timeout_download").get_attribute("value") \
                or context.file_size != context.browser.find_element_by_id("timeout_size").get_attribute("value"):
            raise AssertionError("UI refresh does not reflect the change")

    if whether.strip() == 'not be':
        result = context.browser.find_element_by_id("flag_timeout").text
        #to find some invalid value is accpected by UI
        max_wait = 10
        while 'Saving' in result and max_wait >=0:
            time.sleep(5)
            max_wait -= 1
            result = context.browser.find_element_by_id("flag_timeout").text
        #time.sleep(1)
        #raise AssertionError("!!!!! %s" % result)
        if 'Saved OK.' == result.strip():
            raise AssertionError('Timeout/File size setting information (%s) is not as expected' % result)

@then('The file dropped from URL will {whether} detected out by VA')
def step_impl(context, whether):
    #check policy event log
    print "whether = %s" % whether

    #check if the sample is detected out
    sleep_time = 300 #upto 5 minutes waiting for VA
    temp_timeout_cnt = 5
    while True:
        cmd = "%s 'select %s from %s'" % (conf.PSQL_EXE,'overall_severity','tb_policy_event_total')
        value = context.keyword.ssh_conn.execute_command(cmd)
        value = value.strip()
        if value is None:
            time.sleep(5)
            temp_timeout_cnt -= 1
            if temp_timeout_cnt <=0:
                raise  AssertionError("Timeout for waiting policy event record generation")
            continue
        if value != '4' or sleep_time <= 0:
            break
        time.sleep(5)
        sleep_time -= 5

    cmd = "%s 'select %s from %s'" % (conf.PSQL_EXE,'threat_type','tb_policy_event_total')
    threat_type = context.keyword.ssh_conn.execute_command(cmd)
    print("overall_secrity = %s; threat_type = %s" % (value, threat_type.strip()))

    if sleep_time <=0:
        raise AssertionError("Cannot wait for VA analysis, it takes too long")

    if whether.strip() == 'be':
        if value.strip() not in ['1','2','3']:
            raise AssertionError("VA did not detect out, while this sample should be detected!")
        if int(threat_type.strip()) != 5:
            raise AssertionError("This detection is not detected by VA!")
    elif whether.strip() == 'not be':
        if int(value.strip()) != 0:
            raise AssertionError("VA detect out, while this sample should not be detected!")
    else:
        raise  AssertionError("Incorrect feature definition sentence.")

@then('The file dropped from URL will {whether} submitted to VA')
def step_impl(context, whether):
    #check whether sandbox finish analyzing
    sleep_time = 60
    while True:
        cmd = "%s 'select count(%s) from %s where task_id !=0'" % (conf.PSQL_EXE, 'task_id','tb_sandbox_task_details')
        task_num = context.keyword.ssh_conn.execute_command(cmd)
        if int(task_num.strip()) != 0 or sleep_time <= 0:
            break
        time.sleep(5)
        sleep_time -= 5

    if whether.strip() == 'be':
        if int(task_num) == 0:
            raise AssertionError("Sample should be submitted in to VA! But NOT in this case!")
    elif whether.strip() == 'not be':
        if int(task_num) != 0:
            cmd = "%s 'select * from %s'" % (conf.PSQL_EXE,'tb_sandbox_task_details')
            print context.keyword.ssh_conn.execute_command(cmd)
            raise AssertionError("Sample should not be submitted in to VA! But reality is not as expect!")
    else:
        raise AssertionError("Incorrect feature definition sentence!")


@then('Detection will be displayed on detection page as "{detection_name}"')
def step_impl(context, detection_name):
    return

@given('The URL response content type "content type" is in DDEI ignore list')
def step_impl(context):
    return

@given('The URL response content type "content type" is in DDEI watch list')
def step_impl(context):
    return

@when('Disable the function')
def step_impl(context):
    if context.browser.find_element_by_id("timeout_enable").is_selected():
        context.browser.find_element_by_id("timeout_enable").click()

    context.browser.find_element_by_id("btn_save_linkedfile").click()

    WebDriverWait(context.browser, 20).until(EC.text_to_be_present_in_element((By.ID, "flag_linkedfile"), "Saved OK."))

@then('Enable the function')
def step_impl(context):
    if not context.browser.find_element_by_id("timeout_enable").is_selected():
        context.browser.find_element_by_id("timeout_enable").click()

    context.browser.find_element_by_id("btn_save_linkedfile").click()

    WebDriverWait(context.browser, 20).until(EC.text_to_be_present_in_element((By.ID, "flag_linkedfile"), "Saved OK."))

@when('Sand a mail with {url} that will drop suspicious file')
def step_impl(context, url):
    context.execute_steps(u'''
        Given   %s in mail could possibly drop a malicious file
        And     Set VA customize file type to default
        When    This URL is included in mail and going through DDEI
    ''' % url.strip() )

@then('This file detection will be the child of the URL')
def step_impl(context):
    cmd = "%s 'select %s from %s where parent_sha1 !='''" % (conf.PSQL_EXE,'parent_sha1','tb_sandbox_report_file_analyze')
    parent_sha1 = context.keyword.ssh_conn.execute_command(cmd)
    parent_sha1 = parent_sha1.strip()

    cmd = "%s 'select %s from %s where parent_sha1 ='''" % (conf.PSQL_EXE,'file_sha1','tb_sandbox_report_file_analyze')
    url_sha1 = context.keyword.ssh_conn.execute_command(cmd)
    url_sha1 = url_sha1.strip()

    if parent_sha1 != url_sha1:
        print("url_sha1 = %s; file's parent sha1=%s", (url_sha1, parent_sha1))
        raise  AssertionError("relationship is incorrect in VA report")
