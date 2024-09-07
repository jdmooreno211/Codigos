from Sources.compuertas import Compuertas
from Sources.system_os import OperationsSystem
from Sources.perceptron import Perceptron
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
# Configurar el tema oscuro de la interfaz
ctk.set_appearance_mode("dark")  # Cambiar a un modo oscuro
ctk.set_default_color_theme("dark-blue")  # Usar un tema oscuro
# Variables para compuertas
option = 0
obj_os = OperationsSystem()
obj_perceptron = Perceptron()

# Función para centrar la ventana en la pantalla
def center_window(root, width=1000, height=650):  # Ajustar a un tamaño más grande
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


# Crear la ventana principal
root = ctk.CTk()
root.title("Perceptrón Monocapa   |   Nicolas Torres Robriguez - Juan David Moreno Beltran")
center_window(root)  # Centrar la ventana en la pantalla
root.resizable(False, False)

# Definir la variable seleccionada para el menú desplegable
selected_operation = tk.StringVar(value="AND")  # Cambiar el valor predeterminado a "AND"

# Cargar y agregar la imagen en la parte superior (reducir tamaño de la imagen)
background_image = Image.open(obj_os.search_doc("facatativa-2.jpg"))  # Ruta de la imagen
background_image = background_image.resize((950, 100))  # Ajustar el tamaño de la imagen
bg_image = ImageTk.PhotoImage(background_image)

# Crear un frame para la imagen en la parte superior
image_frame = tk.Label(root, image=bg_image, bg="black")  # Fondo oscuro
image_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Coloca la imagen en la parte superior

# Crear un frame para el menú desplegable y el contenido principal
controls_frame = ctk.CTkFrame(root)
controls_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")






# Crear un frame con scroll para los controles
scrollable_lefth = ctk.CTkScrollableFrame(controls_frame, width=360, height=500)
scrollable_lefth.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
scrollable_frame = ctk.CTkScrollableFrame(root, width=580, height=600)
scrollable_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
# Mover el menú desplegable debajo de la imagen
dropdown_menu = ctk.CTkOptionMenu(scrollable_lefth, values=["AND", "OR", "XOR", "NAND"], variable=selected_operation, command=lambda _: show_interface())
dropdown_menu.grid(row=0, column=0, pady=5, padx=5)
# Frame izquierdo para tabla de verdad
table_frame = ctk.CTkFrame(scrollable_lefth, fg_color="gray30", corner_radius=10)
table_frame.grid(row=1, column=0, padx=5, pady=5)

# Frame para entrada de pesos debajo de la tabla de verdad
weights_frame = ctk.CTkFrame(scrollable_lefth, fg_color="gray30", corner_radius=10)
weights_frame.grid(row=2, column=0, padx=5, pady=5)
# Variables
error_vars = []  # Lista de variables para los errores
error_labels = []  # Lista de etiquetas de error para aplicar colores

# Crear dos frames globales para ser reutilizados
result_frame = None
ideal_weights_frame = None  # Frame para los pesos ideales

def on_closing():
    print("Cerrando la aplicación...")
    root.destroy()  # Destruye la ventana
    sys.exit()  # Cierra el programa
# Función para reiniciar la vista (destruir frames y resetear listas)
def reset_view():
    global result_frame, ideal_weights_frame, error_vars, error_labels
    if table_frame:
        for widget in table_frame.winfo_children():
            widget.destroy()
    if weights_frame:
        for widget in weights_frame.winfo_children():
            widget.destroy()
    if result_frame:
        for widget in result_frame.winfo_children():
            widget.destroy()
    if ideal_weights_frame:
        for widget in ideal_weights_frame.winfo_children():
            widget.destroy()
    error_vars = []  # Resetear la lista de variables de error
    error_labels = []  # Resetear la lista de etiquetas de error

# Función para cambiar los colores de los errores en función del valor    
def update_error_colors(w, opt):
    if opt == 4:
        aux = []
        for i in range(3):
            x = [float(y.get()) for y in w[i]]
            aux.append(x)
        w = aux
    l_w = obj_perceptron.intermediate(option=opt, weigth=w)
    
    for i, error_entry in enumerate(error_labels):
        if l_w[i] == 0:
            error_entry.configure(fg_color="green")  # Cambiar a verde si el error es 0
        else:
            error_entry.configure(fg_color="red")
        error_entry.delete(0, 'end') 
        error_entry.insert(0, f'{l_w[i]}') 

# Función para mostrar la gráfica de evolución del error
# Función para mostrar la gráfica de evolución del error
def plot_error_evolution(data, operation):
    # Limpiar el frame de pesos ideales antes de mostrar la gráfica
    for widget in ideal_weights_frame.winfo_children():
        widget.destroy()

    if operation == "XOR":
        # Extraer y graficar las tres secciones del perceptrón XOR: Y1, Y2 y XOR
        for sub_component in ['Compuerta Y1', 'Compuerta Y2', 'Compuerta XOR']:
            fig, ax = plt.subplots(figsize=(3, 2), dpi=100)  # Tamaño reducido
            epochs = []
            errors_per_pattern = {pattern: [] for pattern in ["Patron(1)", "Patron(2)", "Patron(3)", "Patron(4)"]}

            # Extraer datos por cada época y patrón para el componente actual
            if sub_component in data:
                for epoch_key, epoch_data in data[sub_component].items():
                    if 'Epoca' in epoch_key:
                        epoch_num = int(epoch_key.split()[-1])
                        epochs.append(epoch_num)
                        for pattern_key, pattern_data in epoch_data.items():
                            errors_per_pattern[pattern_key].append(pattern_data["Ep"])

                # Estilos para cada patrón
                styles = {
                    "Patron(1)": {"linestyle": "-", "color": "blue"},
                    "Patron(2)": {"linestyle": "--", "color": "green"},
                    "Patron(3)": {"linestyle": "-.", "color": "orange"},
                    "Patron(4)": {"linestyle": ":", "color": "purple"}
                }

                # Graficar la evolución de los errores por patrón para el componente
                for pattern, error_values in errors_per_pattern.items():
                    ax.plot(epochs, error_values, label=pattern, **styles[pattern], marker='o')

                    # Marcar los puntos donde el error llega a 0
                    zero_epochs = [epoch for epoch, err in zip(epochs, error_values) if err == 0]
                    ax.scatter(zero_epochs, [0] * len(zero_epochs), color=styles[pattern]["color"], zorder=5)

                ax.set_xlabel('Épocas')
                ax.set_ylabel('Error')
                ax.set_title(f'Evolución del Error - {sub_component}')
                ax.legend()
                ax.grid(True)

                # Insertar la figura en el frame de tkinter
                canvas = FigureCanvasTkAgg(fig, master=ideal_weights_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

    else:
        # Para las demás compuertas (AND, OR, NAND), una gráfica normal
        fig, ax = plt.subplots(figsize=(3, 2), dpi=100)  # Tamaño reducido
        epochs = []
        errors_per_pattern = {pattern: [] for pattern in ["Patron(1)", "Patron(2)", "Patron(3)", "Patron(4)"]}

        # Extraer datos por cada época y patrón
        for epoch_key, epoch_data in data.items():
            if 'Epoca' in epoch_key:
                epoch_num = int(epoch_key.split()[-1])
                epochs.append(epoch_num)
                for pattern_key, pattern_data in epoch_data.items():
                    errors_per_pattern[pattern_key].append(pattern_data["Ep"])

        # Estilos para cada patrón
        styles = {
            "Patron(1)": {"linestyle": "-", "color": "blue"},
            "Patron(2)": {"linestyle": "--", "color": "green"},
            "Patron(3)": {"linestyle": "-.", "color": "orange"},
            "Patron(4)": {"linestyle": ":", "color": "purple"}
        }

        # Graficar la evolución de los errores por patrón
        for pattern, error_values in errors_per_pattern.items():
            ax.plot(epochs, error_values, label=pattern, **styles[pattern], marker='o')

            # Marcar los puntos donde el error llega a 0
           
            zero_epochs = [epoch for epoch, err in zip(epochs, error_values) if err == 0]
            ax.scatter(zero_epochs, [0] * len(zero_epochs), color=styles[pattern]["color"], zorder=5)

        ax.set_xlabel('Épocas')
        ax.set_ylabel('Error')
        ax.set_title('Evolución del Error durante el Entrenamiento')
        ax.legend()
        ax.grid(True)

        # Insertar la figura en el frame de tkinter
        canvas = FigureCanvasTkAgg(fig, master=ideal_weights_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=(True))

from PIL import Image, ImageTk

# Función para mostrar la tabla de verdad, los campos de pesos, y los pesos ideales
def show_interface():
    reset_view()  # Reiniciar la vista al seleccionar una nueva operación
    matriz = []

    operation = selected_operation.get()

    if operation in ["AND", "OR", "XOR", "NAND"]:
        # Encabezado para la tabla de verdad
        ctk.CTkLabel(table_frame, text=f"Tabla de Verdad para {operation}", font=("Arial", 16, "bold"), text_color="white").grid(row=0, columnspan=3, pady=10)

        # Encabezados de la tabla
        ctk.CTkLabel(table_frame, text="x1", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=0, pady=5)
        ctk.CTkLabel(table_frame, text="x2", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=1, pady=5)
        ctk.CTkLabel(table_frame, text="yd", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=2, pady=5)

        # Datos de la tabla de verdad
        if operation == "AND":
            option = 2
            table_data = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        elif operation == "OR":
            option = 1
            table_data = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        elif operation == "XOR":
            option = 4
            table_data = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        elif operation == "NAND":
            option = 3
            table_data = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

        # Crear la tabla de verdad
        for i, row in enumerate(table_data):
            for j, val in enumerate(row):
                bg_color = "#37474f" if j < 2 else "#455a64"  # Fondo más oscuro para entradas y salidas
                ctk.CTkLabel(table_frame, text=str(val), font=("Arial", 14), fg_color=bg_color, text_color="white", width=30, height=30, corner_radius=10).grid(row=i+2, column=j)

        # Las salidas deseadas para la operación
        desired_outputs = [row[2] for row in table_data]

        # Campos para pesos debajo de la tabla
        ctk.CTkLabel(weights_frame, text=f"Perceptrón para {operation}", font=("Arial", 16, "bold")).pack(pady=5)
        data_pesos = obj_os.get_json(option=option)  # Obtener el JSON con los datos

        # Graficar la evolución del error en el frame de pesos ideales
        plot_error_evolution(data_pesos, operation)

        if option < 4:
            # Verificar si los 'Pesos ideales: ' están presentes en el JSON
            if 'Pesos ideales: ' in data_pesos:
                list_w = [x for x in data_pesos['Pesos ideales: '].values()]
            else:
                list_w = [0, 0, 0]  # Valores por defecto si no se encuentran los pesos ideales
        else:
            list_w = obj_os.w_xor(data_json=data_pesos)

        if operation == "XOR":
            # Crear campos para pesos XOR en 3x3 (w1, w2, umbral, w3, w4, umbral, w5, w6, umbral)

            xor_weights_frame = ctk.CTkFrame(weights_frame, fg_color="transparent")
            xor_weights_frame.pack(pady=5)
            row_ = []
            labels = ["Y1 w0", "Y1 w1", "Y1 w2", "Y2 w0", "Y2 w1", "Y2 w2", "XOR w0", "XOR w1", "XOR w2"]
            for i in range(3):
                
                for j in range(3):
                    index = i * 3 + j
                    var = tk.StringVar(value=str(list_w[i][j]))  # Crear StringVar

                    label = ctk.CTkLabel(xor_weights_frame, text=f'w{j}', font=("Arial", 14))
                    label.grid(row=i, column=j*2, padx=5, pady=5, sticky="w")
                      
                    entry = ctk.CTkEntry(xor_weights_frame, textvariable=var, placeholder_text=labels[index], font=("Arial", 14), width=80)
                    entry.grid(row=i, column=j*2+1, padx=5, pady=5)
                    row_.append(var)
                matriz.append(row_)
                row_ = []
        else:
            # Mostrar los campos para AND, OR, y NAND (w1, w2, Umbral)
            general_weights_frame = ctk.CTkFrame(weights_frame, fg_color="transparent")
            general_weights_frame.pack(pady=5)

            # Crear StringVar para los valores
            normal_w0_var = tk.StringVar(value=str(list_w[0]))
            normal_w1_var = tk.StringVar(value=str(list_w[1]))
            normal_w2_var = tk.StringVar(value=str(list_w[2]))

            # Campos de entrada para w0, w1 y w2
            ctk.CTkLabel(general_weights_frame, text="w0", font=("Arial", 14)).pack(side="left", padx=2)
            normal_w0 = ctk.CTkEntry(general_weights_frame, textvariable=normal_w0_var, placeholder_text="Bias w0", font=("Arial", 14), width=80)
            normal_w0.pack(side="left", padx=5)

            ctk.CTkLabel(general_weights_frame, text="w1", font=("Arial", 14)).pack(side="left", padx=2)
            normal_w1 = ctk.CTkEntry(general_weights_frame, textvariable=normal_w1_var, placeholder_text="Peso w1", font=("Arial", 14), width=80)
            normal_w1.pack(side="left", padx=5)

            ctk.CTkLabel(general_weights_frame, text="w2", font=("Arial", 14)).pack(side="left", padx=2)
            normal_w2 = ctk.CTkEntry(general_weights_frame, textvariable=normal_w2_var, placeholder_text="Peso w2", font=("Arial", 14), width=80)
            normal_w2.pack(side="left", padx=5)

            matriz = [float(normal_w0_var.get()), float(normal_w1_var.get()), float(normal_w2_var.get())]

        # Mostrar los pesos ideales según la operación
        ctk.CTkLabel(ideal_weights_frame, text=f"Graficos comparativos para {operation}", font=("Arial", 16, "bold")).pack(pady=5)

        # Añadir la imagen debajo de los campos de pesos
        try:
            logo_image = Image.open(obj_os.search_doc("Escudo_Udec.jpg"))  # Asegúrate de tener la ruta correcta
            logo_image = logo_image.resize((150, 150))  # Redimensionar la imagen
            logo_photo = ImageTk.PhotoImage(logo_image)

            # Colocar la imagen justo debajo del frame de pesos
            logo_label = tk.Label(weights_frame, image=logo_photo, bg="black")
            logo_label.image = logo_photo  # Mantener referencia para evitar que se elimine la imagen
            logo_label.pack(pady=5)  # Usar pack() para alinearlo correctamente dentro de la ventana

        except FileNotFoundError:
            print("No se encontró la imagen Escudo_Udec.jpg.")

    # Crear campos y etiquetas para mostrar el error por cada patrón al lado derecho
    ctk.CTkLabel(result_frame, text="Errores por cada Patrón", font=("Arial", 16, "bold")).pack(pady=5)  # Reducir el padding aquí

    # Organizar los errores de forma horizontal y vertical
    errors_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
    errors_frame.pack(fill="x", padx=5, pady=5)  # Reducir el padding vertical aquí

    # Ajustes para mantener la estructura de 4 patrones o 12 dependiendo de la compuerta seleccionada
    if operation in ["XOR"]:
        num_errors = 12
        rows, cols = 3, 4  # 4 filas, 3 columnas para XOR
    else:
        num_errors = 4
        rows, cols = 1, 4  # 1 fila, 4 columnas para AND, OR, NAND

    # Establecer proporciones iguales para las columnas
    for i in range(cols):
        errors_frame.grid_columnconfigure(i * 2, weight=1)

    entry_width = 50  # Ajuste del ancho de las entradas
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j  # Índice para los campos de error
            if index < num_errors:
                ctk.CTkLabel(errors_frame, text=f"Patrón {index+1}: ", font=("Arial", 12)).grid(row=i, column=j*2, padx=1, pady=1)  # Reducir height y padding

                # Añadir el campo de Error
                error_var = ctk.StringVar()
                error_vars.append(error_var)
                error_entry = ctk.CTkEntry(errors_frame, textvariable=error_var, font=("Arial", 12), placeholder_text=f"Error {index+1}", width=entry_width, height=20)
                error_entry.grid(row=i, column=j*2 + 1, padx=5, pady=2, sticky="nsew")  # Reducir height y padding

                error_labels.append(error_entry)  # Guardar la referencia para aplicar colores más tarde

    # Botón para comparar y actualizar los colores de los errores
    if option < 4:
        ctk.CTkButton(result_frame, text="Comparar Errores", font=("Arial", 14), command=lambda:[update_error_colors([float(normal_w0_var.get()), float(normal_w1_var.get()), float(normal_w2_var.get())], opt=option)]).pack(pady=5)  # Reducir padding del botón
    else:
        ctk.CTkButton(result_frame, text="Comparar Errores", font=("Arial", 14), command=lambda:[update_error_colors(w=matriz, opt=option)]).pack(pady=5)


# Crear dos frames para ser reutilizados (uno para la tabla de verdad, uno para los pesos, y otro para los pesos ideales)
main_inner_frame = ctk.CTkFrame(scrollable_frame)
main_inner_frame.pack(pady=10, padx=10, fill="both", expand=True)

right_frame = ctk.CTkFrame(main_inner_frame, width=600, fg_color="transparent")
right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Frame para mostrar los errores
result_frame = ctk.CTkFrame(right_frame, fg_color="gray30", corner_radius=10)
result_frame.pack(pady=10, padx=10, fill="x", expand=False)

# Frame para mostrar los pesos ideales
ideal_weights_frame = ctk.CTkFrame(scrollable_frame, fg_color="gray30", corner_radius=10)
ideal_weights_frame.pack(pady=10, padx=10, fill="x", expand=True)

# Pie de página
footer_label = ctk.CTkLabel(scrollable_frame, text="Nicolas Torres Robriguez - Juan David Moreno Beltran", font=("Arial", 10), text_color="gray")
footer_label.pack(side="bottom", pady=10)

# Mostrar la interfaz para la operación AND al inicio
show_interface()
# Configurar las proporciones de la ventana
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", on_closing)
# Ejecutar la ventana
root.mainloop()
