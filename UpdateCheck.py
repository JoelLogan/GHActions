import os

vulkan_version = "" # Use this to override the Vulkan version.
ubuntu_codename = "" # Use this to override the ubuntu codename.

# Get most recent Vulkan version.

valid_tags = []
for i in [i.split('/')[-1] for i in os.popen("git ls-remote --tags https://github.com/KhronosGroup/Vulkan-Headers.git").read().split()[1::2]]:
	if i[0] == 's' and i[-1].isdigit():
		valid_tags.append(i[4:-2])
		
if not vulkan_version:
	print("Using latest Vulkan version: v", end="")
	for i in valid_tags:
		if i > vulkan_version:
			vulkan_version = i
else:
	if vulkan_version not in valid_tags:
		raise Exception("Vulkan version: Overridden Vulkan version is not valid. Please select a valid Vulkan version. Valid Vulkan versions:\n" + str(valid_tags))
	print("Using Vulkan version override: v", end="")
print(vulkan_version)

# Get the current Ubuntu Codename.

if not ubuntu_codename:
	if os.path.exists("/etc/os-release"):
		file = "/etc/os-release"
	if os.path.exists("/etc/lsb-release"):
		file = "/etc/lsb-release"
	else:
		raise Exception("Ubuntu codename: Ubuntu codename not found. Please verify that this script is executing in an Ubuntu environment. If so, provide a codename override.")
	print("Using current Ubuntu codename: ", end="")
	
	with open(file, "r") as f:
		ubuntu_codename = f.read().split("CODENAME=")[-1].split("\n")[0]
else:
	print("Using Ubuntu codename override: ", end="")
print(ubuntu_codename)

# Generate the Vulkan install script.

with open("InstallVulkan.sh", "w") as f:
	f.write("wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo apt-key add -\nsudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-" + str(vulkan_version) + "-" + str(ubuntu_codename) + ".list https://packages.lunarg.com/vulkan/" + str(vulkan_version) + "/lunarg-vulkan-" + str(vulkan_version) + "-" + str(ubuntu_codename) + ".list\nsudo apt update\nsudo apt install vulkan-sdk")
