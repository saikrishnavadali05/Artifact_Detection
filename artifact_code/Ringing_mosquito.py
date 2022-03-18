"""Code for Ringing and mosquito_noise artifacts."""
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import common_functions
import logging


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
    """Computing sum of Absolute Differences for each block."""
    sad = 0
    sad1 = 0
    sad2= 0
    for i in range(0,BLOCK_ROWS -1) :
        for j in range (0,BLOCK_COLS-1) :
            sad1 = np.abs(block[0][0] - block[1][0]) 
            sad2 = np.abs(block[0][0] - block[0][1])
            sad += sad1 + sad2
    return sad

def compute_blocks_sad(blocks):

    """This line "blocks_sads" I converted to the easy way by splitting """
    blocks_sads = np.array([[[0,0,0] for x in range(len(blocks[0]))] for x in range(len(blocks))])
    print(blocks_sads.shape)

    """This is the converted version of the above line everything is good but the dimensions are not matching"""
    """
    a = []
    r = np.array([0,0,0])    
    for x in range(len(blocks)):
        for x in range(len(blocks[0])):
            a.append(r)
    convert_arr = np.array(a)
    print(convert_arr.shape)
    """

    for i in range (0,len(blocks)):
        for j in range (0,len(blocks[i])):
            blocks_sads[i][j] =  compute_sad_for_block(blocks[i][j])
    return blocks_sads

def check_if_artifacted (blocks_sads):
    """The conditions to label a region"""
    F = blocks_sads < T_FLAT
    T = blocks_sads > T_TEX
    flat_top = (F[0][0].all() and F[0][1].all()) or (F[0][1].all() and F[0][2].all())
    flat_bottom = (F[2][0].all() and F[2][1].all()) or (F[2][1].all() and F[2][2].all())
    flat_left = (F[0][0].all() and F[1][0].all()) or (F[1][0].all() and F[2][0].all())
    flat_right = (F[0][2].all() and F[1][2].all()) or (F[1][2].all() and F[2][2].all())
    flat = flat_top or flat_bottom or flat_left or flat_right
    tex = False
    for i in range (0,len(T)):
        for j in range (0,len(T[i])):
            if i != 1 and j != 1:
                tex = tex or all(T[i][j])
    centre = ( T_FLAT < all(blocks_sads[1][1])) and (all(blocks_sads[1][1]) < T_TEX)
    artifacted = tex and flat and centre
    return artifacted

def check_artifacted_blocks (blocks_sads_map):
    """checking for the artifacted blocks"""
    artifacted_blocks =[]
    len_rows =  len(blocks_sads_map )-1
    for i in range(1,len_rows):
        for j in range(1,len(blocks_sads_map[i])-1):
            if check_if_artifacted(blocks_sads_map[i-1:i+2,j -1:j+2]):
                annoyance = blocks_sads_map[i][j]/((BLOCK_COLS-1)*(BLOCK_ROWS-1)*2)
                artifacted_blocks.append(ArtifactedBlock(i,j,annoyance))
    return artifacted_blocks

def highlight_image_artifacts(image,artifacted_blocks):
    """It is used for highlighting the artifacts on the image."""
    for block in artifacted_blocks:
        start_point = block.y*BLOCK_COLS,block.x*BLOCK_ROWS
        end_point = (block.y+1)*BLOCK_COLS,(block.x+1)*BLOCK_ROWS
        cv2.rectangle (image,start_point,end_point,(0,0,0))

if __name__ == '__main__':
    """The Main function to call all functions and returns total_artifacts_percentage,
    annoyance_score."""
    image_input_path = r"C:\Users\Vissamsetty Bharath\Documents\project_python\image-016.jpg"
    image_output_path = r"C:\Users\Vissamsetty Bharath\Documents\project_python\output.jpg"      
    print("reading image from source path"+ image_input_path)
    image = cv2.imread(image_input_path, cv2.IMREAD_COLOR)
    RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_array = np.array(RGB_img,dtype =np.int64)
    print(image_array.shape)
    rows,cols,char = image.shape
    blocks = common_functions.get_image_blocks(image_array , rows , cols)
    #print(blocks[0][2])
    #print(np.array(blocks[0][2]).shape)
    blocks_sads = compute_blocks_sad(blocks)
    artifacted_blocks = check_artifacted_blocks  (blocks_sads)
    #print(artifacted_blocks)
    #print(blocks_sads)
    annoyance_score = np.average(common_functions.compute_overall_annoyance(artifacted_blocks))
    print ('Annoyance Score:',f'{annoyance_score:.2f}')
    total_artifacts_percentage = np.float_(len(artifacted_blocks)) / np.float_((rows / BLOCK_ROWS)
    *( cols / BLOCK_COLS))*100
    print ('Artifacted Edges:',f'{total_artifacts_percentage:.2f}')
    highlight_image_artifacts(image,artifacted_blocks)
    cv2.imwrite(image_output_path,image)



    """this code for only output image on the screen"""
    """
    plt.subplot(1,2,1)
    plt.imshow(RGB_img)
    plt.subplot(1,2,2)
    plt.imshow(blocks[0][0])
    plt.show()
    """