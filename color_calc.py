import cv2
import numpy as np


def load_convert_image(image_path: str):
    '''
    https://code.adonline.id.au/cmyk-in-python/
    :param image_path: (str)
    :return:
    '''
    img = cv2.imread(image_path)
    # Create float
    bgr = img.astype(float) / 255.
    # Extract channels
    with np.errstate(invalid='ignore', divide='ignore'):
        K = 1 - np.max(bgr, axis=2)
        C = (1 - bgr[..., 2] - K) / (1 - K)
        M = (1 - bgr[..., 1] - K) / (1 - K)
        Y = (1 - bgr[..., 0] - K) / (1 - K)

    # Convert the input BGR image to CMYK colorspace
    CMYK = (np.dstack((C, M, Y, K)) * 255).astype(np.uint8)
    # Split CMYK channels
    # Y, M, C, K = cv2.split(CMYK)
    C, M, Y, K = cv2.split(CMYK)
    np.isfinite(C).all()
    np.isfinite(M).all()
    np.isfinite(K).all()
    np.isfinite(Y).all()
    return (C,M,Y,K)

def main(image_path:str):
    c,m,y,k = load_convert_image(image_path)
    sum_intensities = [(np.sum(channel)/255)*100 for channel in (c,m,y,k)]
    counts = [len(np.where(channel>0)[0]) for channel in (c,m,y,k)]
    average_intensity = [intensity/count for intensity,count in zip(sum_intensities, counts)]
    print(f"average color intensity (0-100%): {average_intensity}")
    channel_pixel_count = [len(np.where(channel>0)[0]) for channel in (c,m,y,k)]
    total_area = c.shape[0]*c.shape[1]
    channel_area = [channel/total_area for channel in channel_pixel_count]
    print(f"channel coverage area (0-100%): {[area*100 for area in channel_area]}")
    white_area = len(np.where((c|m|y|k)==0)[0])/total_area
    print(f"white area(0-100%): {white_area*100}")
    average_consumption = np.asarray(channel_area)*np.asarray(average_intensity)
    print(f"average consumption (coverage% * intensity%): {average_consumption}")
    # show channels
    cv2.imshow('c', c)
    cv2.imshow('m', m)
    cv2.imshow('y', y)
    cv2.imshow('k', k)

    cv2.imwrite('./output/c.jpg', c)
    cv2.imwrite('./output/m.jpg', m)
    cv2.imwrite('./output/y.jpg', y)
    cv2.imwrite('./output/k.jpg', k)

    cv2.waitKey(0)
    print("")

if __name__ == "__main__":
    main("02-lamina.jpg")
