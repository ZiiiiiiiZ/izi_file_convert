# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from converters import PDFToImageConverter, ImageToPDFConverter, ImageToImageConverter

class PDFConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Convertisseur de fichiers")

        self.pdf_path = ""
        self.output_folder = ""
        self.output_format = "JPEG"  # Format par défaut

        self.available_converters = {
            "PDF en Image": PDFToImageConverter,
            "Image en PDF": ImageToPDFConverter,
            "Image en Image": ImageToImageConverter
        }
        #Choix du type de converter
        self.converter_type_label = tk.Label(master, text="Type de conversion:")
        self.converter_type_label.pack()

        self.converter_types = list(self.available_converters.keys())
        self.converter_type_var = tk.StringVar(master)
        self.converter_type_var.set(self.converter_types[0])  # Valeur par défaut
        self.converter_type_menu = ttk.Combobox(master, textvariable=self.converter_type_var, values=self.converter_types, state="readonly")
        self.converter_type_menu.pack(pady=5)
        self.converter_type_menu.bind("<<ComboboxSelected>>", self.update_converter)

        # Bouton pour choisir le fichier
        self.pdf_button = tk.Button(master, text="Choisir un fichier", command=self.browse_pdf)
        self.pdf_button.pack(pady=10)

        self.pdf_label = tk.Label(master, text="Aucun fichier sélectionné")
        self.pdf_label.pack()

        # Bouton pour choisir le dossier de destination
        self.output_folder_button = tk.Button(master, text="Choisir un dossier de destination",
                                               command=self.browse_output_folder)
        self.output_folder_button.pack(pady=10)

        self.output_folder_label = tk.Label(master, text="Aucun dossier sélectionné")
        self.output_folder_label.pack()

        # Choix du format de sortie
        self.format_label = tk.Label(master, text="Format de sortie:")
        self.format_label.pack()

        self.format_options = [] #initialisé à vide, on ne connait pas le bon format tant qu'on a pas choisi de converter.
        self.format_var = tk.StringVar(master)
        self.format_menu = ttk.Combobox(master, textvariable=self.format_var, values=self.format_options, state="readonly")
        self.format_menu.pack(pady=5)
        self.format_menu.bind("<<ComboboxSelected>>", self.update_output_format)
        self.update_converter(None) #permet d'initialiser les bons formats dès l'ouverture de l'app.

        # Bouton de conversion
        self.convert_button = tk.Button(master, text="Convertir", command=self.convert_pdf)
        self.convert_button.pack(pady=20)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def update_converter(self, event):
        """Met à jour le convertisseur sélectionné."""
        self.selected_converter = self.available_converters[self.converter_type_var.get()]
        self.update_format_options()
        self.pdf_path = ""
        self.pdf_label.config(text="Aucun fichier sélectionné")
        self.output_folder = ""
        self.output_folder_label.config(text="Aucun dossier sélectionné")

    def update_output_format(self, event):
        """Met à jour le format de sortie sélectionné."""
        self.output_format = self.format_var.get()

    def update_format_options(self):
        """Met à jour les options de format en fonction du convertisseur sélectionné."""
        # Mise à jour des formats disponibles
        self.format_options = self.selected_converter.get_supported_output_extensions()
        self.format_var.set(self.format_options[0])  # Valeur par défaut
        self.format_menu.config(values=self.format_options)

    def browse_pdf(self):
        """Ouvre une boîte de dialogue pour choisir un fichier."""
        self.pdf_path = filedialog.askopenfilename(
            title="Sélectionner un fichier",
            filetypes=[
                ("Fichiers", " ".join([f"*.{ext}" for ext in self.selected_converter.get_supported_input_extensions()]))
            ],
        )
        if self.pdf_path:
            self.pdf_label.config(text=self.pdf_path)

    def browse_output_folder(self):
        """Ouvre une boîte de dialogue pour choisir un dossier de sortie."""
        self.output_folder = filedialog.askdirectory(title="Sélectionner un dossier de destination")
        if self.output_folder:
            self.output_folder_label.config(text=self.output_folder)

    def convert_pdf(self):
        """Lance la conversion PDF en image dans un thread séparé."""
        if not self.pdf_path or not self.output_folder:
            self.result_label.config(text="Veuillez sélectionner un fichier et un dossier de destination.")
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier et un dossier de destination.")
            return

        self.result_label.config(text="Conversion en cours...")
        self.convert_button.config(state="disabled")
        thread = threading.Thread(target=self.convert_pdf_thread)
        thread.start()
    
    def convert_pdf_thread(self):
        """Fonction qui s'exécute dans le thread et qui réalise la conversion."""
        try:
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            # On gère les arguments en fonction du convertisseur
            if self.selected_converter == ImageToPDFConverter:
                converter_instance = self.selected_converter(self.pdf_path, self.output_folder)
            else:
                converter_instance = self.selected_converter(self.pdf_path, self.output_folder, self.output_format)

            if converter_instance.convert():
                self.result_label.config(text="Conversion terminée !")
            else:
                self.result_label.config(text="Erreur lors de la conversion.")

        except FileNotFoundError as e:
            self.result_label.config(text=e)
            messagebox.showerror("Erreur", e)
        except ValueError as e:
            self.result_label.config(text=e)
            messagebox.showerror("Erreur", e)
        except Exception as e:
            self.result_label.config(text=f"Erreur: {e}")
            messagebox.showerror("Erreur", f"Erreur : {e}")
        finally:
            self.convert_button.config(state="normal")

