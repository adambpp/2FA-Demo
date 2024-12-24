import customtkinter

class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.resizable(width=False, height=False)
        self.title("2FA Demo")


        # LOGIN SCREEN UI CODE
        login_screen = customtkinter.CTkFrame(master=self, border_width=2, width=200)
        login_screen.pack(pady=20, padx=10,ipadx=50, ipady=25, expand=True)

        label = customtkinter.CTkLabel(master=login_screen, text="Login System", font=("Arial", 24))
        label.pack(pady=12, padx=10)

        entry1 = customtkinter.CTkEntry(master=login_screen, placeholder_text="Username")
        entry1.pack(pady=12, padx=10)

        entry2 = customtkinter.CTkEntry(master=login_screen, placeholder_text="Password", show="*")
        entry2.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=login_screen, text="Login", command=lambda: self.login_button_callback(login_screen, otp_screen))
        button.pack(pady=12, padx=10, expand=True)



        # 2FA SCREEN UI CODE
        otp_screen = customtkinter.CTkFrame(master=self, border_width=2)

        otp_entry = customtkinter.CTkEntry(master=otp_screen, placeholder_text="Enter 6-digit code", font=("Arial", 24))
        otp_entry.pack(pady=20, ipadx=100, ipady=10)

        button2 = customtkinter.CTkButton(master=otp_screen, text="Submit")
        button2.pack(pady=12, padx=10,ipadx=30,ipady=15, expand=True)


    def login_button_callback(self, login_screen, otp_screen):
        print("my button was clicked")
        login_screen.pack_forget()
        otp_screen.pack(pady=20, padx=10, ipadx=100, ipady=50, expand=True)





# MAIN
app = Application()
app.mainloop()