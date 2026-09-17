import tkinter as tk
import math
import random

class BeautifulNaturalTree:
    def __init__(self, root, width=900, height=700):
        self.root = root
        self.width = width
        self.height = height
        self.root.title("Árbol Natural Procedimental")
        self.root.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#0f1115")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.time_step = 0
        
        # estructura de datos para almacenar la información de cada rama antes de dibujarla
        self.tree_structure = []
        # Parámetros iniciales: X, Y, Ángulo, Longitud Máxima, Grosor, Retraso para nacer
        self.generate_tree_data(self.width / 2, self.height - 30, 90, 130, 14, start_time=0)
        self.canvas.bind("<Button-1>", self.on_click)
        self.animate()

    def generate_tree_data(self, x, y, angle, max_length, width, start_time):
        """Genera y almacena la estructura del árbol antes de dibujarlo"""
        # Condición de parada para que no se sature el tope
        if max_length < 7 or width < 1:
            return

        # Calcular el punto final destino de esta rama
        rad = math.radians(angle)
        x_end = x + max_length * math.cos(rad)
        y_end = y - max_length * math.sin(rad)

        # Guardamos los datos de la rama
        self.tree_structure.append({
            'x_start': x, 'y_start': y,
            'x_target': x_end, 'y_target': y_end,
            'max_len': max_length, 'angle': angle,
            'width': width, 'start_time': start_time,
            'current_len': 0  # Empezará midiendo 0
        })

        # El tiempo que tardará esta rama en crecer antes de que nazcan sus hijas
        growth_duration = max_length * 0.3 
        next_start_time = start_time + growth_duration

        # --- LÓGICA DE RAMIFICACIÓN ALEATORIA Y NATURAL ---
        
        num_branches = random.choice([1, 2, 2, 3]) if width > 4 else random.choice([1, 2])

        for _ in range(num_branches):
            # Variación aleatoria del ángulo para que se vea orgánico
            angle_offset = random.uniform(15, 35)
            if num_branches == 1:
                # Si es una sola rama, continúa casi recta con una ligera desviación
                next_angle = angle + random.uniform(-10, 10)
            else:
                # Si se divide, unas van a la izquierda y otras a la derecha
                next_angle = angle + random.uniform(-angle_offset, angle_offset)

                # Si es la primera rama, la inclinamos más hacia un lado para dar sensación de crecimiento natural
                if _ == 0:
                    next_angle -= random.uniform(5, 15)
                elif _ == 1:
                    next_angle += random.uniform(5, 15)

                # Si hay una tercera rama, la mantenemos más centrada
                if num_branches == 3 and _ == 2:
                    next_angle += random.uniform(-5, 5)

            # Reducción de longitud asimétrica y aleatoria
            length_factor = random.uniform(0.65, 0.82)
            next_length = max_length * length_factor
            
            # Reducción de grosor proporcional
            next_width = width * random.uniform(0.65, 0.75)

            # Llamada recursiva para planificar la siguiente rama
            self.generate_tree_data(x_end, y_end, next_angle, next_length, next_width, next_start_time)

    def draw_recursive_animation(self, branch):
        """Calcula el crecimiento y dibuja una rama individual basándose en el tiempo global"""
        t = self.time_step - branch['start_time']

        # Si aún no le toca nacer a esta rama, no la dibujamos
        if t < 0:
            return

        # Velocidad de crecimiento de la rama (doble velocidad)
        speed = 3.0
        branch['current_len'] = min(branch['max_len'], t * speed)

        if branch['current_len'] <= 0:
            return

        #  la rama se mantiene en su ángulo base
        rad = math.radians(branch['angle'])
        x_current = branch['x_start'] + branch['current_len'] * math.cos(rad)
        y_current = branch['y_start'] - branch['current_len'] * math.sin(rad)

        # Paleta de colores natural: 
        if branch['width'] > 7:
            color = "#706760"  # Tronco principal
        elif branch['width'] > 3:
            color = "#49423c"  # Ramas medias
        elif branch['width'] > 1.5:
            color = "#4f5546"  # Ramas delgadas / verde oliva
        else:
            color = "#616054"  # Brotes terminales / hojas claros

        self.canvas.create_line(
            branch['x_start'], branch['y_start'], 
            x_current, y_current, 
            fill=color, 
            width=max(1, int(branch['width'])), 
            capstyle=tk.ROUND # Bordes redondeados para un acabado suave
        )

    def animate(self):
        self.canvas.delete("all")

        # Botón para reiniciar el árbol
        self.canvas.create_rectangle(10, 10, 110, 40, fill="#5c5c5c", outline="#1c1c1c", width=2)
        self.canvas.create_text(60, 25, text="Reiniciar", fill="#ffffff", font=("Helvetica", 12, "bold"))

        # Dibuja todas las ramas calculadas en su estado actual de tiempo
        for branch in self.tree_structure:
            self.draw_recursive_animation(branch)

        self.time_step += 1
        self.root.after(20, self.animate)

    def on_click(self, event):
        if 10 <= event.x <= 110 and 10 <= event.y <= 40:
            self.time_step = 0
            self.tree_structure.clear()
            self.generate_tree_data(self.width / 2, self.height - 30, 90, 130, 14, start_time=0)


if __name__ == "__main__":
    root = tk.Tk()
    app = BeautifulNaturalTree(root, width=900, height=700)
    root.mainloop()
