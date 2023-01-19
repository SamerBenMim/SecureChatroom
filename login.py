# import all the required modules
from http import client
import socket
import threading
import tkinter
from tkinter import *
from cerf_req import gen_cert_req
import customtkinter

from Cert import *
import ldapserver
from rsa_fun import generateKeys



def redirReg():
	Window.withdraw()
	import register

def create_toplevel(title,msg):
	window = customtkinter.CTkToplevel()
	window.title(title)
	window.geometry("400x100")

	# create label on CTkToplevel window
	label = customtkinter.CTkLabel(window, text=msg)
	label.pack(side="top", fill="both", expand=True, padx=40, pady=40)


Window = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")

Window.title("Sign In")
Window.resizable(width=False,
							height=False)
Window.configure(width=500,
							height=400)
pls = customtkinter.CTkLabel(Window,
						text="Your Secrets Are Safe With Us !!!!",
										  font=("Arial",20,"bold"))
pls.place(relheight=0.15,
					relx=0.5,
					rely=0.2,
				    anchor="center")

# create a Label
Window.labelName = customtkinter.CTkLabel(Window,
							text="Username: ",
							   justify=CENTER
							   )

Window.labelName.place(relheight=0.1,
							relx=0.1,
							rely=0.3)

# create a entry box for
# tying the message
Window.entryName = customtkinter.CTkEntry(Window)

Window.entryName.place(relwidth=0.4,
							relheight=0.08,
							relx=0.3,
							rely=0.3)

# set the focus of the cursor
Window.entryName.focus()

### Password ####
# create a Label
Window.labelPwd = customtkinter.CTkLabel(Window,
							   text="Password : ",
							   justify=CENTER
							   )

Window.labelPwd.place(relheight=0.1,
							 relx=0.1,
							 rely=0.45)

# create a entry box for
# tying the message
Window.entryPwd = customtkinter.CTkEntry(Window,
							  show='*')

Window.entryPwd.place(relwidth=0.4,
							 relheight=0.08,
							 relx=0.3,
							 rely=0.45)


def connect():
	
	msg = ldapserver.login(Window.entryName.get(),Window.entryPwd.get())
	if (msg == "Authentification succeeded"):
		msgCert = verif_cert(Window.entryName.get())
		print(msgCert)
		if (msgCert == "The certificate is authentic"):
			
			print("The certificate is authentic")
			
		else :
			create_toplevel("HACKER !!!!",msgCert)
	else :
		create_toplevel("Error",msg)
		
Window.go = customtkinter.CTkButton(Window,
						text="Sign In",
						command= connect)

Window.go.place(relx=0.35,
					rely=0.65)


Window.go = customtkinter.CTkButton(Window,
										  text="Sign Up",
										  command=redirReg)

Window.go.place(relx=0.35,  rely=0.75)

Window.mainloop()


