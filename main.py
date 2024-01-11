import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random

# Global vars
directions = {
    'left': [-100, 0, -250, 0],
    'right': [100, 0, 125, 0],
    'down': [35, 50, -35, 125],
    'up': [35, -50, -35, -125],
    'up_left': [-50, -50, -200, -100],
    'up_right': [100, -50, 150, -150],
    'down_left': [-50, 50, -200, 125],
    'down_right': [100, 50, 100, 100]
}


graph_properties = {
    'temperature': {
        'color': 'blue',
        'ylabel': 'Temp (F)',
        'yticks': [60, 80],
        'ylim': [60, 80]
    },
    'pressure': {
        'color': 'red',
        'ylabel': 'Press (psi)',
        'yticks': [50, 150],
        'ylim': [50, 150]
    },
    'load_sensor': {
        'color': 'green',
        'ylabel': 'Load (lb)',
        'yticks': [0, 100],
        'ylim': [0, 100]
    }
}

def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height, bg='white')
    canvas.pack()
    return canvas

def create_sensor_display(canvas, x, y, width, height, title, graph_type, direction):
    # Create graph with transparent background
    canvas_widget, line_plot, timestamps, data = create_graph(canvas, x, y, width, height, title, graph_type)

    # Create display (arrow and caption)
    arrow = create_arrow(canvas, x + 80, y + height / 2, x + 150, y + height / 2, direction)

    # Start updating the graph using FuncAnimation
    ani = start_animation(canvas_widget, line_plot, timestamps, data, graph_type)

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

# Rest of the code remains unchanged


def create_rect(canvas, x, y, width, height, fill_color):
    rectangle = canvas.create_rectangle(x, y, width, height, fill=fill_color)
    return rectangle

def create_arrow(canvas, x1, y1, x2, y2, direction):
    # Create horizontal arrow
    arrow = canvas.create_line(
        x1 + directions[direction][0],
        y1 + directions[direction][1],
        x2 + directions[direction][2],
        y2 + directions[direction][3],
        arrow=tk.LAST,
        width=2
    )

    return arrow

def update_graph(frame, canvas_widget, line_plot, timestamps, data, graph_type):
    # Generate a new data point
    new_data = random.uniform(0, 100) if graph_type == "pressure" else random.uniform(65, 75)

    # Append the new data to the list
    timestamps.append(timestamps[-1] + 1)
    data.append(new_data)

    # Update the line plot with the new data
    line_plot.set_data(timestamps, data)

    # Set x-axis limits based on the data
    line_plot.axes.set_xlim(max(timestamps) - 10, max(timestamps))

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

    canvas = create_canvas(root, 1280, 900)

    # Create temperature displays
    temp_sensor1 = create_sensor_display(canvas, x=450, y=200, width=200, height=100, title="Temp Sensor (1)", graph_type="temperature", direction='left')
    temp_sensor3 = create_sensor_display(canvas, x=20, y=50, width=200, height=100, title="Temp Sensor (3)", graph_type="temperature", direction='right')
    temp_sensor4 = create_sensor_display(canvas, x=20, y=550, width=200, height=100, title="Temp Sensor (4)", graph_type="temperature", direction='right')
    temp_sensor5 = create_sensor_display(canvas, x=20, y=650, width=200, height=100, title="Temp Sensor (5)", graph_type="temperature", direction='right')

    # Create pressure displays
    press_sensor2 = create_sensor_display(canvas, x=450, y=50, width=200, height=100, title="Press Sensor (2)", graph_type="pressure", direction='left')
    press_sensor3 = create_sensor_display(canvas, x=50, y=385, width=200, height=100, title="Press Sensor (3)", graph_type="pressure", direction='down_right')
    press_sensor1 = create_sensor_display(canvas, x=760, y=295, width=200, height=100, title="Press Sensor (1)", graph_type="pressure", direction='down_left')

    # Create load sensors
    load_sensor1 = create_sensor_display(canvas, x=375, y=600, width=200, height=100, title="Load Sensor (1&2)", graph_type="load_sensor", direction='up_left')

    # create servo sensors
    servo2 = create_sensor_display(canvas, x=365, y=325, width=200, height=100, title="Servo (2)", graph_type="pressure", direction='down_left')
    servo1 = create_sensor_display(canvas, x=750, y=575, width=200, height=100, title="Servo (1)", graph_type="pressure", direction='up_left')

    # rocket bodies
    upper = create_rect(canvas, 300, 100, 320, 450, fill_color="lightblue")
    lower = create_rect(canvas, 300, 550, 320, 750, fill_color="lightblue")
    middle = create_rect(canvas, 350, 500, 1000, 490, fill_color="gray")
    
    load = create_rect(canvas, 315, 530, 320, 550, fill_color="gray")
    press_trans3 = create_rect(canvas, 300, 530, 305, 550, fill_color="gray")
    servo = create_rect(canvas, 308, 490, 312, 510, fill_color="gray")

    servo_middle = create_rect(canvas, 700, 500, 710, 520, fill_color="gray")
    press_trans1 = create_rect(canvas, 710, 470, 720, 490, fill_color="gray")

    # Show the Tkinter window
    root.mainloop()

#temp        = *F     = 60 -50 < y < 80 +50
#pressure    = psi    = 50 -50 < y < 150 +50
#servo       = on/off = green/red
#load sensor = lbs    = 0 - 50 < y 100 +50
    
# ON
#  *
    
# OFF
#  *