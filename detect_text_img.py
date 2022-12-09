#import
from craft_text_detector import Craft

def detect_text_img(image_path, name_img):
    output_dir = "outputs/" + name_img + "/"
    # create a craft instance
    craft = Craft(output_dir=output_dir, crop_type="poly", cuda=False)
    # apply craft text detection and export detected regions to output directory
    prediction_result = craft.detect_text(image_path)
    craft.unload_craftnet_model()
    craft.unload_refinenet_model()