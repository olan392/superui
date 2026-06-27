import tkinter as tk

print("[superui] loaded!")


class Window:

    def __init__(self, title="superui", size="400x700"):
        self.title = title

        try:
            self.w, self.h = map(int, size.lower().split("x"))
        except (ValueError, AttributeError):
            self.w, self.h = 400, 700

        self.queue = []
        self.widgets = []
        self.root = None

    def label(self, text):
        if self.root:
            lbl = tk.Label(self.root, text=text)
            lbl.pack(pady=5)
            self.widgets.append(lbl)
        else:
            self.queue.append(("label", text))

    def button(self, text, command=None):
        if self.root:
            btn = tk.Button(
                self.root, text=text, command=lambda: command() if command else None
            )
            btn.pack(pady=5)
            self.widgets.append(btn)
        else:
            self.queue.append(("button", text, command))

    def input(self, placeholder="", on_submit=None):
        """Creates a text field with an automatic submit button next to it.

        Passes the input's text string straight into the on_submit function when
        clicked.
        """
        if self.root:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            self.widgets.append(frame)

            entry = tk.Entry(frame, fg="gray")
            entry.insert(0, placeholder)

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            def on_focus_out(event):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            entry.pack(side=tk.LEFT, padx=5)

            def handle_submit():
                text_value = entry.get()
                if text_value == placeholder:
                    text_value = ""

                # Fire the callback with the text string passed as an argument
                if on_submit:
                    on_submit(text_value)

            btn = tk.Button(frame, text="Submit", command=handle_submit)
            btn.pack(side=tk.LEFT)
        else:
            self.queue.append(("input", placeholder, on_submit))

    def remove(self):
        if self.widgets:
            last_widget = self.widgets.pop()
            last_widget.destroy()
        elif self.queue:
            self.queue.pop()

    def _create_root(self):
        return tk.Tk()

    def run(self):
        self.root = self._create_root()
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.title(self.title)

        for item in self.queue:
            if item[0] == "label":
                self.label(item[1])
            elif item[0] == "button":
                self.button(item[1], item[2])
            elif item[0] == "input":
                self.input(placeholder=item[1], on_submit=item[2])

        self.root.mainloop()
