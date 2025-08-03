# Main crawler, redefined using youtube video tips

import sys
# import time
import modules
from tkinter import Tk, Button, Frame, Entry
from tkinter.scrolledtext import ScrolledText
import queue
import threading

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

    @staticmethod
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

        self.queue = queue.Queue()
        self.check_queue()

    def reset_logging(self):
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def run_module2(self):
        url = self.url_input.get()
        if not url:
            print("Please enter a URL.")
            return
        threading.Thread(target=self.crawl_and_print, args=(url,), daemon=True).start()

    def crawl_and_print(self, url):
        links = []
        for link in LinkCollector.collect_links(url):
            # time.sleep(0.1) # Actually, putting in a sleep here slows it down considerable, and leads to unexpected behavior(according to me).
            self.queue.put(link)  # Pass link to main thread
            links.append(link)
        if not links:
            self.queue.put("No links found.")
        else:
            links = modules.module2.turnListIntoSetVersa(links)
            writer = Writer()
            writer.write_Links(links)

    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                print(msg)  # This will go through PrintLogger in the main thread
        except queue.Empty:
            pass
        self.after(100, self.check_queue)  # Check again after 100ms

    def redirect_logging(self):
            logger = PrintLogger(self.log_widget)
            sys.stdout = logger
            sys.stderr = logger

    def start_crawl(self):
        url = self.url_input.get()
        if not url:
            print("Please enter a URL.")
            return
        self.links_iter = iter(LinkCollector.collect_links(url))
        self.links = []
        self.process_next_link()

    def process_next_link(self):
        try:
            link = next(self.links_iter)
            print(link)
            self.links.append(link)
            self.after(10, self.process_next_link)  # Schedule next link
        except StopIteration:
            if not self.links:
                print("No links found.")
            else:
                links = modules.module2.turnListIntoSetVersa(self.links)
                writer = Writer()
                writer.write_Links(links)

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()