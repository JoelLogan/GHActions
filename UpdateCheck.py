import os

version = "" # Use this to override the vulkan version.

# Get most recent Vulkan version.

if not version:
	print("Using latest Vulkan version.")
	tags = [i.split('/')[-1] for i in os.popen("git ls-remote --tags https://github.com/KhronosGroup/Vulkan-Headers.git").read().split()[1::2]]
	for i in tags:
		if i[0] == 's' and i[-1].isdigit():
			new_version = i[4:-2]
			if new_version > version:
				version = new_version
else:
	print("Using version override!")

# Write the vulkan version to a file
with open("InstallVulkan.sh", "w") as f:
	f.write("wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo apt-key add -\nsudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-" + str(version) + "-focal.list https://packages.lunarg.com/vulkan/" + str(version) + "/lunarg-vulkan-" + str(version) + "-focal.list\nsudo apt update\nsudo apt install vulkan-sdk")
