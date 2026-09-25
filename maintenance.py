import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, BUILDINGS
from ui_helpers import make_button, make_table


class MaintenanceModule:
    def __init__(self, app):
        self.app = app

    def show(self):
        self.app.set_content_title(
            "Maintenance Schedule",
            "Create, edit, and delete planned maintenance records."
        )

        toolbar = tk.Frame(self.app.content, bg=COLORS["light"])
        toolbar.pack(fill="x", padx=28, pady=5)

        columns = ("id", "title", "building", "date", "status")
        headings = ("ID", "Activity", "Building", "Date", "Status")
        widths = (60, 250, 180, 140, 120)

        container = tk.Frame(self.app.content, bg="white")
        container.pack(fill="both", expand=True, padx=28, pady=10)
        tree = make_table(container, columns, headings, widths)

        def load():
            for item in tree.get_children():
                tree.delete(item)

            for row in self.app.db.get_maintenance():
                tree.insert("", "end", values=(
                    row["id"], row["title"], row["building"],
                    row["maintenance_date"], row["status"]
                ))

        def selected_id():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning(
                    "Select record",
                    "Select a maintenance record first."
                )
                return None
            return tree.item(selected[0], "values")[0]

        def open_form(record=None):
            window = tk.Toplevel(self.app)
            window.title("Maintenance Form")
            window.geometry("480x390")
            window.configure(bg="white")
            window.transient(self.app)
            window.grab_set()

            title_value = tk.StringVar(
                value=record["title"] if record else ""
            )
            building_value = tk.StringVar(
                value=record["building"] if record else BUILDINGS[0]
            )
            date_value = tk.StringVar(
                value=record["maintenance_date"] if record else ""
            )
            status_value = tk.StringVar(
                value=record["status"] if record else "Planned"
            )

            form = tk.Frame(window, bg="white")
            form.pack(fill="x", padx=35, pady=25)

            def field(row, label, variable, values=None):
                tk.Label(
                    form, text=label, bg="white",
                    font=("Segoe UI", 10, "bold")
                ).grid(row=row, column=0, sticky="w", pady=8)

                if values:
                    widget = ttk.Combobox(
                        form, textvariable=variable,
                        values=values, state="readonly", width=25
                    )
                else:
                    widget = ttk.Entry(
                        form, textvariable=variable, width=28
                    )

                widget.grid(row=row, column=1, padx=15, pady=8)
                return widget

            field(0, "Activity", title_value)
            field(1, "Building", building_value, BUILDINGS)
            field(2, "Date (YYYY-MM-DD)", date_value)
            field(3, "Status", status_value, ["Planned", "Completed", "Cancelled"])

            def save():
                if not title_value.get().strip() or not date_value.get().strip():
                    messagebox.showwarning(
                        "Missing information",
                        "Enter an activity and date."
                    )
                    return

                if record:
                    self.app.db.update_maintenance(
                        record["id"], title_value.get().strip(),
                        building_value.get(), date_value.get().strip(),
                        status_value.get()
                    )
                else:
                    self.app.db.add_maintenance(
                        title_value.get().strip(),
                        building_value.get(), date_value.get().strip(),
                        status_value.get()
                    )

                window.destroy()
                load()

            make_button(
                window, "Save", save, COLORS["green"], 16
            ).pack(pady=15)

        def add():
            open_form()

        def edit():
            record_id = selected_id()
            if not record_id:
                return

            record = next(
                (
                    row for row in self.app.db.get_maintenance()
                    if str(row["id"]) == str(record_id)
                ),
                None
            )
            if record:
                open_form(record)

        def delete():
            record_id = selected_id()
            if not record_id:
                return

            if messagebox.askyesno(
                "Confirm deletion",
                "Delete this maintenance record?"
            ):
                self.app.db.delete_maintenance(record_id)
                load()

        make_button(
            toolbar, "Add", add, COLORS["green"], 10
        ).pack(side="left", padx=4)

        make_button(
            toolbar, "Edit", edit, COLORS["blue"], 10
        ).pack(side="left", padx=4)

        make_button(
            toolbar, "Delete", delete, COLORS["red"], 10
        ).pack(side="left", padx=4)

        load()
