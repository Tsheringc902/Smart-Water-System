import tkinter as tk
from tkinter import messagebox, ttk

from config import APP_TITLE, COLORS
from database import Database
from login import LoginFrame
from complaints import ComplaintModule
from maintenance import MaintenanceModule
from analytics import AnalyticsModule
from dashboard import DashboardModule


class WaterApp(tk.Tk):
    """Main application window for the Smart Water Issue Monitoring System."""

    WINDOW_SIZE = "1280x780"
    MIN_WIDTH = 1050
    MIN_HEIGHT = 650

    SIDEBAR_WIDTH = 235
    TOPBAR_HEIGHT = 72

    def __init__(self):
        super().__init__()

        self.current_user = None
        self.content = None
        self.sidebar = None
        self.nav_buttons = []

        self._configure_window()
        self._initialize_modules()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.show_login()

    # ================================================================
    # APPLICATION SETUP
    # ================================================================

    def _configure_window(self):
        """Configure the main application window."""

        self.title(APP_TITLE)
        self.geometry(self.WINDOW_SIZE)
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.configure(bg=COLORS["light"])

        # ------------------------------------------------------------
        # ttk styling
        # ------------------------------------------------------------

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "App.TEntry",
            fieldbackground="#FFFFFF",
            foreground="#172B3A",
            insertcolor="#172B3A",
            bordercolor="#B8C5D1",
            lightcolor="#B8C5D1",
            darkcolor="#B8C5D1",
            padding=8,
        )

        style.map(
            "App.TEntry",
            foreground=[
                ("disabled", "#7A8793"),
                ("readonly", "#172B3A")
            ],
            fieldbackground=[
                ("disabled", "#EEF2F5"),
                ("readonly", "#FFFFFF")
            ],
        )

    def _initialize_modules(self):
        """Create the database and application modules."""

        self.db = Database()

        self.complaints = ComplaintModule(self)
        self.maintenance = MaintenanceModule(self)
        self.analytics = AnalyticsModule(self)
        self.dashboard = DashboardModule(self)

    # ================================================================
    # GENERAL WINDOW HELPERS
    # ================================================================

    def clear_window(self):
        """Remove all widgets from the main window."""

        for widget in self.winfo_children():
            widget.destroy()

        self.content = None
        self.sidebar = None
        self.nav_buttons.clear()

    def clear_content(self):
        """Remove widgets from the content area only."""

        if self.content is not None:
            for widget in self.content.winfo_children():
                widget.destroy()

    # ================================================================
    # LOGIN / DASHBOARD
    # ================================================================

    def show_login(self):
        """Display the login screen."""

        self.clear_window()

        self.current_user = None

        login = LoginFrame(self, self)

        login.pack(
            fill="both",
            expand=True
        )

    def show_dashboard(self):
        """Build and display the main application interface."""

        if not self.current_user:
            self.show_login()
            return

        self.clear_window()

        self._build_topbar()
        self._build_main_layout()
        self._build_sidebar()

        self.dashboard.show_home()

    # ================================================================
    # TOP BAR
    # ================================================================

    def _build_topbar(self):
        """Create the application top navigation bar."""

        topbar = tk.Frame(
            self,
            bg=COLORS["navy"],
            height=self.TOPBAR_HEIGHT
        )

        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # ------------------------------------------------------------
        # Application title
        # ------------------------------------------------------------

        title_frame = tk.Frame(
            topbar,
            bg=COLORS["navy"]
        )

        title_frame.pack(
            side="left",
            fill="y",
            padx=24
        )

        tk.Label(
            title_frame,
            text="💧",
            bg=COLORS["navy"],
            fg="white",
            font=("Segoe UI Emoji", 20)
        ).pack(
            side="left",
            padx=(0, 10)
        )

        tk.Label(
            title_frame,
            text="Smart Water System",
            bg=COLORS["navy"],
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(
            side="left"
        )

        # ------------------------------------------------------------
        # User information
        # ------------------------------------------------------------

        user_frame = tk.Frame(
            topbar,
            bg=COLORS["navy"]
        )

        user_frame.pack(
            side="right",
            padx=24
        )

        full_name = self.current_user.get(
            "full_name",
            "User"
        )

        role = self.current_user.get(
            "role",
            "User"
        )

        tk.Label(
            user_frame,
            text=full_name,
            bg=COLORS["navy"],
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="e"
        )

        tk.Label(
            user_frame,
            text=role,
            bg=COLORS["navy"],
            fg="#BFD4E8",
            font=("Segoe UI", 9)
        ).pack(
            anchor="e",
            pady=(2, 0)
        )

    # ================================================================
    # MAIN LAYOUT
    # ================================================================

    def _build_main_layout(self):
        """Create the sidebar and main content areas."""

        body = tk.Frame(
            self,
            bg=COLORS["light"]
        )

        body.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------------
        # Sidebar
        # ------------------------------------------------------------

        self.sidebar = tk.Frame(
            body,
            bg="#173F67",
            width=self.SIDEBAR_WIDTH
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ------------------------------------------------------------
        # Main content
        # ------------------------------------------------------------

        self.content = tk.Frame(
            body,
            bg=COLORS["light"]
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    # ================================================================
    # SIDEBAR
    # ================================================================

    def _build_sidebar(self):
        """Create role-based sidebar navigation."""

        sidebar = self.sidebar

        # ------------------------------------------------------------
        # Brand
        # ------------------------------------------------------------

        brand = tk.Frame(
            sidebar,
            bg="#173F67"
        )

        brand.pack(
            fill="x",
            padx=20,
            pady=(24, 18)
        )

        tk.Label(
            brand,
            text="SMART WATER",
            bg="#173F67",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            brand,
            text="Issue Monitoring & Management",
            bg="#173F67",
            fg="#AFC8E0",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ------------------------------------------------------------
        # Main menu heading
        # ------------------------------------------------------------

        tk.Label(
            sidebar,
            text="MAIN MENU",
            bg="#173F67",
            fg="#AFC8E0",
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(8, 10)
        )

        # ------------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------------

        self._add_nav_button(
            "🏠  Dashboard",
            self.dashboard.show_home
        )

        # ------------------------------------------------------------
        # ROLE-BASED NAVIGATION
        # ------------------------------------------------------------

        role = self.current_user.get("role")

        # ============================================================
        # STUDENT
        # ============================================================

        if role == "Student":

            self._add_nav_button(
                "📝  Submit Complaint",
                self.complaints.show_form
            )

            self._add_nav_button(
                "📋  My Complaints",
                self.complaints.show_my_complaints
            )

        # ============================================================
        # ADMIN
        # ============================================================

        elif role == "Admin":

            self._add_nav_button(
                "📋  Manage Complaints",
                self.complaints.show_manage
            )

            self._add_nav_button(
                "📊  Analytics",
                self.analytics.show
            )

            self._add_nav_button(
                "🔧  Maintenance",
                self.maintenance.show
            )

        # ============================================================
        # MAINTENANCE
        # ============================================================

        elif role == "Maintenance":

            self._add_nav_button(
                "🔧  Maintenance",
                self.maintenance.show
            )

        # ============================================================
        # ACCOUNT
        # ============================================================

        tk.Label(
            sidebar,
            text="ACCOUNT",
            bg="#173F67",
            fg="#AFC8E0",
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(24, 10)
        )

        self._add_nav_button(
            "🔐  Change Password",
            self.show_change_password
        )

        self._add_nav_button(
            "🚪  Logout",
            self.logout
        )

        # ------------------------------------------------------------
        # Footer
        # ------------------------------------------------------------

        footer = tk.Frame(
            sidebar,
            bg="#173F67"
        )

        footer.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=18
        )

        tk.Label(
            footer,
            text="Water Management System",
            bg="#173F67",
            fg="#8EABC5",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w"
        )

    # ================================================================
    # SIDEBAR BUTTON
    # ================================================================

    def _add_nav_button(self, text, command):
        """Create a macOS-safe sidebar navigation button."""

        button = tk.Frame(
            self.sidebar,
            bg="#173F67",
            cursor="hand2",
            height=48
        )

        button.pack(
            fill="x",
            padx=8,
            pady=2
        )

        button.pack_propagate(False)

        label = tk.Label(
            button,
            text=text,
            bg="#173F67",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=14,
            cursor="hand2"
        )

        label.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------------
        # Hover
        # ------------------------------------------------------------

        def on_enter(event):
            button.configure(
                bg=COLORS["blue"]
            )

            label.configure(
                bg=COLORS["blue"],
                fg="white"
            )

        def on_leave(event):
            button.configure(
                bg="#173F67"
            )

            label.configure(
                bg="#173F67",
                fg="white"
            )

        # ------------------------------------------------------------
        # Click
        # ------------------------------------------------------------

        def on_click(event):
            command()

        for widget in (
            button,
            label
        ):

            widget.bind(
                "<Enter>",
                on_enter
            )

            widget.bind(
                "<Leave>",
                on_leave
            )

            widget.bind(
                "<Button-1>",
                on_click
            )

        self.nav_buttons.append(button)

    # ================================================================
    # CONTENT HEADER
    # ================================================================

    def set_content_title(
        self,
        title,
        subtitle=""
    ):
        """Create a clean page title."""

        self.clear_content()

        header = tk.Frame(
            self.content,
            bg=COLORS["light"]
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(28, 12)
        )

        tk.Label(
            header,
            text=title,
            bg=COLORS["light"],
            fg=COLORS["dark"],
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w"
        )

        if subtitle:

            tk.Label(
                header,
                text=subtitle,
                bg=COLORS["light"],
                fg=COLORS["gray"],
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                pady=(5, 0)
            )

    # ================================================================
    # CHANGE PASSWORD
    # ================================================================

    def show_change_password(self):
        """Display the change-password form."""

        if not self.current_user:
            self.show_login()
            return

        self.set_content_title(
            "Change Password",
            "Update your password to keep your account secure."
        )

        form = tk.Frame(
            self.content,
            bg="white",
            highlightthickness=1,
            highlightbackground="#E1E7ED"
        )

        form.pack(
            anchor="nw",
            padx=30,
            pady=10,
            ipadx=28,
            ipady=25
        )

        tk.Label(
            form,
            text="Account Security",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 13, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=14,
            pady=(5, 18)
        )

        old = tk.StringVar()
        new = tk.StringVar()
        confirm = tk.StringVar()

        fields = [
            ("Old Password", old),
            ("New Password", new),
            ("Confirm Password", confirm),
        ]

        entries = []

        for row, (label_text, variable) in enumerate(
            fields,
            start=1
        ):

            tk.Label(
                form,
                text=label_text,
                bg="white",
                fg=COLORS["dark"],
                font=("Segoe UI", 10, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(14, 12),
                pady=9
            )

            entry = ttk.Entry(
                form,
                textvariable=variable,
                show="*",
                width=32,
                style="App.TEntry"
            )

            entry.grid(
                row=row,
                column=1,
                padx=(4, 14),
                pady=9
            )

            entries.append(entry)

        # ------------------------------------------------------------
        # Save password
        # ------------------------------------------------------------

        def save():

            old_password = old.get()
            new_password = new.get()
            confirmation = confirm.get()

            if not old_password or not new_password or not confirmation:

                messagebox.showwarning(
                    "Missing information",
                    "Please fill in all password fields.",
                    parent=self
                )

                return

            if new_password != confirmation:

                messagebox.showerror(
                    "Password error",
                    "New password and confirmation do not match.",
                    parent=self
                )

                return

            if old_password == new_password:

                messagebox.showwarning(
                    "Password error",
                    "Your new password must be different from your old password.",
                    parent=self
                )

                return

            success, message = self.db.change_password(
                self.current_user["id"],
                old_password,
                new_password
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    message,
                    parent=self
                )

                old.set("")
                new.set("")
                confirm.set("")

                entries[0].focus_set()

            else:

                messagebox.showerror(
                    "Password error",
                    message,
                    parent=self
                )

        # ------------------------------------------------------------
        # Change password button
        # ------------------------------------------------------------

        button_frame = tk.Frame(
            form,
            bg=COLORS["green"],
            cursor="hand2",
            height=44
        )

        button_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=(20, 8),
            padx=14,
            sticky="ew"
        )

        button_frame.grid_propagate(False)

        button_label = tk.Label(
            button_frame,
            text="Change Password",
            bg=COLORS["green"],
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )

        button_label.pack(
            fill="both",
            expand=True
        )

        def button_enter(event):

            button_frame.configure(
                bg=COLORS["blue"]
            )

            button_label.configure(
                bg=COLORS["blue"],
                fg="#FFFFFF"
            )

        def button_leave(event):

            button_frame.configure(
                bg=COLORS["green"]
            )

            button_label.configure(
                bg=COLORS["green"],
                fg="#FFFFFF"
            )

        def button_click(event):

            save()

        for widget in (
            button_frame,
            button_label
        ):

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

        entries[0].focus_set()

    # ================================================================
    # LOGOUT
    # ================================================================

    def logout(self):
        """Log the current user out after confirmation."""

        if not self.current_user:

            self.show_login()

            return

        confirmed = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            parent=self
        )

        if confirmed:

            self.current_user = None

            self.show_login()

    # ================================================================
    # CLOSE APPLICATION
    # ================================================================

    def close_app(self):
        """Safely close the application."""

        confirmed = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to close the Smart Water System?",
            parent=self
        )

        if not confirmed:
            return

        try:
            self.db.close()
        except Exception:
            pass

        self.destroy()


# ====================================================================
# START APPLICATION
# ====================================================================

if __name__ == "__main__":

    app = WaterApp()

    app.mainloop()