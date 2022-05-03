#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 18:40:19 2022

@author: arapfaik/scraping-glassdoor-selenium
@modified by ymonjid
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_equivalences(to_college, url, num_equivs, verbose, path):
    
    '''Gathers equivalences as a dataframe, scraped from the given website'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(900, 800)
            
    driver.get(url)

    equivs = []
    state_buttons = Select(driver.find_element_by_name("state_in"))
    options_text = []
    timeout = 10
    for option in state_buttons.options:
        options_text.append(option.text)
    # Loop over the states
    for state in options_text:
        if state != '*' and state != 'None':
            state_buttons = Select(driver.find_element_by_name("state_in"))
            print('--------------------------------------------------------')
            print("State:", state)
            state_buttons.select_by_value(state)
            time.sleep(1)
            button = driver.find_element_by_class_name("defaultButtonSmall")
            button.click()
            time.sleep(1)
            college_buttons = Select(driver.find_element_by_name("college_in"))
            colleges_text = []
            for college in college_buttons.options:
                colleges_text.append(college.text)
            # Loop over the colleges in every state
            for college in colleges_text:
                print('College:', college)
                college_buttons = Select(driver.find_element_by_name("college_in"))
                college_buttons.select_by_value(college)
                time.sleep(1)                 
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'id____UID1'))
                    WebDriverWait(driver, timeout).until(element_present)
                    button = driver.find_element_by_id("id____UID1")
                    button.click()
                    time.sleep(1)
                    table_data = driver.find_elements(By.XPATH,"//table[@class='datadisplaytable']/tbody/tr")

                    # Loop over the rows in the datadisplaytable
                    for row in table_data:
                        try:
                            Transfer_college = row.find_element_by_xpath('.//td[1]').text
                            Transfer_group = row.find_element_by_xpath('.//td[2]').text
                            Transfer_subject = row.find_element_by_xpath('.//td[3]').text
                            Transfer_course_no = row.find_element_by_xpath('.//td[4]').text
                            Transfer_title= row.find_element_by_xpath('.//td[5]').text
                            UW_subject = row.find_element_by_xpath('.//td[6]').text
                            UW_course_no = row.find_element_by_xpath('.//td[7]').text
                            UW_title = row.find_element_by_xpath('.//td[8]').text
                            Effective_term = row.find_element_by_xpath('.//td[9]').text
                            USP_attribute = row.find_element_by_xpath('.//td[10]').text
            
                            #Printing for debugging
                            if verbose:
                                print("Transfer college: {}".format(Transfer_college))
                                print("Transfer group: {}".format(Transfer_group))
                                print("Transfer subject: {}".format(Transfer_subject))
                                print("Transfer course no: {}".format(Transfer_course_no))
                                print("Transfer title: {}".format(Transfer_title))
                                print("UW subject: {}".format(UW_subject))
                                print("UW course no: {}".format(UW_course_no))
                                print("UW title: {}".format(UW_title))
                                print("Effective term: {}".format(Effective_term))
                                print("USP attribute: {}".format(USP_attribute))
                                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    
                            # appending the data to the dictionary equivs
                            equivs.append({"from_school" : Transfer_college,
                            "from_course_department" : Transfer_subject,
                            "from_course_code" : Transfer_course_no,
                            "from_course_name" : Transfer_title, 
                            "from_extra_department" : Transfer_group,
                            "to_school" : to_college,
                            "to_course_department" : UW_subject, 
                            "to_course_code" : UW_course_no,
                            "to_course_name " : UW_title})
                            #"Effective term " : Effective_term,
                            #"USP attribute" : USP_attribute})
                            
                            if len(equivs) > num_equivs:
                                break
                            else:
                                pass
                        except NoSuchElementException:
                            pass
                        if len(equivs) > num_equivs:
                            break
                        else:
                            pass
                except TimeoutException:
                    print("Timed out waiting for page to load")
                    break
            if len(equivs) > num_equivs:
                break
            else:
                pass
    driver.close()
    return pd.DataFrame(equivs)  #This line converts the dictionary object into a pandas DataFrame.