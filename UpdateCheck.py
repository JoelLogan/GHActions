import os

version = "" # Use this to override the vulkan version.

# Get most recent Vulkan version.

if not version:
	print("Using latest Vulkan version.")
	tags = [i.split('/')[-1] for i in os.popen("git ls-remote --tags https://github.com/KhronosGroup/Vulkan-Headers.git").read().split()[1::2]]
	for i in tags:
		if i[0] == 's' and i[-1].isdigit():
			new_version = i[4:]
			if new_version > version:
				version = new_version
				
else:
	print("Using version override!")

# Install the most recent Vulkan version.
print("Installing Vulkan v" + str(version))
os.system("sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test;wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo apt-key add -;wget -qO /etc/apt/sources.list.d/lunarg-vulkan-" + str(version) + "-focal.list https://packages.lunarg.com/vulkan/" + str(version) + "/lunarg-vulkan-" + str(version) + "-focal.list;sudo apt install vulkan-sdk")
