# Main crawler, redefined using youtube video tips

import sys
import modules
from tkinter import Tk, Button, Frame, Entry
from tkinter.scrolledtext import ScrolledText

class Writer(object):
    def __init__(self):
        self.links = {}

    def write_Links(self, links):
        with open('output.txt', 'w') as fileOut:
            for url in links:
                fileOut.write(f"{url}\n")
        
            print(f"Written {len(links)} unique URLs to output.txt")

            fileOut.close()

class LinkCollector(object):
    def __init__(self):
        self.url = ""

    def collect_links(url):
        return modules.module2.getAllMainLinksFromURL(url)

class PrintLogger(object):
    def __init__(self, textbox):
        self.textbox = textbox
    
    def write(self, text):
        self.textbox.configure(state='normal')
        self.textbox.insert('end', text)
        self.textbox.see('end')
        self.textbox.configure(state='disabled')
    
    def flush(self):
        pass

class MainGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.root = Frame(self)
        self.root.pack()

        # Setting up url input Entry
        self.url_input = Entry(self.root, width=50)
        self.url_input.pack()

        # Buttons for interaction
        self.redirect_button = Button(self.root, text="Redirect console to widget", command=self.redirect_logging)
        self.redirect_button.pack()
        self.reset_button = Button(self.root, text="Reset console redirect", command=self.reset_logging)
        self.reset_button.pack()
        self.test_button = Button(self.root, text="Test print", command=self.run_module2)
        self.test_button.pack()

        # Text widget for displaying output
        self.log_widget = ScrolledText(self.root, height=10, width=80, font=("consolas", "10", "normal"))
        self.log_widget.pack()

    def reset_logging(self):
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def run_module2(self):
        url = self.url_input.get()
        if not url:
            print("Please enter a URL.")
            return
        
        links = LinkCollector.collect_links(url)
        if not links:
            print("No links found.")
            return
        else:
            Writer().write_Links(links)

    def redirect_logging(self):
            logger = PrintLogger(self.log_widget)
            sys.stdout = logger
            sys.stderr = logger

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()