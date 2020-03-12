# ROS-Quad-Joystick-control
This is a simulation of quadcopter, controlled by a joystick on ROS-Gazebo (Melodic, gazebo9)

The PID control hasn't been perfectly tuned yet. Thus, I have provided an easy solution of tuning the PID gains by creating a slider-GUI interface for three gains, using rqt-ez-publisher. The joystick is plugged into the USB, and the values are fed by the "JOY" node in ROS. 

The values in the slider file can be changed dynamically, so that the PID values are updated immediately. Make sure to restart the gazebo world (Ctrl + R) after every PID updation.

Here is the YouTube link: https://www.youtube.com/watch?v=csJLEBhIRu4

![Image](https://github.com/NishanthARao/ROS-Quad-Joystick-control/blob/master/Screenshot.png)


# Installation

Make sure you have installed ROS, GAZEBO and their dependencies.
Additionally, you have to install the following packages:
```
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 
sudo apt-get update
sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control ros-melodic-ros-control ros-melodic-ros-controllers
sudo apt-get install ros-melodic-joint-state-controller ros-melodic-effort-controllers ros-melodic-position-controllers
```

1) **SETUP the Joystick.**

You need a linux-compatible joystick with ROS packages installed. Make sure to follow the tutorials to set up the Joystick from the official ROS documentation:
http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

2) **Install the rqt-ez-publisher package for the slider GUI**

The rqt-ez-publisher originally wasn't released for the melodic distro. However, after some requests, OTL has released a version for melodic. (The package may not run perfectly, so please post your queries by opening new issues here: https://github.com/OTL/rqt_ez_publisher/issues). Follow the command to install it:
```
sudo apt-get install ros-melodic-rqt-ez-publisher
```
The above method should work. In case it doesn't work (chances are less likely), and give you errors, uninstall and restart. After that, here is what you need to do. I have assumed that your workspace name is "catkin_ws". Please change it according to the name your workspace. 
```
cd ~/catkin_ws/src
git clone -b melodic-devel https://github.com/OTL/rqt_ez_publisher
```
Once done, 
```
cd ~/catkin_ws 
catkin_make
```
You must not face any issues in the above steps. If you get any errors, recheck with the above instructions.

If this doesn't work, you may have to follow the instructions on this page: https://answers.ros.org/question/240235/how-to-install-packages-from-github/. Make sure that the branch in the github page of rqt-ez-publisher (https://github.com/OTL/rqt_ez_publisher) is set to melodic-devel. 

3) **Download all files and launch gazebo simulator**

1.Add this workspace to your linux environment by sourcing the setup file to .bashrc. Assuming you are inside the home directory, 
```
cd ~
gedit .bashrc
```
Add this line at the end of the file.
```
source ~/catkin_ws/devel/setup.bash
```

4.Create a ROS package in your workspace. We will call it fly_bot. Add the rospy and std_msgs dependencies
```
cd ~/catkin_ws/src
catkin_create_pkg fly_bot rospy std_msgs
```

5.Download all the folders and files into the folder fly_bot. i.e all the folders and files seen in this repo must be present inside the fly_bot. Donot create another folder inside the fly_bot with all these files.

Note: You may have to replace the existing src folder and CMakeLists and package files with these folder and files.

6.Execute the following command to build into your ROS workspace
```
cd ~/catkin_ws
catkin_make
```

This should build the directory without any errors. If you find any errors, please check your steps with those mentioned here.

Now, create executables of the python programs present in the src directory
```
cd ~/catkin_ws/src/fly_bot/src
chmod u+x control.py
chmod u+x pid.py
```

After this, close the terminal. Open another terminal and load the quadcopter into gazebo simulator
```
roslaunch fly_bot Kwad_gazebo.launch
```

You may get some errors of sort "No p gains mentioned in pid...." and "Cannot initialize/load joy_feedback etc ...... and that's fine. You should see the quadcopter starting to hover. The slider GUI must pop up. Initially, it may be empty. If thats the case, go to the empty white bar above in the GUI, and there will be a small green "plus" mark (that stands for addition of any topic). Select /kp, /ki, /kd sequentially. Now, you must see three sliders. Change the min/max value, slide and tune to get optimal values.

**Note**: If you don't change the PID values in the slider, the quadcopter will just move in a random direction and crash. To make sure this doesn't happen, set the slider values initially to the following:

Kp - 10

Ki - 0.0002

Kd - 3.4

Now, you must see the quad hover and be stable. For me, these values of Kp, Ki, Kd worked fine with joystick control:

Kp - 80

Ki - 0.02

Kd - 98

These may not work for you, as initialisation of the quadcopter's parameters in gazebo is random.
