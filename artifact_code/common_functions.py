from cv2 import cv2

BLOCK_ROWS = 5
BLOCK_COLS = 5


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