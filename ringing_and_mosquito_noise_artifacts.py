"""Code for Ringing and mosquito_noise artifacts."""

import numpy as np
from cv2 import cv2

BLOCK_ROWS = 5
BLOCK_COLS = 5
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

def highlight_image_artifacts(image,artifacted_blocks):
    """It is used for highlighting the artifacts on the image."""
    for block in artifacted_blocks:
        start_point = block.y*BLOCK_COLS,block.x*BLOCK_ROWS
        end_point = (block.y+1)*BLOCK_COLS,(block.x+1)*BLOCK_ROWS
        cv2.rectangle (image,start_point,end_point,(0,0,0))

def compute_overall_annoyance(artifacted_blocks):
    """Calculating the total visibility of the image and return the values as int type."""
    annoyance = 0
    if len(artifacted_blocks) != 0:
        for block in artifacted_blocks:
            annoyance += block.annoyance
        return annoyance / len(artifacted_blocks)
    else:
        return 0

def check_if_artifacted (blocks_sads):
    """The conditions to label a region"""
    F = blocks_sads < T_FLAT
    T = blocks_sads > T_TEX
    flat_top = (all(F[0][0]) and all(F[0][1])) or (all(F[0][1]) and all(F[0][2]))
    flat_bottom = (all(F[2][0]) and all(F[2][1])) or (all(F[2][1]) and all(F[2][2]))
    flat_left = (all(F[0][0]) and all(F[1][0])) or (all(F[1][0]) and all(F[2][0]))
    flat_right = (all(F[0][2]) and all(F[1][2])) or (all(F[1][2]) and all(F[2][2]))
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
    for i in range(1,len(blocks_sads_map )-1):
        for j in range(1,len(blocks_sads_map[i])-1):
            if check_if_artifacted(blocks_sads_map[i-1:i+2,j -1:j+2]):
                annoyance = blocks_sads_map[i][j]/((BLOCK_COLS-1)*(BLOCK_ROWS-1)*2)
                artifacted_blocks.append(ArtifactedBlock(i,j,annoyance))
    return artifacted_blocks

def compute_sad_for_block(block):
    """Computing sum of Absolute Differences for each block"""
    sad = 0
    for i in range(0,BLOCK_ROWS -1) :
        for j in range (0,BLOCK_COLS-1) :
            sad += np.abs(block[i][j] - block[i+1][j]) + np.abs(block[i][j]- block[i][j+1])
        type(sad)
    return sad

def compute_blocks_sad(blocks):
    """Computing sum of Absolute Differences for blocks."""
    blocks_sads = np.array([[[0,0,0]for x in range(len(blocks[0]))]for x in range(len(blocks))])
    for i in range(0,len(blocks)):
        for j in range(0,len(blocks[i])):
            blocks_sads[i][j] = compute_sad_for_block(blocks[i][j])
    return blocks_sads

def get_image_blocks(image,rows,cols):
    """Getting the block from the image."""
    blocks = []
    for i in range(0,int (rows / BLOCK_ROWS)):
        blocks.append([])
        for j in range(0,int(cols / BLOCK_COLS)):
            blocks[i].append(image[i*BLOCK_ROWS :(i+1)*BLOCK_ROWS ,j*BLOCK_COLS:(j+1)*BLOCK_COLS])
    return blocks

def measure_artifacts(image_path,output_path):
    """The Main function to call all functions and returns total_artifacts_percentage,
    annoyance_score."""
    image = cv2.imread(image_path)
    image_array = np.array(image,dtype =np.int64)
    print("reading image "+ image_path)
    rows,cols,char = image.shape
    blocks = get_image_blocks(image_array,rows,cols)
    blocks_sads = compute_blocks_sad(blocks)
    artifacted_blocks = check_artifacted_blocks(blocks_sads)
    annoyance_score = np.average(compute_overall_annoyance(artifacted_blocks))
    print ('Annoyance Score:',f'{annoyance_score:.2f}')
    total_artifacts_percentage = np.float_(len(artifacted_blocks)) / np.float_((rows / BLOCK_ROWS)
    *( cols / BLOCK_COLS))*100
    print ('Artifacted Edges:',f'{total_artifacts_percentage:.2f}')
    highlight_image_artifacts(image,artifacted_blocks)
    cv2.imwrite(output_path,image)
    return (total_artifacts_percentage,annoyance_score)

image_output = measure_artifacts(
    r"C:\Users\Vissamsetty Bharath\Documents\project_python\image-016.jpg"
    ,r"C:\Users\Vissamsetty Bharath\Documents\project_python\output.jpg")
