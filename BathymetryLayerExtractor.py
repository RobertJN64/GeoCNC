import rasterio
from rasterio.plot import show
from PIL import Image
from PIL import ImageFilter
from datetime import datetime
import os

def extract_layer(arr, max_v, resize, fname):
    a = (arr < max_v)
    img = Image.fromarray(a)
    img = img.resize((int(img.width/resize), int(img.height/resize)))
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.MaxFilter())
    img.save(fname + ".png")
    print("Saved:", fname)


def main():
    fname = input("Enter file name (without extension): ")
    data = rasterio.open(fname + "/src.tiff")

    print(data.bounds, data.height, data.width)
    np_arr = data.read(1)

    min_v = np_arr.min()
    print("Min Level (meters):", min_v)
    if input("Show map (y/n): ") == "y":
        show(data)

    #Level 0: Base, Level 1-n: Water, Level n+1: Land
    levels = int(input("Enter total number of levels to split into: "))
    resize = int(input("Enter resize factor: "))

    now = datetime.now()
    folder = fname + "/Output " + now.strftime("%m-%d-%Y %H-%M-%S")
    os.mkdir(folder)
    extract_layer(np_arr, 0, resize, folder + "/" + "Layer 0")
    split = min_v / levels

    for i in range(levels-2):
        extract_layer(np_arr, split * (i+1), resize, folder + "/" + "Layer " + str(i+1))

if __name__ == '__main__':
    main()