"""
Simple example demonstrating basic robotic arm control.
This is a minimal example to get started with the simulation.
"""

import sys
import os

# Add parent directory to path to import robotic_arm_sim
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robotic_arm_sim import RoboticArmSimulation
import numpy as np


def simple_movement_demo():
    """Demonstrate simple arm movements."""
    print("=" * 60)
    print("Simple Robotic Arm Movement Demo")
    print("=" * 60)
    
    # Initialize simulation
    print("\n1. Initializing simulation...")
    sim = RoboticArmSimulation()
    
    # Stabilize
    print("2. Stabilizing physics...")
    for _ in range(500):
        sim.step()
    
    print("3. Opening gripper...")
    sim.set_gripper(1.0)  # Fully open
    for _ in range(200):
        sim.step()
    
    print("4. Moving to position 1...")
    sim.set_joint_angles(
        shoulder_pan=0.5,
        shoulder_lift=-0.4,
        elbow=0.6,
        wrist_rotate=0.0
    )
    for _ in range(1000):
        sim.step()
    
    print("5. Closing gripper...")
    sim.set_gripper(0.0)  # Fully closed
    for _ in range(200):
        sim.step()
    
    print("6. Moving to position 2...")
    sim.set_joint_angles(
        shoulder_pan=-0.3,
        shoulder_lift=-0.6,
        elbow=0.8,
        wrist_rotate=0.5
    )
    for _ in range(1000):
        sim.step()
    
    print("7. Opening gripper...")
    sim.set_gripper(1.0)
    for _ in range(200):
        sim.step()
    
    print("8. Returning to home position...")
    sim.set_joint_angles(
        shoulder_pan=0.0,
        shoulder_lift=-0.5,
        elbow=0.8,
        wrist_rotate=0.0
    )
    for _ in range(1000):
        sim.step()
    
    # Get final gripper position
    gripper_pos = sim.get_gripper_position()
    print(f"\n9. Final gripper position: {gripper_pos}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


def inspect_objects():
    """Inspect object positions in the scene."""
    print("\n" + "=" * 60)
    print("Object Inspection")
    print("=" * 60)
    
    sim = RoboticArmSimulation()
    
    # Let objects settle
    for _ in range(500):
        sim.step()
    
    # Print object positions
    objects = ['cube', 'sphere', 'cylinder']
    print("\nObject positions:")
    for obj in objects:
        pos = sim.get_object_position(obj)
        print(f"  {obj:10s}: [{pos[0]:6.3f}, {pos[1]:6.3f}, {pos[2]:6.3f}]")
    
    gripper_pos = sim.get_gripper_position()
    print(f"  {'gripper':10s}: [{gripper_pos[0]:6.3f}, {gripper_pos[1]:6.3f}, {gripper_pos[2]:6.3f}]")
    print("=" * 60)


if __name__ == "__main__":
    # Run simple movement demo
    simple_movement_demo()
    
    # Inspect object positions
    inspect_objects()
