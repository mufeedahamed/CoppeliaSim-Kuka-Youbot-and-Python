# CoppeliaSim-Kuka-Youbot-and-Python
Controlling KUKA Youbot in CoppeliaSim using python script with the help of Inverse Kinematics (IK)

Kuka Youbot can be controled by Lua script which is the default way of controllling the robots in CoppeliaSim. I took the initiative to control the KukaYoubot in CoppeliaSim using external python script. This method involved using of ZeroMQ remote API which allows to control a simulation (or the simulator itself) from an external application or a remote hardware. 

The Robot moves based on IK generated coordinates to position the arm. 

The code is not perfect, requires further adjustments and correction to improve the accuracy.

Cheers!
