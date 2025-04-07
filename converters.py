# converters.py
import fitz
from PIL import Image
import io
import os

class Converter:
    def __init__(self, input_path, output_folder):
        self.input_path = input_path
        self.output_folder = output_folder
        
    def convert(self):
        raise NotImplementedError("La méthode convert doit être implémentée par les classes filles.")
        
    def validate_input(self):
        # Vérification que le fichier existe
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Le fichier {self.input_path} n'existe pas.")
            
        # Vérification que le fichier n'est pas vide
        if os.path.getsize(self.input_path) == 0:
            raise ValueError(f"Le fichier {self.input_path} est vide.")
    @staticmethod
    def get_supported_input_extensions():
        raise NotImplementedError("La méthode get_supported_input_extensions doit être implémentée par les classes filles.")
    @staticmethod
    def get_supported_output_extensions():
        raise NotImplementedError("La méthode get_supported_output_extensions doit être implémentée par les classes filles.")
        

class PDFToImageConverter(Converter):
    def __init__(self, input_path, output_folder, output_format):
        super().__init__(input_path, output_folder)
        self.output_format = output_format
    
    def convert(self):
        self.validate_input()
        try:
            doc = fitz.open(self.input_path)
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                img = Image.open(io.BytesIO(pix.tobytes()))
                img.save(f"{self.output_folder}/page_{page_num + 1}.{self.output_format.lower()}", self.output_format)
            doc.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la conversion : {e}")
            return False
    @staticmethod
    def get_supported_input_extensions():
        return ["pdf"]
    @staticmethod
    def get_supported_output_extensions():
        return ["JPEG", "PNG"]

class ImageToPDFConverter(Converter):
    def __init__(self, input_path, output_folder):
        super().__init__(input_path, output_folder)

    def convert(self):
        self.validate_input()
        try:
            img = Image.open(self.input_path)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PDF')
            img_byte_arr = img_byte_arr.getvalue()
            with open(os.path.join(self.output_folder, os.path.splitext(os.path.basename(self.input_path))[0]) + ".pdf", 'wb') as f:
                f.write(img_byte_arr)
            return True

        except Exception as e:
            print(f"Erreur lors de la conversion : {e}")
            return False
    @staticmethod
    def get_supported_input_extensions():
        return ["jpg", "jpeg", "png"]
    @staticmethod
    def get_supported_output_extensions():
        return ["pdf"]

class ImageToImageConverter(Converter):
    def __init__(self, input_path, output_folder, output_format):
        super().__init__(input_path, output_folder)
        self.output_format = output_format

    def convert(self):
        self.validate_input()
        try:
            img = Image.open(self.input_path)
            img.save(f"{self.output_folder}/{os.path.splitext(os.path.basename(self.input_path))[0]}.{self.output_format.lower()}", self.output_format)
            return True
        except Exception as e:
            print(f"Erreur lors de la conversion : {e}")
            return False
    @staticmethod
    def get_supported_input_extensions():
        return ["jpg", "jpeg", "png"]
    @staticmethod
    def get_supported_output_extensions():
        return ["JPEG", "PNG"]
