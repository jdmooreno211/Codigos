from Sources.compuertas import Compuertas
from Sources.system_os import OperationsSystem
from Sources.perceptron import Perceptron
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

# Configurar el tema oscuro de la interfaz
ctk.set_appearance_mode("dark")  # Cambiar a un modo oscuro
ctk.set_default_color_theme("dark-blue")  # Usar un tema oscuro

# Función para centrar la ventana en la pantalla
def center_window(root, width=950, height=800):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Crear la ventana principal
root = ctk.CTk()
root.title("Perceptrón Monocapa")
center_window(root)  # Centrar la ventana en la pantalla
root.resizable(True, True)

# Definir la variable seleccionada para el menú desplegable
selected_operation = tk.StringVar(value="Seleccione una operación")

# Cargar y agregar la imagen en la parte superior
background_image = Image.open("facatativa-2.jpg")  # Ruta de la imagen
background_image = background_image.resize((950, 250))  # Ajustar el tamaño de la imagen para la cabecera
bg_image = ImageTk.PhotoImage(background_image)

# Crear un frame para la imagen en la parte superior
image_frame = tk.Label(root, image=bg_image, bg="black")  # Fondo oscuro
image_frame.pack(side="top", fill="x")  # Coloca la imagen en la parte superior

# Mover el menú desplegable debajo de la imagen
dropdown_menu = ctk.CTkOptionMenu(root, values=["AND", "OR", "XOR", "NAND"], variable=selected_operation, command=lambda _: show_interface())
dropdown_menu.pack(pady=10, side="top")  # Mover debajo de la imagen

# Crear un frame con scroll para los controles
scrollable_frame = ctk.CTkScrollableFrame(root, width=900, height=500)
scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Variables
error_vars = []  # Lista de variables para los errores
error_labels = []  # Lista de etiquetas de error para aplicar colores

# Crear dos frames globales para ser reutilizados
weights_frame = None
table_frame = None
result_frame = None
ideal_weights_frame = None  # Frame para los pesos ideales
#variables para compuertas
option = 0
obj_os = OperationsSystem()
obj_perceptron = Perceptron()
# Función para reiniciar la vista (destruir frames y resetear listas)
def reset_view():
    global weights_frame, table_frame, result_frame, ideal_weights_frame, error_vars, error_labels
    if weights_frame:
        for widget in weights_frame.winfo_children():
            widget.destroy()
    if table_frame:
        for widget in table_frame.winfo_children():
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
def update_error_colors(w,opt):
    if opt == 4:
        aux = []
        for i in range(3):
            x = [float(y.get()) for y in w[i]]
            print(x)
            aux.append(x)
        w = aux
    l_w = obj_perceptron.intermediate(option=opt,weigth=w)
    print(l_w)
    
    for i,error_entry in enumerate(error_labels):
            if l_w[i] == 0:
                error_entry.configure(fg_color="green")  # Cambiar a verde si el error es 0
            else:
                error_entry.configure(fg_color="red")
            error_entry.delete(0, 'end') 
            error_entry.insert(0, f'{l_w[i]}') 
   
               
        


# Función para mostrar la tabla de verdad, los campos de pesos, y los pesos ideales
def show_interface():
    reset_view()  # Reiniciar la vista al seleccionar una nueva operación
    matriz = []

    operation = selected_operation.get()

    if operation in ["AND", "OR", "XOR", "NAND"]:
        # Redimensionar el ancho del frame para las tablas de verdad
        table_frame.configure(width=200)

        # Encabezado para la tabla de verdad
        ctk.CTkLabel(table_frame, text=f"Tabla de Verdad para {operation}", font=("Arial", 16, "bold"), text_color="white").grid(row=0, columnspan=3, pady=5)

        # Encabezados de la tabla (unidos, con letras más claras)
        ctk.CTkLabel(table_frame, text="x1", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=0, pady=5)
        ctk.CTkLabel(table_frame, text="x2", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=1, pady=5)
        ctk.CTkLabel(table_frame, text="yd", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=2, pady=5)

        # Datos de la tabla de verdad con fondo oscuro y números más claros
        if operation == "AND":
            option = 1
            table_data = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
        elif operation == "OR":
            option = 2
            table_data = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
        elif operation == "XOR":
            option = 4
            table_data = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
        elif operation == "NAND":
            option = 3
            table_data = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

        # Ajustes para centrar la tabla y eliminar espacio extra
        table_frame.pack_propagate(False)  # Evitar que el frame cambie de tamaño
        table_frame.grid_anchor("center")  # Alinear al centro

        # Estilo mejorado para la tabla, oscureciendo el fondo de los números
        for i, row in enumerate(table_data):
            for j, val in enumerate(row):
                bg_color = "#37474f" if j < 2 else "#455a64"  # Fondo más oscuro para entradas y salidas
                ctk.CTkLabel(table_frame, text=str(val), font=("Arial", 14), fg_color=bg_color, text_color="white", width=30, height=30, corner_radius=10).grid(row=i+2, column=j)

        # Las salidas deseadas para la operación
        desired_outputs = [row[2] for row in table_data]

        # Campos para pesos
        ctk.CTkLabel(weights_frame, text=f"Perceptrón para {operation}", font=("Arial", 16, "bold")).pack(pady=10)
        #aqui van las peticiones del precepton
        data_pesos = obj_os.get_json(option=option)
        if option < 4:
            list_w = [x for x in data_pesos['Pesos ideales: '].values()]
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
                    entry = ctk.CTkEntry(xor_weights_frame, textvariable=var, placeholder_text=labels[index], font=("Arial", 14), width=80)
                    entry.grid(row=i, column=j, padx=5, pady=5)  
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
            normal_w0.pack(side="left", padx=10)

            ctk.CTkLabel(general_weights_frame, text="w1", font=("Arial", 14)).pack(side="left", padx=2)
            normal_w1 = ctk.CTkEntry(general_weights_frame, textvariable=normal_w1_var, placeholder_text="Peso w1", font=("Arial", 14), width=80)
            normal_w1.pack(side="left", padx=10)

            ctk.CTkLabel(general_weights_frame, text="w2", font=("Arial", 14)).pack(side="left", padx=2)
            normal_w2 = ctk.CTkEntry(general_weights_frame, textvariable=normal_w2_var, placeholder_text="Peso w2", font=("Arial", 14), width=80)
            normal_w2.pack(side="left", padx=10)
            
            matriz = [float(normal_w0_var.get()),float(normal_w1_var.get()),float(normal_w2_var.get())]
        # Mostrar los pesos ideales según la operación
        ctk.CTkLabel(ideal_weights_frame, text=f"Pesos Ideales para {operation}", font=("Arial", 16, "bold")).pack(pady=10)
            # Campos de entrada para pesos ideales
    # Crear campos y etiquetas para mostrar el error por cada patrón
    ctk.CTkLabel(result_frame, text="Errores por cada Patrón", font=("Arial", 16, "bold")).pack(pady=10)

    # Organizar los errores de forma horizontal y vertical
    errors_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
    errors_frame.pack(fill="x", padx=10, pady=5)

    # Mostrar 4 campos de error para AND, OR, NAND y 12 campos para XOR
    num_errors = 12 if operation == "XOR" else 4
    rows, cols = (3, 4) if operation == "XOR" else (1, 4)

    for i in range(rows):
        for j in range(cols):
            index = i * cols + j  # Índice para los campos de error
            if index < num_errors:
                ctk.CTkLabel(errors_frame, text=f"Patrón {index+1}: ", font=("Arial", 14)).grid(row=i, column=j*2, padx=10, pady=5)

                # Añadir el campo de Error
                error_var = ctk.StringVar()
                error_vars.append(error_var)
                error_entry = ctk.CTkEntry(errors_frame, textvariable=error_var, font=("Arial", 14), placeholder_text=f"Error {index+1}", width=80)
                error_entry.grid(row=i, column=j*2 + 1, padx=10, pady=5)

                error_labels.append(error_entry)  # Guardar la referencia para aplicar colores más tarde
    # Botón para comparar y actualizar los colores de los errores
    if option < 4:
        ctk.CTkButton(result_frame, text="Comparar Errores", font=("Arial", 14),command=lambda:[update_error_colors([float(normal_w0_var.get()),float(normal_w1_var.get()),float(normal_w2_var.get())],opt=option)]).pack(pady=10)
    else:
        ctk.CTkButton(result_frame, text="Comparar Errores", font=("Arial", 14),command=lambda:[update_error_colors(w=matriz,opt=option)]).pack(pady=10)
    
    
# Crear dos frames para ser reutilizados (uno para la tabla de verdad, uno para los pesos, y otro para los pesos ideales)
main_inner_frame = ctk.CTkFrame(scrollable_frame)
main_inner_frame.pack(pady=10, padx=10, fill="both", expand=True)

left_frame = ctk.CTkFrame(main_inner_frame, width=300, fg_color="transparent")
left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

right_frame = ctk.CTkFrame(main_inner_frame, width=300, fg_color="transparent")
right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Frame izquierdo para tabla de verdad
table_frame = ctk.CTkFrame(left_frame, fg_color="gray30", corner_radius=10)
table_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Frame derecho para entrada de pesos
weights_frame = ctk.CTkFrame(right_frame, fg_color="gray30", corner_radius=10)
weights_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Frame para mostrar los errores
result_frame = ctk.CTkFrame(scrollable_frame, fg_color="gray30", corner_radius=10)
result_frame.pack(pady=20, padx=20, fill="x", expand=False)

# Frame para mostrar los pesos ideales
ideal_weights_frame = ctk.CTkFrame(scrollable_frame, fg_color="gray30", corner_radius=10)
ideal_weights_frame.pack(pady=20, padx=20, fill="x", expand=False)

# Pie de página
footer_label = ctk.CTkLabel(scrollable_frame, text="Interfaz para un Perceptrón Monocapa", font=("Arial", 10), text_color="gray")
footer_label.pack(side="bottom", pady=10)

# Ejecutar la ventana
root.mainloop()
