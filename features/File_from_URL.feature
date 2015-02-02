@ssh @BVT @browser @custom_DNS
Feature: URL directed file need to be scanned in 2.1
    As a Mail admin
    I want to prevent the threat from URLs in mail, which could drop malicious file when user click it
    So that I deeply protect internal mail system

@marks
Scenario Outline: [RAT]URLs that could possibly drop malicious file should be detected out
Given   <urls> in mail could possibly drop a malicious file
And     Set VA customize file type to default
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be detected out by VA

    Examples:
    |urls|
    |http://wrs81.winshipway.com/suspicious.7z  |

@wip2
Scenario Outline: URL directed file downloading will stop when exceed timeout
Given    <urls> in mail could possibly drop a malicious file
But    The time to download the file exceeds the "<conn_timeout_value>" and "<download_timeout_value>"
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    |conn_timeout_value| download_timeout_value | urls|
    |1|2| http://wrs81.winshipway.com/big.zip|

@URL_Directed_File_detection
Scenario Outline: [RAT]URLs that could possibly drop malicious file should be detected out
Given   <urls> in mail could possibly drop a malicious file
And     Set VA customize file type to default
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be detected out by VA

    Examples:
    |urls|
    |http://wrs81.winshipway.com/knownvirus.pdf|
    |http://wrs81.winshipway.com/suspicious.pdf|
    |http://wrs81.winshipway.com/suspicious.zip|
    |http://wrs81.winshipway.com/knownvirus.zip|
    |http://wrs71.winshipway.com/suspicious.pdf|
    |http://wrs71.winshipway.com/suspicious.abc|
    |www.ddei.com/suspicious.pdf|
    |http://wrs81.winshipway.com/docs/suspicious.pdf |
    |http://wrs81.winshipway.com:80/suspicious.pdf |
    |https://wrs81.winshipway.com/suspicious.pdf |
    |http://wrs81.winshipway.com/suspicious.pdf, http://wrs71.winshipway.com/suspicious.pdf |

Scenario Outline: Not implemented
Given   <urls> in mail could possibly drop a malicious file
And     Set VA customize file type to default
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be detected out by VA

    Examples:
    |urls|
    |http://wrs81.winshipway.com/fileview.aspx?name=suspicious.pdf |
    |http://wrs81.winshipway.com/fileview.aspx?name=suspicious.pdf|
    |http://wrs81.winshipway.com/fileview.aspx?id=1|
    |http://wrs81.winshipway.com/fileview.aspx?name=/sample/suspicious.pdf |
    |https://wrs81.winshipway.com/fileview.aspx?name=suspicious.pdf |
    |http://wrs81.winshipway.com/fileview.aspx?name=suspicious.pdf&id=1 |


@URL_Directed_File_unsupported
Scenario Outline: [FET] Some special condition will be excluded from this function
Given    <unsupported_urls> in mail could possibly drop a malicious file
And    Set VA customize file type to default
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    | unsupported_urls |
    |ftp://ftp.ddeitest.com/suspicious.pdf |
    |http://wrs81.winshipway.com/suspicious_archive_with_password.zip|
    |http://wrs81.winshipway.com/suspicious_pdf|


@URL_Directed_File_save_without_clue
Scenario Outline: Save-rating URLs that is impossible to drop a malicious file will not be sent to VA
Given    A <save_urls> in mail that is not possible to drop a malicious file
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    | save_urls |
    |http://wrs81.winshipway.com/suspicious_pdf|


@URL_Directed_File_Unsupport_Content_type
Scenario Outline: Special content type of URL will be filtered out from VA analysis
Given    <urls> in mail could possibly drop a malicious file
But    The URL response content type "content type" is in DDEI ignore list
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    | urls | content type|
    |http://wrs81.winshipway.com/suspicious.doc| text/plain |


@URL_Directed_File_supported_Content_type
Scenario Outline: Special content type of URL will be filtered out from VA analysis
Given    <urls> in mail could possibly drop a malicious file
But    The URL response content type "content type" is in DDEI watch list
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be detected out by VA

    Examples:
    | urls |
    |http://wrs81.winshipway.com/suspicious.zip |
    |http://wrs81.winshipway.com/suspicious.rar |
    |http://wrs81.winshipway.com/suspicious.7z  |
    |http://wrs81.winshipway.com/suspicious.eml |
    |http://wrs81.winshipway.com/suspicious.exe |
    |http://wrs81.winshipway.com/suspicious.scr |
    |http://wrs81.winshipway.com/suspicious.msi |
    |http://wrs81.winshipway.com/suspicious.swf |
    |http://wrs81.winshipway.com/suspicious.rtf |
    |http://wrs81.winshipway.com/suspicious.pdf |
    |http://wrs81.winshipway.com/suspicious.jar |
    |http://wrs81.winshipway.com/suspicious.chm |
    |http://wrs81.winshipway.com/suspicious.docx|
    |http://wrs81.winshipway.com/suspicious.xls |
    |http://wrs81.winshipway.com/suspicious.xlsx|
    |http://wrs81.winshipway.com/suspicious.ppt |
    |http://wrs81.winshipway.com/suspicious.pptx|



@URL_Directed_File_UI_normal
Scenario Outline: URL directed file configuration UI checking - normal
Given    i have login DDEI hidden page
And    switch to "URL Filter Setting" tab
When    Set connection Timeout setting value to "<conn_timeout_value>"
And     set download Timeout setting value to "<download_timeout_value>"
And    Set File size setting value to "<Max_filesize_value>"
Then    New value should be accepted by UI and saved

    Examples:
    | conn_timeout_value |download_timeout_value| Max_filesize_value |
    | 1| 2| 1|
    | 10 | 20| 5|
    |60|300|50|
    |5|100|10|

@URL_Directed_File_UI_abnormal_1
Scenario Outline: URL directed file configuration UI checking - abnormal
Given    i have login DDEI hidden page
And    switch to "URL Filter Setting" tab
When    Set connection Timeout setting value to "<conn_timeout_value>"
Then    New value should not be accepted by UI and saved

    Examples:
    | conn_timeout_value |
    | -1|
    | 0 |
    |61|
    | a |
    |abc|
    |1.1|
    |?|
    |%|
    |null|

@URL_Directed_File_UI_abnormal_2
Scenario Outline: URL directed file configuration UI checking - abnormal 2
Given    i have login DDEI hidden page
And    switch to "URL Filter Setting" tab
When    Set download Timeout setting value to "<download_timeout_value>"
Then    New value should not be accepted by UI and saved

    Examples:
    | download_timeout_value |
    | -1|
    | 0 |
    |301|
    | a |
    |abc|
    |1.1|
    |?|
    |%|
    |null|

@URL_Directed_File_UI_abnormal_3
Scenario Outline: URL directed file configuration UI checking - abnormal 3
Given    i have login DDEI hidden page
And    switch to "URL Filter Setting" tab
When    Set File size setting value to "<Max_filesize_value>"
Then    New value should not be accepted by UI and saved

    Examples:
    | Max_filesize_value |
    | -1|
    | 0 |
    |51|
    | a |
    |abc|
    |1.1|
    |?|
    |%|
    |null|

@URL_Directed_File_disable_function
Scenario Outline: URL directed file function disabling
Given    i have login DDEI hidden page
And    switch to "URL Filter Setting" tab
When    Disable the function
And     Sand a mail with <url> that will drop suspicious file
Then    The file dropped from URL will not be submitted to VA
And     Enable the function

    Examples:
    | url |
    |http://wrs81.winshipway.com/suspicious.pdf|
    |http://wrs81.winshipway.com/knownvirus.pdf|


@URL_Directed_File_conf_exceed_timeout
Scenario Outline: URL directed file downloading will stop when exceed timeout
Given    <urls> in mail could possibly drop a malicious file
But    The time to download the file exceeds the "<conn_timeout_value>" and "<download_timeout_value>"
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    |conn_timeout_value| download_timeout_value | urls|
    |1| 2| http://wrs81.winshipway.com/notexist.pdf|
    |1|2| http://wrs81.winshipway.com/big.zip|
    |1|2| http://www.thisurlisnotexist.com/suspicious.pdf|


@URL_Directed_File_conf_exceed_filesize
Scenario Outline: File downloading will not start when exceed file size
Given    <urls> in mail could possibly drop a malicious file
But    The dropped file size exceeds the "<Max_filesize_value>"
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    | Max_filesize_value | urls |
    | 1 | http://wrs81.winshipway.com/big.zip|



@URL_Directed_File_Force_submit
Scenario Outline: Saved File from URL belong to customized VA file type should be sent to VA
Given    <urls> in mail could possibly drop a malicious file
And    Dropped file "<filetype>" is configured to be forcedly submitted to VA
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be submitted to VA

    Examples:
    |urls| filetype|
    |http://wrs81.winshipway.com/save.pdf| PDF|
    |http://wrs81.winshipway.com/save.exe| EXE|


@URL_Directed_File_Force_submit_2
Scenario Outline: Any File from URL in customized VA file type should be sent to VA
Given    <urls> in mail could possibly drop a malicious file
And    Dropped file "<filetype>" is configured to be forcedly submitted to VA
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will be detected out by VA

    Examples:
    |urls| filetype|
    |http://wrs81.winshipway.com/suspicious.pdf| PDF|
    |http://wrs81.winshipway.com/suspicious.exe| EXE|

@URL_Directed_File_no_submit_situation
Scenario Outline: Saved file dropped from URL will not be analyzed if it is not in VA customized file type
Given    <urls> in mail could possibly drop a safe file
But    Dropped file "<filetype>" is configured to be not forcedly submitted to VA
When    This URL is included in mail and going through DDEI
Then    The file dropped from URL will not be submitted to VA

    Examples:
    |urls| filetype|
    |http://wrs81.winshipway.com/save.pdf| PDF|
    |http://wrs81.winshipway.com/save.exe| EXE|


Scenario Outline: VA report re-construction
Given    <urls> in mail could possibly drop a malicious file
When    This URL is included in mail and going through DDEI
Then    This file detection will be the child of the URL

    Examples:
    | urls |
    |http://wrs81.winshipway.com/suspicious.pdf|
    |http://wrs81.winshipway.com/suspicious.zip|


Scenario Outline: URL directed file should be downloaded from the same line with VA
Given    <urls> in mail could possibly drop a malicious file
And    VA port use "<interface>"
When    This URL is included in mail and going through DDEI
Then    File downloading need use the same interface as VA

    Examples:
    | urls | interface|
    | http://wrs81.winshipway.com/suspicious.pdf | management network|
    | http://wrs81.winshipway.com/suspicious.pdf | customized network |
    | http://wrs81.winshipway.com/suspicious.pdf | isolated network |