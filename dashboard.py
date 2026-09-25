import tkinter as tk
from config import COLORS
from ui_helpers import create_card


class DashboardModule:
    def __init__(self, app):
        self.app = app

    def show_home(self):
        user = self.app.current_user
        user_id = user["id"] if user["role"] == "Student" else None

        # ============================================================
        # PAGE TITLE
        # ============================================================
        self.app.set_content_title(
            "Dashboard",
            "Overview of the college water management system."
        )

        # ============================================================
        # SUMMARY CARDS
        # ============================================================
        summary = self.app.db.get_summary(user_id)

        cards = tk.Frame(
            self.app.content,
            bg=COLORS["light"]
        )
        cards.pack(
            fill="x",
            padx=28,
            pady=5
        )

        create_card(
            cards,
            "Total Complaints",
            summary["Total"],
            COLORS["blue"]
        )

        create_card(
            cards,
            "Pending",
            summary["Pending"],
            COLORS["yellow"]
        )

        create_card(
            cards,
            "In Progress",
            summary["In Progress"],
            COLORS["purple"]
        )

        create_card(
            cards,
            "Resolved",
            summary["Resolved"],
            COLORS["green"]
        )

        # ============================================================
        # LOWER CONTENT AREA
        # ============================================================
        lower = tk.Frame(
            self.app.content,
            bg=COLORS["light"]
        )

        lower.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=25
        )

        # ============================================================
        # LEFT CARD - BUILDING WATER STATUS
        # ============================================================
        left = tk.Frame(
            lower,
            bg="white",
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            left,
            text="💧 Building Water Status",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Building status rows
        building_statuses = self.app.db.get_building_statuses()

        for building, status in building_statuses.items():

            row = tk.Frame(
                left,
                bg="white"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=6
            )

            # Status color
            if status == "Normal":
                color = COLORS["green"]
            elif "Critical" in status:
                color = COLORS["red"]
            else:
                color = COLORS["yellow"]

            # Building name
            tk.Label(
                row,
                text=building,
                bg="white",
                fg=COLORS["dark"],
                font=("Segoe UI", 10)
            ).pack(
                side="left"
            )

            # Status
            tk.Label(
                row,
                text=f"● {status}",
                bg="white",
                fg=color,
                font=("Segoe UI", 9, "bold")
            ).pack(
                side="right"
            )

        # ============================================================
        # RIGHT CARD - DAILY WATER-SAVING TIP
        # ============================================================
        right = tk.Frame(
            lower,
            bg="white",
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            right,
            text="💡 Daily Water-Saving Tip",
            bg="white",
            fg=COLORS["dark"],
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Water-saving tips
        tk.Label(
            right,
            text=(
                "Turn off taps properly after use.\n\n"
                "Report leaking pipes quickly.\n\n"
                "Avoid wasting clean drinking water."
            ),
            bg="white",
            fg=COLORS["gray"],
            font=("Segoe UI", 11),
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # ============================================================
        # REPORT A WATER ISSUE BUTTON
        # ============================================================
        if user["role"] == "Student":

            # Frame is used instead of tk.Button because
            # macOS Tkinter can make button text invisible.
            report_button = tk.Frame(
                right,
                bg=COLORS["blue"],
                cursor="hand2",
                height=42
            )

            report_button.pack(
                anchor="w",
                padx=20,
                pady=20,
                fill="x"
            )

            report_button.pack_propagate(False)

            # Visible button text
            report_text = tk.Label(
                report_button,
                text="Report a Water Issue",
                bg=COLORS["blue"],
                fg="white",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2"
            )

            report_text.pack(
                fill="both",
                expand=True
            )

            # ========================================================
            # BUTTON HOVER
            # ========================================================
            def report_enter(event):
                report_button.configure(
                    bg="#245B8F"
                )

                report_text.configure(
                    bg="#245B8F",
                    fg="white"
                )

            def report_leave(event):
                report_button.configure(
                    bg=COLORS["blue"]
                )

                report_text.configure(
                    bg=COLORS["blue"],
                    fg="white"
                )

            # ========================================================
            # BUTTON CLICK
            # ========================================================
            def report_click(event):
                self.app.complaints.show_form()

            # Bind events to both the frame and text
            for widget in (report_button, report_text):

                widget.bind(
                    "<Enter>",
                    report_enter
                )

                widget.bind(
                    "<Leave>",
                    report_leave
                )

                widget.bind(
                    "<Button-1>",
                    report_click
                )