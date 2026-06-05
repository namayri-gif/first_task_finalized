# Part 1: ROS2 Publisher and Subscriber Package
## Project Description

This project was developed using ROS2 Jazzy and Python. The goal was to understand the fundamentals of ROS2 communication by creating a custom publisher node and subscriber node that exchange messages through ROS topics.

## What Was Built and Why

A ROS2 package named `my_first_package` was created containing:
* `simple_publisher.py`
* `simple_subscriber.py`
The publisher node continuously publishes messages to a ROS topic, while the subscriber node listens to the same topic and displays the received messages.
This task was completed to gain hands on experience with:
* ROS2 nodes
* Topics
* Publishers and subscribers
* Package creation and building using `colcon`

## What I Learned

Through this task, I learned:
* How ROS2 nodes communicate using topics
* How to create Python based ROS2 packages
* How to build a workspace using `colcon build`
* How to source a ROS2 workspace
* How to run publisher and subscriber nodes
* Basic ROS2 command line tools for debugging and monitoring topics


## Setups and Creation:
<img width="973" height="573" alt="image" src="https://github.com/user-attachments/assets/fa1f2abc-c5a5-47c9-b0db-c53d0dbe9bf6" />
<img width="942" height="276" alt="image" src="https://github.com/user-attachments/assets/81f2cf05-5495-4bbe-a44a-099dec97ded4" />

## Running Publisher and Subscriber
<img width="894" height="694" alt="image" src="https://github.com/user-attachments/assets/8c9932ba-ec4e-4b89-97d7-b474c6124520" />
<img width="1169" height="664" alt="image" src="https://github.com/user-attachments/assets/0590dbd4-c5fa-47d2-b32b-1fbea7252e0a" />


# Part 2: TurtleBot3 Control Topics

## Project Description
This task focused on understanding how TurtleBot3 receives motion commands in ROS2. The main objective was to identify the velocity control topic and test manual movement commands using ROS2 command line tools.

## What Was Built and Why
In this task, the TurtleBot3 motion control topic was tested using the `/cmd_vel` topic. This topic is used to send velocity commands to the robot.
The velocity command uses the `geometry_msgs/msg/Twist` message type, which contains:
* Linear velocity
* Angular velocity

  
This was done to understand how the robot moves forward, backward, and rotates inside the Gazebo simulator.

[In this part, no additions and changes where made to the code so no pictures to be attached]
## What I Learned

Through this task, I learned:

* TurtleBot3 is controlled through the `/cmd_vel` topic
* `Twist` messages are used to control robot velocity
* `linear.x` controls forward and backward movement
* `angular.z` controls left and right rotation
* ROS2 topics can be inspected using `ros2 topic list` and `ros2 topic info`
* Manual commands can be published using `ros2 topic pub`

## Useful Commands

### List ROS2 Topics
```bash
ros2 topic list
```
### Check the Control Topic
```bash
ros2 topic info /cmd_vel
```
### Move TurtleBot3 Forward
```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}"
```
### Rotate TurtleBot3
```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.5}}"
```
### Stop TurtleBot3
```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

# part 3: ROS2 Keyboard Teleoperation Node

A custom ROS2 node that reads keyboard input and publishes velocity commands to control a TurtleBot3 robot in the Gazebo simulator.
Along with a launch packae for controlling TurtleBot3 robot in Gazebo simulator with Rviz visualization
---
# Package 1: keyboard_teleop
## Overview

This package implements a keyboard teleoperation node for ROS2, inspired by the [`teleop_twist_keyboard`](https://github.com/ros2/teleop_twist_keyboard) package. It maps WASD and arrow keys to `geometry_msgs/Twist` messages published on the `/cmd_vel` topic, with an emergency stop triggered by the spacebar.

---

## Features

- WASD and arrow key control (forward, backward, rotate left/right)
- Publishes `Twist` messages to `/cmd_vel` at 10 Hz
- Emergency stop on `SPACE` — instantly zeroes all velocity
- Release-to-stop behaviour — robot stops when no key is held
- Clean shutdown on `Q` or `Ctrl+C`
- Tested with TurtleBot3 Burger in Gazebo simulator
- Fully commented source code

---

## Key Bindings

| Key | Action |
|-----|--------|
| `W` / `↑` | Move forward |
| `S` / `↓` | Move backward |
| `A` / `←` | Rotate left |
| `D` / `→` | Rotate right |
| `SPACE` | Emergency stop |
| `Q` | Quit node |

## Installation

```bash
# Navigate to your ROS2 workspace source folder
cd ~/ros2_ws/src

# Create the package (if starting fresh)
ros2 pkg create --build-type ament_python keyboard_teleop

# Copy keyboard_teleop_node.py into keyboard_teleop/keyboard_teleop/

# Build
cd ~/ros2_ws
colcon build --packages-select keyboard_teleop
source install/setup.bash
```

---

## Usage

### 1. Launch TurtleBot3 in Gazebo

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### 2. Run the teleoperation node (separate terminal)

```bash
source ~/ros2_ws/install/setup.bash
ros2 run keyboard_teleop keyboard_teleop
```

### 3. Verify it's working (optional, separate terminal)

```bash
# Watch velocity commands being published
ros2 topic echo /cmd_vel

# Watch robot odometry changing
ros2 topic echo /odom
```

> **Important:** The terminal running the teleop node must be active/focused for key input to register.

---

## How It Works

### Node Architecture

```
Keyboard Input (background thread)
        │
        ▼
  get_key() — raw terminal read (termios)
        │
        ▼
  KEY_BINDINGS dict — maps key → (linear_x, angular_z)
        │
        ▼
  Velocity state (_linear_x, _angular_z)
        │
        ▼
  Timer callback (10 Hz) — builds and publishes Twist msg
        │
        ▼
  /cmd_vel topic → TurtleBot3
```

### Key Concepts

**Twist message** — the standard ROS2 velocity command type. This node uses:
- `linear.x` — forward/backward speed in m/s
- `angular.z` — rotation speed in rad/s

All other fields stay at `0.0` since TurtleBot3 is a differential-drive (2D) robot.

**Threading** — keyboard reading runs in a daemon thread so it never blocks the ROS2 spin loop. The timer publishes velocity independently at 10 Hz.

**Emergency stop** — pressing `SPACE` publishes a zero `Twist` immediately, bypassing the timer, for an instant stop.

**Release-to-stop** — if no key is detected within 0.1 seconds, velocity is zeroed automatically. This prevents the robot from continuing if the terminal loses focus.

---

## Velocity Settings

Tuned for TurtleBot3 Burger:

| Parameter | Value |
|-----------|-------|
| Linear speed | 0.22 m/s |
| Angular speed | 1.5 rad/s |

These can be adjusted at the top of `keyboard_teleop_node.py`.

---

## Verification

Robot movement was verified by monitoring `/odom` and `/cmd_vel` topics. Position and orientation values in `/odom` updated in response to keyboard input, and `/cmd_vel` showed correct `linear.x` and `angular.z` values matching the expected velocity constants. It was also tested and ran on Gazebo 3D simulator

---
# Package 2: my_robot_launch

## Overview 
This package provides a launch file that starts the `robot_state_publisher` and opens RViz2 with a custom configuration. It is designed to work alongside the `keyboard_teleop` package to give a full teleoperation and visualization setup for TurtleBot3 Burger.

---
## Features

Launches `robot_state_publisher` with TurtleBot3 Burger URDF
Opens RViz2 automatically with a pre-configured view
Fixed Frame set to `odom`
Displays the 3D robot model
Visualises LiDAR data from `/scan`
Single command to bring up the full visualization stack

Package Structure
```
my_robot_launch/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── robot_launch.py
└── rviz/
    └── robot_config.rviz
```
---

### Requirements
ROS2 Jazzy
`robot_state_publisher`
`rviz2`
`launch_ros`
TurtleBot3 packages

---
### Installation
```bash
# Navigate to your ROS2 workspace source folder
cd ~/ros2_ws/src

# Create the package (if starting fresh)
ros2 pkg create --build-type ament_cmake my_robot_launch

# Add the launch/ and rviz/ folders with the provided files

# Build
cd ~/ros2_ws
colcon build --packages-select my_robot_launch
source install/setup.bash
```
---
### Usage
1. Launch RViz and robot state publisher
```bash
ros2 launch my_robot_launch robot_launch.py
```
2. Run the teleop node (separate terminal)
```bash
source ~/ros2_ws/install/setup.bash
ros2 run keyboard_teleop keyboard_teleop
```
> **Important:** The teleop node must be run in its own terminal since it requires an interactive keyboard input session.
---
How It Works
What the Launch File Does
```
robot_launch.py
      │
      ├── robot_state_publisher  ← loads TurtleBot3 URDF, publishes /robot_description
      │
      └── rviz2                  ← opens with robot_config.rviz pre-loaded
```
RViz Configuration
The `robot_config.rviz` file configures RViz2 with:
Setting	Value
Fixed Frame	`odom`
RobotModel topic	`/robot_description`
LaserScan topic	`/scan`

**Note:** The instruction given asked for PointCould2 sensor but this does not capture the 2D vision for the LaserScan. Thus, it was replaced by the LaserScan

---
### Verification

Once launched, RViz should display the TurtleBot3 robot model. When the teleop node is running in a separate terminal and Gazebo is active, the LiDAR scan points will appear around the robot and update in real time as it moves.

The robot_launch.py gave an error code indicating that a package for the motor_driver is missing (Package was not provided in the material and not provided in the complete example)
<img width="1212" height="160" alt="image" src="https://github.com/user-attachments/assets/4b02bcc5-ab52-4a6d-8d95-0c03800f578f" />

The Rviz file, when launched separately, was successful and showed the 2D expected demonstration. 
<img width="1256" height="838" alt="Screenshot 2026-06-05 105432" src="https://github.com/user-attachments/assets/a170203c-6823-4e40-b446-ea3411dba60d" />


