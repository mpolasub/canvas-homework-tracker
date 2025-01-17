import os
import sys
import tkinter
from tkinter import messagebox
import customtkinter
from PIL import ImageTk, Image
from coursetest import Courses
import pandas as pd


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


customtkinter.set_appearance_mode("System")

app = customtkinter.CTk()  # creating cutstom tkinter window
app.geometry("600x440")
app.title('Canvas HW Collector')
app.wm_attributes('-transparentcolor', 'red')
app.resizable(width=False, height=False)


def create_csv(assignments):
    hw_df = pd.DataFrame(assignments,
                         columns=['Assignments', 'Due Date', 'Days Left', 'Points', 'Course Name', 'Link'])
    hw_df.to_csv('assignments.csv', encoding='utf-8', index=False)


def display_end_message():
    messagebox.showinfo(title="Finished processing", message="Data collection finished. Please view "
                                                             "'assignments.csv'.")


def start_selenium():
    quarter = entry_quarter.get()
    course_manager = Courses(quarter)
    course_manager.start_program()

    assignments = course_manager.get_all_assignments()
    create_csv(assignments)
    entry_quarter.delete(0, 'end')

    display_end_message()


bg_image = ImageTk.PhotoImage(Image.open(resource_path("dist\\assets\\hwbg3.png")))

label = customtkinter.CTkLabel(master=app, image=bg_image)
label.pack()

# creating custom frame
frame = customtkinter.CTkFrame(master=label, width=330, height=242, corner_radius=15)
frame.configure(fg_color="#FFFFFF", bg_color='#ffe0e0')
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Canvas HW Collector", font=('Century Gothic', 20))
l2.configure(text_color="Black")
l2.place(x=60, y=75)

entry_quarter = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Enter Your Quarter')
entry_quarter.configure(border_color='#B2B2B2', fg_color='#F8F8F8', text_color='#696969')
entry_quarter.place(x=55, y=135)

# Create custom button
submit_button = customtkinter.CTkButton(master=frame, width=220, text="Submit", command=start_selenium,
                                        corner_radius=6)
submit_button.configure(fg_color='#E44545', hover_color='#993838', text_color='White')
submit_button.place(x=55, y=180)

cvlogo = customtkinter.CTkImage(Image.open(resource_path("dist\\assets\\cvlogo.png")).resize((100, 100)))
cvlogo.configure(size=(35, 35))
cvimg = customtkinter.CTkLabel(app, text="", image=cvlogo, bg_color="White")

cvimg.place(x=283, y=125)

app.mainloop()
