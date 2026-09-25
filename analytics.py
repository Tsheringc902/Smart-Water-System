import tkinter as tk
from config import COLORS
from ui_helpers import create_card


class AnalyticsModule:
    def __init__(self, app):
        self.app = app

    def show(self):
        self.app.set_content_title(
            "Analytics",
            "Complaint statistics and building water status."
        )

        summary = self.app.db.get_summary()

        top = tk.Frame(self.app.content, bg=COLORS["light"])
        top.pack(fill="x", padx=28, pady=5)

        create_card(top, "Total", summary["Total"], COLORS["blue"])
        create_card(top, "Pending", summary["Pending"], COLORS["yellow"])
        create_card(top, "In Progress", summary["In Progress"], COLORS["purple"])
        create_card(top, "Resolved", summary["Resolved"], COLORS["green"])

        lower = tk.Frame(self.app.content, bg=COLORS["light"])
        lower.pack(fill="both", expand=True, padx=28, pady=20)

        status_frame = tk.Frame(
            lower, bg="white",
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )
        status_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        issue_frame = tk.Frame(
            lower, bg="white",
            highlightbackground="#DDE4EC",
            highlightthickness=1
        )
        issue_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(
            status_frame, text="Building Water Status",
            bg="white", fg=COLORS["dark"],
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=18)

        for building, status in self.app.db.get_building_statuses().items():
            row = tk.Frame(status_frame, bg="white")
            row.pack(fill="x", padx=18, pady=6)

            if status == "Normal":
                color = COLORS["green"]
            elif "Critical" in status:
                color = COLORS["red"]
            else:
                color = COLORS["yellow"]

            tk.Label(
                row, text=building, bg="white",
                fg=COLORS["dark"], anchor="w"
            ).pack(side="left")

            tk.Label(
                row, text=status, bg="white",
                fg=color, font=("Segoe UI", 9, "bold")
            ).pack(side="right")

        tk.Label(
            issue_frame, text="Issue Type Statistics",
            bg="white", fg=COLORS["dark"],
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=18)

        rows = self.app.db.get_issue_counts()
        if not rows:
            tk.Label(
                issue_frame, text="No complaint data available.",
                bg="white", fg=COLORS["gray"]
            ).pack(anchor="w", padx=18)
        else:
            for row in rows:
                tk.Label(
                    issue_frame,
                    text=f"{row['issue_type']}: {row['total']}",
                    bg="white", fg=COLORS["dark"],
                    font=("Segoe UI", 10)
                ).pack(anchor="w", padx=18, pady=6)
