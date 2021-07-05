import pandas as pd
import uuid
import os
import requests
import time
from distributed import Client, LocalCluster,as_completed

def save_images(chunk):
    image_paths = []
    image_ids = [image_id for image_id in chunk['image-id']]
    labels = [label for label in chunk['label']]

    for i in range(len(image_ids)):
        flower_directory = f"raw_data/{labels[i]}/"

        # create flower directory if it does not exist
        if not os.path.exists(flower_directory):
            os.makedirs(flower_directory)
        
        # TODO: account for .jpg .jpeg .png
        if '.jpg' in image_ids[i]:
            suffix = 'jpg'
        elif '.png' in image_ids[i]:
            suffix = 'png'
        elif 'jpeg' in image_ids[i]:
            suffix = 'jpeg'

        file_name = f"{flower_directory}{uuid.uuid4()}.{suffix}"

        image_url = image_ids[i].split('?',1)[0]

        print("Writing {0} to file_name {1}".format(image_url, file_name))

        nb_tries = 10
        while True:
            nb_tries -= 1
            try:
                ## write image url to file
                f = open(file_name, "wb")
                f.write(requests.get(image_url).content)
                f.close()

                image_paths.append(file_name)

                break
            except:
                if nb_tries == 0:
                    print("ERROR")
                    exit(-1)
                else:
                    # dont get yelled at by internet
                    print("got yelled at")
                    time.sleep(1)
    
    return image_paths, labels

def download_and_save_image_ids():
    futures = []
    for chunk in pd.read_csv("inaturalist_csv/image_ids.csv", chunksize= 500):
        future= client.submit(save_images, chunk, key=str(uuid.uuid4()))
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
    df.to_csv("raw_data/image_paths.csv",index=False)

if __name__ == "__main__":
    cluster = LocalCluster()
    client = Client(cluster)
    download_and_save_image_ids()