#!/usr/bin/env python
#---------------------------------------------------
from pid import PID
import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float64MultiArray, Float32
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Joy

global yawSetpoint, thrust, pitchSetpoint, rollSetpoint, kp, ki, kd
yawSetpoint = 0
thrust = 1500
pitchSetpoint = 0
rollSetpoint = 0

kp = 10
ki = 0.0002
kd = 3.8

#---------------------------------------------------
def control_kwad(msg, args):
	#Declare global variables as you dont want these to die, reset to zero and then re-initiate when the function is called again.
	global roll, pitch, yaw, err_roll, err_pitch, err_yaw
	
	#Assign the Float64MultiArray object to 'f' as we will have to send data of motor velocities to gazebo in this format
	f = Float64MultiArray()
	
	#Convert the quaternion data to roll, pitch, yaw data
	#The model_states contains the position, orientation, velocities of all objects in gazebo. In the simulation, there are 3 objects: ground, Contruction_cone, and the quadcopter. So 'msg.pose[2]' will access the 3rd object's pose information i.e the quadcopter's pose.
	orientationObj = msg.pose[2].orientation
	orientationList = [orientationObj.x, orientationObj.y, orientationObj.z, orientationObj.w]
	(roll, pitch, yaw) = (euler_from_quaternion(orientationList))
	
	#send roll, pitch, yaw data to PID() for attitude-stabilisation, along with 'f', to obtain 'fUpdated'
	#Alternatively, you can add your 'control-file' with other algorithms such as Reinforcement learning, and import the main function here instead of PID().
	(fUpdated, err_roll, err_pitch, err_yaw) = PID(roll, pitch, yaw, f, yawSetpoint, thrust, pitchSetpoint, rollSetpoint, kp, ki, kd)
	
	#The object args contains the tuple of objects (velPub, err_rollPub, err_pitchPub, err_yawPub. publish the information to namespace.
	args[0].publish(fUpdated)
	args[1].publish(err_roll)
	args[2].publish(err_pitch)
	args[3].publish(err_yaw)
	#print("Roll: ",roll*(180/3.141592653),"Pitch: ", pitch*(180/3.141592653),"Yaw: ", yaw*(180/3.141592653))
	#print(orientationObj)
	
#----------------------------------------------------
def JoyData(msg4):

	global yawSetpoint, thrust, pitchSetpoint, rollSetpoint
	yawSetpoint = (msg4.axes[0]*10.0)  #Left is positive
	thrust = (msg4.axes[1]*500 + 1500) #Up is positive
	pitchSetpoint = (msg4.axes[2]*10.0) #Up is positive
	rollSetpoint = (msg4.axes[3]*10.0) #Left is positive
	
#----------------------------------------------------
def setKp(msg1):

	global kp
	kp = msg1.data
	
#----------------------------------------------------
def setKi(msg2):

	global ki
	ki = msg2.data
	
#----------------------------------------------------
def setKd(msg3):

	global kd
	kd = msg3.data
	
#----------------------------------------------------

#Initiate the node that will control the gazebo model
rospy.init_node("Control")

#initiate publishers that publish errors (roll, pitch,yaw - setpoint) so that it can be plotted via rqt_plot /err_<name>  
err_rollPub = rospy.Publisher('err_roll', Float32, queue_size=1)
err_pitchPub = rospy.Publisher('err_pitch', Float32, queue_size=1)
err_yawPub = rospy.Publisher('err_yaw', Float32, queue_size=1)

#initialte publisher velPub that will publish the velocities of individual BLDC motors
velPub = rospy.Publisher('/Kwad/joint_motor_controller/command', Float64MultiArray, queue_size=4)

#Subscribe to /gazebo/model_states to obtain the pose in quaternion form
#Upon receiveing the messages, the objects msg, velPub, err_rollPub, err_pitchPub and err_yawPub are sent to "control_kwad" function.
PoseSub = rospy.Subscriber('/gazebo/model_states',ModelStates,control_kwad,(velPub, err_rollPub, err_pitchPub, err_yawPub))

joyData = rospy.Subscriber('/Kwad/joy',Joy,JoyData)

subKp = rospy.Subscriber("/Kp", Float32, setKp)
subKi = rospy.Subscriber("/Ki", Float32, setKi)
subKd = rospy.Subscriber("/Kd", Float32, setKd)
rospy.spin()
