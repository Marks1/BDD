__author__ = 'marks_shen'

from behave import *
import time
import string
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

import sys
sys.path.append("..\..\..\libs")
import conf

@given('i have login DDEI hidden page')
def step_impl(context):
    if context.browser.title == 'Deep Discovery Email Inspector':
        #already login
        #print('already login.')
        return
    context.browser.get(context.hiddenweb)
    try:
        WebDriverWait(context.browser, 10).until(EC.title_contains("Deep Discovery Email Inspector Login"))
    except:
        context.browser.quit()

    try:
        context.browser.find_element_by_id("password").clear()
        context.browser.find_element_by_id("password").send_keys("ddei")
        context.browser.find_element_by_id("login_btn").click()
        time.sleep(2)
        #print('done login')
    except:
        context.browser.quit()


@when('switch to "{hidden_tab}" tab')
def step_impl(context, hidden_tab):
    print "@@@@%s" % hidden_tab

    if hidden_tab == 'Timeout setting':
        element = "timeout_setting"
    if hidden_tab == 'URL Extraction Setting':
        element = 'url_extract'
    try:
        context.browser.switch_to_default_content()
        context.browser.switch_to_frame("left")
        context.browser.find_element_by_id(element).click()
        context.browser.switch_to_default_content()
        context.browser.switch_to_frame("right")
        time.sleep(2)
    except:
        context.browser.quit()

@then('the timeout value of {who} should be {value} minutes')
def step_impl(context, who, value):
    #print "@@@@%s" % value
    if 'Password' in who:
        current_time = context.browser.find_element_by_id("timeout_password").get_attribute("value")
        if current_time != value:
            raise AssertionError('%s default value(%s) is not %s' % (who, current_time, value))
    elif 'VA' in who:
        current_time = context.browser.find_element_by_id("timeout_va").get_attribute("value")
        if current_time != value:
            raise AssertionError('%s default value(%s) is not %s' % (who, current_time, value))
    else:
        raise AssertionError("General error!%s" % context.active_outline )

@given('Input a value "{value}" into {timeout_type} timeout setting')
def step_impl(context, value, timeout_type):
    print("value=%s" % value)
    if 'password' in timeout_type:
        context.timeout_who = 'password'
    elif 'VA' in timeout_type:
        context.timeout_who = 'VA'
    else:
        raise AssertionError("General error!%s" % context.active_outline )

    try:
        context.browser.find_element_by_id("timeout_password")
    except:
        #print("switch to setting page")
        context.execute_steps(u'''
            when switch to "Timeout setting" tab
        ''')
    context.execute_steps(u'''
        when switch to "Timeout setting" tab
    ''')
    if context.timeout_who == 'password':
        context.timeout_value_password = value
        #get original before apply apply new one
        context.timeout_original_value_password = context.browser.find_element_by_id('timeout_password').get_attribute("value")
        context.browser.find_element_by_id("timeout_password").clear()
        if value != 'null':
            context.browser.find_element_by_id("timeout_password").send_keys(value)
        #get password analysis PID at backend
        context.PA_originalPID = context.keyword.exec_command_on_DDEI("ps -ef | grep passwordAnalyzer | grep -v grep | awk '{print $2}'")

    if context.timeout_who == 'VA':
        context.timeout_value_va = value
        context.timeout_original_value_va = context.browser.find_element_by_id('timeout_va').get_attribute("value")
        context.browser.find_element_by_id("timeout_va").clear()
        if value != 'null':
            context.browser.find_element_by_id("timeout_va").send_keys(value)
        context.VA_originalPID = context.keyword.exec_command_on_DDEI("ps -ef | grep task_monitor | grep -v grep | awk '{print $2}'")


@when('I click save')
def step_impl(context):
    context.keyword.exec_command_on_DDEI('echo > /opt/trend/ddei/config/password_bank_file.conf')
    try:
        context.browser.find_element_by_id("btn_save")
    except:
        context.execute_steps('''
            when switch to "Timeout setting" tab
        ''')
    context.browser.find_element_by_id("btn_save").click()
    #wait for saving complete
    time.sleep(2)

@then('User can be infoed that the saving is {result_info}')
def step_impl(context, result_info):
    result = context.browser.find_element_by_id("flag").text
    if 'Saving' in result:
        time.sleep(5)
        result = context.browser.find_element_by_id("flag").text

    failinfo_password = 'The timeout value of Password Analyzer should be between 0 and 60.'
    failinfo_va = 'The timeout value of Virtual Analyzer should be between 5 and 2880.'
    print "User can be infoed that the saving is >%s, result on UI %s" % (result_info, result)
    if result == '':
        raise AssertionError('There is no information after click save')
    else:
        if ('success' in result_info) and ('Saved OK.' != result):
            raise AssertionError('Timeout setting information (%s) is not as expected' % result)
        if 'failed' in result_info:
            if (context.timeout_who == 'password') and (failinfo_password != result):
                raise AssertionError('Timeout setting information (%s) is not as expected' % context.timeout.who)
            if (context.timeout_who == 'VA') and (failinfo_va != result):
                raise AssertionError('Timeout setting information (%s) is not as expected' % context.timeout.who)
        if ('success' not in result_info) and ('failed' not in result_info):
            raise AssertionError("General error!%s" % context.active_outline )


@then('UI shows the new value after reenter this setting page')
def step_impl(context):
    context.execute_steps(u'''
            when switch to "Timeout setting" tab
        ''')
    if context.timeout_who == 'password':
        temp = context.browser.find_element_by_id('timeout_password').get_attribute("value")
        if context.timeout_value_password != temp:
            raise  AssertionError ('% value is not saved' % context.timeout_who)

    elif context.timeout_who == 'VA':
        temp = context.browser.find_element_by_id('timeout_va').get_attribute("value")
        if context.timeout_value_va != temp:
            raise  AssertionError ('% value is not saved' % context.timeout_who)

    else:
        raise AssertionError("General error!%s" % context.active_outline )


@then('UI shows the original value after reenter this setting page')
def step_impl(context):
    context.execute_steps(u'''
            when switch to "Timeout setting" tab
        ''')
    if context.timeout_who == 'password':
        temp = context.browser.find_element_by_id('timeout_password').get_attribute("value")
        print "temp = %s" % temp
        if context.timeout_original_value_password != temp:
            raise  AssertionError ('Invalide % value should not be saved' % context.timeout_who)

    elif context.timeout_who == 'VA':
        temp = context.browser.find_element_by_id('timeout_va').get_attribute("value")
        if context.timeout_original_value_va != temp:
            raise  AssertionError ('Invalide % value should not be saved' % context.timeout_who)

    else:
        raise AssertionError("General error!%s" % context.active_outline )


@then('DDEI take the new value as timeout')
def step_impl(context):
    if context.timeout_who == 'password':
        check_password_timeout_backend(context, context.timeout_value_password)
        pid_should_change(context, 'PA')
    elif context.timeout_who == 'VA':
        check_va_timeout_backend(context, context.timeout_value_va)
        pid_should_change(context, 'VA')
    else:
        raise AssertionError("General error!%s" % context.active_outline )


@then('DDEI still use original value')
def step_impl(context):
    if context.timeout_who == 'password':
        check_password_timeout_backend(context, context.timeout_original_value_password)
        pid_should_not_change(context, 'PA')
    elif context.timeout_who == 'VA':
        check_va_timeout_backend(context, context.timeout_original_value_va)
        pid_should_not_change(context, 'VA')
    else:
        raise AssertionError("General error!%s" % context.active_outline )


#check the value at backend
def check_va_timeout_backend(context, va_time):
    #read the imss.ini
    print "va_time: %s" % va_time
    imss_ini = '/opt/trend/ddei/config/imss.ini'
    shell_cmd = "cat %s | grep sandbox_task_timeout | awk -F '=' '{print $2}'" % imss_ini
    actual_value = context.keyword.exec_command_on_DDEI(shell_cmd)
    if string.atoi(va_time)*30 != string.atoi(actual_value):
        raise AssertionError ('VA timeout in DDEI config(%d) != %d' % (string.atoi(actual_value),string.atoi(va_time)*30))

    #check

def check_password_timeout_backend(context, va_time):
    #read the imss.ini
    imss_ini = '/opt/trend/ddei/config/imss.ini'
    shell_cmd = "cat %s | grep time_out_second | awk -F '=' '{print $2}'" % imss_ini
    actual_value = context.keyword.exec_command_on_DDEI(shell_cmd)
    if string.atoi(va_time)*60 != string.atoi(actual_value):
        raise AssertionError ('password timeout in DDEI config(%d) != %d' % (string.atoi(actual_value),string.atoi(va_time)*60))

def pid_should_change(context, who):
    if who == 'PA':
        currentPID = context.keyword.exec_command_on_DDEI("ps -ef | grep passwordAnalyzer | grep -v grep | awk '{print $2}'")
        #check PA PID
        i=0
        while context.PA_originalPID == currentPID:
            time.sleep(1)
            i = i+1
            currentPID = context.keyword.exec_command_on_DDEI("ps -ef | grep passwordAnalyzer | grep -v grep | awk '{print $2}'")
            if i>= 10:
                break
        if i >=10:
            raise AssertionError('Password analysis PID(%s) does not change after apply ' % context.PA_originalPID)

    if who == 'VA':
        currentPID = context.keyword.exec_command_on_DDEI("ps -ef | grep task_monitor | grep -v grep | awk '{print $2}'")
        i=0
        while context.VA_originalPID == currentPID:
            time.sleep(1)
            currentPID = context.keyword.exec_command_on_DDEI("ps -ef | grep task_monitor | grep -v grep | awk '{print $2}'")
            i = i+1
            if i>= 70:
                break
        if i >=70:
            raise AssertionError('Virtual analysis PID(%s) does not change after apply ' % context.VA_originalPID)


def pid_should_not_change(context, who):
    if who == 'PA':
        #check PA PID
        i=0
        while i<10:
            newpid = context.keyword.exec_command_on_DDEI("ps -ef | grep passwordAnalyzer | grep -v grep | awk '{print $2}'")
            if context.PA_originalPID != newpid:
                raise AssertionError('Password analysis PID(%s) change after apply' % newpid)
            time.sleep(1)
            i = i+1
        if newpid == '':
            raise AssertionError('Password analysis process does not start')
    if who == 'VA':
        #check VA PID
        i=0
        while i<30:
            newpid = context.keyword.exec_command_on_DDEI("ps -ef | grep task_monitor | grep -v grep | awk '{print $2}'")
            if context.VA_originalPID != newpid:
                raise AssertionError('Virtual analysis PID(new %s, old %s) change after apply' % (newpid, context.VA_originalPID))
            time.sleep(1)
            i = i+1
        if newpid == '':
            raise AssertionError('Virtual analysis process does not start')

@given('i have setup password extraction timeout as {time_value} minute')
def step_impl(context, time_value):
    context.execute_steps(u'''
            Given i have login DDEI hidden page
            and Input a value "%s" into password extraction timeout setting
            When I click save
            Then DDEI take the new value as timeout
        ''' % time_value)
    context.timeout_value_password = time_value
    time.sleep(5) #wait to apply at backend

@given('i have setup VA timeout as {time_value} minute')
def step_impl(context,  time_value):
    context.execute_steps(u'''
            Given i have login DDEI hidden page
            and Input a value "%s" into VA timeout setting
            When I click save
            Then DDEI take the new value as timeout
        ''' % time_value)
    context.timeout_value_va = time_value
    time.sleep(5) #wait to apply at backend

@given('send out a mail with virus in password-protected archive')
def step_impl(context):

    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, 'C:\BVT\TestDDEI\BDD\DDEI\mail_sample\\attachment_with_password.eml', 'marks@sender.com')

@when('i send out a suspicious mail, which will make VA timeout')
def step_impl(context):

    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, 'C:\BVT\TestDDEI\BDD\DDEI\mail_sample\\VA_timeout.eml', 'marks@sender.com')

@when('i send out a suspicious mail, which could finish analysis before timeout')
def step_impl(context):
    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, 'C:\BVT\TestDDEI\BDD\DDEI\mail_sample\\VA_high.eml', 'marks@sender.com')

@when('wait for timeout')
def step_impl(context):
    print("sleep %s minutes for VA timeout" % context.timeout_value_va)
    time.sleep(string.atoi(context.timeout_value_va)*60)

@when('i send the mail containing the password {sec:d} second after the timeout')
def step_impl(context, sec):
    #sleep 10 seconds already in sendmail keyword
    real_sleep = string.atoi(context.timeout_value_password) * 60 + sec - 10
    if real_sleep < 0:
        real_sleep = 0
    time.sleep(real_sleep)
    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, "C:\BVT\TestDDEI\BDD\DDEI\mail_sample\password.eml", 'marks@sender.com')

@when('i send the mail containing the password {sec:d} second before timeout')
def step_impl(context, sec):
    real_sleep = string.atoi(context.timeout_value_password) * 60 - sec - 10
    if real_sleep < 0:
        real_sleep = 0
    time.sleep(real_sleep)
    context.keyword.send_one_email(conf.MAIL_TO, conf.SMTP_SERVER, "C:\BVT\TestDDEI\BDD\DDEI\mail_sample\password.eml", 'marks@sender.com')


@then('The mail could not be detected')
def step_impl(context):
    detection_cnt = context.keyword.get_log_count_on_DDEI('tb_policy_event_total')
    print "detection: %s" % detection_cnt
    if detection_cnt !='0':
        raise AssertionError('this mail should not be detected')

@then('The mail could be detected')
def step_impl(context):
    context.keyword.email_should_be_quarantined()