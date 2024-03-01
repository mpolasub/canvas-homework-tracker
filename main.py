import tkinter
import customtkinter
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # creating cutstom tkinter window
app.geometry("600x440")
app.title('Canvas HW Collector')
app.wm_attributes('-transparentcolor', 'red')
app.resizable(width=False, height=False)


def button_function():
    app.destroy()  # destroy current window and creating new one
    w = customtkinter.CTk()
    w.geometry("1280x720")
    w.title('Welcome')
    label = customtkinter.CTkLabel(master=w, text="Home Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    w.mainloop()


img1 = ImageTk.PhotoImage(Image.open("./assets/hwbg3.png"))

label = customtkinter.CTkLabel(master=app, image=img1)
label.pack()

# creating custom frame
frame = customtkinter.CTkFrame(master=label, width=330, height=242, corner_radius=15)
frame.configure(fg_color="#FFFFFF", bg_color='#FFB7B7')
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Canvas HW Collector", font=('Century Gothic', 20))
l2.configure(text_color="Black")
l2.place(x=60, y=75)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Enter Your Quarter')
entry1.configure(border_color='#B2B2B2', fg_color='#F8F8F8',text_color='#696969')
entry1.place(x=55, y=135)

# Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Submit", command=button_function, corner_radius=6)
button1.configure(fg_color='#E44545', hover_color='#993838', text_color='White')
button1.place(x=55, y=180)

cvlogo = customtkinter.CTkImage(Image.open("./assets/cvlogo.png").resize((100, 100)))
cvlogo.configure(size=(35, 35))
cvimg = customtkinter.CTkLabel(app, text="", image=cvlogo, bg_color="White")

cvimg.place(x=283, y=125)


app.mainloop()
