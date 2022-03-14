import numpy as np
from cv2 import cv2

block_rows = 5
block_cols = 5
kernel_x = 3
kernel_y = 3
t_flat = True
t_tex =  False

class ArtifactedBlock:
    def __init__(self,x_coord,y_coord,annoyance):
        self.x = x_coord
        self.y = y_coord
        self.annoyance = annoyance

def highlight_image_artifacts(image,artifacted_blocks):
    for block in artifacted_blocks:
        start_point = block.y*block_cols,block.x*block_rows
        end_point = (block.y+1)*block_cols,(block.x+1)*block_rows
        cv2.rectangle (image,start_point,end_point,(0 ,0 ,0))

def compute_overall_annoyance(artifacted_blocks):
    annoyance = 0
    if len(artifacted_blocks) != 0:
        for block in artifacted_blocks:
            annoyance += block.annoyance
        return annoyance / len(artifacted_blocks)
    else :
        return 0

def check_if_artifacted ( blocks_SADs ):
    f = blocks_SADs < t_flat
    t = blocks_SADs > t_tex
    flat_top = (all(f [0][0]) and all(f[0][1])) or (all(f[0][1]) and all(f[0][2]))
    flat_bottom = (all(f[2][0]) and all(f[2][1])) or (all(f[2][1]) and all(f[2][2]))
    flat_left = (all(f[0][0]) and all(f[1][0])) or (all(f[1][0]) and all(f[2][0]))
    flat_right = (all(f[0][2]) and all(f[1][2])) or (all(f[1][2]) and all(f[2][2]))
    flat = flat_top or flat_bottom or flat_left or flat_right
    tex = False
    for i in range (0, len (t)):
        for j in range (0, len (t[i])):
            if i != 1 and j != 1:
                tex = tex or all(t[i][j])
    centre = ( t_flat < all (blocks_SADs [1][1])) and (all (blocks_SADs [1][1]) < t_tex )
    artifacted = tex and flat and centre
    return artifacted

def check_artifacted_blocks (blocks_SADs_map):
    artifacted_blocks =[]
    for i in range(1,len (blocks_SADs_map ) - 1):
        for j in range(1,len (blocks_SADs_map [i]) - 1):
            if check_if_artifacted (blocks_SADs_map [i -1:i+2, j -1:j +2]) :
                annoyance = blocks_SADs_map[i][j ]/(( block_cols -1) *(block_rows -1) *2)
                print(annoyance)
                artifacted_blocks.append(ArtifactedBlock(i,j,annoyance ))
    return artifacted_blocks

def compute_SAD_for_block(block):
    sad = 0
    for i in range(0,block_rows -1) :
        for j in range (0,block_cols -1) :
            sad += np.abs(block[i][j] - block[i +1][ j]) + np.abs(block[i][j]- block[i][j +1])
    return sad

def compute_blocks_SAD(blocks):
    blocks_SADs = np.array([[[0,0,0]for x in range(len(blocks[0]))]for x in range(len(blocks))])
    print(len(blocks_SADs))
    for i in range(0,len(blocks)):
        for j in range(0,len(blocks[i])):
            blocks_SADs[i][j] = compute_SAD_for_block(blocks[i][j])
    return blocks_SADs

def get_image_blocks(image,rows,cols):
    blocks = []
    for i in range(0,int (rows / block_rows)):
        blocks.append([])
        for j in range(0,int(cols / block_cols)):
            blocks[i].append(image[i*block_rows:(i+1)*block_rows,j*block_cols:(j+1)*block_cols])
    return blocks

def measure_artifacts(image_path,output_path):
    image = cv2.imread(image_path)
    image_array = np.array(image,dtype =np.int64)
    print("reading image "+ image_path)
    rows,cols,char = image.shape
    blocks = get_image_blocks(image_array,rows,cols)
    blocks_SADs = compute_blocks_SAD(blocks)
    artifacted_blocks = check_artifacted_blocks( blocks_SADs)
    annoyance_score = np.average(compute_overall_annoyance(artifacted_blocks))
    print ('Annoyance Score:',float("{:.2f}".format(annoyance_score)))
    total_artifacts_percentage = np.float_(len(artifacted_blocks)) / np.float_((rows / block_rows)
    *( cols / block_cols ))*100
    print ('Artifacted Edges:',float("{:.2f}".format(total_artifacts_percentage)))
    highlight_image_artifacts(image,artifacted_blocks)
    cv2.imwrite(output_path,image)
    return (total_artifacts_percentage,annoyance_score)

image_output = measure_artifacts(
    r"C:\Users\Vissamsetty Bharath\Documents\project_python\image-022.jpg"
    ,r"C:\Users\Vissamsetty Bharath\Documents\project_python\test_write.jpg")
