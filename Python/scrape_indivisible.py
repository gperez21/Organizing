# Scrape Google Trends results for presidential hopefuls
# Gabriel Perez-Putnam 1/8/19

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time


def sleep_time(x):
    """Sleep for X seconds times a number between 0 and 1"""
    random_time = random.random() *2* x
    time.sleep(random_time)

def search_term(driver,state):
    """Pull up the google trends page and search a name"""
    driver.get(indivisible)
    # info contained in iframe - switch in
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    searchbox = driver.find_element_by_class_name("ant-input")
    searchbox.send_keys(state)
    searchbox.send_keys(Keys.RETURN)

    time.sleep(1)

def get_events(driver):
    """Pull the items containing states from the page"""
    events = driver.find_elements_by_class_name("ant-list-item")
    print("We got events")
    return events

def get_text(objects, state):
    """Get text from first 5 objects (states)"""
    info = []
    for x in objects:
        event_info = split_row(x)
        info.append(event_info)
    return info

def split_row(info):
    """Take the raw info and pull out state and index"""
    statex = info.get_attribute('innerText').strip()
    list1 = statex.split("\n")
    return list1[:2]

def clean_row_for_export(variables):
    """Prepares a row of data for export"""
    row = ('\t').join(variables) + '\n'
    return row

def export_to_file(file_name, event_list):
    """Export the beer information to a file"""
    with open(file_name, 'w+', encoding='utf-8') as f:
        header = ['Event','Location']
        export_header = clean_row_for_export(header)
        f.write(export_header)
        for state in event_list:
            for event in state:
                row = clean_row_for_export(event)
                f.write(row)

def iterate_states(states, driver):
    """Go through the list and return the indivisible info"""
    results = []
    for state in states:
        print(state)
        sleep_time(7)
        search_term(driver,state)
        events = get_events(driver)
        results.append(get_text(events, state))
        driver.switch_to.default_content()
    return results



def main():
    """controller"""
    # create a new Chrome session
    driver = webdriver.Chrome(executable_path='C:/Users/perez_g/Desktop/Web Scrapping/env/Scripts/chromedriver.exe')
    # driver.maximize_window()
    driver.implicitly_wait(30)

    states =["California",
            "New York",
            "Virginia",
            "New Jersey",
            "Maryland",
            "Massachusetts",
            "Texas",
            "Connecticut",
            "Illinois",
            "Washington",
            "Minnesota",
            "Georgia",
            "Missouri",
            "Colorado",
            "Michigan",
            "Pennsylvania",
            "North Carolina",
            "Kansas",
            "Arizona",
            "Hawaii",
            "Wisconsin",
            "New Hampshire",
            "Florida",
            "Indiana",
            "Oregon",
            "Ohio",
            "Rhode Island",
            "Nevada",
            "Maine",
            "Nebraska",
            "South Carolina",
            "Iowa",
            "Vermont",
            "Alabama",
            "Alaska",
            "Louisiana",
            "Utah",
            "Delaware",
            "North Dakota",
            "Wyoming",
            "New Mexico",
            "Kentucky",
            "South Dakota",
            "Tennessee",
            "Oklahoma",
            "Idaho",
            "Arkansas",
            "Montana",
            "West Virginia",
            "Mississippi"]

    # URL of initial search
    global indivisible
    indivisible = "https://indivisible.org/groups"
    events_info = iterate_states(states, driver)
    export_to_file('events.txt', events_info)

main()
