from difflib import diff_bytes
from PIL import Image

import cv2
import logging
import numpy as np
import time

logging.basicConfig(filename = 'logs/blockiness_logs.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

#global varibles
block_rows = 8
block_cols = 8
horizontal = 1
verticle = 2
blockiness_low_threshold = 2
blockiness_high_threshold = 3

class ArtifactedEdge:
    point1 = None
    point2 = None
    annoyance = None

    def __init__(self,point1,point2,annoyance):
        self.point = point1
        self.point = point2
        self.annoyance = annoyance


def highlight_image_artifacts(img,artifacted_edges):
    logging.info('Highlighting Image Artifacts...')
    for edge in artifacted_edges:
        cv2.line(img,edge.point1,edge.point2,(0,0,0))
    logging.info('Highlighted Image Artifacts')

def compute_overall_annoyance(artifacted_edges):
    logging.info('Computing Overall Annoyance...')
    annoyance = 0
    if len(artifacted_edges) != 0:
        for edge in artifacted_edges:
            annoyance += edge.annoyance
        logging.info('Computed Overall Annoyance')
        return annoyance/len(artifacted_edges)
    else:
        logging.info('Computed Overall Annoyance')
        return 0

def has_low_pixel_variation(pixel,pixel_array,diff):
    logging.info('Computing Low Pixel Variation...')
    for x in pixel_array:
        current_diff = np.abs(pixel-x)
        if not (np.greater_equal(current_diff,diff-3).all()\
             and np.greater_equal(diff+3,current_diff).all()):
            logging.info('Computed low pixel variation')
            return False
    logging.info('Computed low pixel variation')
    return True

def compute_edge_annoyance(first_block,second_block,direction):
    logging.info('Computing Edge Annoyance...')
    if direction == verticle:
        logging.info('Computed Edge Annoyance@verticle')
        return np.average(np.abs(second_block[0:1,0:block_cols]\
            -first_block[block_rows-1:block_rows,0:block_cols]),axis = 1)

    if direction == horizontal:
        logging.info('Computed Edge Annoyance@horizontal')
        return np.average(np.abs(second_block[0:block_rows,0:1]-\
            first_block[0:block_rows,block_cols-1:block_cols]),axis = 0)

def check_blockiness(first_block,second_block,direction):
    logging.info('Computing Blockiness...')
    total_blockiness = 0
    size = len(first_block)
    blockiness = []

    for x in range(0,size):
        current_blockiness = 0
        if direction == verticle:
            boundary_slope = np.abs(second_block[0][x]-first_block[size-1][x])
            if not has_low_pixel_variation\
                (first_block[size-1][x],second_block[0:size-1,x:x+1],boundary_slope)\
                or not has_low_pixel_variation\
                    (second_block[0][x],first_block[0:size-1,x:x+1],boundary_slope):
                return False

            first_slope = np.abs(first_block[size-1][x] - first_block[size-2][x])
            second_slope = np.abs(second_block[1][x] - second_block[0][x])
            current_blockiness = boundary_slope - np.float_(first_slope + second_slope)/2

        if direction == horizontal:
            boundary_slope = np.abs(second_block[x][0]-first_block[x][size-1])
            if not has_low_pixel_variation\
                (first_block[x][size-1],second_block[x:x+1,0:size-1],boundary_slope)\
                or not has_low_pixel_variation\
                    (second_block[x][0],first_block[x:x+1,0:size-1],boundary_slope):
                return False

            first_slope = np.abs(first_block[x][size-1] - first_block[x][size-2])
            second_slope = np.abs(second_block[x][1] - second_block[x][0])
            current_blockiness = boundary_slope - np.float_(first_slope + second_slope)/2

        if np.greater(blockiness_low_threshold,np.float_(current_blockiness)).all()\
            or np.greater(np.float_(current_blockiness),blockiness_high_threshold).all():
                return False

        total_blockiness += current_blockiness
        blockiness.append(current_blockiness)

    total_blockiness = np.float_(total_blockiness)/np.float_(size)

    for b in blockiness:
        if np.greater(np.abs(total_blockiness - b),2).any():
            return False

    blocked = blockiness_low_threshold <= total_blockiness [0] <= blockiness_high_threshold\
                and total_blockiness[1] <= blockiness_high_threshold \
                and total_blockiness[2] <= blockiness_high_threshold \
                or (blockiness_low_threshold <= total_blockiness[1] <= blockiness_high_threshold\
                    and total_blockiness[0] <= blockiness_high_threshold\
                    and total_blockiness[2] <= blockiness_high_threshold)\
                or (blockiness_low_threshold <= total_blockiness[2] <= blockiness_high_threshold \
                    and total_blockiness[0] <= blockiness_high_threshold\
                    and total_blockiness[1] <= blockiness_high_threshold)
    logging.info('Computed Blockiness')
    return blocked

def get_artifacted_edges(blocks):
    logging.info('Fetching Artifacted Edges...')
    artifacted_edges = []
    for i in range(0,int(len(blocks)-1)):
        for j in range(0,len(blocks[i])-1):
            right_blocked = check_blockiness(blocks[i][j],blocks[i][j+1],horizontal)
            if right_blocked:
                annoyance = compute_edge_annoyance(blocks[i][j],blocks[i+1][j],horizontal)
                artifacted_edges.append(ArtifactedEdge(((j+1) \
                    *block_cols,i*block_rows),((j+1)*block_cols,(i+1)*block_rows),annoyance))

            bottom_blocked = check_blockiness(blocks[i][j],blocks[i][j+1],verticle)
            if bottom_blocked:
                annoyance = compute_edge_annoyance(blocks[i][j],blocks[i+1][j],verticle)
                artifacted_edges.append(ArtifactedEdge(((j+1)\
                    *block_cols,i*block_rows),((j+1)*block_cols,(i+1)*block_rows),annoyance))
    logging.info('Fetched Artifacted Edges')
    return artifacted_edges

def get_image_blocks(image):
    blocks = []
    rows,cols,ch = image.shape
    logging.info('Fetching Image Blocks...')
    for i in range(0,int(rows/block_rows)):
        blocks.append([])
        for j in range(0,int(cols/block_cols)):
            blocks[i].append(image[i*block_rows:(i+1)*block_rows,j*block_cols:(j+1)*block_cols])
    logging.info('Fetcted Image Blocks ')
    return blocks

if __name__ == "__main__" :
    startTime = time.time()
    logging.info('Main-Page')
    img = Image.open('blockiness_test.jpeg')
    img_array = np.array(img)
    rows,cols,ch = img_array.shape
    blocks = get_image_blocks(img_array)
    artifacted_edges = get_artifacted_edges(blocks)

    annoyance_score = np.average(compute_overall_annoyance(artifacted_edges))
	#print(annoyance_score)

    total_artifacts_percentage = np.float_(len(artifacted_edges))\
        /np.float_(((rows/block_rows)*(cols/block_cols)*2))*100
	#print(total_artifacts_percentage)

    highlight_image_artifacts(img, artifacted_edges)
	#cv2.imwrite("Desktop/SWAMIwork/Artifact_Detection/output",img)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))