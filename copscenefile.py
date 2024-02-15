import random
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

global sims
sims = {}
client = RemoteAPIClient()
sim = client.require('sim')
sim = client.getObject('sim')

sim.stopSimulation()
# Start simulation
sim.startSimulation()

# TO RANDOM PLACE THE OBJECT-----------------------------
# Get handles
object_handle = sim.getObjectHandle('peg')
table_handle = sim.getObjectHandle('ME_Platfo2_sub1')
# Get the table's position to use as a reference
table_position = sim.getObjectPosition(table_handle, -1)
# Get the table's position to use as a reference
table_position = sim.getObjectPosition(table_handle, -1)
# Generate random position within bounds
x_pos = random.uniform(-0.450,-0.47)
y_pos = random.uniform(0.61,0.65)
# Assuming the object should be placed on top of the table, not adjusting Z here
# Calculate new position for the object, relative to the world frame
new_position = [0 + x_pos, 0+ y_pos, 0 + 0.21]
# Set the object's position
sim.setObjectPosition(object_handle, -1, new_position)
sim.wait(20) 


target_handle = sim.getObjectHandle('IK_Target')  # IK target for the arm
jointHandles = [sim.getObjectHandle('youBotArmJoint0'), sim.getObjectHandle('youBotArmJoint1'), sim.getObjectHandle('youBotArmJoint2'), sim.getObjectHandle('youBotArmJoint3'), sim.getObjectHandle('youBotArmJoint4')]

gripperHandles=[sim.getObjectHandle('finger1'), sim.getObjectHandle('finger2')]
sim.setJointTargetPosition(gripperHandles[0], -0.02)
sim.setJointTargetPosition(gripperHandles[1], 0.02)
sim.wait(30)


# Object position (example, replace with actual detection logic)
dummy_handle = sim.getObjectHandle('pegdummy')
object_position = sim.getObjectPosition(dummy_handle, -1)
[a,b,c] = object_position
#object_position = [-0.45, 0.65, 0.21]  # Replace with the detected position

# Move IK target to the object position
sim.setObjectPosition(target_handle, -1, [a-0.3,b+0.05,c+0.01])

sim.setJointTargetPosition(gripperHandles[0], -0.015)
sim.setJointTargetPosition(gripperHandles[1], 0.015)
sim.wait(10)

connectorHandle = sim.getObjectHandle('peg')  # Create a small dummy object
sim.setObjectParent(connectorHandle, jointHandles[4], True)  # Parent it to the gripper

sim.setObjectPosition(target_handle, -1, [a-0.3,b+0.05,c+0.2])


# TO MOVE THE ROBOT TOWARDS THE WALL-----------------------------

# Retrieve handles
youBotHandle = sim.getObjectHandle('youBot')
wheelJoints = [
    sim.getObjectHandle('rollingJoint_fl'),  # Front left wheel
    sim.getObjectHandle('rollingJoint_rl'),  # Rear left wheel
    sim.getObjectHandle('rollingJoint_rr'),  # Rear right wheel
    sim.getObjectHandle('rollingJoint_fr')   # Front right wheel
]

# Set the desired wheel velocities
velocity = 1.0  # Adjust this value as necessary
for joint in wheelJoints:
    sim.setJointTargetVelocity(joint, velocity)

# Let the robot move for a short duration
sim.wait(40)  # Adjust the time as necessary

# Stop the robot by setting wheel velocities to zero
for joint in wheelJoints:
    sim.setJointTargetVelocity(joint, 0)
    
    
def rotate_robot(client, rotation_speed):
    sim = client.getObject('sim')
    
    # Wheel joint names in the KUKA YouBot
    wheel_joints = ['rollingJoint_fl', 'rollingJoint_rl', 'rollingJoint_fr', 'rollingJoint_rr']
    
    # Get handles for each wheel joint
    wheel_handles = [sim.getObjectHandle(wheel_joint) for wheel_joint in wheel_joints]
    
    # Set wheel velocities for rotation: To rotate, front-left and rear-left wheels go one direction,
    # front-right and rear-right go the opposite direction.
    for i, wheel_handle in enumerate(wheel_handles):
        if i < 2:  # Front-left and rear-left wheels
            sim.setJointTargetVelocity(wheel_handle, rotation_speed)
        else:  # Front-right and rear-right wheels
            sim.setJointTargetVelocity(wheel_handle, -rotation_speed)

    
rotation_speed = 1.0  # Adjust the speed as needed, positive for one direction, negative for the opposite
rotate_robot(client, rotation_speed)

# Wait a bit to see the rotation
sim.wait(16)  # Adjust the duration of rotation as needed

# Optionally, stop the wheels after rotation
rotate_robot(client, 0)
            
#----------------after coming near the wall

holedummy_handle = sim.getObjectHandle('holedummy')
holeobject_position = sim.getObjectPosition(holedummy_handle, -1)
[e,f,g] = holeobject_position

# Move IK target to the object position

sim.setObjectPosition(target_handle, -1, [e,f-4.5,g+4.5])

#[e-0.37,-3.0,2.8]
sim.wait(30)

sim.setObjectParent(connectorHandle, -1, True)  # Parent it to the gripper

sim.setJointTargetPosition(gripperHandles[0], 0)
sim.setJointTargetPosition(gripperHandles[1], 0)

sim.setObjectPosition(target_handle, -1, [e,f,g])


sim.wait(40)

#Stop simulation
sim.stopSimulation()

#print('Program ended')