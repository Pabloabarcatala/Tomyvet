import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
from tkcalendar import Calendar
from PIL import Image, ImageTk
import sqlite3

class TomyVetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TomyVet - Software de Veterinaria")
        self.root.geometry("900x600")
        self.root.configure(bg='#2c3e50')
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background='#2c3e50')
        self.style.configure("TLabel", background='#2c3e50', foreground='white', font=('Helvetica', 12))
        self.style.configure("TButton", background='#16a085', foreground='white', font=('Helvetica', 12))
        self.style.configure("Treeview", background='#ecf0f1', foreground='black', rowheight=25, fieldbackground='#ecf0f1')
        self.style.configure("Treeview.Heading", background='#34495e', foreground='white', font=('Helvetica', 12, 'bold'))
        self.style.map("TButton", background=[('active', '#1abc9c')])

        self.logo = ImageTk.PhotoImage(Image.open("logo.png").resize((200, 200)))
        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        self.bienvenida_frame = ttk.Frame(self.root, padding="10")
        self.bienvenida_frame.grid(row=0, column=0, sticky="nsew")

        logo_label = ttk.Label(self.bienvenida_frame, image=self.logo)
        logo_label.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        ttk.Label(self.bienvenida_frame, text="Bienvenido a la aplicación de TomyVet", font=("Helvetica", 16, 'bold')).grid(column=0, row=1, padx=10, pady=10, columnspan=2)

        ttk.Button(self.bienvenida_frame, text="Usuario Nuevo", command=self.mostrar_registro).grid(column=0, row=2, padx=10, pady=10)
        ttk.Button(self.bienvenida_frame, text="Usuario Registrado", command=self.mostrar_login).grid(column=1, row=2, padx=10, pady=10)

    def mostrar_login(self):
        self.bienvenida_frame.grid_remove()
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        logo_label = ttk.Label(self.login_frame, image=self.logo)
        logo_label.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        ttk.Label(self.login_frame, text="Iniciar Sesión", font=("Helvetica", 16, 'bold')).grid(column=0, row=1, padx=10, pady=10, columnspan=2)

        ttk.Label(self.login_frame, text="Usuario:").grid(column=0, row=2, padx=10, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.login_frame, text="Contraseña:").grid(column=0, row=3, padx=10, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(self.login_frame, text="Iniciar Sesión", command=self.verificar_login).grid(column=0, row=4, padx=10, pady=10, columnspan=2)
        ttk.Button(self.login_frame, text="Volver", command=self.volver_bienvenida).grid(column=0, row=5, padx=10, pady=10, columnspan=2)

    def mostrar_registro(self):
        self.bienvenida_frame.grid_remove()
        self.registro_frame = ttk.Frame(self.root, padding="10")
        self.registro_frame.grid(row=0, column=0, sticky="nsew")

        logo_label = ttk.Label(self.registro_frame, image=self.logo)
        logo_label.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        ttk.Label(self.registro_frame, text="Registrar Usuario", font=("Helvetica", 16, 'bold')).grid(column=0, row=1, padx=10, pady=10, columnspan=2)

        ttk.Label(self.registro_frame, text="Usuario:").grid(column=0, row=2, padx=10, pady=5)
        self.reg_username_entry = ttk.Entry(self.registro_frame)
        self.reg_username_entry.grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.registro_frame, text="Contraseña:").grid(column=0, row=3, padx=10, pady=5)
        self.reg_password_entry = ttk.Entry(self.registro_frame, show="*")
        self.reg_password_entry.grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(self.registro_frame, text="Registrar", command=self.registrar_usuario).grid(column=0, row=4, padx=10, pady=10, columnspan=2)
        ttk.Button(self.registro_frame, text="Volver", command=self.volver_bienvenida).grid(column=0, row=5, padx=10, pady=10, columnspan=2)

    def verificar_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conexion.close()

        if user:
            self.login_frame.grid_remove()
            self.mostrar_interfaz_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar_usuario(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Debe completar todos los campos")
            return

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, password))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Usuario registrado exitosamente")
        self.volver_bienvenida()

    def volver_bienvenida(self):
        self.login_frame.grid_remove() if hasattr(self, 'login_frame') else None
        self.registro_frame.grid_remove() if hasattr(self, 'registro_frame') else None
        self.bienvenida_frame.grid()

    def mostrar_interfaz_principal(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_inicio = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_inicio, text='Inicio')

        self.tab_pacientes = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_pacientes, text='Pacientes')

        self.tab_citas = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_citas, text='Citas')

        self.tab_inventario = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_inventario, text='Inventario')

        self.tab_facturas = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_facturas, text='Facturas')

        self.tab_control.pack(expand=1, fill='both')

        self.crear_tab_inicio()
        self.crear_tab_pacientes()
        self.crear_tab_citas()
        self.crear_tab_inventario()
        self.crear_tab_facturas()

    def crear_tab_inicio(self):
        ttk.Label(self.tab_inicio, text="Calendario de Citas", font=("Helvetica", 16, 'bold')).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.calendario = Calendar(self.tab_inicio, selectmode='day', date_pattern='yyyy-mm-dd', background='lightblue', foreground='black')
        self.calendario.grid(column=0, row=1, padx=10, pady=10, columnspan=2, sticky="nsew")

        ttk.Button(self.tab_inicio, text="Actualizar Citas", command=self.mostrar_citas_calendario).grid(column=0, row=2, padx=10, pady=10, columnspan=2)

        self.citas_text = scrolledtext.ScrolledText(self.tab_inicio, width=60, height=10)  # Hacemos el calendario más grande
        self.citas_text.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        self.mostrar_citas_calendario()

    def mostrar_citas_calendario(self):
        fecha_seleccionada = self.calendario.get_date()

        self.citas_text.delete('1.0', tk.END)
        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Citas WHERE fecha=?', (fecha_seleccionada,))
        rows = cursor.fetchall()
        conexion.close()

        for row in rows:
            nombre_paciente = row[1]
            fecha = row[2]
            motivo = row[3]
            self.citas_text.insert(tk.END, f"Paciente: {nombre_paciente}, Fecha: {fecha}, Motivo: {motivo}\n")

    def crear_tab_pacientes(self):
        ttk.Label(self.tab_pacientes, text="Gestión de Pacientes", font=("Helvetica", 16, 'bold')).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.nombre_paciente = tk.StringVar()
        self.nombre_dueno = tk.StringVar()
        self.direccion_dueno = tk.StringVar()
        self.telefono_dueno = tk.StringVar()
        self.tipo_animal_paciente = tk.StringVar()
        self.raza_paciente = tk.StringVar()
        self.edad_paciente = tk.StringVar()
        self.historial_paciente = tk.StringVar()

        ttk.Label(self.tab_pacientes, text="Nombre del Paciente:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.nombre_paciente).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Nombre del Dueño:").grid(column=0, row=2, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.nombre_dueno).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Dirección del Dueño:").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.direccion_dueno).grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Teléfono del Dueño:").grid(column=0, row=4, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.telefono_dueno).grid(column=1, row=4, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Tipo de Animal:").grid(column=0, row=5, padx=10, pady=5)
        ttk.Combobox(self.tab_pacientes, textvariable=self.tipo_animal_paciente, values=["Perro", "Gato", "Ave", "Reptil", "Otro"]).grid(column=1, row=5, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Raza:").grid(column=0, row=6, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.raza_paciente).grid(column=1, row=6, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Edad:").grid(column=0, row=7, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.edad_paciente).grid(column=1, row=7, padx=10, pady=5)

        ttk.Label(self.tab_pacientes, text="Historial Médico:").grid(column=0, row=8, padx=10, pady=5)
        ttk.Entry(self.tab_pacientes, textvariable=self.historial_paciente).grid(column=1, row=8, padx=10, pady=5)

        ttk.Button(self.tab_pacientes, text="Agregar Paciente", command=self.agregar_paciente).grid(column=0, row=9, padx=10, pady=10, columnspan=2)

        self.tree_pacientes = ttk.Treeview(self.tab_pacientes, columns=("id", "nombre", "nombre_dueno", "direccion_dueno", "telefono_dueno", "tipo_animal", "raza", "edad", "historial"), show='headings')
        self.tree_pacientes.heading("id", text="ID")
        self.tree_pacientes.heading("nombre", text="Nombre del Paciente")
        self.tree_pacientes.heading("nombre_dueno", text="Nombre del Dueño")
        self.tree_pacientes.heading("direccion_dueno", text="Dirección del Dueño")
        self.tree_pacientes.heading("telefono_dueno", text="Teléfono del Dueño")
        self.tree_pacientes.heading("tipo_animal", text="Tipo de Animal")
        self.tree_pacientes.heading("raza", text="Raza")
        self.tree_pacientes.heading("edad", text="Edad")
        self.tree_pacientes.heading("historial", text="Historial Médico")

        self.tree_pacientes.grid(column=0, row=10, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Button(self.tab_pacientes, text="Actualizar", command=self.mostrar_pacientes).grid(column=0, row=11, padx=10, pady=10, columnspan=2)

    def agregar_paciente(self):
        nombre = self.nombre_paciente.get()
        nombre_dueno = self.nombre_dueno.get()
        direccion_dueno = self.direccion_dueno.get()
        telefono_dueno = self.telefono_dueno.get()
        tipo_animal = self.tipo_animal_paciente.get()
        raza = self.raza_paciente.get()
        edad = self.edad_paciente.get()
        historial = self.historial_paciente.get()

        if not edad.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Pacientes (nombre, nombre_dueno, direccion_dueno, telefono_dueno, tipo_animal, raza, edad, historial_medico)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, nombre_dueno, direccion_dueno, telefono_dueno, tipo_animal, raza, int(edad), historial))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Paciente agregado exitosamente")
        self.mostrar_pacientes()

    def mostrar_pacientes(self):
        for i in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(i)
        
        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Pacientes')
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_pacientes.insert("", "end", values=row)
        
        conexion.close()

    def crear_tab_citas(self):
        ttk.Label(self.tab_citas, text="Gestión de Citas", font=("Helvetica", 16, 'bold')).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.nombre_paciente_cita = tk.StringVar()
        self.fecha_cita = tk.StringVar()
        self.motivo_cita = tk.StringVar()

        ttk.Label(self.tab_citas, text="Nombre del Paciente:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Entry(self.tab_citas, textvariable=self.nombre_paciente_cita).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.tab_citas, text="Fecha (YYYY-MM-DD):").grid(column=0, row=2, padx=10, pady=5)
        ttk.Entry(self.tab_citas, textvariable=self.fecha_cita).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.tab_citas, text="Motivo:").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self.tab_citas, textvariable=self.motivo_cita).grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(self.tab_citas, text="Agregar Cita", command=self.agregar_cita).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

        self.tree_citas = ttk.Treeview(self.tab_citas, columns=("id", "nombre_paciente", "fecha", "motivo"), show='headings')
        self.tree_citas.heading("id", text="ID")
        self.tree_citas.heading("nombre_paciente", text="Nombre del Paciente")
        self.tree_citas.heading("fecha", text="Fecha")
        self.tree_citas.heading("motivo", text="Motivo")

        self.tree_citas.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Button(self.tab_citas, text="Actualizar", command=self.mostrar_citas).grid(column=0, row=6, padx=10, pady=10, columnspan=2)

    def agregar_cita(self):
        nombre_paciente = self.nombre_paciente_cita.get()
        fecha = self.fecha_cita.get()
        motivo = self.motivo_cita.get()

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Citas (nombre_paciente, fecha, motivo)
            VALUES (?, ?, ?)
        ''', (nombre_paciente, fecha, motivo))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Cita agregada exitosamente")
        self.mostrar_citas()

    def mostrar_citas(self):
        for i in self.tree_citas.get_children():
            self.tree_citas.delete(i)
        
        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Citas')
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_citas.insert("", "end", values=row)
        
        conexion.close()

    def crear_tab_inventario(self):
        ttk.Label(self.tab_inventario, text="Gestión de Inventario", font=("Helvetica", 16, 'bold')).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.nombre_medicamento = tk.StringVar()
        self.cantidad_medicamento = tk.IntVar()
        self.precio_medicamento = tk.DoubleVar()

        ttk.Label(self.tab_inventario, text="Nombre:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Entry(self.tab_inventario, textvariable=self.nombre_medicamento).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.tab_inventario, text="Cantidad:").grid(column=0, row=2, padx=10, pady=5)
        ttk.Entry(self.tab_inventario, textvariable=self.cantidad_medicamento).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.tab_inventario, text="Precio:").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self.tab_inventario, textvariable=self.precio_medicamento).grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(self.tab_inventario, text="Agregar Medicamento", command=self.agregar_medicamento).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

        self.tree_inventario = ttk.Treeview(self.tab_inventario, columns=("id", "nombre", "cantidad", "precio"), show='headings')
        self.tree_inventario.heading("id", text="ID")
        self.tree_inventario.heading("nombre", text="Nombre")
        self.tree_inventario.heading("cantidad", text="Cantidad")
        self.tree_inventario.heading("precio", text="Precio")

        self.tree_inventario.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Button(self.tab_inventario, text="Actualizar", command=self.mostrar_inventario).grid(column=0, row=6, padx=10, pady=10, columnspan=2)

    def agregar_medicamento(self):
        nombre = self.nombre_medicamento.get()
        cantidad = self.cantidad_medicamento.get()
        precio = self.precio_medicamento.get()

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Inventario (nombre_medicamento, cantidad, precio)
            VALUES (?, ?, ?)
        ''', (nombre, cantidad, precio))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Medicamento agregado exitosamente")
        self.mostrar_inventario()

    def mostrar_inventario(self):
        for i in self.tree_inventario.get_children():
            self.tree_inventario.delete(i)
        
        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Inventario')
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_inventario.insert("", "end", values=row)
        
        conexion.close()

    def crear_tab_facturas(self):
        ttk.Label(self.tab_facturas, text="Gestión de Facturas", font=("Helvetica", 16, 'bold')).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.nombre_paciente_factura = tk.StringVar()
        self.monto_total_factura = tk.DoubleVar()
        self.fecha_factura = tk.StringVar()

        ttk.Label(self.tab_facturas, text="Nombre del Paciente:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Entry(self.tab_facturas, textvariable=self.nombre_paciente_factura).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(self.tab_facturas, text="Monto Total:").grid(column=0, row=2, padx=10, pady=5)
        ttk.Entry(self.tab_facturas, textvariable=self.monto_total_factura).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(self.tab_facturas, text="Fecha (YYYY-MM-DD):").grid(column=0, row=3, padx=10, pady=5)
        ttk.Entry(self.tab_facturas, textvariable=self.fecha_factura).grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(self.tab_facturas, text="Agregar Factura", command=self.agregar_factura).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

        self.tree_facturas = ttk.Treeview(self.tab_facturas, columns=("id", "nombre_paciente", "monto_total", "fecha"), show='headings')
        self.tree_facturas.heading("id", text="ID")
        self.tree_facturas.heading("nombre_paciente", text="Nombre del Paciente")
        self.tree_facturas.heading("monto_total", text="Monto Total")
        self.tree_facturas.heading("fecha", text="Fecha")

        self.tree_facturas.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Button(self.tab_facturas, text="Actualizar", command=self.mostrar_facturas).grid(column=0, row=6, padx=10, pady=10, columnspan=2)

    def agregar_factura(self):
        nombre_paciente = self.nombre_paciente_factura.get()
        monto_total = self.monto_total_factura.get()
        fecha = self.fecha_factura.get()

        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Facturas (nombre_paciente, monto_total, fecha)
            VALUES (?, ?, ?)
        ''', (nombre_paciente, monto_total, fecha))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Factura agregada exitosamente")
        self.mostrar_facturas()

    def mostrar_facturas(self):
        for i in self.tree_facturas.get_children():
            self.tree_facturas.delete(i)
        
        conexion = sqlite3.connect('tomyvet.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM Facturas')
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree_facturas.insert("", "end", values=row)
        
        conexion.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = TomyVetApp(root)
    root.mainloop()
