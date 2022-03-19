from cv2 import cv2

import logging

BLOCK_ROWS = 5
BLOCK_COLS = 5
T_FLAT = True
T_TEX =  False


def get_image_blocks (image , rows , cols):
    """Getting the block from the image."""
    blocks = []
    srows = int(rows / BLOCK_ROWS)
    scols = int(cols / BLOCK_COLS)
    for i in range (0,srows): 
        blocks.append([])
        for j in range (0,scols):
            blocks[i].append(image[i*BLOCK_ROWS :(i+1)*BLOCK_ROWS ,j*BLOCK_COLS :(j+1)*BLOCK_COLS])
    return(blocks)


def compute_overall_annoyance(artifacted_blocks):
    """Calculating the total visibility of the image and return the values as int type."""
    annoyance = 0
    if len(artifacted_blocks) != 0:
        for block in artifacted_blocks:
            annoyance += block.annoyance
        return annoyance / len(artifacted_blocks)
    else:
        return 0


def conditions_to_satisy_artifact(F_threshold, T_threshold, blocks_sads):
    flat_top = (F_threshold[0][0].all() and F_threshold[0][1].all()) or (F_threshold[0][1].all() and F_threshold[0][2].all())
    flat_bottom = (F_threshold[2][0].all() and F_threshold[2][1].all()) or (F_threshold[2][1].all() and F_threshold[2][2].all())
    flat_left = (F_threshold[0][0].all() and F_threshold[1][0].all()) or (F_threshold[1][0].all() and F_threshold[2][0].all())
    flat_right = (F_threshold[0][2].all() and F_threshold[1][2].all()) or (F_threshold[1][2].all() and F_threshold[2][2].all())
    flat = flat_top or flat_bottom or flat_left or flat_right
    tex = False
    for i in range (0, len(T_threshold)):
        for j in range (0, len(T_threshold[i])):
            if i != 1 and j != 1:
                tex = tex or all(T_threshold[i][j])
    centre = ( T_FLAT < all(blocks_sads[1][1])) and (all(blocks_sads[1][1]) < T_TEX)
    artifacted = tex and flat and centre
    return artifacted


def log_artifact(message):
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning(message)