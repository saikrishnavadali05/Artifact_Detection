"""Code for Ringing and mosquito_noise artifacts."""
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import common_functions


"""Constant values that can be used in this program."""
BLOCK_ROWS = common_functions.BLOCK_ROWS
BLOCK_COLS = common_functions.BLOCK_COLS
KERNEL_X = 3
KERNEL_Y = 3
T_FLAT = True
T_TEX =  False

class ArtifactedBlock:
    """It assigns values to the variables x,y and annoyance."""
    def __init__(self,x_coord,y_coord,annoyance):
        self.x = x_coord
        self.y = y_coord
        self.annoyance = annoyance
       
def compute_sad_for_block(block):
    """Computing sum of Absolute Differences for each block"""
    sad = sad1 = sad2 = 0
    count = 0
    for i in range(0,BLOCK_ROWS -1) :
        for j in range (0,BLOCK_COLS-1) :
            sad1 = np.abs(block[i][j] - block[i+1][j])
            sad2 = np.abs(block[i][j] - block[i][j+1])
            sad = sad + sad1 + sad2
            count =count + 1
    print(count)
    return sad

def compute_blocks_sad(blocks):
    """Computing sum of Absolute Differences for blocks."""
    count = 0
    blocks_sads = np.array([[[0,0,0]for x in range(len(blocks[0]))]for x in range(len(blocks))]) 
    for i in range(0,len(blocks)):
        for j in range(0,len(blocks[i])):
            blocks_sads[i][j] = compute_sad_for_block(blocks[i][j])
            count = count + 1
    print(count)
    return blocks_sads,count

def measure_artifacts(image_path,output_path):
    """The Main function to call all functions and returns total_artifacts_percentage,
    annoyance_score."""
    print("reading image from source path"+ image_path)
    image = cv2.imread(image_path)
    image_array = np.array(image,dtype =np.int64)
    rows,cols,char = image.shape
    blocks = common_functions.get_image_blocks(image , rows , cols)
    blocks1 = np.array(blocks)
    #print(blocks1.shape)
    #print(len(blocks),len(blocks[0]))
    #print(blocks)
    blocks_sads = compute_sad_for_block(blocks)
    #blocks_sads = compute_blocks_sad(blocks)
    print(blocks_sads,"2")


image_output = measure_artifacts(
    r"C:\Users\Vissamsetty Bharath\Documents\project_python\image-016.jpg"
    ,r"C:\Users\Vissamsetty Bharath\Documents\project_python\output.jpg")

















"""

    #imgplot = plt.imshow(image)
    #plt.show()





        annoyance_score = np.average(compute_overall_annoyance(artifacted_blocks))
    print ('Annoyance Score:',f'{annoyance_score:.2f}')
    total_artifacts_percentage = np.float_(len(artifacted_blocks)) / np.float_((rows / BLOCK_ROWS)
    *( cols / BLOCK_COLS))*100
    print ('Artifacted Edges:',f'{total_artifacts_percentage:.2f}')
    highlight_image_artifacts(image,artifacted_blocks)
    cv2.imwrite(output_path,image)
    return (total_artifacts_percentage,annoyance_score)
"""