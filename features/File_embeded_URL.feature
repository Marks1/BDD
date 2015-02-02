@ssh @BVT @custom_DNS @browser
Feature: URLs that is embeded in attachment should be extracted and scanned in 2.1
    As a Mail admin
    I want to prevent the threat from URLs in mail, which is hidden in attachment
    So that I deeply protect internal mail system

@basic
Scenario Outline: [RAT]Known URLs in PDF and Office document should be extracted and detected
Given   malicious <URL> in a <file>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    This mail should be detected out by WRS

    Examples:
    |URL| file |
    |http://wrs21.winshipway.com | ExcelWithbedURL.xls |

@wip
Scenario Outline: [RAT]Total num of URLs that extracted from attachment and mail body should be 20 at most
Given   Total 10 URLs in a <file>
And     15 URLs in mail body
When    This file is attached in mail and going through DDEI
Then    Only 20 URLs are sent to scan

    Examples:
    | file | number |
    | PdfWith10BedURL.pdf | 20|

@Doc_embeded_URL_UI_default_disable
Scenario: [UI] Document embeded URL scanning function is disabled by default
Given    i have login DDEI hidden page
When    switch to "URL Extraction Setting" tab
Then    URL from document check box should be disabled by default
And     malicious URL in doc should not be detected


@Doc_embeded_URL_support_doc_type
Scenario Outline: [RAT]Known URLs in PDF and Office document should be extracted and detected
Given   malicious <URL> in a <file>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    This mail should be detected out by WRS

    Examples:
    |URL| file |
    |http://wrs21.winshipway.com | PdfWithbedURL.pdf |
    |http://wrs21.winshipway.com | DocWithbedURL.doc |
    |http://wrs21.winshipway.com | PptbedURL.ppt |
    |http://wrs21.winshipway.com | ExcelWithbedURL.xls |
    |http://wrs21.winshipway.com | Doc2007WithbedURL.docx |
    |http://wrs21.winshipway.com | Ppt2007WithbedURL.pptx |
    |http://wrs21.winshipway.com | Excel2007WithbedURL.xlsx |

@Doc_embeded_Unknown_URL
Scenario Outline: [RAT]Unrated URLs in PDF and Office document should be extracted and analyzed
Given   unrated <URL> in a <file>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    This URL should be extracted and sent to VA for analysis

    Examples:
    |URL| file |
    |http://wrs71.winshipway.com/suspicious.pdf | PdfWithUnratedURL.pdf |
    |http://wrs71.winshipway.com/suspicious.pdf | Doc2007WithUnratedURL.docx |

@Doc_embeded_URL_max_URL_num
Scenario Outline: [RAT]20 URLs in attachment should be all parsed out for scanning
Given   Total 25 URLs in a <file>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    Only 20 URLs are sent to scan

    Examples:
    | file |
    | PdfWith20BedURL.pdf |
    | Doc2007With20BedURL.docx |

@Doc_embeded_URL_max_URL_num2
Scenario Outline: [RAT]Total num of URLs that extracted from attachment and mail body should be 20 at most
Given   Total 10 URLs in a <file>
And     15 URLs in mail body
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    Only 20 URLs are sent to scan

    Examples:
    | file | number |
    | PdfWith10BedURL.pdf | 20|
    | Doc2007With10BedURL.docx | 20|

@Doc_embeded_URL_multiple_attachment
Scenario Outline: [RAT]URLs in several attachments should be all parsed out for scanning
Given   malicious <URL> in a <file>
And     malicious <URL2> in a <file2>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    This mail should be detected out by WRS
And     Only 2 URLs are sent to scan

    Examples:
    |URL| file | URL2| file2|
    |http://wrs21.winshipway.com | PdfWithbedURL.pdf | http://wrs49.winshipway.com | DocWithbedURL2.docx |



@Doc_embeded_URL_max_URL_count
Scenario Outline: [UI] Change the maximum count of URLs extracted from mail
Given   Set max-URL count to 15 on hidden page
And   Total 25 URLs in a <file>
And     enable Doc_extracted_URL_scan function
When    This file is attached in mail and going through DDEI
Then    Only 15 URLs are sent to scan

    Examples:
    | file |
    | PdfWith20BedURL.pdf |
