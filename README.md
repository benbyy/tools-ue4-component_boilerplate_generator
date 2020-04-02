# tools-ue4-component_boilerplate_generator
An un-commented, spaghetti-filled, Python script that generates all that code you have to 
write for every component you add to your Actor class

Usage

Values:
('-C', '--class') Class Name of the Component you want
('-c', '--cat')  The UPROPERTY Category to assign
('-n', '--name') The name of the pointer to your new Component

Flags:
These configure the types of methods to generate and are set to False by default. 
These do not accept values. If a flag is included in the command, it will be set to True

NOTE: For '--root' , -r throws an exception, but '--root' works fine. Use that. 
  If you know what this happens, let me know! 

NOTE: '--root' will not be generated unless '--attach' is also set

('-g', '--get')   Create "Getter"
('-s', '--set')   Create "Setter"
('-a', '--attach') Setup Attachment to parent Actor
('-r', '--root')  Whether to make this component the Actor's RootComponent

Example Usage:
python component_code_gen.py --class UStaticMeshComponent --name MyStaticMesh --cat Physics -g -s -a --root
