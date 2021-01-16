import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications import vgg16


def get_prediction_class(filename):
    """

    Gets the prediction class from VGG16 pretrained model

    Input Args:

        filename = absolute path of an image

    Output:

        output_class

    """

    vgg_model = vgg16.VGG16(weights="imagenet")

    # load an image in PIL format
    original = load_img(filename, target_size=(224, 224))

    # convert the PIL image to a numpy array
    # IN PIL - image is in (width, height, channel)
    # In Numpy - image is in (height, width, channel)
    numpy_image = img_to_array(original)

    # Convert the image / images into batch format
    # expand_dims will add an extra dimension to the data at a particular axis
    # We want the input matrix to the network to be of the form (batchsize, height, width, channels)
    # Thus we add the extra dimension to the axis 0.
    image_batch = np.expand_dims(numpy_image, axis=0)

    # prepare the image for the VGG model
    processed_image = vgg16.preprocess_input(image_batch.copy())

    # get the predicted probabilities for each class
    predictions = vgg_model.predict(processed_image)
    # print predictions
    # convert the probabilities to class labels
    # we will get top 5 predictions which is the default
    label_vgg = decode_predictions(predictions)
    # print VGG16 predictions
    output_class = label_vgg[0][0][1]

    return output_class
