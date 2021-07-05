from cv2 import cv2
import pandas as pd
from distributed import Client, LocalCluster,as_completed
import matplotlib.pyplot as plt
import uuid
import os
import random
import dask.array as da

THRESHOLD = 900

class ImageManager:
    def __init__(self):
        pass

    def clean_chunk(self, chunk):

        # clean image paths will be added to csv at the very end
        clean_image_paths = []
        clean_image_labels = []

        raw_image_paths = [image_path for image_path in chunk['image-path']]
        raw_image_labels = [label for label in chunk['label']]

        # got through all the raw image paths and clean them
        for i in range(len(raw_image_paths)):
            flower_directory = f"clean_data/{raw_image_labels[i]}/"

            # create flower directory if it does not exist
            if not os.path.exists(flower_directory):
                os.makedirs(flower_directory)

            clean_image_path = raw_image_paths[i].replace("raw_data", "clean_data")
            clean_image_label = raw_image_labels [i]

            clean_image_paths.append(clean_image_path)
            clean_image_labels.append(raw_image_labels[i])

            print(f"Cleaning and augmenting {raw_image_paths[i]}")

            clean_image = ImageManager.clean_image(raw_image_paths[i])
                
            cv2.imwrite(clean_image_path,clean_image)

            # agument images and get their paths,labels
            augmented_image_paths,augmented_image_labels = ImageManager.augment_image(clean_image_path, clean_image_label, flower_directory)

            clean_image_paths += augmented_image_paths
            clean_image_labels += augmented_image_labels
            
        return clean_image_paths, clean_image_labels 
    
    def clean_images(self, image_paths_csv):

        cluster = LocalCluster()
        client = Client(cluster)

        futures = []

        for chunk in pd.read_csv(image_paths_csv, chunksize= 500):
            future= client.submit(self.clean_chunk, chunk, key=str(uuid.uuid4()))
            futures.append(future)

        completed = as_completed(futures)

        image_paths =[]
        labels = []

        for i in completed:
            p,l = i.result()

            image_paths += p
            labels += l

        d = {'image-path' : image_paths, 'label' : labels}
        df = pd.DataFrame(data=d)
        df.to_csv("clean_data/image_paths.csv",index=False)


    @staticmethod
    def augment_image(image_path, image_label,save_dir):

        image_paths = []
        image_labels = []

        # need to specify this or the images will be empty when written
        if '.jpg' in image_path:
            suffix = 'jpg'
        elif '.png' in image_path:
            suffix = 'png'
        elif 'jpeg' in image_path:
            suffix = 'jpeg'

        # read in original image
        img = cv2.imread(image_path)

        # flip image
        img_flipped = ImageManager.horiztonal_flip_image(img, True)

        file_path = f"{save_dir}{uuid.uuid4()}.{suffix}"

        cv2.imwrite(file_path,img_flipped)

        image_paths.append(file_path)
        image_labels.append(image_label)

        # rotate iamge
        img_rotated = ImageManager.rotate_image(img, 30)

        file_path = f"{save_dir}{uuid.uuid4()}.{suffix}"

        cv2.imwrite(file_path,img_rotated)

        image_paths.append(file_path)
        image_labels.append(image_label)

        # zoom image
        img_zoomed = ImageManager.zoom_image(img, 0.5)

        file_path = f"{save_dir}{uuid.uuid4()}.{suffix}"

        cv2.imwrite(file_path,img_zoomed)

        image_paths.append(file_path)
        image_labels.append(image_label)

        return image_paths,image_labels

    @staticmethod
    def fill(img, h, w):
        img = cv2.resize(img, (h, w), cv2.INTER_CUBIC)
        return img

    @staticmethod
    def zoom_image(img, value):
        if value > 1 or value < 0:
            print("Value for zoom should be less than 1 and greater than 0")
            return img
        value = random.uniform(value, 1)
        h, w = img.shape[:2]
        h_taken = int(value * h)
        w_taken = int(value * w)
        h_start = random.randint(0, h - h_taken)
        w_start = random.randint(0, w - w_taken)
        img = img[h_start : h_start + h_taken, w_start : w_start + w_taken, :]
        img = ImageManager.fill(img, h, w)
        return img

    @staticmethod
    def rotate_image(img, angle):
        angle = int(random.uniform(-angle, angle))
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((int(w / 2), int(h / 2)), angle, 1)
        img = cv2.warpAffine(img, M, (w, h))
        return img

    @staticmethod
    def horiztonal_flip_image(img, flag):
        if flag:
            return cv2.flip(img, 1)
        else:
            return img

    @staticmethod
    def clean_image(image_path):
        image = cv2.imread(image_path)

        scaled = cv2.resize(image, (500, 500))

        segment = ImageManager.segment_image(scaled)

        #TODO: scaled pixels using https://machinelearningmastery.com/how-to-normalize-center-and-standardize-images-with-the-imagedatagenerator-in-keras/
        #scaled_pixels = ImageManager.scale_pixels(scaled)

        #print (scaled_pixels)

        return segment 

    @staticmethod
    def segment_image(img):
        HLS_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

        left_boundary = HLS_img[:, 0:20]
        top_boundary = HLS_img[:20, :]
        right_boundary = HLS_img[:, -20:]
        bottom_boundary = HLS_img[-20:, :]

        boundary_hues = (
            top_boundary[:, :, 0].flatten().tolist()
            + left_boundary[:, :, 0].flatten().tolist()
            + right_boundary[:, :, 0].flatten().tolist()
            + bottom_boundary[:,:,0].flatten().tolist()
        )

        x = da.from_array(boundary_hues)

        h,bins = da.histogram(x,bins=256,range=[0,256])

        h = h.compute()

        hue_thresholds = [i for i in range(256) if h[i] >= THRESHOLD]

        #if (len(boundary_hues) == 0):
        #    print("hello")

        #hist = plt.hist(boundary_hues, 256, [0, 256])

        #hue_thresholds = [i for i in range(256) if hist[0][i] >= THRESHOLD]

        for row in range(HLS_img.shape[0]):
            for col in range(HLS_img.shape[1]):
                for hue in hue_thresholds:
                    if HLS_img[row][col][0] == hue:
                        HLS_img[row][col][0] = 0
                        HLS_img[row][col][1] = 0
                        HLS_img[row][col][2] = 0
                        break

        return cv2.cvtColor(HLS_img, cv2.COLOR_HLS2BGR)

    @staticmethod
    def scale_pixels(image):
        normalized = ImageManager.normalize_pixels(image)
        centered = ImageManager.center_pixels(normalized)
        return centered

    @staticmethod
    def normalize_pixels(image):
        pixels = image.astype("float32")
        pixels /= 255.0
        return pixels

    @staticmethod
    def center_pixels(image):
        pixels = image - image.mean()
        return pixels


if __name__ == "__main__":
    manager = ImageManager()
    manager.clean_images("raw_data/image_paths.csv")
    cv2.destroyAllWindows()
