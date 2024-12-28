import customtkinter

from Project.code_gen import AccountStorage


class Application(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.resizable(width=False, height=False)
        self.title("2FA Demo")
        self.acc_database = AccountStorage()


        ### LOGIN SCREEN UI CODE ###
        self.login_screen = customtkinter.CTkFrame(master=self, border_width=2, width=200)
        self.login_screen.pack(pady=20, padx=10,ipadx=50, ipady=25, expand=True)

        self.label = customtkinter.CTkLabel(master=self.login_screen, text="Login System", font=("Arial", 24))
        self.label.pack(pady=12, padx=10)

        self.new_email = customtkinter.CTkEntry(master=self.login_screen, placeholder_text="E-mail")
        self.new_email.pack(pady=12, padx=10)

        self.new_password = customtkinter.CTkEntry(master=self.login_screen, placeholder_text="Password", show="*")
        self.new_password.pack(pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=self.login_screen, text="Create Account", command=self.login_button_callback)
        self.login_button.pack(pady=12, padx=10, expand=True)



        ### 2FA SCREEN UI CODE ###
        self.otp_screen = customtkinter.CTkFrame(master=self, border_width=2)

        self.otp_info_label = customtkinter.CTkLabel(master=self.otp_screen, text="Please enter the 6-digit code that was sent to your email", font=("Arial", 20))
        self.otp_info_label.pack(pady=12, padx=10)
        # accessing a protected method of the inherited tkinter label so that I can get the text to wrap
        self.otp_info_label._label.configure(wraplength=275)

        self.otp_entry = customtkinter.CTkEntry(
            master=self.otp_screen, font=("Arial", 48), validate="key", validatecommand=(self.register(self.input_validation), "%P")
        )
        self.otp_entry.pack(pady=5, ipadx=75, ipady=15)
        # modifying the internal tkinter entry widget in order to center the inputted text
        self.otp_entry._entry.configure(justify="center")

        self.invalid_label = customtkinter.CTkLabel(master=self.otp_screen, text="", font=("Arial", 12), text_color="red")
        self.invalid_label.pack(pady=0, padx=10)

        self.otp_submit_button = customtkinter.CTkButton(master=self.otp_screen, text="Submit", command=self.otp_button_callback)
        self.otp_submit_button.pack(padx=10,ipadx=30,ipady=15, expand=True)


        ### EXTRA IDK SCREEN FOR SUCCESSFUL 2FA ###
        self.main_system_screen = customtkinter.CTkFrame(master=self, border_width=2)

        self.welcome_label = customtkinter.CTkLabel(master=self.main_system_screen, text="Welcome!", font=("Arial", 20))
        self.welcome_label.pack(pady=12, padx=10, fill="both", expand=True)


    def login_button_callback(self):
        self.acc_database.add_account(self.new_email.get(), self.new_password.get())
        self.acc_database.send_otp_code(self.new_email.get(), self.new_password.get())
        self.login_screen.pack_forget()
        self.otp_screen.pack(pady=20, padx=10, ipadx=100, ipady=50, expand=True)

    def otp_button_callback(self):
        code_verification = self.acc_database.verify_otp_code(self.otp_entry.get())
        if code_verification:
            self.invalid_label.configure(text="")
            self.otp_screen.pack_forget()
            self.main_system_screen.pack(pady=20, padx=10, ipadx=100, ipady=50, fill="both", expand=True)
            print("SUCCESS")
        else:
            self.invalid_label.configure(text="Invalid Code")
            print("FAILURE")


    def input_validation(self, text_if_allowed):
        # case for when there is only one char left which is needed or else it can't be deleted
        if len(text_if_allowed) == 0:
            return True
        elif len(text_if_allowed) > 6 or not text_if_allowed.isdigit():
            return False
        else:
            return True

