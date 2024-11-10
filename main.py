import tkinter as tk

# from blockchain import HealthcareBlockchain
from gui import HealthcareApp


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareApp(root)
    root.mainloop()
