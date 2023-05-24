# DESCRIPTION
 The pipeline consists of a Deep Learning framework - UNet implementation- for Medical Image (CT) Segmentation, Surface 3D Reconstruction, Mesh Optimization, Operative Assistance and 3D printing.


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
Here you can see the reconstructed and 3d printed mesh

![image](https://user-images.githubusercontent.com/81852029/209874035-5edd3dd6-f5ce-4f06-8d6e-5182b157ea33.png)
![image](https://user-images.githubusercontent.com/81852029/209874046-89eca555-57c8-4364-9e05-b5f72f91c3de.png)

Here you can see the pictures of operative assistance process:

![image](https://user-images.githubusercontent.com/81852029/209874120-97b111de-a20b-433a-8160-39ed925e6a20.png)
![image](https://user-images.githubusercontent.com/81852029/209874137-0765b394-ae9c-4124-b222-d55b13477457.png)
![image](https://user-images.githubusercontent.com/81852029/209874145-40aaa393-24c6-4e48-8cdd-303727c52e62.png)





