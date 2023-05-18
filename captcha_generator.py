# this code generates the audio and image captcha and takes the input of user, the user is given 3 attempts after exceeding the attempt 30 seconds timer is displayed

# import required library
from tkinter import *
import tkinter.messagebox
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
import string
import random
import os
import pyttsx3
import time

# variable declaration
audio_captcha = ''
image_captcha = ''

max_attempts = 3
current_attempts = 0

timer_running = False


# function to disply the timer
def display_timer():
    global timer_running
    if timer_running:
        tkinter.messagebox.showinfo(
            "ERROR!!!", "Please wait for the timer to finish.")
        return

    timer_running = True
    Label_Timer.config(text="")
    for i in range(30, -1, -1):
        Label_Timer.config(text=f"Time Remaining: {i} seconds")
        root.update()
        time.sleep(1)
    Label_Timer.config(text="")
    timer_running = False

    # Enable the window after the timer completes
    root.attributes('-disabled', False)


# code to generate random image captcha(RANGE(4)) - for image_captcha
def generate_captcha():
    data_set = list(string.ascii_uppercase + string.digits)  # A-Z, 0-9
    s = ''
    for i in range(4):
        a = random.choice(data_set)
        s = s + a
        data_set.remove(a)

    global image_captcha
    image_captcha = s

    return s


# code to generate random audio captcha(RANGE(4)) - for audio_captcha
def generate_digit_captcha():
    s1 = ''
    s = ''
    for i in range(4):
        a = str(random.randint(0, 9))
        s = s + a
        s1 = s1 + a + " "

    global audio_captcha
    audio_captcha = s

    return s1

# code to generate captcha image


def generate_image_captcha():
    os.startfile('c1.png')


def generate_first_image():
    img = ImageCaptcha()

    s = generate_captcha()
    value = img.generate(s)
    img.write(s, "c1.png")


def regenerate_image_captcha():
    img = ImageCaptcha()
    s = generate_captcha()
    value = img.generate(s)
    img.write(s, "c1.png")

    # Load and display the regenerated image captcha in the Image_Label
    image_path = "c1.png"
    captcha_image = ImageTk.PhotoImage(Image.open(image_path))
    Image_Label.config(image=captcha_image)
    # Update the reference to avoid garbage collection
    Image_Label.image = captcha_image


def generate_audio_captcha():
    s = generate_digit_captcha()

    voiceEngine = pyttsx3.init()

    voiceEngine.setProperty('rate', 170)
    voiceEngine.setProperty('volume', 1.0)

    voices = voiceEngine.getProperty('voices')
    voiceEngine.setProperty('voice', voices[1].id)

    voiceEngine.say(s)
    voiceEngine.runAndWait()
    voiceEngine.say(s)
    voiceEngine.runAndWait()


def regenerate_audio_captcha():
    generate_audio_captcha()

# code to return audio


def get_audio():
    return audio_captcha

# code to return image


def get_image():
    return image_captcha

# code to check audio and image captcha


def check_audio_captcha():
    global current_attempts
    if checkbox_var.get():
        if ans.get() == "":
            tkinter.messagebox.showinfo(
                "ERROR!!!", "Please enter an audio captcha code.")
            return  # Exit the function if the entry box is empty

        if ans.get() == get_audio():
            tkinter.messagebox.showinfo("SUCCESS!!!", "Captcha Code Matched.")
            ans.set("")
            current_attempts = 0  # Reset the number of attempts
        else:
            current_attempts += 1
            if current_attempts >= max_attempts:
                # Convert the message into speech
                voiceEngine = pyttsx3.init()
                voiceEngine.say(
                    "Captcha Code does not Match. Maximum attempts reached.")
                voiceEngine.runAndWait()
                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Captcha Code does not Match. Maximum attempts reached.")

                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Please wait for the timer to finish.")
                ans.set("")
                # Disable the window after the timer starts
                root.attributes('-disabled', True)
                display_timer()
                regenerate_audio_captcha()
            else:
                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Captcha Code does not Match.")
                ans.set("")
    else:
        tkinter.messagebox.showinfo(
            "ERROR!!!", "Please check the 'I am not a robot' box.")


def check_image_captcha():
    global current_attempts
    if checkbox_var.get():
        if ans1.get() == "":
            tkinter.messagebox.showinfo(
                "ERROR!!!", "Please enter an image captcha code.")
            return  # Exit the function if the entry box is empty

        if ans1.get() == get_image():
            tkinter.messagebox.showinfo("SUCCESS!!!", "Captcha Code Matched.")
            ans1.set("")
            current_attempts = 0  # Reset the number of attempts
        else:
            current_attempts += 1
            if current_attempts >= max_attempts:
                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Captcha Code does not Match. Maximum attempts reached.")
                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Please wait for the timer to finish.")
                ans1.set("")
                # Disable the window after the timer starts
                root.attributes('-disabled', True)
                display_timer()
                regenerate_image_captcha()
            else:
                tkinter.messagebox.showinfo(
                    "WRONG!!!", "Captcha Code does not Match.")
                ans1.set("")
    else:
        tkinter.messagebox.showinfo(
            "ERROR!!!", "Please check the 'I am not a robot' box.")


# creating Tkinter GUI
root = Tk()
root.title("GUI : CAPTCHA Generation")
root.geometry("1100x500")
root.configure(background='#ffd9db')


# toggle box for "I am not a robot"
def toggle_checkbox():
    if timer_running:
        # Enable the window after the timer completes
        root.attributes('-disabled', True)
        tkinter.messagebox.showinfo(
            "ERROR!!!", "Please wait for the timer to finish.")


checkbox_var = BooleanVar()

Tops = Frame(root, bg='#ff5c75', pady=1, width=550, height=50, relief="ridge")
Tops.grid(row=0, column=0)

ans = StringVar()
ans1 = StringVar()
generate_first_image()

# code for creating frames,labels and buttons inside the GUI -(main frame)
Title_Label = Label(Tops, font=('Comic Sans MS', 16, 'bold'),
                    text="\t\tGUI Based CAPTCHA Generation\t\t", bg='black', fg='white', justify="center")
Title_Label.grid(row=0, column=0)
MainFrame = Frame(root, bg='Powder Blue', pady=2,
                  width=1350, height=100, relief=RIDGE)
MainFrame.grid(row=1, column=0)

# code for creating frames,labels and buttons inside the GUI -(audio captcha-LEFT FRAME)
LeftFrame = Frame(MainFrame, bd=10, width=200, height=200,
                  padx=10, pady=2, bg='#68DEED', relief=RIDGE)
LeftFrame.pack(side=LEFT)

# code for creating frames,labels and buttons inside the GUI -(IMAGE captcha-RIGHT FRAME)
RightFrame = Frame(MainFrame, bd=10, width=200, height=200,
                   padx=10, pady=2, bg='#68DEED', relief=RIDGE)
RightFrame.pack(side=RIGHT)

Label_1 = Label(RightFrame, font=('lato black', 33, 'bold'),
                text=" Audio Captcha ", padx=2, pady=2, bg="yellow", fg="black")
Label_1.grid(row=0, column=0, sticky=W)

Label_2 = Label(RightFrame, font=('arial', 20, 'bold'),
                text="", padx=2, pady=2, bg="#68DEED", fg="black")
Label_2.grid(row=1, column=0, sticky=W)

Label_9 = Button(RightFrame, font=('arial', 19, 'bold'), text="Play Audio",
                 padx=2, pady=2, bg="blue", fg="white", command=generate_audio_captcha)
Label_9.grid(row=4, column=0)

Label_7 = Label(RightFrame, font=('arial', 20, 'bold'),
                text="", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=2, column=0, sticky=W)

Entry_1 = Entry(RightFrame, font=('arial', 20, 'bold'), bd=2, fg="black", textvariable=ans, width=14,
                justify=LEFT).grid(row=5, column=0)

Label_7 = Label(RightFrame, font=('arial', 20, 'bold'),
                text="", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=6, column=0, sticky=W)

Label_7 = Label(RightFrame, font=('arial', 20, 'bold'),
                text=" ", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=6, column=1, sticky=W)

Label_8 = Button(RightFrame, font=('Arial', 25, 'bold'), text="Check",
                 padx=2, pady=2, bg="white", fg="blue", command=check_audio_captcha)
Label_8.grid(row=9, column=0)

Label_4 = Button(RightFrame, font=('arial', 15, 'bold'), text="Regenerate",
                 padx=2, pady=2, bg="white", fg="red", command=regenerate_audio_captcha)
Label_4.grid(row=10, column=0)

Label_7 = Label(RightFrame, font=('arial', 20, 'bold'),
                text=" ", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=11, column=1, sticky=W)

Checkbox = Checkbutton(RightFrame, text="I am not a robot", variable=checkbox_var, font=('arial', 15, 'bold'), pady=2,
                       padx=2, bg="#68DEED", fg="black", command=toggle_checkbox)
# Adjust the row and column values as needed
Checkbox.grid(row=6, column=0, columnspan=3)


# Lables - left frame
Label_1 = Label(LeftFrame, font=('lato black', 33, 'bold'),
                text=" Image Captcha ", padx=2, pady=2, bg="yellow", fg="black")
Label_1.grid(row=0, column=0, sticky=W)

Label_2 = Label(LeftFrame, font=('arial', 20, 'bold'), text="",
                padx=2, pady=2, bg="#68DEED", fg="black")
Label_2.grid(row=1, column=0, sticky=W)


# Add a new label widget to display the image captcha in the LeftFrame section
Image_Label = Label(LeftFrame, padx=2, pady=2, bg="#68DEED")
Image_Label.grid(row=4, column=0)

# Load and display the image captcha in the Image_Label
image_path = "c1.png"  # Assuming the image captcha is saved as "c1.png"
captcha_image = ImageTk.PhotoImage(Image.open(image_path))
Image_Label.config(image=captcha_image)

Label_7 = Label(LeftFrame, font=('arial', 20, 'bold'), text="",
                padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=2, column=0, sticky=W)

Entry_1 = Entry(LeftFrame, font=('arial', 20, 'bold'), bd=2, fg="black", textvariable=ans1, width=14,
                justify=LEFT).grid(row=5, column=0)

Label_7 = Label(LeftFrame, font=('arial', 20, 'bold'), text="",
                padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=6, column=0, sticky=W)

Label_7 = Label(LeftFrame, font=('arial', 20, 'bold'),
                text=" ", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=6, column=1, sticky=W)

Label_8 = Button(LeftFrame, font=('Arial', 25, 'bold'), text="Check",
                 padx=2, pady=2, bg="white", fg="blue", command=check_image_captcha)
Label_8.grid(row=9, column=0)

Label_4 = Button(LeftFrame, font=('arial', 15, 'bold'), text="Regenerate",
                 padx=2, pady=2, bg="white", fg="red", command=regenerate_image_captcha)
Label_4.grid(row=10, column=0)

Label_7 = Label(LeftFrame, font=('arial', 20, 'bold'),
                text=" ", padx=2, pady=2, bg="#68DEED", fg="black")
Label_7.grid(row=11, column=1, sticky=W)


Label_Timer = Label(MainFrame, font=('arial', 16, 'bold'),
                    text="", pady=2, padx=2, bg="Powder Blue", fg="black")
Label_Timer.pack(side=TOP)

Checkbox = Checkbutton(LeftFrame, text="I am not a robot", variable=checkbox_var, font=('arial', 15, 'bold'), pady=2,
                       padx=2, bg="#68DEED", fg="black", command=toggle_checkbox)
# Adjust the row and column values as needed
Checkbox.grid(row=6, column=0, columnspan=2)


root.mainloop()
