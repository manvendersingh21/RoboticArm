# Quick Start Guide

Get up and running with the MuJoCo robotic arm simulation in 5 minutes!

## 1. Prerequisites

- Python 3.8 or higher
- pip package manager

## 2. Installation

```bash
# Clone the repository (after it's created on GitHub)
git clone https://github.com/YOUR_USERNAME/mujoco-robotic-arm.git
cd mujoco-robotic-arm

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Run Your First Simulation

### Option A: Automated Demo (No GUI Required)

Run the automated pick-and-place demonstration:

```bash
python robotic_arm_sim.py
```

This will:
- Initialize the robotic arm
- Pick up three different objects (cube, sphere, cylinder)
- Place them at different locations
- Print progress to console

**Expected output:**
```
============================================================
MuJoCo Robotic Arm Simulation
============================================================

Initializing simulation...
Simulation initialized successfully!

Starting demonstrations...

=== Pick and Place Demo: cube ===
1. Moving to home position...
   Home position reached
...
```

### Option B: Interactive Control (Requires Display)

Launch interactive visualization with keyboard controls:

```bash
python interactive_demo.py
```

**Keyboard Controls:**
- `Q`/`W` - Shoulder pan
- `A`/`S` - Shoulder lift
- `Z`/`X` - Elbow
- `E`/`R` - Wrist rotate
- `G`/`H` - Gripper open/close
- `D` - Run demo sequence
- `SPACE` - Return to home
- `ESC` - Exit

### Option C: Simple Example

Run a basic example script:

```bash
cd examples
python simple_example.py
```

This provides a minimal example of controlling the arm programmatically.

## 4. Understanding the Code

### Basic Usage Pattern

```python
from robotic_arm_sim import RoboticArmSimulation

# Create simulation
sim = RoboticArmSimulation()

# Control joints (angles in radians)
sim.set_joint_angles(
    shoulder_pan=0.5,      # -π to π
    shoulder_lift=-0.3,    # -π/2 to π/2
    elbow=0.8,             # -π/2 to π/2
    wrist_rotate=0.0       # -π to π
)

# Control gripper (0.0=closed, 1.0=open)
sim.set_gripper(0.5)

# Step simulation forward
sim.step(steps=1000)

# Get object positions
cube_pos = sim.get_object_position('cube')
print(f"Cube is at: {cube_pos}")
```

### Inverse Kinematics

Reach a specific 3D position:

```python
from robotic_arm_sim import calculate_ik_simplified
import numpy as np

# Target position (x, y, z)
target = np.array([0.4, 0.2, 0.15])

# Calculate joint angles
angles = calculate_ik_simplified(target)

# Apply to arm
sim.set_joint_angles(*angles)
```

## 5. Next Steps

### Experiment with Different Scenarios

1. **Modify object positions**: Edit `models/robotic_arm.xml`
2. **Change gripper parameters**: Adjust kp values for different grip strength
3. **Create custom trajectories**: Use `smooth_trajectory()` function
4. **Add new objects**: Follow examples in the XML model

### Explore Advanced Features

- Custom inverse kinematics solvers
- Force/torque sensing
- Vision-based grasping
- Multi-object manipulation

### Integrate with Other Tools

- **ROS/ROS2**: For robot control interfaces
- **OpenAI Gym**: For reinforcement learning
- **Computer Vision**: For object detection

## Troubleshooting

### "No module named 'mujoco'"

```bash
pip install --upgrade mujoco
```

### "Cannot find model file"

Make sure you're in the project root directory:
```bash
cd mujoco-robotic-arm
python robotic_arm_sim.py
```

### OpenGL errors on remote server

MuJoCo requires OpenGL. On headless servers:
```bash
# Install mesa
sudo apt-get install libosmesa6-dev libgl1-mesa-glx libglfw3

# Or use offscreen rendering (modify code to use mujoco.Renderer)
```

### Gripper not grasping properly

1. Check friction values in XML model
2. Increase solver iterations: `<option iterations="50"/>`
3. Verify gripper is fully closed: `sim.set_gripper(0.0)`
4. Ensure proper approach angle

## Additional Resources

- **Full Documentation**: See `README.md`
- **GitHub Setup**: See `GITHUB_SETUP.md`
- **MuJoCo Docs**: https://mujoco.readthedocs.io/
- **Example Code**: Check `examples/` directory

## Support

Having issues? 

1. Check `README.md` for detailed troubleshooting
2. Review the example scripts in `examples/`
3. Consult MuJoCo documentation
4. Open an issue on GitHub (after repository is created)

---

**Enjoy simulating! 🤖**
