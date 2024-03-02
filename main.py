import tkinter
import customtkinter
from PIL import ImageTk, Image
from coursetest import Courses


# prereqs



customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # creating cutstom tkinter window
app.geometry("600x440")
app.title('Canvas HW Collector')
app.wm_attributes('-transparentcolor', 'red')
app.resizable(width=False, height=False)


def button_function():
    quarter = entry_quarter.get()
    # course_manager = Courses(quarter)
    # course_manager.start_program()


bg_image = ImageTk.PhotoImage(Image.open("./assets/hwbg3.png"))

label = customtkinter.CTkLabel(master=app, image=bg_image)
label.pack()

# creating custom frame
frame = customtkinter.CTkFrame(master=label, width=330, height=242, corner_radius=15)
frame.configure(fg_color="#FFFFFF", bg_color='#FFB7B7')
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Canvas HW Collector", font=('Century Gothic', 20))
l2.configure(text_color="Black")
l2.place(x=60, y=75)

entry_quarter = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Enter Your Quarter')
entry_quarter.configure(border_color='#B2B2B2', fg_color='#F8F8F8', text_color='#696969')
entry_quarter.place(x=55, y=135)

# Create custom button
submit_button = customtkinter.CTkButton(master=frame, width=220, text="Submit", command=button_function,
                                        corner_radius=6)
submit_button.configure(fg_color='#E44545', hover_color='#993838', text_color='White')
submit_button.place(x=55, y=180)

cvlogo = customtkinter.CTkImage(Image.open("./assets/cvlogo.png").resize((100, 100)))
cvlogo.configure(size=(35, 35))
cvimg = customtkinter.CTkLabel(app, text="", image=cvlogo, bg_color="White")

cvimg.place(x=283, y=125)

app.mainloop()
