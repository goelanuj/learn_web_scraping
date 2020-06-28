import time
import re
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.

# driver.get('http://www.google.com/');

driver.get('https://careers.peopleclick.com/careerscp/client_homedepot/int1068645304/search.do?sortBy=JP_POSTEDON')
# Submit Search
searchForm = driver.find_element_by_id("com.peopleclick.cp.formdata.SEARCHCRITERIA_KEYWORDS")
searchForm.clear()
searchForm.send_keys("manager")
searchFunction = driver.find_element_by_id("com.peopleclick.cp.formdata.FLD_JOB_FUNCTION")
#searchFunction.clear()
searchFunction.send_keys("Technology")
searchForm.submit()
#time.sleep(10)
#//*[@id="pf-rwd-Searchresultsmain"]/form[1]/div/span[1]/span[1]

try:
    results_count_xpath = "//*[@id=\"pf-rwd-Searchresultsmain\"]/form[1]/div/span[1]/span[1]"
    results_count = int(driver.find_element_by_xpath(results_count_xpath).text.translate({ord(i): None for i in ','}))

#    str.replace('e', '')
# print(str.translate({ord(i): None for i in '123'}))

except NameError:
    print("There is an excption on website result counts.")
else:
  print("Got proper result counts to proceed ")

if results_count > 0:
    pages_to_scan = math.ceil(results_count/10) - 2
    print("Total pages to scan - " + str(pages_to_scan))
else:
    print("no jobs found")
    exit()

list_of_job_titles = []
DEBUG_SEARCH="N"
# DEBUG_SEARCH="Y"
DEBUG_SEARCH_TEXT="Cyber Security - Threat Intel Manager"
for i in range(pages_to_scan):
    # results_list_xpath =  "//*[@id=\"pf-rwd-Searchresultsmain\"]/form[2]"
    results_list_xpath =  "//*[@id=\"pf-rwd-searchlist-main\"]/div[1]/*"
    pg_results_list = driver.find_elements_by_xpath(results_list_xpath)
    pg_results_count = pg_results_list.__len__()
    # print(pg_results_count)
    for x in range(pg_results_count):
        if pg_results_list[x].tag_name == 'div':
    #       print(x)
    #       print(pg_results_list[x].text)
            findSaveBtnElement = pg_results_list[x].find_element_by_xpath(".//div[4]/button[1]")
            findJobTitle = pg_results_list[x].find_element_by_xpath(".//div[1]/div[1]/label[1]")
    #       print(findSaveBtnElement.tag_name)
    #       print(findSaveBtnElement.get_attribute('value'))
    #       time.sleep(1)
    #       findSaveBtnElement.click()
    #       WebDriverWait(driver, 10).until(EC.element_to_be_clickable(findSaveBtnElement)).click()
            f1 = re.search("Senior|Sr", pg_results_list[x].text, re.IGNORECASE)
            f2 = re.search("Manager", pg_results_list[x].text, re.IGNORECASE)
    #        f3 = re.search("lead manager", pg_results_list[x].text, re.IGNORECASE)
    #        print(pg_results_list[x].text)
            # Debug search
            if DEBUG_SEARCH == "Y":
                fd = re.search(DEBUG_SEARCH_TEXT, pg_results_list[x].text, re.IGNORECASE)
                if f1 and f2 and fd:
                    #           Line below splits the whole text into two parts till the search world Save (lable from tbe button) and adds the first part to the list object
                    #           a = (pg_results_list[x].text).split("Save",1)
                    list_of_job_titles.append((pg_results_list[x].text).split("Save", 1)[0])
                    print(f1)
                    print(f2)
                    print(fd)
                    print(findSaveBtnElement.text)
                    print(pg_results_list[x].text)
                    print("Special - Job Title")
                    print(findJobTitle.text)
            else:
                if f1 and f2:
        #           Line below splits the whole text into two parts till the search world Save (lable from tbe button) and adds the first part to the list object
        #           a = (pg_results_list[x].text).split("Save",1)
                    list_of_job_titles.append((pg_results_list[x].text).split("Save",1)[0])
    #time.sleep(1)
    searchNextBtn = driver.find_element_by_css_selector(".pf-rwd-secondaryBar-singleWrapper > .hidden-xs > .pf-rwd-navButton:nth-child(9)")
    # XPATH // *[ @ id = "pf-rwd-Searchresultsmain"] / form[1] / div / span[3] / span / input[6]
    # searchNextBtn = driver.find_element_by_css_selector(".pf-rwd-Searchresultsmain > form:nth-child(1) > div > span.pf-rwd-secondaryBar-singleWrapper.pf-rwd-pagination.hidden-xs > span > input:nth-child(9)")
    # searchNextBtn = driver.find_element_by_xpath("// *[ @ id = \"pf-rwd-Searchresultsmain\"] / form[1] / div / span[3] / span / input[6]")
    #// *[ @ id = "pf-rwd-Searchresultsmain"] / form[1] / div / span[3] / span / input[8]
    #// *[ @ id = "pf-rwd-Searchresultsmain"] / form[1] / div / span[3] / span / input[8]
    #// *[ @ id = "pf-rwd-Searchresultsmain"] / form[1] / div / span[3] / span / input[8]
    #// *[ @ id = "pf-rwd-Searchresultsmain"] / form[1] / div / span[3] / span / input[6]

    if searchNextBtn:
        searchNextBtn.click()
    else:
        print("End of pages or Error")

job_titles = []
job_code = []
number_of_jobs = len(list_of_job_titles)
print(number_of_jobs)
for x in range(number_of_jobs):
    # print(list_of_job_titles[x])
    f1 = re.search("Senior|Sr", list_of_job_titles[x], re.IGNORECASE)
    f2 = re.search("Manager", list_of_job_titles[x], re.IGNORECASE)
    if f1 and f2:
        rec = list_of_job_titles[x].split("Job ID:", 1)
        jobTitle = rec[0].split("\n",1)[0]
        job_titles.append(jobTitle)
        jobID = int((rec[1].strip()).split("\n",1)[0])
        #print(tjobID)
        #jobID = tjobID.split("\n",1)[0]
#        list_of_job_titles[x].split("Job ID:",1)[0]
        #print(jobID)
        job_code.append(jobID)
print("Found matching Job " + str(len(job_titles)) + " and Job code " + str(len(job_code)))
print(job_titles)
print(job_code)
#driver.quit()