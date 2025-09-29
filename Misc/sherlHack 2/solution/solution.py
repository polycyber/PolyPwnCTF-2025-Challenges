import math
import time
import matplotlib.pyplot as plt

# Information provided in the challenge

# [29 MAR 2025 21:34:00]
# COORDINATES LANDMARKS A (45.50394422783684, -73.62675236294805) — AZIMUTH 30.04°
# COORDINATES LANDMARKS B (45.52688057562694, -73.53571295727556) — AZIMUTH 47.45°

# [29 MAR 2025 21:36:10]
# COORDINATES LANDMARKS A (45.50394422783684, -73.62675236294805) — AZIMUTH 328.35°
# COORDINATES LANDMARKS B (45.52688057562694, -73.53571295727556) — AZIMUTH 28.26°

# Bomb dropping time: 21:40:00

# Define constants
R = 6371000  # Radius of the Earth in meters

# Coordinates of landmarks in degrees
landmark1_lat_deg = 45.50394422783684
landmark1_lon_deg = -73.62675236294805
landmark2_lat_deg = 45.52688057562694
landmark2_lon_deg = -73.53571295727556

# Convert coordinates to radians
lat1 = math.radians(landmark1_lat_deg)
lon1 = math.radians(landmark1_lon_deg)
lat2 = math.radians(landmark2_lat_deg)
lon2 = math.radians(landmark2_lon_deg)

# Reference point (origin)
lat0, lon0 = lat1, lon1

# Calculate differences for cartesian coordinates
dx = R * (lon2 - lon1) * math.cos(lat0)
dy = R * (lat2 - lat1)

# Landmarks in cartesian coordinates
landmark1 = (0, 0)
landmark2 = (dx, dy)

print(f"Landmark 1 is at {landmark1}")
print(f"Landmark 2 is at {landmark2}")

# Define times
T1 = time.mktime(time.strptime("29 MAR 2025 21:34:00", "%d %b %Y %H:%M:%S"))
T2 = time.mktime(time.strptime("29 MAR 2025 21:36:10", "%d %b %Y %H:%M:%S"))
TBOMB = time.mktime(time.strptime("29 MAR 2025 21:40:00", "%d %b %Y %H:%M:%S"))

# Time differences in seconds
T1_rel = 0  # Reference time
T2_rel = T2 - T1
TBOMB_rel = TBOMB - T1

# Azimuth angles
azimuth_land1_t1 = 30.04
azimuth_land2_t1 = 47.45
azimuth_land1_t2 = 328.35
azimuth_land2_t2 = 28.26

def carthesian_to_gps(x, y):
    dx_new, dy_new = x, y
    # Convert local (dx, dy) back to GPS (latitude, longitude)
    lon_new = lon0 + (dx_new / (R * math.cos(lat0)))
    lat_new = lat0 + (dy_new / R)

    # Convert radians to degrees
    lat_new_deg = math.degrees(lat_new)
    lon_new_deg = math.degrees(lon_new)

    return lat_new_deg, lon_new_deg

###############################################################
################## At Time T1 #################################
###############################################################

# Calculate the slopes of the lines
# tan(theta) = dy/dx
dx_on_dy_1_t1 = math.tan(math.radians(90 - azimuth_land1_t1))
dx_on_dy_2_t1 = math.tan(math.radians(90 - azimuth_land2_t1))

# Calculate the y-intercepts
# y = ax + b => b = y - ax
y_intercept1_t1 = landmark1[1] - dx_on_dy_1_t1 * landmark1[0]
y_intercept2_t1 = landmark2[1] - dx_on_dy_2_t1 * landmark2[0]

# Calculate the intersection point
# ax + b = cx + d => x = (d - b) / (a - c)
x_t1 = (y_intercept2_t1 - y_intercept1_t1) / (dx_on_dy_1_t1 - dx_on_dy_2_t1)
y_t1 = dx_on_dy_1_t1 * x_t1 + y_intercept1_t1
plane_t1 = (x_t1, y_t1)

print(f"Plane position at T1: {plane_t1} or {carthesian_to_gps(x_t1, y_t1)}")

###############################################################
################## At Time T2 #################################
###############################################################

# Calculate the slopes of the lines
# tan(theta) = dy/dx
dx_on_dy_1_t2 = math.tan(math.radians(90 - azimuth_land1_t2))
dx_on_dy_2_t2 = math.tan(math.radians(90 - azimuth_land2_t2))

# Calculate the y-intercepts
# y = ax + b => b = y - ax
y_intercept1_t2 = landmark1[1] - dx_on_dy_1_t2 * landmark1[0]
y_intercept2_t2 = landmark2[1] - dx_on_dy_2_t2 * landmark2[0]

# Calculate the intersection point
# ax + b = cx + d => x = (d - b) / (a - c)
x_t2 = (y_intercept2_t2 - y_intercept1_t2) / (dx_on_dy_1_t2 - dx_on_dy_2_t2)
y_t2 = dx_on_dy_1_t2 * x_t2 + y_intercept1_t2
plane_t2 = (x_t2, y_t2)

print(f"Plane position at T2: {plane_t2} or {carthesian_to_gps(x_t2, y_t2)}")

###############################################################
################## At Time BOMB ###############################
###############################################################

# Calculate the distance and speed
distance = math.hypot(x_t2 - x_t1, y_t2 - y_t1)
time_interval = T2_rel - T1_rel

# Calculate total time from T1 to TBOMB
total_time = TBOMB_rel - T1_rel

# Calculate the plane's position at TBOMB
ratio = total_time / time_interval
x_bomb = x_t1 + (x_t2 - x_t1) * ratio
y_bomb = y_t1 + (y_t2 - y_t1) * ratio
plane_bomb = (x_bomb, y_bomb)

print(f"Plane position at TBOMB: {plane_bomb} or {carthesian_to_gps(x_bomb, y_bomb)}")

# Alternative method :
speed = distance / time_interval
distance_bomb = speed * (TBOMB_rel - T1_rel)
sin_angle = (y_t2 - y_t1) / distance
cos_angle = (x_t2 - x_t1) / distance
x_bomb_2 = x_t1 + distance_bomb * cos_angle
y_bomb_2 = y_t1 + distance_bomb * sin_angle

assert math.isclose(x_bomb, x_bomb_2, rel_tol=1e-9)
assert math.isclose(y_bomb, y_bomb_2, rel_tol=1e-9)

###############################################################
################## Plotting ###################################
###############################################################

import matplotlib.pyplot as plt

# Determine plot limits
all_x = [landmark1[0], landmark2[0], plane_t1[0], plane_t2[0], plane_bomb[0]]
all_y = [landmark1[1], landmark2[1], plane_t1[1], plane_t2[1], plane_bomb[1]]
x_min = min(all_x) - 3000
x_max = max(all_x) + 3000
y_min = min(all_y) - 3000
y_max = max(all_y) + 3000

# Function to plot azimuth lines
def plot_azimuth_line(landmark, azimuth_deg, label):
    angle_rad = math.radians(90 - azimuth_deg)
    x0, y0 = landmark
    L = math.hypot(x_max - x_min, y_max - y_min) * 1.5  # Extend beyond plot limits
    
    x1 = x0 + L * math.cos(angle_rad)
    y1 = y0 + L * math.sin(angle_rad)
    x2 = x0 - L * math.cos(angle_rad)
    y2 = y0 - L * math.sin(angle_rad)
    
    plt.plot([x1, x2], [y1, y2], linestyle='--', label=label)

# Function to plot heading and north at each plane point
def plot_heading_and_north(x, y):
    # Length of the arrows
    arrow_length = 5000  # Adjust as needed
    
    # North arrow (pointing upwards)
    plt.arrow(x, y, 0, arrow_length, head_width=500, head_length=1000, fc='k', ec='k')
    plt.text(x, y + arrow_length + 1000, 'N', ha='center', va='bottom', fontsize=12)

# Create plot
plt.figure(figsize=(12, 10))

# Plot landmarks
plt.scatter(*landmark1, color='red', s=100, label='Landmark 1')
plt.scatter(*landmark2, color='blue', s=100, label='Landmark 2')

# Plot plane positions
plt.scatter(*plane_t1, color='green', s=100, label='Plane at T1')
plt.scatter(*plane_t2, color='purple', s=100, label='Plane at T2')
plt.scatter(*plane_bomb, color='orange', s=100, label='Plane at TBOMB')

# Plot azimuth lines at T1
plot_azimuth_line(landmark1, azimuth_land1_t1, 'Azimuth from Landmark 1 at T1')
plot_azimuth_line(landmark2, azimuth_land2_t1, 'Azimuth from Landmark 2 at T1')

# Plot azimuth lines at T2
plot_azimuth_line(landmark1, azimuth_land1_t2, 'Azimuth from Landmark 1 at T2')
plot_azimuth_line(landmark2, azimuth_land2_t2, 'Azimuth from Landmark 2 at T2')

# Plot plane's trajectory
plt.plot([plane_t1[0], plane_t2[0], plane_bomb[0]],
         [plane_t1[1], plane_t2[1], plane_bomb[1]],
         color='black', linestyle='-', linewidth=2, label='Plane Path')

# Plot heading and north at each plane point
plot_heading_and_north(plane_t1[0], plane_t1[1])
plot_heading_and_north(plane_t2[0], plane_t2[1])
plot_heading_and_north(plane_bomb[0], plane_bomb[1])

# Labels and legend
plt.xlabel('X Coordinate (meters)', fontsize=14)
plt.ylabel('Y Coordinate (meters)', fontsize=14)
plt.title('Plane Position and Azimuths Over Time', fontsize=16)
plt.legend(fontsize=12, loc='upper left')
plt.grid(True)
plt.axis('equal')

# Adjust plot limits for readability
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Show plot
plt.savefig("./solution/visualisation.png")
