import customtkinter

from Project.code_gen import AccountStorage


class Application(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.resizable(width=False, height=False)
        self.title("2FA Demo")
        self.acc_database = AccountStorage()


        # LOGIN SCREEN UI CODE
        login_screen = customtkinter.CTkFrame(master=self, border_width=2, width=200)
        login_screen.pack(pady=20, padx=10,ipadx=50, ipady=25, expand=True)

        label = customtkinter.CTkLabel(master=login_screen, text="Login System", font=("Arial", 24))
        label.pack(pady=12, padx=10)

        self.entry1 = customtkinter.CTkEntry(master=login_screen, placeholder_text="Username")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=login_screen, placeholder_text="Password", show="*")
        self.entry2.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=login_screen, text="Login", command=lambda: self.login_button_callback(login_screen, otp_screen))
        button.pack(pady=12, padx=10, expand=True)



        # 2FA SCREEN UI CODE
        otp_screen = customtkinter.CTkFrame(master=self, border_width=2)

        otp_entry = customtkinter.CTkEntry(
            master=otp_screen, placeholder_text="Enter 6-digit code", font=("Arial", 24), validate="key", validatecommand=(self.register(self.input_validation), "%P")
        )
        otp_entry.pack(pady=20, ipadx=100, ipady=10)

        invalid_label = customtkinter.CTkLabel(master=otp_screen, text="Invalid Code", font=("Arial", 12), text_color="red")
        invalid_label.pack(pady=0, padx=10)

        button2 = customtkinter.CTkButton(master=otp_screen, text="Submit")
        button2.pack(pady=12, padx=10,ipadx=30,ipady=15, expand=True)


    def login_button_callback(self, login_screen, otp_screen):
        print("my button was clicked")
        self.acc_database.add_account(self.entry1.get(), self.entry2.get())
        login_screen.pack_forget()
        otp_screen.pack(pady=20, padx=10, ipadx=100, ipady=50, expand=True)

    def input_validation(self, text_if_allowed):
        # case for when there is only one char left which is needed or else it can't be deleted
        if len(text_if_allowed) == 0:
            return True
        elif len(text_if_allowed) > 6 or not text_if_allowed.isdigit():
            return False
        else:
            return True

