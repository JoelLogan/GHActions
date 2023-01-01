import os,shutil,yaml

actionlocation = '/.github/workflows'
actionnames = ['testbuild.yml']

home = os.getcwd()

os.makedirs(home + '/vulkan')
print('Made /vulkan')
os.chdir(home + '/vulkan')
print('Current Directory: ' + home)
os.popen('git clone https://github.com/KhronosGroup/Vulkan-Headers.git').read()
print('Vulkan Headers repo cloned')
os.chdir(home + '/Vulkan-Headers')
print('Current Directory: ' + os.getcwd())

version = os.popen('git describe --tags --abbrev=0').read().lstrip('v')

print("Latest version: " + version)

os.chdir(home)
shutil.rmtree("vulkan")

os.chdir(home + actionlocation)

for action in actionnames:
    checkedversion = ""
    actionfile = open(os.getcwd() + '/' + action)
    actionfileyaml = yaml.safe_load(actionfile)
    print("Loaded action file")
    for key, value in actionfileyaml.items():
        if "VULKAN_VERSION" in value:
            checkedversion = str(value)
            print("Found VULKAN_VERSION: "+ checkedversion[20:27])
            if (checkedversion[20:27] != version):
                actionfileyaml['env'] = {'VULKAN_VERSION': version}
                actionfile.close()
                print("Modified VULKAN_VERSION")
                with open(os.getcwd() + '/' + action, 'w') as modifiedactionfile:
                    yaml.dump(actionfileyaml, modifiedactionfile, sort_keys=False, default_flow_style=False)
                    modifiedactionfile.close()
                    print("Saved VULKAN_VERSION")
                modifiedfileread = open(os.getcwd() + '/' + action, 'r')
                fixedlines = ""
                for line in modifiedfileread:
                    new_line = line.replace('True: [', 'on: [')
                    fixedlines = fixedlines + new_line
                modifiedfilewrite = open(os.getcwd() + '/' + action, 'w')
                modifiedfilewrite.write(fixedlines)
                modifiedfilewrite.close()
                print("Fixed True to on")


print("Finished")
                

