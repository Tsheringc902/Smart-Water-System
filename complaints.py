import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import COLORS, BUILDINGS, ISSUE_TYPES, PRIORITIES, STATUSES
from ui_helpers import make_table
from exports import export_complaints_to_csv, export_complaints_to_excel


class ComplaintModule:
    def __init__(self, app):
        self.app = app

    # ================================================================
    # MAC-SAFE BUTTON
    # ================================================================
    def make_safe_button(
        self,
        parent,
        text,
        command,
        bg_color,
        width=150,
        height=40
    ):
        """
        Creates a Mac-safe button using Frame + Label.

        This avoids the macOS Tkinter issue where native buttons
        can display white/invisible text on a light background.
        """

        button = tk.Frame(
            parent,
            bg=bg_color,
            width=width,
            height=height,
            cursor="hand2"
        )

        # Keep the requested width and height.
        button.pack_propagate(False)

        label = tk.Label(
            button,
            text=text,
            bg=bg_color,
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )

        label.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------------
        # Hover colour
        # ------------------------------------------------------------
        hover_color = self._darken_color(bg_color)

        def button_enter(event):
            button.configure(
                bg=hover_color
            )

            label.configure(
                bg=hover_color,
                fg="#FFFFFF"
            )

        def button_leave(event):
            button.configure(
                bg=bg_color
            )

            label.configure(
                bg=bg_color,
                fg="#FFFFFF"
            )

        def button_click(event):
            command()

        # Bind to both frame and label so clicking the text also works.
        for widget in (button, label):

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

        return button

    # ================================================================
    # DARKER HOVER COLOUR
    # ================================================================
    def _darken_color(self, color):

        color_map = {
            COLORS.get("blue"): "#245B8F",
            COLORS.get("green"): "#247A4A",
            COLORS.get("purple"): "#5A45A8",
            COLORS.get("gray"): "#596773",
            COLORS.get("red"): "#A83232",
            COLORS.get("yellow"): "#B88900",
        }

        return color_map.get(
            color,
            "#245B8F"
        )

    # ================================================================
    # SUBMIT COMPLAINT FORM
    # ================================================================
    def show_form(self):

        self.app.set_content_title(
            "Submit Water Complaint",
            "Report a water-related problem."
        )

        # ------------------------------------------------------------
        # Main white form area
        # ------------------------------------------------------------
        form = tk.Frame(
            self.app.content,
            bg="white"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=5
        )

        # ------------------------------------------------------------
        # Fields container
        # ------------------------------------------------------------
        fields = tk.Frame(
            form,
            bg="white"
        )

        fields.pack(
            fill="x",
            padx=25,
            pady=22
        )

        # ============================================================
        # COMBOBOX HELPER
        # ============================================================
        def add_combo(
            row,
            label,
            values,
            default
        ):

            tk.Label(
                fields,
                text=label,
                bg="white",
                fg=COLORS["dark"],
                font=("Segoe UI", 10, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=8
            )

            variable = tk.StringVar(
                value=default
            )

            combo = ttk.Combobox(
                fields,
                textvariable=variable,
                values=values,
                state="readonly",
                width=35
            )

            combo.grid(
                row=row,
                column=1,
                sticky="w",
                padx=18,
                pady=8
            )

            return variable

        # ============================================================
        # BUILDING
        # ============================================================
        building = add_combo(
            0,
            "Building",
            BUILDINGS,
            BUILDINGS[0]
        )

        # ============================================================
        # ISSUE TYPE
        # ============================================================
        issue = add_combo(
            1,
            "Issue Type",
            ISSUE_TYPES,
            ISSUE_TYPES[0]
        )

        # ============================================================
        # PRIORITY
        # ============================================================
        priority = add_combo(
            2,
            "Priority",
            PRIORITIES,
            "Medium"
        )

        # ============================================================
        # PHOTO
        # ============================================================
        tk.Label(
            fields,
            text="Photo (Optional)",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        photo = tk.StringVar()

        photo_frame = tk.Frame(
            fields,
            bg="white"
        )

        photo_frame.grid(
            row=3,
            column=1,
            sticky="w",
            padx=18,
            pady=8
        )

        # Photo path
        ttk.Entry(
            photo_frame,
            textvariable=photo,
            width=28
        ).pack(
            side="left"
        )

        # ============================================================
        # BROWSE BUTTON
        # ============================================================
        def browse():

            path = filedialog.askopenfilename(
                filetypes=[
                    (
                        "Image files",
                        "*.png *.jpg *.jpeg"
                    ),
                    (
                        "All files",
                        "*.*"
                    )
                ]
            )

            if path:
                photo.set(path)

        browse_button = self.make_safe_button(
            photo_frame,
            "Browse",
            browse,
            COLORS["gray"],
            width=95,
            height=34
        )

        browse_button.pack(
            side="left",
            padx=5
        )

        # ============================================================
        # DESCRIPTION
        # ============================================================
        tk.Label(
            fields,
            text="Description",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=4,
            column=0,
            sticky="nw",
            pady=8
        )

        description = tk.Text(
            fields,
            width=55,
            height=7,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        description.grid(
            row=4,
            column=1,
            sticky="w",
            padx=18,
            pady=8
        )

        # ============================================================
        # SUBMIT FUNCTION
        # ============================================================
        def submit():

            text = description.get(
                "1.0",
                "end"
            ).strip()

            if not text:

                messagebox.showwarning(
                    "Missing description",
                    "Please describe the water issue."
                )

                return

            self.app.db.add_complaint(
                self.app.current_user["id"],
                building.get(),
                issue.get(),
                priority.get(),
                text,
                photo.get().strip()
            )

            messagebox.showinfo(
                "Success",
                "Complaint submitted successfully."
            )

            self.show_my_complaints()

        # ============================================================
        # FORM BUTTONS
        # ============================================================
        buttons = tk.Frame(
            form,
            bg="white"
        )

        buttons.pack(
            anchor="w",
            padx=25,
            pady=10
        )

        # ------------------------------------------------------------
        # SUBMIT COMPLAINT
        # ------------------------------------------------------------
        submit_button = self.make_safe_button(
            buttons,
            "Submit Complaint",
            submit,
            COLORS["green"],
            width=185,
            height=40
        )

        submit_button.pack(
            side="left",
            padx=(0, 12)
        )

        # ------------------------------------------------------------
        # CLEAR FORM
        # ------------------------------------------------------------
        clear_button = self.make_safe_button(
            buttons,
            "Clear Form",
            self.show_form,
            COLORS["gray"],
            width=130,
            height=40
        )

        clear_button.pack(
            side="left"
        )

    # ================================================================
    # MY COMPLAINTS
    # ================================================================
    def show_my_complaints(self):

        self.app.set_content_title(
            "My Complaints",
            "Track your submitted complaints."
        )

        container = tk.Frame(
            self.app.content,
            bg="white"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=5
        )

        columns = (
            "id",
            "building",
            "issue",
            "priority",
            "description",
            "status",
            "date"
        )

        headings = (
            "ID",
            "Building",
            "Issue",
            "Priority",
            "Description",
            "Status",
            "Date"
        )

        widths = (
            60,
            150,
            120,
            90,
            300,
            110,
            150
        )

        tree = make_table(
            container,
            columns,
            headings,
            widths
        )

        # ------------------------------------------------------------
        # Load user's complaints
        # ------------------------------------------------------------
        for row in self.app.db.get_user_complaints(
            self.app.current_user["id"]
        ):

            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["building"],
                    row["issue_type"],
                    row["priority"],
                    row["description"],
                    row["status"],
                    row["created_at"]
                )
            )

        # ============================================================
        # VIEW SELECTED
        # ============================================================
        def view_selected():

            selected = tree.selection()

            if not selected:

                messagebox.showwarning(
                    "Select complaint",
                    "Select a complaint first."
                )

                return

            complaint_id = tree.item(
                selected[0],
                "values"
            )[0]

            self.show_details(
                complaint_id
            )

        view_button = self.make_safe_button(
            self.app.content,
            "View Selected Details",
            view_selected,
            COLORS["blue"],
            width=210,
            height=40
        )

        view_button.pack(
            anchor="w",
            padx=48,
            pady=(0, 20)
        )

    # ================================================================
    # COMPLAINT DETAILS
    # ================================================================
    def show_details(
        self,
        complaint_id
    ):

        row = self.app.db.get_complaint(
            complaint_id
        )

        if not row:

            messagebox.showerror(
                "Error",
                "Complaint was not found."
            )

            return

        window = tk.Toplevel(
            self.app
        )

        window.title(
            f"Complaint Details #{complaint_id}"
        )

        window.geometry(
            "600x520"
        )

        window.configure(
            bg="white"
        )

        window.transient(
            self.app
        )

        # ------------------------------------------------------------
        # Title
        # ------------------------------------------------------------
        tk.Label(
            window,
            text=f"Complaint Details #{complaint_id}",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=20
        )

        details = tk.Frame(
            window,
            bg="white"
        )

        details.pack(
            fill="both",
            expand=True,
            padx=30
        )

        fields = [
            ("Reported By", row["full_name"]),
            ("Username", row["username"]),
            ("Building", row["building"]),
            ("Issue Type", row["issue_type"]),
            ("Priority", row["priority"]),
            ("Status", row["status"]),
            ("Created At", row["created_at"]),
            ("Updated At", row["updated_at"]),
            (
                "Photo Path",
                row["photo_path"] or "Not attached"
            ),
            ("Description", row["description"])
        ]

        for label, value in fields:

            line = tk.Frame(
                details,
                bg="white"
            )

            line.pack(
                fill="x",
                pady=4
            )

            tk.Label(
                line,
                text=f"{label}:",
                bg="white",
                fg=COLORS["dark"],
                font=("Segoe UI", 10, "bold"),
                width=16,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                line,
                text=str(value),
                bg="white",
                fg=COLORS["gray"],
                font=("Segoe UI", 10),
                wraplength=350,
                justify="left",
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        # ============================================================
        # CLOSE
        # ============================================================
        close_button = self.make_safe_button(
            window,
            "Close",
            window.destroy,
            COLORS["gray"],
            width=120,
            height=40
        )

        close_button.pack(
            pady=20
        )

    # ================================================================
    # MANAGE COMPLAINTS
    # ================================================================
    def show_manage(self):

        self.app.set_content_title(
            "Manage Complaints",
            "Search, view, update, and export complaints."
        )

        # ============================================================
        # TOOLBAR
        # ============================================================
        toolbar = tk.Frame(
            self.app.content,
            bg=COLORS["light"]
        )

        toolbar.pack(
            fill="x",
            padx=28,
            pady=5
        )

        # Search label
        tk.Label(
            toolbar,
            text="Search:",
            bg=COLORS["light"],
            fg=COLORS["dark"],
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left"
        )

        search = tk.StringVar()

        ttk.Entry(
            toolbar,
            textvariable=search,
            width=25
        ).pack(
            side="left",
            padx=8
        )

        # Status label
        tk.Label(
            toolbar,
            text="Status:",
            bg=COLORS["light"],
            fg=COLORS["dark"],
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(15, 5)
        )

        status = tk.StringVar(
            value="All"
        )

        status_combo = ttk.Combobox(
            toolbar,
            textvariable=status,
            values=["All"] + STATUSES,
            state="readonly",
            width=15
        )

        status_combo.pack(
            side="left"
        )

        # ============================================================
        # TABLE
        # ============================================================
        columns = (
            "id",
            "student",
            "building",
            "issue",
            "priority",
            "status",
            "date"
        )

        headings = (
            "ID",
            "Reported By",
            "Building",
            "Issue",
            "Priority",
            "Status",
            "Date"
        )

        widths = (
            60,
            150,
            150,
            120,
            90,
            110,
            150
        )

        container = tk.Frame(
            self.app.content,
            bg="white"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=10
        )

        tree = make_table(
            container,
            columns,
            headings,
            widths
        )

        # ============================================================
        # LOAD DATA
        # ============================================================
        def load():

            for item in tree.get_children():

                tree.delete(
                    item
                )

            rows = self.app.db.get_all_complaints(
                search.get().strip(),
                status.get()
            )

            for row in rows:

                tree.insert(
                    "",
                    "end",
                    values=(
                        row["id"],
                        row["full_name"],
                        row["building"],
                        row["issue_type"],
                        row["priority"],
                        row["status"],
                        row["created_at"]
                    )
                )

        # ============================================================
        # GET SELECTED ID
        # ============================================================
        def selected_id():

            selected = tree.selection()

            if not selected:

                messagebox.showwarning(
                    "Select complaint",
                    "Select a complaint first."
                )

                return None

            return tree.item(
                selected[0],
                "values"
            )[0]

        # ============================================================
        # VIEW
        # ============================================================
        def view():

            complaint_id = selected_id()

            if complaint_id:
                self.show_details(
                    complaint_id
                )

        # ============================================================
        # UPDATE STATUS
        # ============================================================
        def update_status():

            complaint_id = selected_id()

            if not complaint_id:
                return

            dialog = tk.Toplevel(
                self.app
            )

            dialog.title(
                "Update Status"
            )

            dialog.geometry(
                "350x220"
            )

            dialog.configure(
                bg="white"
            )

            dialog.transient(
                self.app
            )

            tk.Label(
                dialog,
                text="New Status",
                bg="white",
                fg=COLORS["dark"],
                font=("Segoe UI", 11, "bold")
            ).pack(
                pady=20
            )

            new_status = tk.StringVar(
                value="Pending"
            )

            ttk.Combobox(
                dialog,
                textvariable=new_status,
                values=STATUSES,
                state="readonly",
                width=20
            ).pack()

            # --------------------------------------------------------
            # SAVE
            # --------------------------------------------------------
            def save():

                self.app.db.update_complaint_status(
                    complaint_id,
                    new_status.get()
                )

                dialog.destroy()

                load()

                messagebox.showinfo(
                    "Success",
                    "Status updated."
                )

            save_button = self.make_safe_button(
                dialog,
                "Save",
                save,
                COLORS["green"],
                width=120,
                height=40
            )

            save_button.pack(
                pady=20
            )

        # ============================================================
        # SEARCH
        # ============================================================
        search_button = self.make_safe_button(
            toolbar,
            "Search",
            load,
            COLORS["blue"],
            width=90,
            height=34
        )

        search_button.pack(
            side="left",
            padx=8
        )

        # ============================================================
        # VIEW DETAILS
        # ============================================================
        view_button = self.make_safe_button(
            toolbar,
            "View Details",
            view,
            COLORS["purple"],
            width=120,
            height=34
        )

        view_button.pack(
            side="left",
            padx=4
        )

        # ============================================================
        # UPDATE STATUS
        # ============================================================
        update_button = self.make_safe_button(
            toolbar,
            "Update Status",
            update_status,
            COLORS["green"],
            width=135,
            height=34
        )

        update_button.pack(
            side="left",
            padx=4
        )

        # ============================================================
        # EXPORT CSV
        # ============================================================
        def export_csv():

            rows = self.app.db.get_all_complaints(
                search.get().strip(),
                status.get()
            )

            export_complaints_to_csv(
                rows
            )

        csv_button = self.make_safe_button(
            toolbar,
            "CSV",
            export_csv,
            COLORS["gray"],
            width=70,
            height=34
        )

        csv_button.pack(
            side="left",
            padx=4
        )

        # ============================================================
        # EXPORT EXCEL
        # ============================================================
        def export_excel():

            rows = self.app.db.get_all_complaints(
                search.get().strip(),
                status.get()
            )

            export_complaints_to_excel(
                rows
            )

        excel_button = self.make_safe_button(
            toolbar,
            "Excel",
            export_excel,
            COLORS["gray"],
            width=75,
            height=34
        )

        excel_button.pack(
            side="left",
            padx=4
        )

        # ============================================================
        # STATUS FILTER
        # ============================================================
        status_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: load()
        )

        # ============================================================
        # INITIAL LOAD
        # ============================================================
        load()