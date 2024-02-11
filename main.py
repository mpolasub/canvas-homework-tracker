from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

TERM = "Winter 2024"

# keep chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create & configure the chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://canvas.uw.edu/courses/")

input("Press 'enter' once you nave logged in.")

all_courses = driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
term_courses = []

for course in all_courses:
    if TERM in course.text:
        term_courses.append(course.find_element(By.CSS_SELECTOR, value="a"))

print(term_courses)
# term_courses[0].click()
#
for course in term_courses:
    course.click()
    time.sleep(2)
    assignments_tab = driver.find_element(By.LINK_TEXT, value="Assignments")
    assignment_toggle_button = driver.find_element(By.CSS_SELECTOR, value="[aria-controls='assignment_group_upcoming_assignments']")
    print(assignment_toggle_button.get_attribute('aria-expanded'))
    # if not assignment_toggle_button.get_attribute('aria-expanded'):
    #     assignment_toggle_button.click()

