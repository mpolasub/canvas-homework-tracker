from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import datetime
import pandas as pd


TERM = "Winter 2024"

all_assignments = {}
assignment_list = []

# keep chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create & configure the chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://canvas.uw.edu/courses/")


def get_days_left(due_text):  # EX: due_text = "Mar 17 at 11:59pm"
    days_left = 0
    today = datetime.date.today()
    due_date_split = due_text.split(" at ")
    month_day = due_date_split[0]
    if "Feb 29" in month_day:
        month_day = "Feb 28"
        days_left = 1
    my_date = datetime.datetime.strptime(month_day, "%b %d")
    day = int(my_date.strftime("%d"))
    month = int(my_date.strftime("%m"))
    full_due_date = datetime.date(today.year, month, day)
    days_left += (full_due_date - today).days
    return days_left


def get_assignment_details(hws, name):
    for assignment in hws:
        assignment_text = assignment.text.split("\n")
        assignment_name = assignment_text[0]
        points = assignment_text[-2]
        if points.split()[0] == "Due":
            points = "None"
        assignment_link = assignment.find_element(By.LINK_TEXT, value=assignment_name).get_attribute('href')
        # if "â€”" in assignment_name:
        #     assignment_name.replace("â€”", "--")
        all_assignments[course_name][assignment_name] = {}
        due_date = assignment.find_element(By.CSS_SELECTOR, value=".ig-details__item.assignment-date-due span").text
        all_assignments[course_name][assignment_name]["due"] = due_date
        days_left = get_days_left(due_date)
        all_assignments[course_name][assignment_name]["days_left"] = days_left
        all_assignments[course_name][assignment_name]["points"] = points

        assignment_tuple = (assignment_name, due_date, days_left, points, name, assignment_link)
        assignment_list.append(assignment_tuple)


input("Press 'enter' once you have logged in.")

all_courses = driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
num_course = 0

# get all relevant courses and put them in term_courses
for course in all_courses:
    if TERM in course.text:
        num_course += 1

# cycling through all courses
for i in range(num_course):
    all_courses = driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
    term_courses = []

    # get all relevant courses and put them in term_courses
    for course in all_courses:
        if TERM in course.text:
            term_courses.append(course.find_element(By.CSS_SELECTOR, value="a"))

    try:
        course = term_courses[i]
        print(course)
        course_name = course.get_attribute("title")
        all_assignments[course_name] = {}
        course.click()
        time.sleep(2)

        assignments_tab = driver.find_element(By.LINK_TEXT, value="Assignments")
        assignments_tab.click()
        time.sleep(5)

        u_assignments_group = driver.find_element(By.CLASS_NAME, value="assignment-list")
        assignments_info = u_assignments_group.find_elements(By.CLASS_NAME, value="ig-info")

        get_assignment_details(assignments_info, course_name)

        main_page = driver.find_element(By.ID, value="global_nav_courses_link")
        main_page.click()
        time.sleep(1)

        courses_page = driver.find_element(By.LINK_TEXT, value="All Courses")
        courses_page.click()
        time.sleep(1)
    #
    except StaleElementReferenceException:
        pass

print(all_assignments)

""""" JSON Format
full_course = {
    "course_name1": {
        "assignment_name": {
            "due": "Feb 14 at 11:59PM",
            "days_left": days_left,
            "points": points
        }
    },
    "course_name2": {
        "assignment_name1": {
            "due": "Feb 19 at 11:59PM",
            "days_left": days_left
        },
        "assignment_name2": {
            "due": "Feb 15 at 11:59PM",
            "days_left": days_left
        }
    }
}
"""""

# populating csv

hw_df = pd.DataFrame(assignment_list, columns=['Assignments', 'Due Date', 'Days Left', 'Points', 'Course Name', 'Link'])
hw_df.to_csv('assignments.csv', encoding='utf-8', index=False)
