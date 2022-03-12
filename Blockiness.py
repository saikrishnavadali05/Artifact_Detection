"""
This code is extracted directly from the research paper.
"""
#code for Blockiness

import numpy as np
import cv2

BLOCK_ROWS = 8
BLOCK_COLS = 8
HORIZONTAL_DIRECTION = 1
VERTICAL_DIRECTION = 2
BLOCKINESS_LOW_THRESHOLD = 2
BLOCKINESS_HIGH_THRESHOLD = 3

class ArtifactedEdge:
    point1 = None
    point2 = None
    annoyance = None
    def __init__ (self , point1 , point2 , annoyance) :
        self.point1 = point1
        self.point2 = point2
        self.annoyance = annoyance

def highlight_image_artifacts( image , artifacted_edges ) :
    for edge in artifacted_edges :
        cv2.line( image , edge.point1 , edge.point2 , (0 , 0 , 0) )

def compute_overall_annoyance( artifacted_edges ) :
    annoyance = 0
    if len ( artifacted_edges ) != 0:
        for edge in artifacted_edges :
            annoyance += edge . annoyance
        return annoyance / len ( artifacted_edges )
    else :
        return 0
  
def compute_edge_annoyance(first_block , second_block , direction) :
    if direction == VERTICAL_DIRECTION :
        return np . average ( np . abs ( second_block [0:1 , 0: BLOCK_COLS ] -
      first_block [ BLOCK_ROWS -1: BLOCK_ROWS , 0: BLOCK_COLS ]) , axis =1)
    if direction == HORIZONTAL_DIRECTION :
        return np . average ( np . abs ( second_block [0: BLOCK_ROWS , 0:1] -
      first_block [0: BLOCK_ROWS , BLOCK_COLS -1: BLOCK_COLS ]) , axis =0)

def has_low_pixel_variation(pixel , pixel_array , diff) :
    for x in pixel_array :
        current_diff = np . abs ( pixel - x )
        if not ( np . greater_equal ( current_diff , diff -3) . all () \
      and np . greater_equal ( diff +3 , current_diff ) . all () ) :
            return False
    return True

def check_blockiness ( first_block , second_block , direction ) :
    total_blockiness = 0
    size = len ( first_block )
    blockinesses = []
    for x in range (0 , size ) :
        current_blockiness = 0
        if direction == VERTICAL_DIRECTION :
            boundary_slope = np . abs ( second_block [0][ x ] - first_block [ size-1][ x ])
            if not has_low_pixel_variation(first_block[ size -1][ x ] ,
        second_block[0: size -1 , x : x +1] , boundary_slope ) \
          or not has_low_pixel_variation(second_block[0][x] ,
            first_block[0: size -1 , x : x +1] , boundary_slope ) :
                return False
            first_slope = np . abs ( first_block [ size -1][ x ] - first_block [ size -2][ x ])
            second_slope = np . abs ( second_block [1][ x ] - second_block [0][ x ])
            current_blockiness = boundary_slope - np . float_ ( first_slope +second_slope ) /2
        elif direction == HORIZONTAL_DIRECTION :
            boundary_slope = np . abs ( second_block [ x ][0] - first_block [ x ][ size-1])
            if not has_low_pixel_variation( first_block [ x ][ size -1] ,
        second_block [ x : x +1 , 0: size -1] , boundary_slope ) \
          or not has_low_pixel_variation( second_block [ x ][0] ,
            second_block [ x : x +1 , 0: size -1] , boundary_slope ) :
                return False
            first_slope = np.abs(first_block[x][size -1] - first_block[ x ][size -2])
            second_slope = np.abs( second_block [ x ][1] - second_block [ x ][0])
            current_blockiness = boundary_slope-np.float_(first_slope+second_slope)/2

        if np.greater(BLOCKINESS_LOW_THRESHOLD,np.float_( current_blockiness
        ) ) . all () \
              or np.greater( np.float_(current_blockiness) ,
                  BLOCKINESS_HIGH_THRESHOLD ) . all () :
            return False

        total_blockiness += current_blockiness
        blockinesses.append(current_blockiness)
    total_blockiness = np . float_ (total_blockiness)/np.float_(size)
    for b in blockinesses :
        if np.greater( np.abs(total_blockiness - b),2).any() :
            return False

    blocked = (BLOCKINESS_HIGH_THRESHOLD<= total_blockiness [0] <=
    BLOCKINESS_HIGH_THRESHOLD\
      and total_blockiness [1] <= BLOCKINESS_HIGH_THRESHOLD\
      and total_blockiness [2] <= BLOCKINESS_HIGH_THRESHOLD)\
        or (BLOCKINESS_LOW_THRESHOLD<= total_blockiness [1] <=
            BLOCKINESS_HIGH_THRESHOLD\
            and total_blockiness [0] <= BLOCKINESS_HIGH_THRESHOLD\
           and total_blockiness [2] <= BLOCKINESS_HIGH_THRESHOLD) \
        or (BLOCKINESS_LOW_THRESHOLD <= total_blockiness [2] <=
            BLOCKINESS_HIGH_THRESHOLD\
            and total_blockiness [0] <= BLOCKINESS_HIGH_THRESHOLD\
            and total_blockiness [1] <= BLOCKINESS_HIGH_THRESHOLD)
    return blocked


def get_artifacted_edges(blocks) :
    artifacted_edges = []
    for i in range (0 , len(blocks ) - 1) :
        for j in range (0 , len (blocks [ i ]) - 1) :
            right_blocked = check_blockiness ( blocks [ i ][ j ] , blocks [ i ][ j +1] ,HORIZONTAL_DIRECTION )
        if right_blocked :
            annoyance = compute_edge_annoyance(blocks [ i ][ j ] , blocks [ i ][ j+1] , HORIZONTAL_DIRECTION)
            artifacted_edges . append ( ArtifactedEdge ((( j +1) * BLOCK_COLS , i *BLOCK_ROWS ) , (( j +1) * BLOCK_COLS , ( i +1) * BLOCK_ROWS ) ,annoyance ) )
        bottom_blocked = check_blockiness ( blocks [ i ][ j ] , blocks [ i +1][ j ] ,VERTICAL_DIRECTION )
        if bottom_blocked :
            annoyance = compute_edge_annoyance(blocks [ i ][ j ] , blocks [ i+1][ j ] , VERTICAL_DIRECTION)
            artifacted_edges.append(ArtifactedEdge (( j * BLOCK_COLS , ( i +1) *BLOCK_ROWS ) , (( j +1) * BLOCK_COLS , ( i +1) * BLOCK_ROWS ) ,annoyance))
    return artifacted_edges

def get_image_blocks (image) :
    blocks = []
    rows , cols , ch = image.shape
    for i in range(0 , rows / BLOCK_ROWS):
        blocks.append ([])
        for j in range(0 , cols / BLOCK_COLS ) :
            blocks[ i ].append(image [ i * BLOCK_ROWS :( i +1) * BLOCK_ROWS , j *BLOCK_COLS :( j +1) * BLOCK_COLS ])
    return blocks

def measure_artifacts(image_path , output_path) :
    image = cv2.imread(image_path , 1)
    image_array = np.array(image , dtype = np . int64)
    rows , cols , ch = image.shape
    blocks = get_image_blocks ( image_array )
    artifacted_edges = get_artifacted_edges ( blocks )
    annoyance_score = np . average(compute_overall_annoyance (artifacted_edges))
    print  ("Annoyance Score : %0.2 f ",annoyance_score)
    total_artifacts_percentage = np . float_ ( len ( artifacted_edges ) ) / np .float_ ((( rows / BLOCK_ROWS ) *( cols / BLOCK_COLS ) *2) ) * 100
    print  ("Artifacted Edges: %0.2 f ",total_artifacts_percentage)
    highlight_image_artifacts ( image , artifacted_edges )
    cv2 . imwrite ( output_path , image )
    return ( total_artifacts_percentage , annoyance_score )
