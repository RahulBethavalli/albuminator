import numpy as np

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications import vgg16

from pathlib import Path
import shutil
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def download_vgg16(model_file_path):
    # saves the vgg model in model_file_path
    vgg_model = vgg16.VGG16()
    print('downloading model')
    vgg_model.save(model_file_path)
    print('model saved')



def get_prediction_class(filename):
    """

    Gets the prediction class from VGG16 pretrained model

    Input Args:

        filename = absolute path of an image

    Output:

        output_class

    """
    model_file_path = "saved_models/vgg16_weights_tf_dim_ordering_tf_kernels.h5"

    if not os.path.exists(model_file_path):
        print('downloading the vgg model')
        download_vgg16(model_file_path)
        print('download of vgg model finished')

    vgg_model = vgg16.VGG16(weights=model_file_path)
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


def create_sorted_folder():
    ''' Created the sorted_folder to be diaplayed given the uplo 
    '''
    input_folder = 'uploads'

    path = Path(input_folder)

    file_paths = list(path.glob('*'))
    file_paths = [i.as_posix() for i in file_paths]
    file_paths = [pth for pth in file_paths if allowed_file(pth)]

    file_classes = [get_prediction_class(pth) for pth in file_paths]

    output_folder = 'sorted_folder'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for f_name, f_class in zip(file_paths, file_classes):
        src = f_name
        dest = os.path.join(output_folder, f_class, f_name.split('/')[-1])
        dest_folder = '/'.join(dest.split('/')[:-1])

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        shutil.move(src, dest)
        
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


