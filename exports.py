import csv
from tkinter import filedialog, messagebox


def export_complaints_to_csv(rows):
    if not rows:
        messagebox.showinfo("Export", "There are no complaints to export.")
        return

    path = filedialog.asksaveasfilename(
        title="Save complaint report",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not path:
        return

    headings = [
        "Complaint ID", "Reported By", "Building", "Issue Type",
        "Priority", "Description", "Status", "Created At", "Updated At"
    ]

    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headings)

        for row in rows:
            writer.writerow([
                row["id"],
                row["full_name"],
                row["building"],
                row["issue_type"],
                row["priority"],
                row["description"],
                row["status"],
                row["created_at"],
                row["updated_at"]
            ])

    messagebox.showinfo("Export completed", f"Report saved to:\n{path}")


def export_complaints_to_excel(rows):
    if not rows:
        messagebox.showinfo("Export", "There are no complaints to export.")
        return

    try:
        from openpyxl import Workbook
    except ImportError:
        messagebox.showerror(
            "Excel export unavailable",
            "Install openpyxl first using:\n\npip install openpyxl"
        )
        return

    path = filedialog.asksaveasfilename(
        title="Save Excel report",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )

    if not path:
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Complaints"

    headings = [
        "Complaint ID", "Reported By", "Building", "Issue Type",
        "Priority", "Description", "Status", "Created At", "Updated At"
    ]
    sheet.append(headings)

    for row in rows:
        sheet.append([
            row["id"],
            row["full_name"],
            row["building"],
            row["issue_type"],
            row["priority"],
            row["description"],
            row["status"],
            row["created_at"],
            row["updated_at"]
        ])

    workbook.save(path)
    messagebox.showinfo("Export completed", f"Excel report saved to:\n{path}")
