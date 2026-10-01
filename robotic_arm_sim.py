"""
MuJoCo Robotic Arm Simulation with Gripper
This script demonstrates a robotic arm that can grip and manipulate objects.
"""

import mujoco
import numpy as np
import time
from typing import Tuple, Optional


class RoboticArmSimulation:
    """Robotic arm simulation with gripper control."""
    
    def __init__(self, model_path: str = "models/robotic_arm.xml"):
        """Initialize the simulation.
        
        Args:
            model_path: Path to the MuJoCo XML model file
        """
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        
        # Joint indices
        self.shoulder_pan_idx = self.model.actuator('shoulder_pan_actuator').id
        self.shoulder_lift_idx = self.model.actuator('shoulder_lift_actuator').id
        self.elbow_idx = self.model.actuator('elbow_actuator').id
        self.wrist_rotate_idx = self.model.actuator('wrist_rotate_actuator').id
        self.left_finger_idx = self.model.actuator('left_finger_actuator').id
        self.right_finger_idx = self.model.actuator('right_finger_actuator').id
        
        # Body indices for objects
        self.cube_id = self.model.body('cube').id
        self.sphere_id = self.model.body('sphere').id
        self.cylinder_id = self.model.body('cylinder').id
        
        # Initialize viewer
        self.viewer = None
        
    def reset(self):
        """Reset the simulation to initial state."""
        mujoco.mj_resetData(self.model, self.data)
        
    def set_joint_angles(self, shoulder_pan: float, shoulder_lift: float, 
                        elbow: float, wrist_rotate: float):
        """Set target angles for arm joints.
        
        Args:
            shoulder_pan: Shoulder pan angle (radians)
            shoulder_lift: Shoulder lift angle (radians)
            elbow: Elbow angle (radians)
            wrist_rotate: Wrist rotation angle (radians)
        """
        self.data.ctrl[self.shoulder_pan_idx] = shoulder_pan
        self.data.ctrl[self.shoulder_lift_idx] = shoulder_lift
        self.data.ctrl[self.elbow_idx] = elbow
        self.data.ctrl[self.wrist_rotate_idx] = wrist_rotate
        
    def set_gripper(self, opening: float):
        """Set gripper opening.
        
        Args:
            opening: Gripper opening (0.0 = closed, 1.0 = fully open)
        """
        gripper_pos = opening * 0.04  # Max opening is 0.04 meters
        self.data.ctrl[self.left_finger_idx] = gripper_pos
        self.data.ctrl[self.right_finger_idx] = gripper_pos
        
    def get_object_position(self, object_name: str) -> np.ndarray:
        """Get the position of an object.
        
        Args:
            object_name: Name of the object ('cube', 'sphere', or 'cylinder')
            
        Returns:
            3D position of the object
        """
        body_id = self.model.body(object_name).id
        return self.data.xpos[body_id].copy()
    
    def get_gripper_position(self) -> np.ndarray:
        """Get the current gripper position.
        
        Returns:
            3D position of the gripper
        """
        sensor_id = self.model.sensor('gripper_position').id
        sensor_adr = self.model.sensor_adr[sensor_id]
        return self.data.sensordata[sensor_adr:sensor_adr+3].copy()
    
    def step(self, steps: int = 1):
        """Step the simulation forward.
        
        Args:
            steps: Number of simulation steps to take
        """
        for _ in range(steps):
            mujoco.mj_step(self.model, self.data)
    
    def render(self, width: int = 1280, height: int = 720) -> np.ndarray:
        """Render the current simulation state.
        
        Args:
            width: Image width
            height: Image height
            
        Returns:
            RGB image array
        """
        if self.viewer is None:
            self.viewer = mujoco.Renderer(self.model, height=height, width=width)
        
        self.viewer.update_scene(self.data)
        return self.viewer.render()


def smooth_trajectory(start: np.ndarray, end: np.ndarray, 
                      steps: int) -> np.ndarray:
    """Generate a smooth trajectory between two points.
    
    Args:
        start: Starting joint angles
        end: Target joint angles
        steps: Number of interpolation steps
        
    Returns:
        Array of interpolated joint angles
    """
    trajectory = np.linspace(start, end, steps)
    return trajectory


def example_pick_and_place(sim: RoboticArmSimulation, 
                          target_object: str = 'cube',
                          place_position: Tuple[float, float] = (0.2, -0.3)):
    """Demonstrate picking and placing an object.
    
    Args:
        sim: RoboticArmSimulation instance
        target_object: Name of object to pick ('cube', 'sphere', or 'cylinder')
        place_position: (x, y) coordinates for placement
    """
    print(f"\n=== Pick and Place Demo: {target_object} ===")
    
    # 1. Move to home position with gripper open
    print("1. Moving to home position...")
    home_angles = np.array([0.0, -0.5, 0.8, 0.0])
    trajectory = smooth_trajectory(
        np.array([sim.data.ctrl[i] for i in range(4)]),
        home_angles,
        steps=100
    )
    
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(1.0)  # Open gripper
        sim.step(10)
    
    print("   Home position reached")
    time.sleep(0.5)
    
    # 2. Get object position and move above it
    obj_pos = sim.get_object_position(target_object)
    print(f"2. Object position: {obj_pos}")
    
    # Calculate inverse kinematics (simplified approach)
    # Move to position above object
    approach_angles = calculate_ik_simplified(obj_pos + np.array([0, 0, 0.1]))
    
    print("3. Approaching object...")
    trajectory = smooth_trajectory(home_angles, approach_angles, steps=150)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(1.0)
        sim.step(10)
    
    print("   Position above object reached")
    time.sleep(0.3)
    
    # 3. Lower gripper to object
    print("4. Lowering to object...")
    grasp_angles = calculate_ik_simplified(obj_pos + np.array([0, 0, 0.02]))
    trajectory = smooth_trajectory(approach_angles, grasp_angles, steps=80)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(1.0)
        sim.step(10)
    
    print("   At object height")
    time.sleep(0.3)
    
    # 4. Close gripper to grasp
    print("5. Closing gripper...")
    for i in range(100):
        sim.set_gripper(1.0 - i/100.0)
        sim.step(5)
    
    print("   Object grasped")
    time.sleep(0.5)
    
    # 5. Lift object
    print("6. Lifting object...")
    lift_angles = calculate_ik_simplified(obj_pos + np.array([0, 0, 0.15]))
    trajectory = smooth_trajectory(grasp_angles, lift_angles, steps=100)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(0.0)  # Keep gripper closed
        sim.step(10)
    
    print("   Object lifted")
    time.sleep(0.5)
    
    # 6. Move to placement position
    print("7. Moving to placement position...")
    place_pos_3d = np.array([place_position[0], place_position[1], 0.15])
    place_angles = calculate_ik_simplified(place_pos_3d)
    trajectory = smooth_trajectory(lift_angles, place_angles, steps=150)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(0.0)
        sim.step(10)
    
    print("   Placement position reached")
    time.sleep(0.3)
    
    # 7. Lower and release
    print("8. Lowering and releasing...")
    lower_angles = calculate_ik_simplified(place_pos_3d - np.array([0, 0, 0.1]))
    trajectory = smooth_trajectory(place_angles, lower_angles, steps=80)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(0.0)
        sim.step(10)
    
    # Open gripper
    for i in range(80):
        sim.set_gripper(i/80.0)
        sim.step(5)
    
    print("   Object released")
    time.sleep(0.3)
    
    # 8. Retract
    print("9. Retracting...")
    retract_angles = calculate_ik_simplified(place_pos_3d + np.array([0, 0, 0.1]))
    trajectory = smooth_trajectory(lower_angles, retract_angles, steps=80)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(1.0)
        sim.step(10)
    
    print("10. Returning to home...")
    trajectory = smooth_trajectory(retract_angles, home_angles, steps=100)
    for angles in trajectory:
        sim.set_joint_angles(*angles)
        sim.set_gripper(1.0)
        sim.step(10)
    
    print("=== Demo Complete ===\n")


def calculate_ik_simplified(target_pos: np.ndarray) -> np.ndarray:
    """Simplified inverse kinematics for the robotic arm.
    
    This is a simplified IK solver that works for this specific arm configuration.
    For production use, consider using a proper IK solver.
    
    Args:
        target_pos: Target 3D position for the gripper
        
    Returns:
        Joint angles [shoulder_pan, shoulder_lift, elbow, wrist_rotate]
    """
    x, y, z = target_pos
    
    # Shoulder pan (rotation around z-axis)
    shoulder_pan = np.arctan2(y, x)
    
    # Distance in xy plane
    r = np.sqrt(x**2 + y**2)
    
    # Arm segment lengths (from XML model)
    l1 = 0.4  # link1 length
    l2 = 0.3  # link2 length
    
    # Height from shoulder
    h = z - 0.3  # base height
    
    # Distance from shoulder to target (2D)
    d = np.sqrt(r**2 + h**2)
    
    # Law of cosines for elbow angle
    cos_elbow = (l1**2 + l2**2 - d**2) / (2 * l1 * l2)
    cos_elbow = np.clip(cos_elbow, -1, 1)
    elbow = np.arccos(cos_elbow) - np.pi  # Negative because of joint direction
    
    # Shoulder lift angle
    alpha = np.arctan2(h, r)
    beta = np.arccos(np.clip((l1**2 + d**2 - l2**2) / (2 * l1 * d), -1, 1))
    shoulder_lift = alpha + beta - np.pi/2
    
    # Wrist rotate (keep pointing down)
    wrist_rotate = 0.0
    
    return np.array([shoulder_pan, shoulder_lift, elbow, wrist_rotate])


def main():
    """Main simulation loop."""
    print("=" * 60)
    print("MuJoCo Robotic Arm Simulation")
    print("=" * 60)
    
    # Initialize simulation
    print("\nInitializing simulation...")
    sim = RoboticArmSimulation()
    print("Simulation initialized successfully!")
    
    # Let simulation settle
    print("\nStabilizing simulation...")
    for _ in range(500):
        sim.step()
    
    print("\nStarting demonstrations...\n")
    
    # Demonstrate picking different objects
    objects_to_pick = ['cube', 'sphere', 'cylinder']
    place_positions = [(0.2, -0.3), (-0.2, 0.3), (0.3, 0.3)]
    
    for obj, place_pos in zip(objects_to_pick, place_positions):
        example_pick_and_place(sim, obj, place_pos)
        
        # Wait between demonstrations
        for _ in range(500):
            sim.step()
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
