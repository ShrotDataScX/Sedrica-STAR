## ROS 2, Linux Terminal, and Workspace Notes
Simple explanations for GitHub notes
This document explains the terminal, ROS 2 workspace, source files, bashrc, apt, sudo, and the exact issue that happened while working with TurtleBot3 and the Sedrica ROS workspace.
# 1. The issue that happened
You had two ROS workspaces on your laptop:
/home/shrot/turtlebot3_ws
/home/shrot/Sedrica/ros2_ws
You wanted to use the new workspace:
~/Sedrica/ros2_ws
But ROS was still finding some packages from the old workspace:
~/turtlebot3_ws
So commands like this:
ros2 pkg prefix turtlebot3_teleop
were showing paths from the old workspace, even though you were working inside the Sedrica workspace.
Child-like explanation: ROS had a school bag. You wanted it to use the new bag, but old books from the old bag were still inside. So ROS kept taking some packages from the old bag.
Technical explanation: The environment variables AMENT_PREFIX_PATH and COLCON_PREFIX_PATH still contained paths from /home/shrot/turtlebot3_ws. Also, the Sedrica workspace was built while the old workspace was active, so the generated install/setup.bash remembered the old workspace as an underlay.
# 2. What is a ROS 2 workspace?
A ROS 2 workspace is a project folder where ROS packages are stored, built, and installed.
ros2_ws
├── src
├── build
├── install
└── log
Term / Command	Child-like meaning	Technical meaning
src	The place where your real code lives.	Contains source code of ROS packages, repositories, launch files, nodes, messages, etc.
build	A construction area.	Temporary build files created by colcon while compiling packages.
install	The finished usable version.	Contains installed package files that ROS actually uses after building.
log	A notebook of what happened.	Contains build logs, warnings, and errors from colcon.

# 3. What is colcon build?
colcon is the build tool used in ROS 2. It looks inside src, builds all packages, and places usable output inside install.
cd ~/Sedrica/ros2_ws
colcon build
Simple meaning: Build my ROS 2 packages and make them ready to use.
# 4. What is source?
source tells the current terminal to read a script and apply its settings immediately.
source /opt/ros/humble/setup.bash
source ~/Sedrica/ros2_ws/install/setup.bash
Child-like meaning: Teach this terminal where ROS and my packages are.
Technical meaning: source runs a shell script in the current shell process. This changes environment variables such as PATH, AMENT_PREFIX_PATH, COLCON_PREFIX_PATH, PYTHONPATH, and LD_LIBRARY_PATH for the current terminal.
# 5. What is .bashrc?
.bashrc is a hidden file that runs automatically whenever you open a new Bash terminal.
~/.bashrc
same as:
/home/shrot/.bashrc
If you put source commands inside .bashrc, they run automatically in every new terminal.
source /opt/ros/humble/setup.bash
source ~/Sedrica/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
This is useful, but dangerous if you accidentally source the wrong or old workspace.
# 6. Underlay and overlay
An underlay is a workspace loaded before another workspace. An overlay is a workspace loaded on top of another one.
Clean setup:
/opt/ros/humble
        ↓
~/Sedrica/ros2_ws
Accidental mixed setup:
/opt/ros/humble
        ↓
~/turtlebot3_ws
        ↓
~/Sedrica/ros2_ws
Your Sedrica workspace had accidentally been built on top of turtlebot3_ws. Because of this, Sedrica remembered turtlebot3_ws and kept loading it again.
# 7. Important commands and terms
Term / Command	Child-like meaning	Technical meaning
sudo	Do this as admin.	Runs a command with root/administrator privileges. Example: sudo apt install git.
apt	Ubuntu app store from terminal.	Ubuntu package manager used to install, update, remove, and search software packages.
sudo apt update	Refresh the app list.	Downloads the latest package index from configured software repositories.
sudo apt upgrade	Upgrade installed apps.	Installs newer versions of already installed packages.
sudo apt install <package>	Install an app.	Installs a package and its dependencies from Ubuntu repositories.
sudo apt remove <package>	Remove an app.	Removes an installed package but may keep configuration files.
nano ~/.bashrc	Open the terminal settings file.	Opens .bashrc in the nano terminal text editor.
grep	Search for text.	Searches files or command output for matching text patterns.
grep -R	Search inside folders too.	Recursively searches through directories and files.
echo	Print something.	Prints text or environment variable values to the terminal.
export	Save a setting for programs.	Creates or modifies an environment variable available to child processes.
source	Load settings into this terminal.	Executes a shell script in the current shell environment.
rm -rf	Delete forcefully.	Removes files/folders recursively and forcefully. Dangerous if used on wrong path.
cd	Go to a folder.	Changes the current working directory.
ls	Show files here.	Lists files and folders in the current directory.
pwd	Where am I?	Prints the current working directory.
~	My home folder.	Shortcut for the current user home directory, e.g. /home/shrot.

# 8. ROS 2 specific commands and terms
Term / Command	Child-like meaning	Technical meaning
ros2 node list	Show running ROS programs.	Lists currently active ROS nodes visible in the same ROS domain.
ros2 node info <node>	Tell me about this node.	Displays publishers, subscribers, services, and actions for a node.
ros2 pkg list	Show installed ROS packages.	Lists ROS packages visible in the current environment.
ros2 pkg prefix <package>	Where did ROS find this package?	Prints the install prefix of a package. Very useful for debugging workspace confusion.
ros2 run <pkg> <exe>	Run one ROS program.	Runs one executable from a ROS package.
ros2 launch <pkg> <launch.py>	Start many ROS programs together.	Runs a launch file that can start multiple nodes and configurations.
node	One running ROS program.	A process participating in the ROS graph, usually publishing/subscribing or offering services.
package	A ROS project unit.	A directory with package.xml and code/resources that colcon can build.
topic	A message channel.	Named bus where nodes publish and subscribe to messages.
publisher	Message sender.	A node component that sends messages to a topic.
subscriber	Message receiver.	A node component that receives messages from a topic.
launch file	A start-up recipe.	Python/XML/YAML file describing which nodes and parameters to start.

# 9. Environment variables used in your case
Term / Command	Child-like meaning	Technical meaning
ROS_DISTRO	Which ROS version am I using?	Stores the active ROS distribution name, e.g. humble.
TURTLEBOT3_MODEL	Which TurtleBot model should load?	Used by TurtleBot3 packages to choose burger, waffle, or waffle_pi.
ROS_DOMAIN_ID	ROS classroom number.	DDS domain ID. Nodes with the same domain ID can discover and communicate with each other.
AMENT_PREFIX_PATH	ROS package search list.	List of install prefixes that ROS uses to find packages.
COLCON_PREFIX_PATH	Workspace chain list.	List of prefixes/underlays known to colcon setup files.
PATH	Command search list.	Folders where the shell looks for executable commands.
PYTHONPATH	Python import search list.	Folders where Python looks for modules/packages.
LD_LIBRARY_PATH	Library search list.	Folders where Linux looks for shared libraries at runtime.

# 10. Commands from the debugging process
These were the important commands used to find and fix the issue.
Find old workspace line in .bashrc:
grep turtlebot3_ws ~/.bashrc
Edit .bashrc:
nano ~/.bashrc
Comment the old workspace line:
#source ~/turtlebot3_ws/install/setup.bash
Add the Sedrica workspace to .bashrc:
echo "source ~/Sedrica/ros2_ws/install/setup.bash" >> ~/.bashrc
Reload .bashrc:
source ~/.bashrc
Check where ROS finds a package:
ros2 pkg prefix turtlebot3_teleop
Check if old workspace is still in package search paths:
echo $AMENT_PREFIX_PATH | tr ':' '\n' | grep turtlebot3_ws
Search inside Sedrica install folder for old workspace references:
grep -R "turtlebot3_ws" ~/Sedrica/ros2_ws/install -n | head
Clean old build output:
rm -rf build install log
Load only ROS Humble:
source /opt/ros/humble/setup.bash
Rebuild cleanly:
colcon build
Load the clean workspace:
source install/setup.bash
# 11. Why deleting build, install, and log fixed it
The wrong old workspace memory was stored inside the generated install folder. This happened because the Sedrica workspace was built while turtlebot3_ws was active.
rm -rf build install log
source /opt/ros/humble/setup.bash
colcon build
This deleted the old generated files and rebuilt the workspace from a clean Humble-only environment.
Final simple summary: The old workspace got stuck inside the new workspace. We removed the old memory by deleting build/install/log and rebuilding cleanly.
# 12. Safe final .bashrc example for your setup
A clean .bashrc section for your current Humble system can look like this:
export PATH=$HOME/.local/bin:$PATH

source /opt/ros/humble/setup.bash
source ~/Sedrica/ros2_ws/install/setup.bash

export ROS_DOMAIN_ID=30
export TURTLEBOT3_MODEL=burger
source /usr/share/gazebo/setup.sh
Avoid sourcing old workspaces unless you intentionally want to use them.
