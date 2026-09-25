import tkinter as tk
from tkinter import ttk, messagebox

from config import COLORS, ROLES


class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["light"])
        self.app = app
        self.build()

    def build(self):
        # ============================================================
        # HEADER
        # ============================================================
        header = tk.Frame(
            self,
            bg=COLORS["navy"],
            height=115
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💧 SMART WATER",
            bg=COLORS["navy"],
            fg="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(20, 0))

        tk.Label(
            header,
            text="College Water Issue Monitoring and Management System",
            bg=COLORS["navy"],
            fg="#DDEBFA",
            font=("Segoe UI", 11)
        ).pack(pady=5)

        # ============================================================
        # LOGIN CARD
        # ============================================================
        card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#D6DEE8",
            highlightthickness=1
        )

        card.place(
            relx=0.5,
            rely=0.55,
            anchor="center",
            width=450,
            height=455
        )

        # Title
        tk.Label(
            card,
            text="Login to your account",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(25, 20))

        # ============================================================
        # FORM
        # ============================================================
        form = tk.Frame(
            card,
            bg="white"
        )
        form.pack(
            fill="x",
            padx=50
        )

        # Username
        tk.Label(
            form,
            text="Username",
            bg="white",
            fg="#172B3A",
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x")

        username = ttk.Entry(
            form,
            font=("Segoe UI", 11)
        )
        username.pack(
            fill="x",
            ipady=6,
            pady=(5, 13)
        )

        # Password
        tk.Label(
            form,
            text="Password",
            bg="white",
            fg="#172B3A",
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x")

        password = ttk.Entry(
            form,
            show="*",
            font=("Segoe UI", 11)
        )
        password.pack(
            fill="x",
            ipady=6,
            pady=(5, 13)
        )

        # Role
        tk.Label(
            form,
            text="Role",
            bg="white",
            fg="#172B3A",
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).pack(fill="x")

        role = tk.StringVar(value="Student")

        role_box = ttk.Combobox(
            form,
            textvariable=role,
            values=ROLES,
            state="readonly",
            font=("Segoe UI", 11)
        )

        role_box.pack(
            fill="x",
            ipady=5,
            pady=(5, 18)
        )

        # ============================================================
        # LOGIN FUNCTION
        # ============================================================
        def do_login():
            user = self.app.db.authenticate(
                username.get().strip(),
                password.get(),
                role.get()
            )

            if user:
                self.app.current_user = user
                self.app.show_dashboard()
            else:
                messagebox.showerror(
                    "Login failed",
                    "Invalid username, password, or role."
                )

        # ============================================================
        # MAC-SAFE LOGIN BUTTON
        # ============================================================
        # Using Frame + Label instead of tk.Button prevents the
        # macOS Tk theme from making the button text invisible.

        login_button = tk.Frame(
            form,
            bg=COLORS["blue"],
            cursor="hand2",
            height=44
        )

        login_button.pack(
            fill="x",
            pady=(0, 2)
        )

        login_button.pack_propagate(False)

        login_text = tk.Label(
            login_button,
            text="LOGIN",
            bg=COLORS["blue"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )

        login_text.pack(
            fill="both",
            expand=True
        )

        # Hover effect
        def button_enter(event):
            login_button.configure(
                bg="#245B8F"
            )
            login_text.configure(
                bg="#245B8F",
                fg="white"
            )

        def button_leave(event):
            login_button.configure(
                bg=COLORS["blue"]
            )
            login_text.configure(
                bg=COLORS["blue"],
                fg="white"
            )

        def button_click(event):
            do_login()

        for widget in (login_button, login_text):
            widget.bind(
                "<Enter>",
                button_enter
            )
            widget.bind(
                "<Leave>",
                button_leave
            )
            widget.bind(
                "<Button-1>",
                button_click
            )

        # ============================================================
        # DEMO ACCOUNTS
        # ============================================================
        tk.Label(
            card,
            text=(
                "Demo accounts:\n"
                "student / Student123\n"
                "maintenance / Maintenance123\n"
                "admin / Admin123"
            ),
            bg="white",
            fg=COLORS["gray"],
            font=("Segoe UI", 9),
            justify="center"
        ).pack(
            pady=15
        )

        # ============================================================
        # KEYBOARD SUPPORT
        # ============================================================
        password.bind(
            "<Return>",
            lambda event: do_login()
        )

        username.bind(
            "<Return>",
            lambda event: password.focus_set()
        )

        username.focus_set()