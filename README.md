# Detection of Two Types of Artifacts
1. Blockiness Detection
2. Ringing and Mosquito Noise Detection

# Things to do
1. Lint the Code.
2. Doc Strings have to be included whereever possible within the code.
3. Setup logging through out the program.
4. Include sample images within the repo for testing the code.
5. common functions should be written seperate file.
6. code has to be executed in a faster way.
7. Acknowledge the research paper and research work.
8. Upload the paper pdf here.

# Key Concepts
1. JPEG Compression
2. Artifact created by human
3. Disturbance created
4. Blocking Artifacts
5. Convert an image into an 8*8 block (64 pixels)
6. Mean Absolute Difference (MAD) of slope (gradient)
7. MAD between 2 neighbouring block
8. Every block will have 4 neighbouring blocks
9. Mean Square Error Difference (MSE D)
10. novelty of this paper : MAD of 8*8 block

* Constraints
  - to reduce to the amount of false positives
  - Absolute Diff of slope of all n tuples should not have larger deviation two(along the SAD - Sum of absolute difference)


# Blockiness Algorithm
1. Consider Image
2. Split image into blocks
3. Compute artifacts from blocks, Edges are being computed.
4. Apply constraints on those blocks
5. Quantization of artifacts
6. Drawing Lines
