# MuJoCo Robotic Arm Simulation

A sophisticated robotic arm simulation with gripper functionality built using MuJoCo physics engine. This project demonstrates object manipulation, inverse kinematics, and interactive control of a multi-joint robotic arm.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![MuJoCo](https://img.shields.io/badge/mujoco-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **4-DOF Robotic Arm**: Shoulder pan, shoulder lift, elbow, and wrist rotation joints
- **Parallel Gripper**: Two-finger gripper with position control
- **Object Manipulation**: Pick and place demonstration with multiple objects (cube, sphere, cylinder)
- **Inverse Kinematics**: Simplified IK solver for target position reaching
- **Interactive Control**: Real-time keyboard control with visualization
- **Physics Simulation**: Accurate dynamics, contacts, and friction using MuJoCo

## Demo

The simulation includes:
- Automated pick-and-place sequences
- Interactive manual control
- Multiple graspable objects with different geometries
- Real-time visualization with adjustable camera views

## Requirements

- Python 3.8 or higher
- MuJoCo 3.0 or higher
- NumPy
- GLFW (for visualization)
- Matplotlib (optional, for plotting)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/mujoco-robotic-arm.git
cd mujoco-robotic-arm
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import mujoco; print(f'MuJoCo version: {mujoco.__version__}')"
```

## Usage

### Basic Simulation

Run the automated pick-and-place demonstration:

```bash
python robotic_arm_sim.py
```

This will:
1. Initialize the robotic arm simulation
2. Demonstrate picking up a cube, sphere, and cylinder
3. Place each object at different target locations
4. Print progress information to the console

### Interactive Demo

Launch the interactive visualization with keyboard controls:

```bash
python interactive_demo.py
```

**Keyboard Controls:**

| Key | Action |
|-----|--------|
| `Q` / `W` | Rotate shoulder pan left/right |
| `A` / `S` | Move shoulder lift up/down |
| `Z` / `X` | Bend/extend elbow |
| `E` / `R` | Rotate wrist left/right |
| `G` / `H` | Open/close gripper |
| `SPACE` or `HOME` | Return to home position |
| `D` | Run automated demo sequence |
| `P` | Print current arm state |
| `ESC` | Exit simulation |

### Programmatic Usage

You can also use the simulation in your own Python scripts:

```python
from robotic_arm_sim import RoboticArmSimulation, calculate_ik_simplified
import numpy as np

# Initialize simulation
sim = RoboticArmSimulation()

# Set joint angles directly
sim.set_joint_angles(
    shoulder_pan=0.5,
    shoulder_lift=-0.3,
    elbow=0.8,
    wrist_rotate=0.0
)

# Control gripper (0.0 = closed, 1.0 = open)
sim.set_gripper(0.5)

# Step simulation
sim.step(steps=1000)

# Get object position
cube_pos = sim.get_object_position('cube')
print(f"Cube position: {cube_pos}")

# Calculate inverse kinematics
target_pos = np.array([0.4, 0.2, 0.15])
joint_angles = calculate_ik_simplified(target_pos)
sim.set_joint_angles(*joint_angles)

# Render frame
image = sim.render(width=1280, height=720)
```

## Project Structure

```
mujoco-robotic-arm/
├── models/
│   └── robotic_arm.xml          # MuJoCo model definition
├── robotic_arm_sim.py           # Main simulation class and demos
├── interactive_demo.py          # Interactive visualization
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore patterns
```

## Model Architecture

### Robotic Arm Specifications

- **Base**: Fixed cylinder platform
- **Link 1 (Shoulder)**: 0.3m length, revolute joint (pan)
- **Link 2 (Upper Arm)**: 0.4m length, revolute joint (lift)
- **Link 3 (Forearm)**: 0.3m length, revolute joint (elbow)
- **Wrist**: Revolute joint for rotation
- **Gripper**: Parallel jaw with 0.04m maximum opening

### Joint Ranges

| Joint | Range | Description |
|-------|-------|-------------|
| Shoulder Pan | -180° to 180° | Base rotation |
| Shoulder Lift | -90° to 90° | Vertical arm movement |
| Elbow | -90° to 90° | Forearm articulation |
| Wrist Rotate | -180° to 180° | End-effector rotation |
| Gripper Fingers | 0 to 0.04m | Parallel jaw opening |

### Objects

The simulation includes three graspable objects:

1. **Cube**: 0.05m × 0.05m × 0.05m, mass 0.1kg
2. **Sphere**: 0.02m radius, mass 0.08kg
3. **Cylinder**: 0.02m radius, 0.06m height, mass 0.12kg

All objects have high friction coefficients for realistic grasping.

## Advanced Features

### Inverse Kinematics

The `calculate_ik_simplified()` function provides analytical IK for the arm:

```python
import numpy as np
from robotic_arm_sim import calculate_ik_simplified

# Target position in workspace
target = np.array([0.5, 0.3, 0.2])

# Calculate joint angles
angles = calculate_ik_simplified(target)
# Returns: [shoulder_pan, shoulder_lift, elbow, wrist_rotate]
```

**Note**: This is a simplified 2D planar IK solver. For full 3D manipulation and orientation control, consider implementing a numerical IK solver using Jacobian methods or optimization.

### Trajectory Planning

Generate smooth trajectories between poses:

```python
from robotic_arm_sim import smooth_trajectory
import numpy as np

start_angles = np.array([0.0, -0.5, 0.8, 0.0])
end_angles = np.array([0.5, -0.3, 0.6, 0.5])

# Generate 100 interpolation steps
trajectory = smooth_trajectory(start_angles, end_angles, steps=100)

for angles in trajectory:
    sim.set_joint_angles(*angles)
    sim.step(10)
```

### Custom Object Manipulation

Add your own objects by modifying `models/robotic_arm.xml`:

```xml
<body name="my_object" pos="0.4 0.0 0.03">
  <freejoint/>
  <inertial pos="0 0 0" mass="0.15" diaginertia="0.0002 0.0002 0.0002"/>
  <geom name="my_object_geom" type="box" size="0.03 0.03 0.03" 
        rgba="1.0 0.5 0.0 1" friction="1.0 0.005 0.0001"/>
</body>
```

## Troubleshooting

### Issue: "No module named 'mujoco'"

**Solution**: Ensure MuJoCo is properly installed:
```bash
pip install mujoco
```

### Issue: "Cannot find model file"

**Solution**: Make sure you're running the scripts from the project root directory:
```bash
cd mujoco-robotic-arm
python robotic_arm_sim.py
```

### Issue: OpenGL/Rendering errors

**Solution**: 
- On Linux, ensure you have OpenGL libraries: `sudo apt-get install libgl1-mesa-glx libosmesa6`
- On macOS, update your graphics drivers
- On remote servers, use offscreen rendering or X11 forwarding

### Issue: Gripper not grasping objects

**Solution**: 
- Ensure gripper is closing fully (`set_gripper(0.0)`)
- Check that object friction is adequate in the XML model
- Verify gripper is positioned correctly around the object
- Increase contact solver iterations in XML: `<option iterations="50"/>`

## Performance Tips

1. **Simulation Speed**: Reduce visualization frequency for faster-than-realtime simulation
2. **Stability**: Increase solver iterations for better contact stability
3. **Rendering**: Use lower resolution for faster rendering during development

## Future Enhancements

Potential improvements and extensions:

- [ ] Full 6-DOF IK solver with orientation control
- [ ] ROS/ROS2 integration for robot control
- [ ] Machine learning-based grasping policies
- [ ] Force/torque sensor feedback
- [ ] Vision-based object detection and localization
- [ ] Multi-arm coordination
- [ ] Trajectory optimization for smooth motion
- [ ] Collision avoidance algorithms
- [ ] Real robot hardware integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MuJoCo](https://mujoco.org/) - Advanced physics simulation engine
- [DeepMind](https://github.com/deepmind/mujoco) - For open-sourcing MuJoCo

## References

- MuJoCo Documentation: https://mujoco.readthedocs.io/
- MuJoCo Forum: https://github.com/deepmind/mujoco/discussions
- Robotic Manipulation: https://manipulation.mit.edu/

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Happy Simulating! 🤖**
