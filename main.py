# main.py
import tkinter as tk
from gui import PDFConverterGUI

def main():
    root = tk.Tk()
    converter = PDFConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
