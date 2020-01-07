#!/bin/bash
folder_dir=("Semisphere" "Cuboid" "Cylinder" "Ring" "Sphere" "Stick")

for folder in ${folder_dir[@]}; do
	if [ -d "$folder"]; then
		rm "$folder"_obj/*.obj
	else 
		mkdir "$folder"_obj
	fi

	for file in "$folder"/*.stl ; do
		extensionless=$(basename -s .stl "$file")
		assimp export "$folder"/"$extensionless".stl "$folder"_obj/"$extensionless".obj
	done
	rm "${folder}"_obj/*.mtl
	
done
