import cv2
from difflib import diff_bytes
import numpy as np
from PIL import Image

#global varibles
block_rows = 8
block_cols = 8
horizontal = 1
verticle = 2

class ArtifactedEdge:
        point1 = None
        point2 = None
        annoyance = None

        def __init__(self,point1,point2,annoyance):
                self.point = point1
                self.point = point2
                self.annoyance = annoyance

def highlight_image_artifacts(img,artifacted_edges):
        for edge in artifacted_edges:
                cv2.line(img,edge.point1,edge.point2,(0,0,0))

def compute_overall_annoyance(artifacted_edges):
        annoyance = 0
        if len(artifacted_edges) != 0:
                for edge in artifacted_edges:
                        annoyance += edge.annoyance
                return annoyance/len(artifacted_edges)
        else:
                return 0

def has_low_pixel_variation(pixel,pixel_array,diff):
        for x in pixel_array:
                current_diff = np.abs(pixel-x)
                if not (np.greater_equal(current_diff,diff-3).all() and np.greater_equal(diff+3,current_diff).all()):
                        return False
        return True

def compute_edge_annoyance(first_block,second_block,direction):
        if direction == verticle:
                return np.average(np.abs(second_block[0:1,0:block_cols]-first_block[block_rows-1:block_rows,0:block_cols]),axis = 1)
        
        if direction == horizontal:
                return np.average(np.abs(second_block[0:block_rows,0:1]-first_block[0:block_rows,block_cols-1:block_cols]),axis = 0)

def check_blockiness(first_block,second_block,direction):
        total_blockiness = 0
        size = len(first_block)
        blockiness = []
        #TOBECODED

def get_artifacted_edges(blocks):
        artifacted_edges = []
        for i in range(0,int(len(blocks)-1)):
                for j in range(0,len(blocks[i])-1):
                        right_blocked = check_blockiness(blocks[i][j],blocks[i][j+1],horizontal)
                        if right_blocked:
                                annoyance = compute_edge_annoyance(blocks[i][j],blocks[i+1][j],horizontal)
                                artifacted_edges.append(ArtifactedEdge(((j+1)*block_cols,i*block_rows),((j+1)*block_cols,(i+1)*block_rows),annoyance))

                        bottom_blocked = check_blockiness(blocks[i][j],blocks[i][j+1],verticle)
                        if bottom_blocked:
                                annoyance = compute_edge_annoyance(blocks[i][j],blocks[i+1][j],verticle)
                                artifacted_edges.append(ArtifactedEdge(((j+1)*block_cols,i*block_rows),((j+1)*block_cols,(i+1)*block_rows),annoyance))

def get_image_blocks(image):
        blocks = []
        rows,cols,ch = image.shape

        for i in range(0,int(rows/block_rows)):
                blocks.append([])
                for j in range(0,int(cols/block_cols)):
                        blocks[i].append(image[i*block_rows:(i+1)*block_rows,j*block_cols:(j+1)*block_cols])
        return blocks

def measure_artifacts(img):
        img_array = np.array(img)
        rows,cols,ch = img_array.shape
        blocks = get_image_blocks(img_array)
        artifacted_edges = get_artifacted_edges(blocks)

if __name__ == "__main__" :
        img = Image.open('test.jpeg')
        measure_artifacts(img)
