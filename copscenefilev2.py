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

sim.startSimulation()

# TO RANDOMLY PLACE THE OBJECT-----------------------------
# Get handles
object_handle = sim.getObjectHandle('peg')
table_handle = sim.getObjectHandle('ME_Platfo2_sub1')
# Get the table's position to use as a reference
table_position = sim.getObjectPosition(table_handle, -1)
# Get the table's position to use as a reference
table_position = sim.getObjectPosition(table_handle, -1)
# Generate random position within bounds
x_pos = random.uniform(-0.450,-0.25)
y_pos = random.uniform(0.5,0.69)
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
sim.wait(20)

# Object position (example, replace with actual detection logic)
dummy_handle = sim.getObjectHandle('pegdummy')
object_position = sim.getObjectPosition(dummy_handle)
[a,b,c] = object_position

# Move IK target to the object position
sim.setObjectPosition(target_handle, -1, [a,b,c])

sim.setJointTargetPosition(gripperHandles[0], -0.010)
sim.setJointTargetPosition(gripperHandles[1], 0.010)
sim.wait(10)

connectorHandle = sim.getObjectHandle('peg')  # Create a small dummy object
connectorHandle1 = sim.getObjectHandle('youBotArmJoint4') 

peg_ori=sim.getObjectOrientation(jointHandles[4])
connectorHandle = sim.getObjectHandle('peg')  # Create a small dummy objec
sim.setObjectPosition(connectorHandle, connectorHandle1,[-0.06,-0.01,0.092])
sim.setObjectOrientation(connectorHandle, -1, peg_ori)
sim.setObjectParent(connectorHandle, connectorHandle1, True)  # Parent it to the gripper

connectorHandle2 = sim.getObjectHandle('youBot_ref') 
sim.setObjectPosition(target_handle, connectorHandle2,[0,-0.1,0.5])


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

# Move IK target to the object position
sim.setObjectPosition(target_handle, -1, holeobject_position)

sim.wait(30)
sim.setObjectParent(connectorHandle, -1, True)  # Parent it to the gripper

sim.setJointTargetPosition(gripperHandles[0], 0)
sim.setJointTargetPosition(gripperHandles[1], 0)

sim.setObjectPosition(target_handle, 1, [-0.500,-1.600,0.296])
sim.wait(40)

#Stop simulation
sim.stopSimulation() 
