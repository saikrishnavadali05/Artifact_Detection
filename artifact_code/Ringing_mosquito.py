"""Code for Ringing and mosquito_noise artifacts."""
import time
from cv2 import cv2
import numpy as np
import common_functions


#Constant values that can be used in this program.
BLOCK_ROWS = common_functions.BLOCK_ROWS
BLOCK_COLS = common_functions.BLOCK_COLS
KERNEL_X = 3
KERNEL_Y = 3
T_FLAT = common_functions.T_FLAT
T_TEX =  common_functions.T_TEX


class ArtifactedBlock:
    """It assigns values to the variables x,y and annoyance."""
    x = None
    y = None
    annoyance = None
    def __init__(self, x_coord, y_coord, annoyance):
        self.x = x_coord
        self.y = y_coord
        self.annoyance = annoyance


def compute_sad_for_block(block):
    """Computing sum of Absolute Differences for each block."""
    sad = sad1 = sad2 = 0
    for i in range(0, BLOCK_ROWS -1):
        for j in range (0, BLOCK_COLS-1):
            sad1 = np.abs(block[i][j] - block[i+1][j])
            sad2 = np.abs(block[i][j] - block[i][j+1])
            sad += sad1 + sad2
    return sad


def compute_blocks_sad(blocks):
    """Computing sum of Absolute Differences for a group of block """
    blocks_sads = np.array([[[0, 0, 0] for x in range(len(blocks[0]))] for x in range(len(blocks))])
    for i in range (0, len(blocks)):
        for j in range (0, len(blocks[i])):
            blocks_sads[i][j] =  compute_sad_for_block(blocks[i][j])
    return blocks_sads


def check_if_artifacted (blocks_sads):
    """The conditions to label a region"""
    F_threshold = blocks_sads < T_FLAT
    T_threshold  = blocks_sads > T_TEX
    flat_top = (F_threshold[0][0].all() and F_threshold[0][1].all()) or (F_threshold[0][1].all()
    and F_threshold[0][2].all())
    flat_bottom = (F_threshold[2][0].all() and F_threshold[2][1].all()) or (F_threshold[2][1].all()
    and F_threshold[2][2].all())
    flat_left = (F_threshold[0][0].all() and F_threshold[1][0].all()) or (F_threshold[1][0].all()
    and F_threshold[2][0].all())
    flat_right = (F_threshold[0][2].all() and F_threshold[1][2].all()) or (F_threshold[1][2].all()
    and F_threshold[2][2].all())
    flat = flat_top or flat_bottom or flat_left or flat_right
    tex = False
    for i in range (0, len(T_threshold)):
        for j in range (0, len(T_threshold[i])):
            if i != 1 and j != 1:
                tex = tex or all(T_threshold[i][j])
    centre = (T_FLAT < blocks_sads [1][1]).all () and (blocks_sads [1][1] < T_TEX ).all ()
    artifacted = tex and flat and centre
    return artifacted


def check_artifacted_blocks (blocks_SADs_map):
    """The function is used to check on the entire image"""
    artifacted_blocks = []
    for i in range (1, len ( blocks_SADs_map ) - 1):
        for j in range (1, len ( blocks_SADs_map [i]) - 1):
            if check_if_artifacted ( blocks_SADs_map [i -1:i+2, j -1:j +2]) :
                annoyance = blocks_SADs_map [i][j ]/(( BLOCK_COLS -1) *(BLOCK_ROWS -1) *2)
                artifacted_blocks.append( ArtifactedBlock (i,j, annoyance ))
    return artifacted_blocks


if __name__ == '__main__':
    #The Main function to call all functions and returns total_artifacts_percentage,annoyance_score.
    start = time.time()
    image_input_path = r"C:\Users\Vissamsetty Bharath\Documents\project_python\Ringing_mosquito_test1.jpg"
    image_output_path = r"C:\Users\Vissamsetty Bharath\Documents\project_python\output_image.jpg"
    print("reading image from source path"+ image_input_path)
    common_functions.log_artifact('Image has read from source - Step - 1')
    image = cv2.imread(image_input_path, cv2.IMREAD_COLOR)
    image_array = np.array(image, dtype =np.int64)
    rows,cols,char = image.shape
    blocks = common_functions.get_image_blocks(image_array, rows, cols)
    common_functions.log_artifact('executed get_image_blocks function - Step - 2')
    blocks_sads = compute_blocks_sad(blocks)
    common_functions.log_artifact('executed compute_blocks_sad function - Step - 3')
    artifacted_blocks = check_artifacted_blocks(blocks_sads)
    print("The threshold values for Flat Threshold and Textural Threshold ", T_FLAT,T_TEX)
    common_functions.log_artifact('executed check_artifacted_blocks function - Step - 4')
    common_functions.log_artifact('output the values of Annoyance Score and Artifacted Edges - Step - 5')
    annoyance_score = np.average(common_functions.compute_overall_annoyance(artifacted_blocks))
    print ('Annoyance Score:', f'{annoyance_score}')
    total_artifacts_percentage = np.float_(len(artifacted_blocks)) / np.float_((rows / BLOCK_ROWS)
    *( cols / BLOCK_COLS))*100
    print ('Artifacted Edges:', f'{total_artifacts_percentage}')
    common_functions.highlight_image_artifacts(image, artifacted_blocks)
    common_functions.log_artifact('artifact is highlighted on image - Step - 6')
    common_functions.log_artifact('writing image into output file - Step - 7')
    cv2.imwrite(image_output_path, image)
    end = time.time()
    print("The time of execution of the whole program is :", end-start)
