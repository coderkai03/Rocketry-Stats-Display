import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random

graph_properties = {
    'temperature': {
        'color': 'blue',
        'ylabel': 'Temp (F)',
        'yticks': [60, 80],
        'ylim': [60, 80],
        'units': '°F'
    },
    'pressure': {
        'color': 'red',
        'ylabel': 'Press (psi)',
        'yticks': [50, 150],
        'ylim': [50, 150],
        'units': 'psi'
    },
    'load_sensor': {
        'color': 'green',
        'ylabel': 'Load (lb)',
        'yticks': [0, 100],
        'ylim': [0, 100],
        'units': 'lb'
    }
}

def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.grid(row=0, column=0)
    return canvas


def create_servo(canvas, x, y, diameter, title, initial_state=True):
    # Create red/green circle
    color = 'green' if initial_state else 'red'
    circle = canvas.create_oval(x, y, x + diameter/4, y + diameter/4, outline='black', width=2, fill=color)

    # Create label under the circle
    label = canvas.create_text(x + diameter / 8, y + diameter / 4 + 10, text=title, anchor=tk.CENTER, font=('Arial', 10, 'bold'))

    return circle, label

def create_sensor_display(canvas, x, y, width, height, title, graph_type):
    canvas_widget = None
    line_plot = None
    timestamps = []
    data = []
    ani = None
    circle = None
    label = None

    if graph_type == "servo":
        # Create servo display with red/green circle
        initial_state = random.choice([True, False])
        circle, label = create_servo(canvas, x, y, height, title, initial_state)
    else:
        # Create graph with transparent background
        canvas_widget, line_plot, timestamps, data = create_graph(canvas, x, y, width, height, title, graph_type)
        # Start updating the graph using FuncAnimation
        ani = start_animation(canvas_widget, line_plot, timestamps, data, graph_type)

    return canvas_widget, line_plot, timestamps, data, ani, circle, label


def create_graph(canvas, x, y, width, height, title, graph_type):
    fig, ax = plt.subplots(figsize=(4, 4), tight_layout=True)

    # Initial data for demonstration
    initial_value = 0

    timestamps = [0]
    data = [initial_value]

    # Set the appropriate graph type
    properties = graph_properties.get(graph_type, {})
    line_plot, = ax.plot(timestamps, data, color=properties.get('color', 'black'), linewidth=2)
    ax.set_ylabel(properties.get('ylabel', ''))
    ax.set_yticks(properties.get('yticks', []))
    ax.set_ylim(properties.get('ylim', []))

    # Set the title with decreased font size
    ax.set_title(title, fontsize=10)

    # Remove horizontal values on the x-axis
    ax.set_xticks([])
    ax.set_xlim([-10, 1])

    # Set the background color to transparent
    ax.set_facecolor('none')

    canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().place(x=x, y=y, width=width, height=height)

    return canvas_widget, line_plot, timestamps, data


def create_rect(canvas, x, y, width, height, fill_color):
    rectangle = canvas.create_rectangle(x, y, width, height, fill=fill_color)
    return rectangle

def update_servo_state(canvas, circle, label):
    # Toggle the servo state (change color and label)
    current_color = canvas.itemcget(circle, 'fill')
    new_state = current_color == 'red'
    color = 'green' if new_state else 'red'
    canvas.itemconfig(circle, fill=color)
    canvas.itemconfig(label, text="ON" if new_state else "OFF")
    return new_state


servo_states = {"servo1": True, "servo2": True}

def update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type):
    properties = graph_properties.get(graph_type, {})
    
    if graph_type == "servo":
        # Update the state of each servo alternately
        for servo_id in servo_states:
            # Retrieve the corresponding circle and label for the servo
            circle, label = servo_states[servo_id]['objects']
            servo_states[servo_id]['state'] = update_servo_state(canvas_widget, circle, label)
    else:
        # For other types, generate a new data point without checking the y-limits
        new_data = random.uniform(0, 100)
        # Append the new data to the list
        timestamps.append(timestamps[-1] + 1)
        data.append(data[-1] + 1)
        
        # Update the line plot with the new data
        line_plot.set_data(timestamps, data)

        # Adjust y-limits if the new data point is outside the current limits
        if data[-1] < properties['ylim'][0]:
            properties['ylim'][0] = data[-1]  # Adjust the lower limit
            properties['ylim'][1] = data[-1] + 10
        elif data[-1] > properties['ylim'][1]:
            properties['ylim'][0] = data[-1] - 10  # Adjust the upper limit
            properties['ylim'][1] = data[-1]

        # Set y-axis limits based on the updated limits
        line_plot.axes.set_ylim(properties['ylim'])
        line_plot.axes.set_yticks(properties['ylim'])
        
        # Set x-axis limits based on the data
        line_plot.axes.set_xlim(max(timestamps) - 10, max(timestamps))

        # Update xlabel with the latest value
        line_plot.axes.set_xlabel(f"{data[-1]:.2f} {properties['units']}")

        # Print all data values in the console
        print(f"{graph_type.capitalize()} values:", data)


def start_animation(canvas_widget, line_plot, timestamps, data, graph_type):
    # Use FuncAnimation for smooth animation
    ani = FuncAnimation(plt.gcf(), lambda frame: update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type), interval=1000)
    
    # Return the animation object to prevent deletion
    return ani


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sensor UI")

    # Create canvas for the diagram
    diagram_canvas = create_canvas(root, 800, 900)
    diagram_canvas.grid(row=0, column=0, padx=10, pady=10)

    # Create canvas for graphs/sensors
    graph_canvas = create_canvas(root, 480, 900)
    graph_canvas.grid(row=0, column=1, padx=10, pady=10)

    # Create temperature displays
    temp_sensor1 = create_sensor_display(graph_canvas, x=20, y=50, width=200, height=100, title="TS1", graph_type="temperature")
    temp_sensor3 = create_sensor_display(graph_canvas, x=20, y=200, width=200, height=100, title="TS3", graph_type="temperature")
    temp_sensor4 = create_sensor_display(graph_canvas, x=20, y=350, width=200, height=100, title="TS4", graph_type="temperature")
    temp_sensor5 = create_sensor_display(graph_canvas, x=20, y=500, width=200, height=100, title="TS5", graph_type="temperature")

    # Create pressure displays
    press_sensor2 = create_sensor_display(graph_canvas, x=250, y=50, width=200, height=100, title="PS2", graph_type="pressure")
    press_sensor3 = create_sensor_display(graph_canvas, x=250, y=200, width=200, height=100, title="PS3", graph_type="pressure")
    press_sensor1 = create_sensor_display(graph_canvas, x=250, y=350, width=200, height=100, title="PS1", graph_type="pressure")

    # Create load sensors
    load_sensor1 = create_sensor_display(graph_canvas, x=250, y=500, width=200, height=100, title="LS1&2", graph_type="load_sensor")

    # Create servo sensors
    servo2 = create_sensor_display(graph_canvas, x=250, y=650, width=200, height=100, title="Servo2", graph_type="servo")
    servo1 = create_sensor_display(graph_canvas, x=250, y=800, width=200, height=100, title="Servo1", graph_type="servo")

    # Rocket bodies
    upper = create_rect(diagram_canvas, 50, 100, 70, 450, fill_color="lightblue")
    lower = create_rect(diagram_canvas, 50, 550, 70, 750, fill_color="lightblue")
    middle = create_rect(diagram_canvas, 100, 500, 500, 490, fill_color="gray")

    load = create_rect(diagram_canvas, 65, 530, 70, 550, fill_color="gray")
    press_trans3 = create_rect(diagram_canvas, 50, 530, 55, 550, fill_color="gray")

    servo_middle = create_rect(diagram_canvas, 250, 500, 260, 520, fill_color="gray")
    press_trans1 = create_rect(diagram_canvas, 260, 470, 270, 490, fill_color="gray")
    fill_tank = create_rect(diagram_canvas, 500, 450, 520, 750, fill_color="lightblue")

    # Labels on the rocket diagram
    diagram_canvas.create_text(50, 325, text="TS1", anchor=tk.SW, font=('Arial', 8, 'bold'))
    diagram_canvas.create_text(20, 75, text="TS3", anchor=tk.SW, font=('Arial', 8, 'bold'))
    diagram_canvas.create_text(50, 600, text="TS4", anchor=tk.SW, font=('Arial', 8, 'bold'))
    diagram_canvas.create_text(50, 700, text="TS5", anchor=tk.SW, font=('Arial', 8, 'bold'))

    diagram_canvas.create_text(80, 75, text="PS2", anchor=tk.SW, font=('Arial', 8, 'bold'))
    diagram_canvas.create_text(20, 525, text="PS3", anchor=tk.SW, font=('Arial', 8, 'bold'))
    diagram_canvas.create_text(250, 450, text="PS1", anchor=tk.SW, font=('Arial', 8, 'bold'))

    diagram_canvas.create_text(80, 525, text="LS1&2", anchor=tk.SW, font=('Arial', 8, 'bold'))

    # Create servo sensors
    servo2 = create_sensor_display(diagram_canvas, x=45, y=465, width=200, height=100, title="Servo2", graph_type="servo")
    servo1 = create_sensor_display(diagram_canvas, x=250, y=525, width=200, height=100, title="Servo1", graph_type="servo")

    # Labels
    diagram_canvas.create_text(60, 770, text="ENGINE", anchor=tk.CENTER, font=('Arial', 12, 'bold'))
    diagram_canvas.create_text(260, 770, text="FILL STATION", anchor=tk.CENTER, font=('Arial', 12, 'bold'))
    diagram_canvas.create_text(510, 770, text="FILL TANK", anchor=tk.CENTER, font=('Arial', 12, 'bold'))

    # Show the Tkinter window
    root.mainloop()
