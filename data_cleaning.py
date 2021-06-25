from cv2 import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
import h5py
import random
import H5pyHelper
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn import preprocessing

THRESHOLD = 500
inps = [
    "Abronia elliptica",
    "Abronia fragrans",
    "Abronia nana",
    "Achillea millefolium",
    "Acmispon wrightii",
    "Aconitum columbianum",
    "Actaea rubra",
    "Agastache pallidiflora",
    "Agastache urticifolia",
    "Agoseris aurantiaca",
    "Agoseris glauca",
    "Aliciella haydenii",
    "Aliciella pinnatifida",
    "Aliciella subnuda",
    "Alisma triviale",
    "Allionia incarnata",
    "Allium acuminatum",
    "Allium cernuum",
    "Allium geyeri",
    "Allium macropetalum",
    "Allium nevadense",
    "Allium schoenoprasum",
    "Almutaster pauciflorus",
    "Alyssum simplex",
    "Amauriopsis dissecta",
    "Amelanchier utahensis",
    "Anagallis arvensis",
    "Anaphalis margaritacea",
    "Androsace septentrionalis",
    "Androstephium breviflorum",
    "Anemone multifida",
    "Anemone narcissiflora",
    "Anemone patens",
    "Anemopsis californica",
    "Angelica grayi",
    "Angelica pinnata",
    "Antennaria anaphaloides",
    "Antennaria dimorpha",
    "Antennaria media",
    "Antennaria microphylla",
    "Antennaria parvifolia",
    "Antennaria rosea",
    "Antennaria umbrinella",
    "Anthemis cotula",
    "Anticlea elegans",
    "Anticlea vaginata",
    "Apocynum androsaemifolium",
    "Apocynum cannabinum",
    "Aquilegia caerulea",
    "Aquilegia caerulea",
    "Aquilegia chrysantha",
    "Aquilegia elegantula",
    "Arctium minus",
    "Arctostaphylos patula",
    "Arenaria lanuginosa",
    "Argemone polyanthemos",
    "Arnica chamissonis",
    "Arnica cordifolia",
    "Arnica latifolia",
    "Arnica longifolia",
    "Arnica mollis",
    "Arnica parryi",
    "Arnica rydbergii",
    "Artemisia cana",
    "Artemisia dracunculus",
    "Artemisia ludoviciana",
    "Artemisia michauxiana",
    "Artemisia norvegica",
    "Artemisia nova",
    "Artemisia scopulorum",
    "Artemisia tridentata",
    "Asclepias asperula",
    "Asclepias involucrata",
    "Asclepias speciosa",
    "Asclepias subverticillata",
    "Astragalus allochrous",
    "Astragalus alpinus",
    "Astragalus amphioxys",
    "Astragalus calycosus",
    "Astragalus ceramicus",
    "Astragalus cicer",
    "Astragalus desperatus",
    "Astragalus flavus",
    "Astragalus hallii",
    "Astragalus kentrophyta",
    "Astragalus lentiginosus",
    "Astragalus miser",
    "Astragalus missouriensis",
    "Astragalus mollissimus",
    "Astragalus musiniensis",
    "Astragalus newberryi",
    "Astragalus nuttallianus",
    "Astragalus praelongus",
    "Astragalus tephrodes",
    "Atriplex canescens",
    "Atriplex confertifolia",
    "Berlandiera lyrata",
    "Berteroa incana",
    "Bistorta bistortoides",
    "Bistorta vivipara",
    "Boechera lemmonii",
    "Boechera pendulocarpa",
    "Boechera perennans",
]


class ImageManager:
    def __init__(self):
        self.lb = preprocessing.LabelBinarizer()
        self.lb.fit(inps)
        self.set_default()

    def set_default(self):
        self.features = []
        self.labels = []
        self.batches = 500

    def start_menu(self):
        self.directory = "/home/sorozco0612/dev/flora_dex/raw_data/"

        self.create_dataset(self.directory)

        if not (self.features == []) and not (self.labels == []):
            x_train, x_test, y_train, y_test = train_test_split(
                np.array(self.features), np.array(self.labels)
            )
            # self.append_to_dataset(temp_filename)
            H5pyHelper.append_to_dataset(
                os.path.join(self.directory, "data.h5"),
                x_train,
                "x_train",
            )
            H5pyHelper.append_to_dataset(
                os.path.join(self.directory, "data.h5"),
                y_train,
                "y_train",
            )
            H5pyHelper.append_to_dataset(
                os.path.join(self.directory, "data.h5"),
                x_test,
                "x_test",
            )
            H5pyHelper.append_to_dataset(
                os.path.join(self.directory, "data.h5"),
                y_test,
                "y_test",
            )

        ## shuffle dataset
        hf = h5py.File("/home/sorozco0612/dev/flora_dex/raw_data/data.h5", "a")
        random.seed(datetime.now())
        random.shuffle(hf[feature_name])
        random.shuffle(hf[label_name])

        hf.close()

    def create_dataset(self, search_directory):

        # find all .png files within a given folder
        for component in os.listdir(search_directory):

            path = search_directory + component

            # recursively find .png files in sub directories
            if os.path.isdir(path):
                print("Diving into {0}".format(path))
                self.create_dataset(path + "/")

            elif component.endswith(".jpg"):

                clean = ImageManager.clean_image(path)

                if len(self.features) == self.batches:
                    x_train, x_test, y_train, y_test = train_test_split(
                        np.array(self.features), np.array(self.labels)
                    )
                    # self.append_to_dataset(temp_filename)
                    H5pyHelper.append_to_dataset(
                        os.path.join(self.directory, "data.h5"),
                        x_train,
                        "x_train",
                    )
                    H5pyHelper.append_to_dataset(
                        os.path.join(self.directory, "data.h5"),
                        y_train,
                        "y_train",
                    )
                    H5pyHelper.append_to_dataset(
                        os.path.join(self.directory, "data.h5"),
                        x_test,
                        "x_test",
                    )
                    H5pyHelper.append_to_dataset(
                        os.path.join(self.directory, "data.h5"),
                        y_test,
                        "y_test",
                    )
                    self.features = []
                    self.labels = []

                # show image to user
                # cv2.imshow("image", clean)
                # cv2.waitKey(1000)

                # input cleaned image into dataset
                self.features.append(clean)

                # get directory name
                directory_name = search_directory.split("/")[-2]

                label_one_hot = np.array(self.lb.transform([directory_name]))
                label_one_hot = label_one_hot.flatten()

                # store label into dataset
                self.labels.append(label_one_hot)

                self.augment_data(clean, label_one_hot)

    def augment_data(self, img, label):
        img_flipped = ImageManager.horiztonal_flip_image(img, True)
        self.features.append(img_flipped)
        self.labels.append(label)

        img_rotated = ImageManager.rotate_image(img, 30)
        self.features.append(img_rotated)
        self.labels.append(label)

        img_zoomed = ImageManager.zoom_image(img, 0.5)
        self.features.append(img_zoomed)
        self.labels.append(label)

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

        # image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
        # image = cv2.GaussianBlur(image, (3, 3), 0)
        scaled = cv2.resize(image, (500, 500))
        # segment = ImageManager.segment_image(scaled)
        # blur = cv2.medianBlur(segment, 3)

        # cv2.imshow("image", blur)
        # cv2.waitKey(1000)

        # scaled = ImageManager.scale_image(image)
        scaled_pixels = ImageManager.scale_pixels(scaled)

        # HSV provides more color contrast with yellow lines.
        # It was alot easier to isolate the yellow lines in HSV than in BGR
        # hsv = cv2.cvtColor(scaled, cv2.COLOR_BGR2HSV)

        # hsv mask to get yellow from image in medium lighting
        # hsv_thresh = cv2.inRange(
        #    hsv, np.array([0, 0, 63], np.uint8), np.array([107, 243, 255], np.uint8)
        # )

        ## gaussian blue reduces noise from image. Used to keep the most prominent edges from an image
        # hsv_blur = cv2.GaussianBlur(hsv_thresh, (13, 13), 0)

        ## edge detection
        ## canny = cv2.Canny(hsv_blur, 246, 255)
        # canny = cv2.Canny(hsv_blur, 0, 255)

        # region = ImageManager.region_of_interest(scaled)

        # give single color channel. Needed for 2DConv
        # region = region.reshape(list(region.shape) + [1])

        return scaled_pixels

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
        )

        hist = plt.hist(boundary_hues, 256, [0, 256])

        hue_thresholds = [i for i in range(256) if hist[0][i] >= THRESHOLD]

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
    manager.start_menu()
    cv2.destroyAllWindows()
