import tkinter as tk
from tkinter import ttk


# ================================================================
# SAFE BUTTON FOR macOS
# ================================================================
def make_button(
    parent,
    text,
    command,
    color,
    width=15,
    height=40
):
    """
    Create a custom button that works reliably on macOS.

    A Frame + Label is used instead of the native tk.Button because
    the macOS Tk theme can sometimes make button text invisible.

    Existing calls such as:

        make_button(parent, "Add", command, COLORS["blue"], 15)

    are still supported.
    """

    # Existing project uses width values such as 8, 10, 15, 20, 25.
    # Convert those values into a sensible pixel width.
    try:
        requested_width = int(width) * 10
    except (TypeError, ValueError):
        requested_width = 150

    # Prevent buttons from becoming too small.
    requested_width = max(80, requested_width)

    # ------------------------------------------------------------
    # Main button frame
    # ------------------------------------------------------------
    button = tk.Frame(
        parent,
        bg=color,
        width=requested_width,
        height=height,
        cursor="hand2"
    )

    # VERY IMPORTANT:
    # Prevent the frame from shrinking to the label's natural size.
    button.pack_propagate(False)

    # ------------------------------------------------------------
    # Button text
    # ------------------------------------------------------------
    label = tk.Label(
        button,
        text=text,
        bg=color,
        fg="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        anchor="center",
        justify="center",
        cursor="hand2"
    )

    label.pack(
        fill="both",
        expand=True
    )

    # ------------------------------------------------------------
    # Hover colour
    # ------------------------------------------------------------
    hover_color = _get_hover_color(color)

    # ------------------------------------------------------------
    # Mouse enters button
    # ------------------------------------------------------------
    def on_enter(event):
        button.configure(
            bg=hover_color
        )

        label.configure(
            bg=hover_color,
            fg="#FFFFFF"
        )

    # ------------------------------------------------------------
    # Mouse leaves button
    # ------------------------------------------------------------
    def on_leave(event):
        button.configure(
            bg=color
        )

        label.configure(
            bg=color,
            fg="#FFFFFF"
        )

    # ------------------------------------------------------------
    # Mouse click
    # ------------------------------------------------------------
    def on_click(event):
        command()

    # Bind events to both frame and label.
    for widget in (button, label):

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

    return button


# ================================================================
# HOVER COLOUR
# ================================================================
def _get_hover_color(color):

    # Common colours from the Smart Water project.
    hover_map = {
        "#2F80ED": "#2168C4",
        "#3498DB": "#2677B5",
        "#2980B9": "#216A9C",

        "#27AE60": "#208A4C",
        "#2E8B57": "#247044",

        "#8E44AD": "#71368A",
        "#9B59B6": "#7D3C98",

        "#E67E22": "#C96816",
        "#F39C12": "#C87F0A",

        "#E74C3C": "#C0392B",
        "#C0392B": "#A93226",

        "#95A5A6": "#7F8C8D",
        "#7F8C8D": "#626F70",

        "#34495E": "#283747",

        "#173F67": "#245B8F",
    }

    return hover_map.get(
        color,
        _darken_hex(color)
    )


# ================================================================
# SIMPLE HEX COLOUR DARKENER
# ================================================================
def _darken_hex(color):

    try:

        color = color.lstrip("#")

        if len(color) != 6:
            return "#245B8F"

        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

        red = max(0, int(red * 0.80))
        green = max(0, int(green * 0.80))
        blue = max(0, int(blue * 0.80))

        return "#{:02X}{:02X}{:02X}".format(
            red,
            green,
            blue
        )

    except Exception:
        return "#245B8F"


# ================================================================
# DASHBOARD CARD
# ================================================================
def create_card(
    parent,
    title,
    value,
    color
):
    """
    Create a dashboard summary card.

    Used by dashboard.py like:

        create_card(
            cards,
            "Total Complaints",
            summary["Total"],
            COLORS["blue"]
        )
    """

    card = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#D8E0E8",
        highlightthickness=1,
        width=240,
        height=100
    )

    card.pack_propagate(False)

    # ------------------------------------------------------------
    # Top colour strip
    # ------------------------------------------------------------
    strip = tk.Frame(
        card,
        bg=color,
        height=6
    )

    strip.pack(
        fill="x"
    )

    strip.pack_propagate(False)

    # ------------------------------------------------------------
    # Card content
    # ------------------------------------------------------------
    content = tk.Frame(
        card,
        bg="white"
    )

    content.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=10
    )

    tk.Label(
        content,
        text=title,
        bg="white",
        fg="#607D94",
        font=("Segoe UI", 10, "bold"),
        anchor="w"
    ).pack(
        anchor="w"
    )

    tk.Label(
        content,
        text=str(value),
        bg="white",
        fg="#26343D",
        font=("Segoe UI", 22, "bold"),
        anchor="w"
    ).pack(
        anchor="w",
        pady=(6, 0)
    )

    # ------------------------------------------------------------
    # Allow cards to sit beside each other.
    # ------------------------------------------------------------
    card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=6
    )

    return card


# ================================================================
# TABLE
# ================================================================
def make_table(
    parent,
    columns,
    headings,
    widths,
    height=18
):
    """
    Create a clean Treeview table.

    Parameters:
        parent   - parent widget
        columns  - internal column names
        headings - visible column headings
        widths   - column widths
        height   - number of visible rows

    Returns:
        ttk.Treeview
    """

    # ------------------------------------------------------------
    # Table container
    # ------------------------------------------------------------
    table_frame = tk.Frame(
        parent,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True
    )

    # ------------------------------------------------------------
    # Style
    # ------------------------------------------------------------
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "SmartWater.Treeview",
        background="#FFFFFF",
        foreground="#26343D",
        fieldbackground="#FFFFFF",
        font=("Segoe UI", 10),
        rowheight=30,
        borderwidth=0
    )

    style.configure(
        "SmartWater.Treeview.Heading",
        background="#E9EEF3",
        foreground="#26343D",
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )

    style.map(
        "SmartWater.Treeview",
        background=[
            ("selected", "#4F718D")
        ],
        foreground=[
            ("selected", "#FFFFFF")
        ]
    )

    style.map(
        "SmartWater.Treeview.Heading",
        background=[
            ("active", "#DCE5EC")
        ],
        foreground=[
            ("active", "#26343D")
        ]
    )

    # ------------------------------------------------------------
    # Treeview
    # ------------------------------------------------------------
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=height,
        style="SmartWater.Treeview"
    )

    # ------------------------------------------------------------
    # Configure columns
    # ------------------------------------------------------------
    for index, column in enumerate(columns):

        if index < len(headings):
            heading = headings[index]
        else:
            heading = column

        if index < len(widths):
            column_width = widths[index]
        else:
            column_width = 120

        tree.heading(
            column,
            text=heading
        )

        tree.column(
            column,
            width=column_width,
            minwidth=60,
            anchor="center",
            stretch=False
        )

    # ------------------------------------------------------------
    # Vertical scrollbar
    # ------------------------------------------------------------
    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    # ------------------------------------------------------------
    # Horizontal scrollbar
    # ------------------------------------------------------------
    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    # ------------------------------------------------------------
    # Grid layout
    # ------------------------------------------------------------
    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )

    return tree


# ================================================================
# LABEL HELPER
# ================================================================
def make_label(
    parent,
    text,
    bg="white",
    fg="#26343D",
    size=10,
    bold=False,
    anchor="w"
):
    """
    Simple consistent Label helper.
    """

    weight = "bold" if bold else "normal"

    label = tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=("Segoe UI", size, weight),
        anchor=anchor
    )

    return label


# ================================================================
# ENTRY HELPER
# ================================================================
def make_entry(
    parent,
    width=30
):
    """
    Create a visible standard Tkinter entry.

    This avoids macOS ttk colour problems.
    """

    entry = tk.Entry(
        parent,
        width=width,
        bg="#FFFFFF",
        fg="#172B3A",
        insertbackground="#172B3A",
        selectbackground="#B8D4F0",
        selectforeground="#172B3A",
        relief="solid",
        bd=1,
        font=("Segoe UI", 10)
    )

    return entry