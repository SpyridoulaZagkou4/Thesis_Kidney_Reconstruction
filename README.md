# PIPELINE 

![Screenshot 2022-12-16 112350](https://user-images.githubusercontent.com/81852029/208066328-5c4f0c2f-de5d-48a6-a76d-9c9ec8202602.png)


# REQUIREMENTS
1. Tensorflow
2. miscnn
3. vedo
4. vtk
5. SimpleITK
6. numpy
7. math
8. matplotlib
9. pymeshlab
10. nibabel

# USAGE

First you have to download kits19 dataset from this repository: https://github.com/neheller/kits19 and then you have to add the path of the dataset to 
```segmentation.py``` notebook to the data_path variable.

For the 3d printing preprocessing you have to create a .json file that will contain the paths for all nifti & stl files that you create during the processes
(reconstruction, merging, cropping, hole filling,..).

For the process of operative assistance you have to run ```preoperative_planning.py``` by only adding the paths for stl files for kidney and tumor. To see the consecutive steps you can press space button.


# RESULTS



