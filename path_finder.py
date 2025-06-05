
import imageio.v3 as imageio
import numpy as np
import random


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)



def visualize(**kwargs):

    import matplotlib.pyplot as plt

    num_images = len(kwargs)

    for i, (key, value) in enumerate(kwargs.items()):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(value, cmap='Greys_r')
        plt.axis('off')
        plt.title(key)

    plt.show()




def draw_path(universe, path_list, path_color=BLUE):

    # first point is start point and last point is end point
    start_pt = path_list[0]
    end_pt = path_list[-1]

    if len(universe.shape) == 2:
        rgb_image = np.stack((universe, universe, universe), axis=-1)
    else:
        rgb_image = universe.copy()

    rgb_image[start_pt] = GREEN # start point green
    rgb_image[end_pt] = RED # end point red

    for i in range(1, len(path_list) - 1):
        point = path_list[i]
        rgb_image[point] = path_color # mid point blue

    return rgb_image





def path_exists(universe, start_x, start_y, end_x, end_y):



    height, width = universe.shape


    # breadth-first search

    visited_dict = {}

    pixel_queue = []
    path_len_queue = []
    path_queue = []

    pixel_queue.append((start_y, start_x))
    path_len_queue.append(0)
    path_queue.append([])

    found_path_list = None

    while pixel_queue:
        curr_y, curr_x = pixel_queue.pop(0)
        curr_path_len = path_len_queue.pop(0)
        curr_path = path_queue.pop(0)

        curr_pt = (curr_y, curr_x)

        # check that pixel is black
        if universe[curr_y, curr_x] != 0:
            continue # skip because pixel is not black

        # check that pixel hasn't already been visited
        if curr_pt in visited_dict:
            continue # skip because we've already visited this pixel

        # add point to visited dict
        visited_dict[curr_pt] = True


        # add point to path list
        curr_path.append(curr_pt)


        # check if end point
        if curr_y == end_y and curr_x == end_x:
            found_path_list = curr_path.copy()
            break # you found the end!

        # add neighboring pixels to pixel_queue

        # below
        if curr_y < height - 1:
            pixel_queue.append((curr_y + 1, curr_x))
            path_len_queue.append(curr_path_len + 1)
            path_queue.append(curr_path.copy())

        # above
        if curr_y > 0:
            pixel_queue.append((curr_y - 1, curr_x))
            path_len_queue.append(curr_path_len + 1)
            path_queue.append(curr_path.copy())

        # left
        if curr_x > 0:
            pixel_queue.append((curr_y, curr_x - 1))
            path_len_queue.append(curr_path_len + 1)
            path_queue.append(curr_path.copy())

        # right
        if curr_x < width - 1:
            pixel_queue.append((curr_y, curr_x + 1))
            path_len_queue.append(curr_path_len + 1)
            path_queue.append(curr_path.copy())



    b_found_path = True if found_path_list else False


    return b_found_path, found_path_list
    



def one_pair(universe):

    # get list of all black pixels
    black_pixels = np.where(universe == 0)
    black_pixels_y = black_pixels[0].tolist()
    black_pixels_x = black_pixels[1].tolist()

    black_pixels = list(zip(black_pixels_x, black_pixels_y)) # (x, y)

    # pick random start and end points on black pixels
    start_x, start_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((start_x, start_y))
    end_x, end_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((end_x, end_y))


    # find path from start to end
    b_found_path, path_list = path_exists(universe, start_x, start_y, end_x, end_y)


    if b_found_path:

        print('path exists')

        rgb_image = draw_path(universe, path_list)

        # visualize(rgb_image=rgb_image)

        # write out path as image
        imageio.imwrite('output_path.png', rgb_image)

    else:
        print('path does NOT exist')


def two_pairs(universe):

    # get list of all black pixels
    black_pixels = np.where(universe == 0)
    black_pixels_y = black_pixels[0].tolist()
    black_pixels_x = black_pixels[1].tolist()

    black_pixels = list(zip(black_pixels_x, black_pixels_y)) # (x, y)

    # FIRST PAIR
    start_1_x, start_1_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((start_1_x, start_1_y))
    end_1_x, end_1_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((end_1_x, end_1_y))


    # SECOND PAIR
    start_2_x, start_2_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((start_2_x, start_2_y))
    end_2_x, end_2_y = black_pixels[random.randint(0, len(black_pixels) - 1)]
    black_pixels.remove((end_2_x, end_2_y))


    # find path from start to end
    b_found_path_1, path_list_1 = path_exists(universe, start_1_x, start_1_y, end_1_x, end_1_y)

    if b_found_path_1:
        rgb_image_1 = draw_path(universe, path_list_1)

        # convert rgb to black and white
        universe_2 = np.maximum(rgb_image_1[:,:,0], rgb_image_1[:,:,1])
        universe_2 = np.maximum(universe_2, rgb_image_1[:,:,2])

        # find path from start to end
        b_found_path_2, path_list_2 = path_exists(universe_2, start_2_x, start_2_y, end_2_x, end_2_y)


        if b_found_path_2:

            print('both paths exist')

            rgb_image_2 = draw_path(rgb_image_1, path_list_2, path_color=PURPLE)

            # visualize(rgb_image_2=rgb_image_2)

            # write out both paths as image
            imageio.imwrite('output_path_two_pairs.png', rgb_image_2)

        else:
            print('one or more paths do NOT exist')

    else:
        print('one or more paths do NOT exist')







def main():

    example_file_ring = 'input_examples/small-ring.png' # 5x5
    example_file_polygons = 'input_examples/polygons.png' # 100x100
    example_file_bars = 'input_examples/bars.png' # 11x11

    # CHOSEN_EXAMPLE = example_file_ring
    CHOSEN_EXAMPLE = example_file_polygons
    # CHOSEN_EXAMPLE = example_file_bars


    universe = imageio.imread(CHOSEN_EXAMPLE)


    one_pair(universe)
    # two_pairs(universe)




if __name__ == '__main__':
    main()

