import rasterio
from rasterio.plot import show
from PIL import Image

def extract_layer(arr, min_v, max_v):
    height, width = arr.shape
    img = Image.new('1', (width, height), color=1)



    val = 0
    for y in range(0, height):
        print(round(y*100/height, 1), '%', sep='')
        for x in range(0, width):
            val = max(val, arr[y][x])
            if min_v <= arr[y][x] <= max_v:
                img.putpixel((x, y), 0)


    img.save("output.png")
    print("saved")
    print(val)
    #show(data)


def main():
    fp = r'GreatLakes.tiff'
    data = rasterio.open(fp)

    print(data.bounds, data.height, data.width)
    np_arr = data.read(1)
    extract_layer(np_arr, 0, 0)

if __name__ == '__main__':
    main()