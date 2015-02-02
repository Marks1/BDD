__author__ = 'Marks Shen'

from selenium import webdriver
import sys
sys.path.append("..\..\libs")
from BVTLibrary import BVTLibrary
import conf

sys.path.append("steps")
import common_utility

def before_feature(context, feature):
    print "prepare for test"
    context.keyword = BVTLibrary()
    context.tool = common_utility.common_utility(context)
    if 'browser' in feature.tags:
        context.browser = webdriver.Firefox()
        context.hiddenweb = 'https://%s/hidden/rdqa.php' % conf.DDEI_IP
    if 'ssh' in feature.tags:
        context.keyword.connect_to_DDEI(conf.DDEI_IP)
        context.keyword.login_DDEI(conf.SSH_USR, conf.SSH_PWD)
    if 'CLI' in feature.tags:
        install_pexpect(context)
        #copy local script to DDEI
        context.keyword.upload_file_to_DDEI('steps\CLI\cli_test.py', '/root/cli_test.py')
    if 'custom_DNS' in feature.tags:
        if conf.CUSTOM_DNS is None:
            dnsIPv4 = '10.204.253.237'
        else:
            dnsIPv4 = conf.CUSTOM_DNS

        current_dns = context.keyword.exec_command_on_DDEI("clish -c 'show network dns' | grep name | awk '{print $2}'")

        if current_dns.strip() != dnsIPv4:
            cmd = "clish -c $'enable\n configure network dns ipv4 %s'" % dnsIPv4
            context.keyword.exec_command_on_DDEI(cmd)
        #set proxy
        set_proxy(context)


def after_feature(context, feature):
    print "cleanup testing"
    if 'browser' in feature.tags:
        context.browser.quit()
    if 'ssh' in feature.tags:
        context.keyword.disconnect_from_DDEI()


def before_scenario(context, scenario):
    print "clean up environment"
    context.keyword.purge_DB('ddei', 'tb_policy_event_total')
    context.keyword.purge_DB('ddei', 'tb_policy_event')
    context.keyword.purge_DB('ddei', 'tb_quarantine')
    context.keyword.purge_DB('ddei', 'tb_sandbox_tasks_history')
    context.keyword.purge_DB('ddei', 'tb_sandbox_task_details')
    context.keyword.purge_DB('ddei', 'tb_sandbox_urlfilter_cache')
    context.keyword.purge_DB('ddei', 'tb_sandbox_report_file_analyze')

    #list of attachments
    context.targetDoc = []

def install_pexpect(context):
    #install pexpect on DDEI
    context.keyword.upload_file_to_DDEI('tools\pexpect-3.3.tar.gz', '/root/pexpect-3.3.tar.gz')
    context.keyword.upload_file_to_DDEI('steps\CLI\pexpect_install.sh', '/root/pexpect_install.sh')
    #context.keyword.exec_command_on_DDEI('tar zxvf /root/pexpect-3.3.tar.gz')
    #context.keyword.exec_command_on_DDEI('cd /root/pexpect-3.3')
    #rc = context.keyword.ssh_conn.execute_command('python setup.py install',return_stdout=False, return_stderr=True, return_rc=True)
    #if rc[1] == 1:
    #    print 'install pexpect fail %s' % rc[0]
    context.keyword.ssh_conn.execute_command('/root/pexpect_install.sh > /root/pexpect_install_log',return_stdout=False, return_stderr=True, return_rc=True)

def set_proxy(context):
    context.keyword.set_au_proxy_server()
    restart_imss = '/opt/trend/ddei/script/S99IMSS restart'
    context.keyword.exec_command_on_DDEI(restart_imss)