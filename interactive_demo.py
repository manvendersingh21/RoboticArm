"""
Interactive MuJoCo Robotic Arm Demo with Visualization
Provides keyboard controls and real-time visualization of the robotic arm.
"""

import mujoco
import mujoco.viewer
import numpy as np
import threading
import time
from robotic_arm_sim import RoboticArmSimulation, calculate_ik_simplified


class InteractiveRoboticArm:
    """Interactive robotic arm with keyboard controls."""
    
    def __init__(self, model_path: str = "models/robotic_arm.xml"):
        """Initialize interactive simulation.
        
        Args:
            model_path: Path to MuJoCo XML model
        """
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        
        # Control state
        self.target_joint_angles = np.zeros(4)  # [shoulder_pan, shoulder_lift, elbow, wrist]
        self.gripper_opening = 1.0  # 0=closed, 1=open
        
        # Control parameters
        self.joint_step = 0.05  # radians per keypress
        self.gripper_step = 0.1
        
        # Actuator indices
        self.shoulder_pan_idx = 0
        self.shoulder_lift_idx = 1
        self.elbow_idx = 2
        self.wrist_rotate_idx = 3
        self.left_finger_idx = 4
        self.right_finger_idx = 5
        
        # Demo mode
        self.demo_mode = False
        self.auto_mode = False
        
    def update_controls(self):
        """Update actuator controls based on current targets."""
        self.data.ctrl[self.shoulder_pan_idx] = self.target_joint_angles[0]
        self.data.ctrl[self.shoulder_lift_idx] = self.target_joint_angles[1]
        self.data.ctrl[self.elbow_idx] = self.target_joint_angles[2]
        self.data.ctrl[self.wrist_rotate_idx] = self.target_joint_angles[3]
        
        gripper_pos = self.gripper_opening * 0.04
        self.data.ctrl[self.left_finger_idx] = gripper_pos
        self.data.ctrl[self.right_finger_idx] = gripper_pos
    
    def run_interactive(self):
        """Run interactive simulation with viewer."""
        print("\n" + "=" * 70)
        print(" " * 20 + "ROBOTIC ARM INTERACTIVE DEMO")
        print("=" * 70)
        print("\nKeyboard Controls:")
        print("-" * 70)
        print("  Shoulder Pan:    Q / W  (rotate left/right)")
        print("  Shoulder Lift:   A / S  (lift up/down)")
        print("  Elbow:           Z / X  (bend/extend)")
        print("  Wrist Rotate:    E / R  (rotate left/right)")
        print("  Gripper:         G / H  (open/close)")
        print()
        print("  Demo Mode:       D      (run pick-and-place demo)")
        print("  Reset:           SPACE  (return to home position)")
        print("  Home Position:   HOME   (move to home)")
        print("  Quit:            ESC")
        print("-" * 70)
        print("\nStarting interactive viewer...\n")
        
        # Launch viewer with keyboard callback
        with mujoco.viewer.launch_passive(self.model, self.data, 
                                         key_callback=self.key_callback) as viewer:
            
            # Simulation loop
            while viewer.is_running():
                step_start = time.time()
                
                # Update controls
                self.update_controls()
                
                # Step simulation
                mujoco.mj_step(self.model, self.data)
                
                # Sync viewer
                viewer.sync()
                
                # Maintain real-time rate
                time_until_next_step = self.model.opt.timestep - (time.time() - step_start)
                if time_until_next_step > 0:
                    time.sleep(time_until_next_step)
    
    def key_callback(self, keycode):
        """Handle keyboard input.
        
        Args:
            keycode: Key code from viewer
        """
        import glfw
        
        # Shoulder pan (Q/W)
        if keycode == glfw.KEY_Q:
            self.target_joint_angles[0] += self.joint_step
            print(f"Shoulder Pan: {self.target_joint_angles[0]:.2f} rad")
        elif keycode == glfw.KEY_W:
            self.target_joint_angles[0] -= self.joint_step
            print(f"Shoulder Pan: {self.target_joint_angles[0]:.2f} rad")
        
        # Shoulder lift (A/S)
        elif keycode == glfw.KEY_A:
            self.target_joint_angles[1] += self.joint_step
            print(f"Shoulder Lift: {self.target_joint_angles[1]:.2f} rad")
        elif keycode == glfw.KEY_S:
            self.target_joint_angles[1] -= self.joint_step
            print(f"Shoulder Lift: {self.target_joint_angles[1]:.2f} rad")
        
        # Elbow (Z/X)
        elif keycode == glfw.KEY_Z:
            self.target_joint_angles[2] += self.joint_step
            print(f"Elbow: {self.target_joint_angles[2]:.2f} rad")
        elif keycode == glfw.KEY_X:
            self.target_joint_angles[2] -= self.joint_step
            print(f"Elbow: {self.target_joint_angles[2]:.2f} rad")
        
        # Wrist rotate (E/R)
        elif keycode == glfw.KEY_E:
            self.target_joint_angles[3] += self.joint_step
            print(f"Wrist Rotate: {self.target_joint_angles[3]:.2f} rad")
        elif keycode == glfw.KEY_R:
            self.target_joint_angles[3] -= self.joint_step
            print(f"Wrist Rotate: {self.target_joint_angles[3]:.2f} rad")
        
        # Gripper (G/H)
        elif keycode == glfw.KEY_G:
            self.gripper_opening = min(1.0, self.gripper_opening + self.gripper_step)
            print(f"Gripper Opening: {self.gripper_opening:.2f}")
        elif keycode == glfw.KEY_H:
            self.gripper_opening = max(0.0, self.gripper_opening - self.gripper_step)
            print(f"Gripper Opening: {self.gripper_opening:.2f}")
        
        # Home position
        elif keycode == glfw.KEY_HOME or keycode == glfw.KEY_SPACE:
            self.target_joint_angles = np.array([0.0, -0.5, 0.8, 0.0])
            self.gripper_opening = 1.0
            print("Moving to home position")
        
        # Demo mode
        elif keycode == glfw.KEY_D:
            print("\nStarting automated demo sequence...")
            self.run_demo_sequence()
        
        # Print current state
        elif keycode == glfw.KEY_P:
            self.print_state()
    
    def print_state(self):
        """Print current arm state."""
        print("\n" + "-" * 50)
        print("Current Arm State:")
        print(f"  Shoulder Pan:  {self.target_joint_angles[0]:6.2f} rad")
        print(f"  Shoulder Lift: {self.target_joint_angles[1]:6.2f} rad")
        print(f"  Elbow:         {self.target_joint_angles[2]:6.2f} rad")
        print(f"  Wrist Rotate:  {self.target_joint_angles[3]:6.2f} rad")
        print(f"  Gripper:       {self.gripper_opening:6.2f}")
        
        # Get gripper position
        sensor_id = self.model.sensor('gripper_position').id
        sensor_adr = self.model.sensor_adr[sensor_id]
        gripper_pos = self.data.sensordata[sensor_adr:sensor_adr+3]
        print(f"  Position: [{gripper_pos[0]:.3f}, {gripper_pos[1]:.3f}, {gripper_pos[2]:.3f}]")
        print("-" * 50 + "\n")
    
    def run_demo_sequence(self):
        """Run an automated demo sequence."""
        print("\n=== Automated Demo Sequence ===")
        
        # This is a simplified demo that moves the arm through predefined positions
        demo_positions = [
            ([0.0, -0.3, 0.5, 0.0], 1.0, "Position 1"),
            ([0.5, -0.5, 0.8, 0.5], 0.5, "Reaching"),
            ([0.5, -0.5, 0.8, 0.5], 0.0, "Grasping"),
            ([0.0, -0.3, 0.5, 0.0], 0.0, "Lifting"),
            ([-0.5, -0.4, 0.6, -0.5], 0.0, "Moving"),
            ([-0.5, -0.4, 0.6, -0.5], 1.0, "Releasing"),
            ([0.0, -0.5, 0.8, 0.0], 1.0, "Home"),
        ]
        
        for angles, gripper, description in demo_positions:
            print(f"  → {description}")
            self.target_joint_angles = np.array(angles)
            self.gripper_opening = gripper
            time.sleep(1.5)
        
        print("=== Demo Complete ===\n")


def main():
    """Run interactive demo."""
    try:
        arm = InteractiveRoboticArm()
        arm.run_interactive()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
