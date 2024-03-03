from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import datetime


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


class Courses:
    all_assignments = {}
    assignment_list = []
    TERM = ""
    driver = ""
    ticker = 0

    def __init__(self, quarter):
        self.TERM = quarter
        self.driver = webdriver.Chrome()

    def wait_for_login(self):
        url = self.driver.current_url  # get url
        if url == "https://canvas.uw.edu/courses" and self.ticker == 1:
            return
        if url == "https://idp.u.washington.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1" and self.ticker != 1:
            self.ticker += 1
        time.sleep(2)

        self.wait_for_login()

    def start_program(self):
        print(self.TERM)
        self.driver.get("https://canvas.uw.edu/courses/")
        print("starting wait")
        self.wait_for_login()

    def get_assignment_details(self, hws, name):
        for assignment in hws:
            assignment_text = assignment.text.split("\n")
            assignment_name = assignment_text[0]
            points = assignment_text[-2]
            if points.split()[0] == "Due":
                points = "None"
            assignment_link = assignment.find_element(By.LINK_TEXT, value=assignment_name).get_attribute('href')
            # if "â€”" in assignment_name:
            #     assignment_name.replace("â€”", "--")
            self.all_assignments[name][assignment_name] = {}
            due_date = assignment.find_element(By.CSS_SELECTOR, value=".ig-details__item.assignment-date-due span").text
            self.all_assignments[name][assignment_name]["due"] = due_date
            days_left = get_days_left(due_date)
            self.all_assignments[name][assignment_name]["days_left"] = days_left
            self.all_assignments[name][assignment_name]["points"] = points

            assignment_tuple = (assignment_name, due_date, days_left, points, name, assignment_link)
            self.assignment_list.append(assignment_tuple)

    # input("Press 'enter' once you have logged in.")
    def get_all_assignments(self):
        all_courses = self.driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
        num_course = 0

        # get all relevant courses and put them in term_courses
        for course in all_courses:
            if self.TERM in course.text:
                num_course += 1

        # cycling through all courses
        for i in range(num_course):
            all_courses = self.driver.find_elements(By.CLASS_NAME, value="course-list-table-row")
            term_courses = []

            # get all relevant courses and put them in term_courses
            for course in all_courses:
                if self.TERM in course.text:
                    term_courses.append(course.find_element(By.CSS_SELECTOR, value="a"))

            try:
                course = term_courses[i]
                print(course)
                course_name = course.get_attribute("title")
                self.all_assignments[course_name] = {}
                course.click()
                time.sleep(2)

                assignments_tab = self.driver.find_element(By.LINK_TEXT, value="Assignments")
                assignments_tab.click()
                time.sleep(5)

                u_assignments_group = self.driver.find_element(By.CLASS_NAME, value="assignment-list")
                assignments_info = u_assignments_group.find_elements(By.CLASS_NAME, value="ig-info")

                self.get_assignment_details(assignments_info, course_name)

                main_page = self.driver.find_element(By.ID, value="global_nav_courses_link")
                main_page.click()
                time.sleep(1)

                courses_page = self.driver.find_element(By.LINK_TEXT, value="All Courses")
                courses_page.click()
                time.sleep(1)
            #
            except StaleElementReferenceException:
                pass

        return self.assignment_list
