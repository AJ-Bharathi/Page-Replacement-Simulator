import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import random
from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement

# Animation control variables
paused = False
speed = 800  # Default speed
theme = "Classic"  # Default theme
page_faults = 0  # Track page faults

# Theme configurations
themes = {
    "1": ("Classic", {"bg": "white", "grid": "black", "text": "black"}),
    "2": ("Dark Mode", {"bg": "black", "grid": "white", "text": "white"}),
    "3": ("Cyberpunk", {"bg": "#1a1a2e", "grid": "#e94560", "text": "#0f3460"}),
    "4": ("Galaxy", {"bg": "#00001a", "grid": "#9999ff", "text": "#ffffff"}),
    "5": ("Steampunk", {"bg": "#3b2f2f", "grid": "#d4a017", "text": "#ffcc00"}),
    "6": ("Chromatic Bloom", {"bg": "#ffccff", "grid": "#ff66b2", "text": "#6600cc"}),
    "7": ("Aesthetic Purple", {"bg": "#2e004f", "grid": "#cc99ff", "text": "#f5ccff"})
}

# Function to get user input for theme selection
def get_user_choice():
    print("Choose a theme:")
    for num, (name, _) in themes.items():
        print(f"{num}. {name}")
    theme_choice = input("Enter theme number: ")
    return themes.get(theme_choice, themes["1"])  # Default to "Classic"

# Get theme selection from user
theme_name, theme_colors = get_user_choice()
theme = theme_name

# Get animation speed from user
speed_mapping = {"1": 1200, "2": 800, "3": 400}
print("\nChoose Animation Speed:")
print("1. Slow")
print("2. Normal")
print("3. Fast")
speed_choice = input("Enter speed number: ")
speed = speed_mapping.get(speed_choice, 800)  # Default to normal speed

# Get user inputs for page replacement simulation
try:
    reference_string = list(map(int, input("Enter reference sequence : ").split()))
    frame_size = int(input("Enter frame size: "))
    if not reference_string or frame_size <= 0:
        raise ValueError
except ValueError:
    print("Invalid input! Please enter a valid reference string and frame size.")
    exit(1)

# User selects the algorithm
print("Select Page Replacement Algorithm:")
print("1. FIFO\n2. LRU\n3. Optimal")
choice = input("Enter choice (1/2/3): ")

if choice == "1":
    algorithm = "FIFO"
    result = fifo_page_replacement(reference_string, frame_size)
elif choice == "2":
    algorithm = "LRU"
    result = lru_page_replacement(reference_string, frame_size)
elif choice == "3":
    algorithm = "Optimal"
    result = optimal_page_replacement(reference_string, frame_size)
else:
    print("Invalid choice. Defaulting to FIFO.")
    algorithm = "FIFO"
    result = fifo_page_replacement(reference_string, frame_size)

# Extract the frame states from the tuple
if isinstance(result, tuple) and len(result) == 2:
    page_faults, frame_states = result  # Extract only the frame states
else:
    frame_states = result  # Assume it's already in the correct format

# Debugging - Ensure frame_states is properly formatted
print("\nDebug: Checking frame states...")
if not frame_states or not isinstance(frame_states, list) or not all(isinstance(frame, list) for frame in frame_states):
    print("Error: Frame states are empty or improperly formatted.")
    print("Debug Info:", frame_states)  # Print for debugging
    exit(1)

print("Frame states loaded successfully!")

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Key press event handler
def on_key(event):
    global paused, ani, speed
    if event.key == ' ':  # Spacebar to pause/resume
        paused = not paused
    elif event.key == 'n' and paused:  # 'N' to step forward manually
        ani.event_source.stop()
        update(ani.frame_seq.next())
    elif event.key in speed_mapping:  # Speed controls
        speed = speed_mapping[event.key]
        ani.event_source.interval = speed

# Function to generate a random color for pages
def get_page_color(page):
    return "lightgrey" if page == " " else (random.random(), random.random(), random.random())

# Animation update function
def update(frame):
    global page_faults
    if paused:
        return
    
    ax.clear()
    ax.set_title(f"{algorithm} Page Replacement - {theme} Theme", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Frames")
    ax.set_xticks(range(len(reference_string)))
    ax.set_yticks(range(frame_size))
    ax.grid(True, linestyle='dotted', alpha=0.6, color=theme_colors["grid"])
    ax.set_facecolor(theme_colors["bg"])
    
    current_frame = frame_states[frame] if frame < len(frame_states) else [" "] * frame_size
    prev_frame = frame_states[frame - 1] if frame > 0 else [" "] * frame_size

    # Make sure prev_frame is always the same length as frame_size
    while len(prev_frame) < frame_size:
        prev_frame.append(" ")

    # Draw frames with color coding
    for i in range(frame_size):
        page = current_frame[i] if i < len(current_frame) else " "
        color = get_page_color(page)
        ax.text(frame, i, str(page), fontsize=12, ha='center', va='center',
                bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.3'))
        
        if frame > 0 and i < len(prev_frame) and prev_frame[i] != page:
            ax.plot([frame - 1, frame], [i, i], 'r-o', linewidth=2)
            page_faults += 1
        else:
            ax.plot([frame - 1, frame], [i, i], 'g-o', linewidth=2)
    
    ax.text(0, frame_size + 0.5, f"Page Faults: {page_faults}", fontsize=12, fontweight='bold', color='red')
    plt.show()

# Set up animation
ani = animation.FuncAnimation(fig, update, frames=len(frame_states), interval=speed, repeat=False)

# Connect key events
fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()