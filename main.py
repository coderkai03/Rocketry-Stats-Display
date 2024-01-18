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
    },
    'servo': {
        'color': 'gray',  # or any color you prefer
        'ylabel': '',  # No need for ylabel in servo type
        'yticks': [],  # No need for yticks in servo type
        'units': ''  # No need for units in servo type
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

    # Create title under the circle
    title = canvas.create_text(x + diameter / 8, y + diameter / 4 - 40, text=title, anchor=tk.CENTER, font=('Arial', 10, 'bold'))

    return circle, label

def create_sensor_display(canvas, x, y, width, height, title, graph_type, diagram, label):
    if graph_type == "servo":
        # Create servo components directly without a graph
        servo_components = create_servo(canvas, x, y, diameter=100, title=title, initial_state=True)
        return (*servo_components, None)  # Returning None for animation

    # For other sensor types, create the graph and start animation
    canvas_widget, line_plot, timestamps, data = create_graph(canvas, x, y, width, height, title, graph_type)
    ani = start_graph_animation(canvas_widget, line_plot, timestamps, data, graph_type, diagram, label)

    return canvas_widget, line_plot, timestamps, data, ani


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

def update_servo_state(frame, canvas, circle, label):
    # Toggle the servo state (change color and label)
    current_color = canvas.itemcget(circle, 'fill')
    new_state = current_color == 'red'
    color = 'green' if new_state else 'red'
    canvas.itemconfig(circle, fill=color)
    canvas.itemconfig(label, text="OPEN" if new_state else "CLOSED")
    return new_state


servo_states = {"servo1": True, "servo2": True}

def update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type, diagram, label):
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

        label_text = diagram.itemcget(label, "text")
        diagram.itemconfig(label, text=f'{label_text[0:3]}\n{data[-1]} {graph_properties[graph_type]["units"]}')

        
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


def start_graph_animation(canvas_widget, line_plot, timestamps, data, graph_type, diagram, label):
    # Use FuncAnimation for smooth animation
    ani = FuncAnimation(plt.gcf(), lambda frame: update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type, diagram, label), interval=1000)
    
    # Return the animation object to prevent deletion
    return ani

def start_servo_animation(canvas_widget, circle, label):
    # Use FuncAnimation for smooth animation
    ani = FuncAnimation(plt.gcf(), lambda frame: update_servo_state(frame, canvas_widget, circle, label), interval=500)
    
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

    # Labels on the rocket diagram
    ts1_text = diagram_canvas.create_text(100, 325, text="TS1", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ts3_text = diagram_canvas.create_text(20, 75, text="TS3", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ts4_text = diagram_canvas.create_text(120, 620, text="TS4", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ts5_text = diagram_canvas.create_text(120, 720, text="TS5", anchor=tk.SW, font=('Arial', 8, 'bold'))

    ps2_text = diagram_canvas.create_text(80, 75, text="PS2", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ps3_text = diagram_canvas.create_text(10, 550, text="PS3", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ps1_text = diagram_canvas.create_text(250, 450, text="PS1", anchor=tk.SW, font=('Arial', 8, 'bold'))

    ls1_text = diagram_canvas.create_text(120, 530, text="LS1", anchor=tk.SW, font=('Arial', 8, 'bold'))
    ls2_text = diagram_canvas.create_text(120, 570, text="LS2", anchor=tk.SW, font=('Arial', 8, 'bold'))

    # Create temperature displays
    temp_sensor1 = create_sensor_display(graph_canvas, x=20, y=50, width=200, height=100, title="Temp Sensor 1", graph_type="temperature", diagram=diagram_canvas, label=ts1_text)
    temp_sensor3 = create_sensor_display(graph_canvas, x=20, y=200, width=200, height=100, title="Temp Sensor 3", graph_type="temperature", diagram=diagram_canvas, label=ts3_text)
    temp_sensor4 = create_sensor_display(graph_canvas, x=20, y=350, width=200, height=100, title="Temp Sensor 4", graph_type="temperature", diagram=diagram_canvas, label=ts4_text)
    temp_sensor5 = create_sensor_display(graph_canvas, x=20, y=500, width=200, height=100, title="Temp Sensor 5", graph_type="temperature", diagram=diagram_canvas, label=ts5_text)

    # Create pressure displays
    press_sensor2 = create_sensor_display(graph_canvas, x=250, y=50, width=200, height=100, title="Press Sensor 2", graph_type="pressure", diagram=diagram_canvas, label=ps2_text)
    press_sensor3 = create_sensor_display(graph_canvas, x=250, y=200, width=200, height=100, title="Press Sensor 3", graph_type="pressure", diagram=diagram_canvas, label=ps3_text)
    press_sensor1 = create_sensor_display(graph_canvas, x=250, y=350, width=200, height=100, title="Press Sensor 1", graph_type="pressure", diagram=diagram_canvas, label=ps1_text)

    # Create load sensors
    load_sensor1 = create_sensor_display(graph_canvas, x=250, y=500, width=200, height=100, title="Load Sensor 1", graph_type="load_sensor", diagram=diagram_canvas, label=ls1_text)
    load_sensor2 = create_sensor_display(graph_canvas, x=250, y=650, width=200, height=100, title="Load Sensor 2", graph_type="load_sensor", diagram=diagram_canvas, label=ls2_text)
    
    # Rocket bodies
    upper = create_rect(diagram_canvas, 30, 100, 90, 450, fill_color="lightblue")
    lower = create_rect(diagram_canvas, 30, 580, 90, 750, fill_color="lightblue")
    middle = create_rect(diagram_canvas, 100, 500, 500, 490, fill_color="gray")

    #temp sensor dots
    temp_sensor1_indicator = diagram_canvas.create_oval(60, 300, 70, 310, outline='black', width=2, fill='black')
    temp_sensor4_indicator = diagram_canvas.create_oval(60, 600, 70, 610, outline='black', width=2, fill='black')
    temp_sensor5_indicator = diagram_canvas.create_oval(60, 700, 70, 710, outline='black', width=2, fill='black')

    load = create_rect(diagram_canvas, 65, 530, 70, 550, fill_color="pink")
    press_trans3 = create_rect(diagram_canvas, 50, 530, 55, 550, fill_color="gray")
    ps2_rect = create_rect(diagram_canvas, 80, 80, 90, 100, fill_color='gray')

    press_trans1 = create_rect(diagram_canvas, 260, 470, 270, 490, fill_color="gray")
    fill_tank = create_rect(diagram_canvas, 480, 450, 540, 750, fill_color="lightblue")

    # Create servo sensors
    servo2 = create_servo(graph_canvas, x=200, y=800, diameter=100, title="Servo2", initial_state=True)
    servo1 = create_servo(graph_canvas, x=300, y=800, diameter=100, title="Servo1", initial_state=True)

    # Create servo sensors
    dservo2 = create_servo(diagram_canvas, x=50, y=480, diameter=100, title="Servo2", initial_state=True)
    dservo1 = create_servo(diagram_canvas, x=200, y=440, diameter=100, title="Servo1", initial_state=True)

    # Start servo animation
    ani_servo1 = start_servo_animation(graph_canvas, *servo1)
    ani_servo2 = start_servo_animation(graph_canvas, *servo2)

    # Start servo animation
    dani_servo1 = start_servo_animation(diagram_canvas, *dservo1)
    dani_servo2 = start_servo_animation(diagram_canvas, *dservo2)

    # Labels
    diagram_canvas.create_text(60, 770, text="ENGINE", anchor=tk.CENTER, font=('Arial', 12, 'bold'))
    diagram_canvas.create_text(260, 770, text="FILL STATION", anchor=tk.CENTER, font=('Arial', 12, 'bold'))
    diagram_canvas.create_text(510, 770, text="FILL TANK", anchor=tk.CENTER, font=('Arial', 12, 'bold'))

    # Show the Tkinter window
    root.mainloop()
