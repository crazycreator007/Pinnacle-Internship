import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
from datetime import date
import json
import os


# =========================
# APP SETTINGS
# =========================

APP_BG = "#0f172a"
PANEL_BG = "#1e293b"
CARD_BG = "#334155"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
ACCENT_DARK = "#0284c7"
REMINDER_COLOR = "#f59e0b"
TODAY_COLOR = "#22c55e"


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Calendar & Reminder App By Yogesh")
root.geometry("1000x720")
root.configure(bg=APP_BG)
root.resizable(False, False)


# =========================
# DATE & REMINDER DATA
# =========================

today = date.today()
current_year = today.year
current_month = today.month

REMINDER_FILE = "data/reminders.json"


def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_reminders():
    os.makedirs("data", exist_ok=True)

    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)


reminders = load_reminders()


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg=APP_BG
)
header.pack(fill="x", padx=35, pady=(25, 10))


title = tk.Label(
    header,
    text="📅 Calendar & Reminder",
    font=("Segoe UI", 26, "bold"),
    bg=APP_BG,
    fg=TEXT
)
title.pack(side="left")


subtitle = tk.Label(
    header,
    text="Plan your day. Stay organized.",
    font=("Segoe UI", 11),
    bg=APP_BG,
    fg=MUTED
)
subtitle.pack(side="right", pady=10)


# =========================
# MAIN CONTENT
# =========================

content = tk.Frame(
    root,
    bg=APP_BG
)
content.pack(fill="both", expand=True, padx=35, pady=15)


# =========================
# CALENDAR CARD
# =========================

calendar_card = tk.Frame(
    content,
    bg=PANEL_BG,
    padx=20,
    pady=20
)
calendar_card.pack(side="left", fill="both", expand=True)


# =========================
# NAVIGATION
# =========================

navigation = tk.Frame(
    calendar_card,
    bg=PANEL_BG
)
navigation.pack(fill="x", pady=(0, 15))


def button_style(button):
    button.configure(
        bg=CARD_BG,
        fg=TEXT,
        activebackground=ACCENT_DARK,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    )


def previous_month():
    global current_month, current_year

    current_month -= 1

    if current_month == 0:
        current_month = 12
        current_year -= 1

    show_calendar()


def next_month():
    global current_month, current_year

    current_month += 1

    if current_month == 13:
        current_month = 1
        current_year += 1

    show_calendar()


previous_button = tk.Button(
    navigation,
    text="◀",
    font=("Segoe UI", 13, "bold"),
    width=4,
    command=previous_month
)
button_style(previous_button)
previous_button.pack(side="left")


month_label = tk.Label(
    navigation,
    text="",
    font=("Segoe UI", 18, "bold"),
    bg=PANEL_BG,
    fg=TEXT
)
month_label.pack(side="left", expand=True)


next_button = tk.Button(
    navigation,
    text="▶",
    font=("Segoe UI", 13, "bold"),
    width=4,
    command=next_month
)
button_style(next_button)
next_button.pack(side="right")


# =========================
# CALENDAR FRAME
# =========================

calendar_frame = tk.Frame(
    calendar_card,
    bg=PANEL_BG
)
calendar_frame.pack()


# =========================
# REMINDER PANEL
# =========================

reminder_card = tk.Frame(
    content,
    bg=PANEL_BG,
    width=280,
    padx=20,
    pady=20
)
reminder_card.pack(
    side="right",
    fill="y",
    padx=(20, 0)
)

reminder_card.pack_propagate(False)


reminder_title = tk.Label(
    reminder_card,
    text="🔔 Reminders",
    font=("Segoe UI", 17, "bold"),
    bg=PANEL_BG,
    fg=TEXT
)
reminder_title.pack(anchor="w")


selected_date_label = tk.Label(
    reminder_card,
    text="Select a date",
    font=("Segoe UI", 11),
    bg=PANEL_BG,
    fg=MUTED
)
selected_date_label.pack(
    anchor="w",
    pady=(5, 15)
)


reminder_list = tk.Listbox(
    reminder_card,
    bg=APP_BG,
    fg=TEXT,
    selectbackground=ACCENT_DARK,
    selectforeground="white",
    font=("Segoe UI", 10),
    relief="flat",
    bd=0,
    height=15
)
reminder_list.pack(
    fill="both",
    expand=True
)


# =========================
# REMINDER FUNCTIONS
# =========================

selected_date = (
    f"{today.year}-"
    f"{today.month:02d}-"
    f"{today.day:02d}"
)


def update_reminder_panel(date_key):

    reminder_list.delete(0, tk.END)

    selected_date_label.config(
        text=date_key
    )

    if date_key not in reminders:
        reminder_list.insert(
            tk.END,
            "No reminders yet."
        )
        return

    for reminder in reminders[date_key]:
        reminder_list.insert(
            tk.END,
            "• " + reminder
        )


def add_reminder(day):

    global selected_date

    selected_date = (
        f"{current_year}-"
        f"{current_month:02d}-"
        f"{day:02d}"
    )

    reminder = simpledialog.askstring(
        "Add Reminder",
        f"Enter reminder for {selected_date}:"
    )

    if reminder and reminder.strip():

        reminders.setdefault(
            selected_date,
            []
        ).append(
            reminder.strip()
        )

        save_reminders()

        update_reminder_panel(selected_date)
        show_calendar()

        messagebox.showinfo(
            "Success",
            "Reminder added successfully!"
        )

def delete_reminder():
    global selected_date

    selection = reminder_list.curselection()

    if not selection:
        messagebox.showwarning(
            "No Selection",
            "Please select a reminder to delete."
        )
        return

    index = selection[0]

    if selected_date in reminders:

        reminders[selected_date].pop(index)

        if not reminders[selected_date]:
            del reminders[selected_date]

        save_reminders()

        update_reminder_panel(selected_date)
        show_calendar()


def edit_reminder():
    global selected_date

    selection = reminder_list.curselection()

    if not selection:
        messagebox.showwarning(
            "No Selection",
            "Please select a reminder to edit."
        )
        return

    index = selection[0]

    if selected_date not in reminders:
        return

    old_reminder = reminders[selected_date][index]

    new_reminder = simpledialog.askstring(
        "Edit Reminder",
        "Update your reminder:",
        initialvalue=old_reminder
    )

    if new_reminder and new_reminder.strip():

        reminders[selected_date][index] = new_reminder.strip()

        save_reminders()
        update_reminder_panel(selected_date)
        show_calendar()

        messagebox.showinfo(
            "Success",
            "Reminder updated successfully!"
        )

def select_date(day):

    global selected_date

    selected_date = (
        f"{current_year}-"
        f"{current_month:02d}-"
        f"{day:02d}"
    )

    update_reminder_panel(selected_date)
def add_selected_reminder():
    if selected_date is None:
        messagebox.showwarning(
            "Select Date",
            "Please select a date first."
        )
        return

    reminder = simpledialog.askstring(
        "Add Reminder",
        f"Enter reminder for {selected_date}:"
    )

    if reminder and reminder.strip():
        reminders.setdefault(
            selected_date,
            []
        ).append(reminder.strip())

        save_reminders()
        update_reminder_panel(selected_date)
        show_calendar()

        messagebox.showinfo(
            "Success",
            "Reminder added successfully!"
        )


# =========================
# REMINDER BUTTONS
# =========================

add_button = tk.Button(
    reminder_card,
    text="+ Add Reminder",
    font=("Segoe UI", 10, "bold"),
    command=add_selected_reminder
)

add_button.configure(
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_DARK,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    pady=8
)

add_button.pack(
    fill="x",
    pady=(15, 8)
)


delete_button = tk.Button(
    reminder_card,
    text="Delete Selected",
    font=("Segoe UI", 10),
    command=delete_reminder
)
edit_button = tk.Button(
    reminder_card,
    text="✏ Edit Selected",
    font=("Segoe UI", 10),
    command=edit_reminder
)

edit_button.configure(
    bg=CARD_BG,
    fg=TEXT,
    activebackground="#475569",
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    pady=8
)

edit_button.pack(
    fill="x",
    pady=(8, 0)
)

delete_button.configure(
    bg=CARD_BG,
    fg=TEXT,
    activebackground="#475569",
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    pady=8
)

delete_button.pack(
    fill="x"
)


# =========================
# CALENDAR DISPLAY
# =========================

def show_calendar():

    for widget in calendar_frame.winfo_children():
        widget.destroy()

    month_label.config(
        text=f"{calendar.month_name[current_month]} {current_year}"
    )

    weekdays = [
        "MON",
        "TUE",
        "WED",
        "THU",
        "FRI",
        "SAT",
        "SUN"
    ]

    for column, day_name in enumerate(weekdays):

        label = tk.Label(
            calendar_frame,
            text=day_name,
            font=("Segoe UI", 9, "bold"),
            bg=PANEL_BG,
            fg=MUTED,
            width=8,
            pady=8
        )

        label.grid(
            row=0,
            column=column,
            padx=3,
            pady=3
        )

    month_calendar = calendar.monthcalendar(
        current_year,
        current_month
    )

    for row, week in enumerate(
        month_calendar,
        start=1
    ):

        for column, day in enumerate(week):

            if day == 0:
                continue

            date_key = (
                f"{current_year}-"
                f"{current_month:02d}-"
                f"{day:02d}"
            )

            has_reminder = date_key in reminders

            is_today = (
                day == today.day
                and current_month == today.month
                and current_year == today.year
            )

            if is_today:
                bg = TODAY_COLOR
                fg = "white"

            elif has_reminder:
                bg = REMINDER_COLOR
                fg = "white"

            else:
                bg = CARD_BG
                fg = TEXT

            text = str(day)

            if has_reminder:
                text += "\n🔔"

            date_button = tk.Button(
                calendar_frame,
                text=text,
                font=("Segoe UI", 10, "bold"),
                width=8,
                height=3,
                bg=bg,
                fg=fg,
                activebackground=ACCENT_DARK,
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda d=day: select_date(d)
            )

            date_button.grid(
                row=row,
                column=column,
                padx=3,
                pady=3
            )


# =========================
# FOOTER
# =========================

footer = tk.Label(
    root,
    text="Click a date to view reminders • Add reminders and manage your schedule",
    font=("Segoe UI", 10),
    bg=APP_BG,
    fg=MUTED
)

footer.pack(
    pady=(5, 15)
)


# =========================
# START APP
# =========================

show_calendar()
update_reminder_panel(selected_date)

root.mainloop()