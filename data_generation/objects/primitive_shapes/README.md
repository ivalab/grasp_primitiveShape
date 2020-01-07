# Primitive shapes
Primitive shapes generated automatically from Matlab code

Because the Matlab scripts output ```.stl``` files, the bash
script ```convert.sh``` will convert all the file with `.obj` extension, which is the format required for using them in V-rep.

Run ``` convert.sh``` in the terminal if there is no .obj files
(Note that the folder must be created for the generation)
The bash script will recursively find all the .stl file and proceed by converting and moving them into the [shape]_obj folder.

Please install the asimp package first via ```sudo apt-get install assimp-utils```
