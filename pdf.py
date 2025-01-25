import os
from tkinter import Tk, filedialog, messagebox, PhotoImage
from tkinter.ttk import Button, Label, Style, Frame
from tkinter import Menu
import fitz  
from PyPDF2 import PdfReader, PdfWriter
from tkinter import messagebox as MessageBox
import webbrowser
from tkinter import Toplevel

def select_pdf():
    """Permite al usuario seleccionar un archivo PDF"""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        selected_label.config(text=f"Seleccionado: {os.path.basename(file_path)}")
        return file_path
    return None

def split_pdf():
    """Dividir un PDF en páginas"""
    pdf_path = select_pdf()
    if not pdf_path:
        return
    output_dir = filedialog.askdirectory(title="Selecciona la carpeta de salida")
    if not output_dir:
        return

    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_path = os.path.join(output_dir, f"pagina_{i + 1}.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
        messagebox.showinfo("Éxito", "El PDF se dividió correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def merge_pdfs():
    
    pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_paths:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not output_path:
        return

    try:
        writer = PdfWriter()
        for pdf_path in pdf_paths:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        messagebox.showinfo("Éxito", "Los PDFs se agruparon correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def pdf_to_images():
    """Convertir un PDF a imágen en alta calidad """
    pdf_path = select_pdf()
    if not pdf_path:
        return
    output_dir = filedialog.askdirectory(title="Selecciona la carpeta de salida")
    if not output_dir:
        return

    try:
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            zoom = 3  # (300 DPI)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            image_path = os.path.join(output_dir, f"pagina_{page_number + 1}.png")
            pix.save(image_path)
        pdf_document.close()
        messagebox.showinfo("Éxito", "El PDF se convirtió en imágene correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def show_info():
    """Muestra la información con un enlace."""
    info_window = Toplevel(root)
    info_window.title("Información")
    info_window.geometry("400x200")
    
    info_message = "Desarrollador: Mike GH\n\nVersión: 1.0 \n\nVisita mi sitio web:\n\n https://devmike117.netlify.app/"
    Label(info_window, text=info_message, font=("Arial", 12)).pack(pady=10)

 
# Configuración de la interfaz gráfica
root = Tk()
root.title("Gestión de PDF")
root.geometry("500x400")
root.resizable(False, False)

# Menú superior
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Pestaña de Información
info_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Información", menu=info_menu)
info_menu.add_command(label="Acerca de", command=show_info)

# Estilo personalizado
style = Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 14), background="#f0f0f0")
style.configure("TFrame", background="#f0f0f0")

# Fondo y marco principal
root.configure(bg="#e6e6e6")
main_frame = Frame(root, padding=20, style="TFrame")
main_frame.pack(expand=True, fill="both")

# Título y descripción
Label(main_frame, text="Gestión de PDFs", font=("Arial", 18, "bold"), background="#e6e6e6").pack(pady=10)
Label(main_frame, text="Dividir, agrupar y convertir PDFs en imágenes", background="#e6e6e6").pack(pady=5)

# Botones
Button(main_frame, text="Dividir PDF", command=split_pdf, width=20).pack(pady=10)
Button(main_frame, text="Agrupar PDFs", command=merge_pdfs, width=20).pack(pady=10)
Button(main_frame, text="Convertir PDF a Imágen", command=pdf_to_images, width=20).pack(pady=10)

# Etiqueta para mostrar archivo seleccionado
selected_label = Label(main_frame, text="No se ha seleccionado ningún archivo", wraplength=400, background="#e6e6e6")
selected_label.pack(pady=10)

# Botón de salida
Button(main_frame, text="Salir", command=root.quit, width=20).pack(pady=20)

# Icono de la ventana
try:
    icon = PhotoImage(file="image.png")
    root.iconphoto(False, icon)
except:
    pass  # Si no existe el archivo, no se establece el icono

root.mainloop()



# pyinstaller --onefile --noconsole pdf.py
#agregar icono e imagen utilizada

#pyinstaller --onefile --noconsole --icon=image.ico  pdf.py