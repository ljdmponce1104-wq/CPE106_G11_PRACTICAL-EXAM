import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tkinter as tk
from tkinter import ttk, messagebox

from data.database import initialize_database
from business.ticket_service import TicketService


NAVY = "#0B2F68"
NAVY_DARK = "#071F4A"
TEAL = "#12B8A3"
TEAL_DARK = "#0A9D8C"
WHITE = "#FFFFFF"
LIGHT = "#F4F7FB"
TEXT = "#12345B"
MUTED = "#6B7C93"
BORDER = "#D9E1EC"


class ConcertTicketApp(tk.Tk):
    def __init__(self):
        super().__init__()

        initialize_database()
        self.service = TicketService()

        self.title("Concert Ticket Tracking System")
        self.geometry("1240x820")
        self.minsize(1100, 720)
        self.configure(bg=LIGHT)

        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.event_var = tk.StringVar()
        self.event_date_var = tk.StringVar(value="Select an event")
        self.venue_var = tk.StringVar(value="Select an event")
        self.type_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="All")
        self.queue_status_var = tk.StringVar()

        self._configure_styles()
        self._build_ui()
        self._select_first_event()
        self.refresh_table()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Segoe UI keeps the interface clean without looking overly heavy.
        style.configure("App.TFrame", background=LIGHT)
        style.configure(
            "Card.TLabelframe",
            background=WHITE,
            bordercolor=BORDER,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=WHITE,
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "App.TLabel",
            background=WHITE,
            foreground=TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Title.TLabel",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=NAVY,
            foreground="#D9E7FF",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Teal.TButton",
            background=TEAL,
            foreground=WHITE,
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            padding=(15, 8),
        )
        style.map(
            "Teal.TButton",
            background=[("active", TEAL_DARK), ("disabled", "#A9CFC8")],
            foreground=[("disabled", "#F4F4F4")],
        )
        style.configure(
            "Navy.TButton",
            background=NAVY,
            foreground=WHITE,
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            padding=(13, 7),
        )
        style.map("Navy.TButton", background=[("active", NAVY_DARK)])

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=31,
            bordercolor=BORDER,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 9, "bold"),
            padding=7,
        )
        style.map("Treeview", background=[("selected", "#DDF5F1")])

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=WHITE, height=82)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = tk.Frame(header, bg=WHITE)
        logo.pack(side="left", padx=22)

        tk.Label(
            logo,
            text="TICKETS",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 17, "bold"),
        ).pack(side="left")

        tk.Label(
            logo,
            text=" QUEUE",
            bg=WHITE,
            fg=TEAL,
            font=("Segoe UI", 17, "bold"),
        ).pack(side="left")

        tk.Label(
            logo,
            text="  |  GROUP 11",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=10)

        tk.Label(
            header,
            text="SOFTWARE DESIGN LABORATORY",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 9),
        ).pack(side="right", padx=22)

        # Hero
        hero = tk.Frame(self, bg=NAVY, height=150)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_left = tk.Frame(hero, bg=NAVY)
        hero_left.pack(fill="both", expand=True, padx=34, pady=24)

        ttk.Label(
            hero_left,
            text="CONCERT TICKET TRACKING SYSTEM",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            hero_left,
            text="CPE106L-4 Practical Exam",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(6, 13))

        tk.Label(
            hero_left,
            textvariable=self.queue_status_var,
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        # Main content
        content = tk.Frame(self, bg=LIGHT)
        content.pack(fill="both", expand=True, padx=22, pady=18)

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(2, weight=1)

        # Event selection
        event_card = ttk.LabelFrame(
            content,
            text="  SELECT EVENT  ",
            style="Card.TLabelframe",
            padding=14,
        )
        event_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 9),
            pady=(0, 12),
        )

        ttk.Label(
            event_card,
            text="Concert / Event",
            style="App.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.event_combo = ttk.Combobox(
            event_card,
            textvariable=self.event_var,
            values=self.service.event_names(),
            state="readonly",
            width=54,
        )
        self.event_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.event_combo.bind("<<ComboboxSelected>>", self._event_changed)

        ttk.Label(
            event_card,
            textvariable=self.event_date_var,
            style="Muted.TLabel",
        ).grid(row=2, column=0, sticky="w")

        ttk.Label(
            event_card,
            textvariable=self.venue_var,
            style="Muted.TLabel",
        ).grid(row=3, column=0, sticky="w", pady=(3, 0))

        # Ticket request
        form = ttk.LabelFrame(
            content,
            text="  TICKET REQUEST  ",
            style="Card.TLabelframe",
            padding=14,
        )
        form.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(9, 0),
            pady=(0, 12),
        )

        fields = [
            ("Customer Name", 0),
            ("Contact Number", 1),
            ("Ticket Type", 2),
            ("Quantity (1–10)", 3),
        ]

        for label, row in fields:
            ttk.Label(
                form,
                text=label,
                style="App.TLabel",
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 8),
                pady=4,
            )

        ttk.Entry(
            form,
            textvariable=self.name_var,
            width=27,
        ).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Entry(
            form,
            textvariable=self.contact_var,
            width=27,
        ).grid(row=1, column=1, sticky="ew", pady=4)

        self.type_combo = ttk.Combobox(
            form,
            textvariable=self.type_var,
            state="readonly",
            width=25,
        )
        self.type_combo.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Spinbox(
            form,
            from_=1,
            to=10,
            textvariable=self.quantity_var,
            width=25,
        ).grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Button(
            form,
            text="ADD TO QUEUE",
            style="Teal.TButton",
            command=self.add_ticket,
        ).grid(row=4, column=1, sticky="e", pady=(9, 0))

        form.columnconfigure(1, weight=1)

        # Generic event cards
        cards = tk.Frame(content, bg=LIGHT)
        cards.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 12),
        )
        cards.columnconfigure((0, 1, 2), weight=1)

        card_events = self.service.event_names()[:3]

        for i, event_name in enumerate(card_events):
            info = self.service.get_event_info(event_name)

            card = tk.Frame(
                cards,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=6,
            )

            tk.Label(
                card,
                text="2026",
                bg=TEAL,
                fg=WHITE,
                font=("Segoe UI", 8, "bold"),
                padx=9,
                pady=4,
            ).pack(anchor="w", padx=12, pady=(12, 8))

            tk.Label(
                card,
                text=event_name,
                bg=WHITE,
                fg=NAVY,
                font=("Segoe UI", 10, "bold"),
                wraplength=280,
                justify="left",
            ).pack(anchor="w", padx=12)

            tk.Label(
                card,
                text=info["date"],
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9),
            ).pack(anchor="w", padx=12, pady=(6, 2))

            tk.Label(
                card,
                text=info["venue"],
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9),
            ).pack(anchor="w", padx=12, pady=(0, 12))

            ttk.Button(
                card,
                text="SELECT",
                style="Navy.TButton",
                command=lambda n=event_name: self.select_event(n),
            ).pack(anchor="e", padx=12, pady=(0, 12))

        # Queue management
        queue_card = ttk.LabelFrame(
            content,
            text="  QUEUE MANAGEMENT  ",
            style="Card.TLabelframe",
            padding=10,
        )
        queue_card.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
        )

        controls = tk.Frame(queue_card, bg=WHITE)
        controls.pack(fill="x", pady=(0, 8))

        ttk.Button(
            controls,
            text="PROCESS NEXT",
            style="Teal.TButton",
            command=self.process_next,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            controls,
            text="CANCEL PURCHASE",
            style="Navy.TButton",
            command=self.cancel_purchase,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            controls,
            text="REFRESH",
            style="Navy.TButton",
            command=self.refresh_table,
        ).pack(side="left", padx=4)

        tk.Label(
            controls,
            text="Search",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(28, 6))

        self.search_entry = ttk.Entry(
            controls,
            textvariable=self.search_var,
            width=25,
        )
        self.search_entry.pack(side="left", padx=4)
        self.search_entry.bind("<Return>", lambda _event: self.search_records())

        status_combo = ttk.Combobox(
            controls,
            textvariable=self.status_var,
            values=("All", "Waiting", "Served", "Cancelled"),
            state="readonly",
            width=9,
        )
        status_combo.pack(side="left", padx=5)
        status_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.search_records(),
        )

        ttk.Button(
            controls,
            text="SEARCH",
            style="Navy.TButton",
            command=self.search_records,
        ).pack(side="left", padx=4)

        ttk.Button(
            controls,
            text="CLEAR",
            command=self.clear_search,
        ).pack(side="left", padx=4)

        tk.Label(
            controls,
            textvariable=self.queue_status_var,
            bg=WHITE,
            fg=TEAL_DARK,
            font=("Segoe UI", 9),
        ).pack(side="right", padx=6)

        # Table
        table_frame = tk.Frame(queue_card, bg=WHITE)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "queue",
            "customer",
            "event",
            "date",
            "type",
            "qty",
            "status",
            "created",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "queue": "QUEUE #",
            "customer": "CUSTOMER",
            "event": "EVENT",
            "date": "DATE",
            "type": "TICKET TYPE",
            "qty": "QTY",
            "status": "STATUS",
            "created": "CREATED",
        }

        widths = {
            "queue": 70,
            "customer": 150,
            "event": 210,
            "date": 155,
            "type": 105,
            "qty": 55,
            "status": 80,
            "created": 145,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center",
            )

        yscroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=yscroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        # Footer
        footer = tk.Frame(self, bg=NAVY_DARK, height=34)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="Mapúa University • Software Design Laboratory • Group 11",
            bg=NAVY_DARK,
            fg="#D9E7FF",
            font=("Segoe UI", 8),
        ).pack(side="left", padx=22, pady=9)

        tk.Label(
            footer,
            text="CPE106L-4_B3",
            bg=NAVY_DARK,
            fg=WHITE,
            font=("Segoe UI", 8),
        ).pack(side="right", padx=22)

    def _select_first_event(self):
        self.select_event(self.service.event_names()[0])

    def select_event(self, event_name):
        self.event_var.set(event_name)
        self._event_changed()

    def _event_changed(self, _event=None):
        event = self.service.get_event_info(self.event_var.get())

        if event is None:
            self.event_date_var.set("Select an event")
            self.venue_var.set("Select an event")
            self.type_var.set("")
            self.type_combo["values"] = ()
            return

        self.event_date_var.set(event["date"])
        self.venue_var.set(event["venue"])

        valid_types = event["ticket_types"]
        self.type_combo["values"] = valid_types

        # Automatically maintain a valid ticket type.
        if self.type_var.get() not in valid_types:
            self.type_var.set(valid_types[0])

    def add_ticket(self):
        success, errors, queue_number = self.service.add_ticket(
            self.name_var.get(),
            self.contact_var.get(),
            self.event_var.get(),
            self.type_var.get(),
            self.quantity_var.get(),
        )

        if not success:
            messagebox.showerror(
                "Invalid Request",
                "\n".join(f"• {error}" for error in errors),
            )
            return

        messagebox.showinfo(
            "Request Added",
            f"Ticket request added successfully.\n\n"
            f"Queue Number: #{queue_number}\n"
            f"Event: {self.event_var.get()}\n"
            f"Ticket Type: {self.type_var.get()}\n"
            f"Quantity: {self.quantity_var.get()}",
        )

        self.clear_form()
        self.refresh_table()

    def process_next(self):
        record = self.service.process_next()

        if record is None:
            messagebox.showinfo(
                "Queue Empty",
                "There are no waiting ticket requests to process.",
            )
            self.refresh_table()
            return

        messagebox.showinfo(
            "Processing Complete",
            f"Queue #{record['queue_number']} has been processed.\n\n"
            f"Customer: {record['customer_name']}\n"
            f"Event: {record['event_name']}\n"
            f"Ticket Type: {record['ticket_type']}\n"
            f"Quantity: {record['quantity']}",
        )

        self.refresh_table()

    def cancel_purchase(self):
        """Cancel the selected waiting purchase after confirmation."""
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Purchase Selected",
                "Please select a waiting purchase from the table first.",
            )
            return

        values = self.tree.item(selected[0], "values")

        if not values:
            messagebox.showwarning(
                "No Purchase Selected",
                "Please select a waiting purchase from the table first.",
            )
            return

        queue_number = values[0]
        customer_name = values[1]
        status = values[6]

        if status != "Waiting":
            messagebox.showwarning(
                "Cannot Cancel Purchase",
                "Only purchases with a Waiting status can be cancelled.",
            )
            return

        confirmed = messagebox.askyesno(
            "Cancel Purchase",
            f"Cancel Queue #{queue_number} for {customer_name}?\n\n"
            "The purchase will be marked as Cancelled and will remain "
            "in the database for record keeping.",
        )

        if not confirmed:
            return

        success, result = self.service.cancel_purchase(queue_number)

        if not success:
            messagebox.showerror(
                "Cancellation Failed",
                result,
            )
            return

        messagebox.showinfo(
            "Purchase Cancelled",
            f"Queue #{queue_number} has been cancelled successfully.",
        )

        self.refresh_table()

    def search_records(self):
        rows = self.service.search(
            self.search_var.get(),
            self.status_var.get(),
        )
        self.populate_table(rows)

    def refresh_table(self):
        rows = self.service.search("", "All")
        self.populate_table(rows)

        count = self.service.waiting_count()
        self.queue_status_var.set(f"WAITING: {count}")

    def populate_table(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["queue_number"],
                    row["customer_name"],
                    row["event_name"],
                    row["event_date"],
                    row["ticket_type"],
                    row["quantity"],
                    row["status"],
                    row["created_at"],
                ),
            )

    def clear_search(self):
        """Clear only the search/filter controls and restore all records."""
        self.search_var.set("")
        self.status_var.set("All")
        self.search_entry.focus_set()
        self.refresh_table()

    def clear_form(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.quantity_var.set("1")
        self._event_changed()


if __name__ == "__main__":
    app = ConcertTicketApp()
    app.mainloop()
