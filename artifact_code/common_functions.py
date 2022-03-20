"""Code which is used for both blockiness and also Ringing and mosquito_noise artifacts."""
import logging
from cv2 import cv2
import matplotlib.pyplot as plt

#Constant values that can be used in this program.
BLOCK_ROWS = 5
BLOCK_COLS = 5
T_FLAT = 1
T_TEX =  200


def get_image_blocks (image, rows, cols):
    """Getting the block from the image."""
    blocks = []
    srows = int(rows / BLOCK_ROWS)
    scols = int(cols / BLOCK_COLS)
    for i in range (0, srows):
        blocks.append([])
        for j in range (0, scols):
            blocks[i].append(image[i*BLOCK_ROWS :(i+1)*BLOCK_ROWS, j*BLOCK_COLS :(j+1)*BLOCK_COLS])
    return blocks


def compute_overall_annoyance(artifacted_blocks):
    """Calculating the total visibility of the image and return the values as int type."""
    annoyance = 0
    if len(artifacted_blocks) != 0:
        for block in artifacted_blocks:
            annoyance += block.annoyance
        return annoyance / len(artifacted_blocks)
    else:
        return 0


def highlight_image_artifacts(image,artifacted_blocks):
    """It is used for highlighting the artifacts on the image."""
    for block in artifacted_blocks:
        start_point = block.y*BLOCK_COLS, block.x*BLOCK_ROWS
        end_point = (block.y+1)*BLOCK_COLS, (block.x+1)*BLOCK_ROWS
        cv2.rectangle (image, start_point, end_point, (0, 0, 0))


def log_artifact(message):
    """This function is used to write the execution time of the functions in the log file."""
    logging.basicConfig(filename= r"C:\Users\Vissamsetty Bharath\Downloads\Artifact_Detection-master\logs\log_file_ringing.log",
    format='%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    logger.warning(message)


def printing_image(input_image, modified_image):
    """This function is used to print the image on the screen."""
    plt.subplot(1,2,1)
    plt.imshow(input_image)
    plt.subplot(1,2,2)
    plt.imshow(modified_image)
    plt.show()
