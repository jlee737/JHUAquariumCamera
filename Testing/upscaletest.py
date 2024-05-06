import cv2
from cv2 import dnn_superres

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread(r"C:\Users\Jaechan Lee\Desktop\JHU\__SP24\MultiD_AquariumProject\Upscaling\BlurryDavid.jpg")

# Read the desired model
path = r"C:\Users\Jaechan Lee\Desktop\JHU\__SP24\MultiD_AquariumProject\Upscaling\ESPCN_x2.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("espcn", 2)

# Upscale the image
result = sr.upsample(image)
result = sr.upsample(result)

# Save the image
cv2.imshow("test", result)
cv2.waitKey(0)
