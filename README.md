# Project work (group 1) from Defragmentation Workshop from October 2022

### Group members: 
- Daniel Waiger 
- Camille Loiseau 
- Tatiana Woller 
- Anna Agafonova 
- Gayathri Nadar

This project would not have been successful without the friendly collaboration of the team members :)


### Analysis Goal
- Segment 'only' the cytoplasm (neurons) in confocal single slice mouse brain images with no nuclei stain. 

### Workflow 
1. `save_tiff.py`: save the images saved in propietary format into tiff for easy accessibility by other programs. The channels are split and saved separately. Works on a folder of images. 
2. `cytoplasm_segmentation.ipynb`: 
    - Read images in folder, randomly pick one for training an Object classifier in napari-devbio package.
    - Initially training could be done by adding labels in napari window.
    - Option to also load labels from image file - possibly saved using napari > labels > save as image.
    - We **train a classifier** to identify cytoplasm region in cells.
    - The classifier is saved to disk.
3. `batch_prediction_using_classifier.ipynb`: 
    - Read images in folder, read classifier model 
    - Apply to images in the folder in a loop and save label maps of the segmentation.
    
### Images 
- Images used for training: 2D, single channel containing the cytoplasm 

 
