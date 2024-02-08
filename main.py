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

input("Please log in.")

all_courses = driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
term_courses = []

for course in all_courses:
    if TERM in course.text:
        term_courses.append(course)

print(all_courses)
print(term_courses)
