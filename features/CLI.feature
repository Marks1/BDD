@ssh @BVT @CLI
Feature: Command Line Interface Functions
    As a Mail admin
    I want to configure DDEI through CLI
    So that I could setup some running parameters without web access

@CLI_Normal_mode_basic_command
Scenario Outline: Normal mode basic command
    Given   i have login CLISH normal mode
    When    i execute command "<cli_command>"
    Then    i could get output like "<cli_output_pattern>"

    Examples:
    |cli_command|cli_output_pattern|
    |?|.*TraceRoute|
    |help|.*CONTEXT SENSITIVE HELP.*MOVEMENT KEYS.*DELETION KEYS|
    |history|.*history|
    |ping|.* Web Address either IP or FQDN|
    |ping 10.204.16.2|.*from.*icmp.*ttl.*time|
    |resolve|.* Web Address either IP or FQDN|
    |resolve baidu.com|.*has address|
    |traceroute 10.204.16.2|.*30 hops max, 60 byte packets|

	
@CLI_Normal_mode_show_command
Scenario Outline: Normal mode show command
    Given   i have login CLISH normal mode
    When    i execute command "<cli_command>"
    Then    i could get output like "<cli_output_pattern>"

    Examples:
    |cli_command|cli_output_pattern|
    |show DDEI version|.*2\.1|
    |show DDEI management-port|.*10.204.191.67 255.255.255.0|
    |show DDEI operation-mode|.*MTA|
    |show kernel iostat|.*avg-cpu:.*Device.*sda|
    |show memory statistic|.*buffers|
    |show memory vm|.*-memory--|
	|show network arp|.* Web Address either IP or FQDN|
	|show network arp 8.8.8.8|.*-- no entry|
	|show network dns|.*nameserver1|
	|show network dns ipv6|.*|
	|show network hostname|.*hostname:|
	|show process ltrace|.*Unsigned integer|
	|show process stack|.*Unsigned integer|
	|show process top|.*|
	|show process trace|.*Unsigned integer|
	|show service ntp|.*ntpd is|
	|show service ntp enabled|.*no|
	|show service ntp server-address|.*\.*\.*\.|
	|show service ssh|.*SSH service is|
	|show storage statistic|.*Filesystem.*Size.*Used.*Avail.*Use.*Mounted|
	|show system date|.*:*:|
	|show system timezone|.*UTC|
	|show system timezone city|.*UTC|
	|show system timezone continent|.*UTC|
	|show system timezone country|.*American.*Japan.*Korea|
	|show system uptime|.*user.*average|
	|show system version|.*OpenVA|

	
@CLI_Priviledge_mode_basic_command
Scenario Outline: Priviledge mode command
    Given   i have login CLISH Priviledge mode
    When    i execute command "<cli_command>"
    Then    i could get output like "<cli_output_pattern>"

    Examples:
    |cli_command|cli_output_pattern|
    |?|.*TraceRoute|
    |help|.*CONTEXT SENSITIVE HELP.*MOVEMENT KEYS.*DELETION KEYS|
    |history|.*history|
    |ping|.* Web Address either IP or FQDN|
    |ping 10.204.16.2|.*from.*icmp.*ttl.*time|
    |resolve|.* Web Address either IP or FQDN|
    |resolve baidu.com|.*has address|
    |traceroute 10.204.16.2|.*30 hops max, 60 byte packets|
	|configure network hostname|.* Hostname or FQDN|
	|configure network dns ipv4|.*IP address AAA.BBB.CCC.DDD|
	|stop process core 0|.*no process killed|
	|stop service postfix|.*Stopping Postfix|
	|start service postfix|.*Starting Postfix|
	
	
@CLI_Priviledge_mode_show_command
Scenario Outline: Priviledge mode command
    Given   i have login CLISH Priviledge mode
    When    i execute command "<cli_command>"
    Then    i could get output like "<cli_output_pattern>"

    Examples:
    |cli_command|cli_output_pattern|
    |show DDEI version|.*2\.1|
    |show DDEI management-port|.*10.204.191.67 255.255.255.0|
    |show DDEI operation-mode|.*MTA|
    |show kernel iostat|.*avg-cpu:.*Device.*sda|
    |show memory statistic|.*buffers|
    |show memory vm|.*-memory--|
	|show network arp|.* Web Address either IP or FQDN|
	|show network arp 8.8.8.8|.*-- no entry|
	|show network dns|.*nameserver1|
	|show network dns ipv6|.*|
	|show network hostname|.*hostname:|
	|show process ltrace|.*Unsigned integer|
	|show process stack|.*Unsigned integer|
	|show process top|.*|
	|show process trace|.*Unsigned integer|
	|show service ntp|.*ntpd is|
	|show service ntp enabled|.*no|
	|show service ntp server-address|.*\.*\.*\.|
	|show service ssh|.*SSH service is|
	|show storage statistic|.*Filesystem.*Size.*Used.*Avail.*Use.*Mounted|
	|show system date|.*:*:|
	|show system timezone|.*UTC|
	|show system timezone city|.*UTC|
	|show system timezone continent|.*UTC|
	|show system timezone country|.*American.*Japan.*Korea|
	|show system uptime|.*user.*average|
	|show system version|.*OpenVA|
