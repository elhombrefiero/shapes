#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


class Volume:
    """ Volume comprises a starting elevation, a delta Z, an angle, and a flow area

    Input angle is in degrees
    Input coordinates will be the middle of the bottom portion of the volume
    MATPLOTLIB uses the bottom left corner as the input to the Rectangle class
    """
    x_bottom_left = None
    y_bottom_left = None

    x_bottom_right = None
    y_bottom_right = None

    x_bottom_middle = None
    y_bottom_middle = None

    x_middle_left = None
    y_middle_left = None

    x_middle_right = None
    y_middle_right = None

    x_top_left = None
    y_top_left = None

    x_top_right = None
    y_top_right = None

    x_top_middle = None
    y_top_middle = None

    x_cor = 0
    y_cor = 0
    angle_deg = 0
    angle_rad = 0
    flow_area = 0
    length = 0.0

    def plot_me(self):
         # rect = Rectangle((self.x_cor, self.y_cor), self.flow_area, self.length, angle=self.angle_deg)
        fig, ax = plt.subplots()
        # ax.add_patch(rect)
        # ax.set(xlim=(-5,5), ylim=(-5,5))
        x = [self.x_bottom_left, self.x_bottom_right, self.x_top_right, self.x_top_left, self.x_bottom_left]
        y = [self.y_bottom_left, self.y_bottom_right, self.y_top_right, self.y_top_left, self.y_bottom_left]
        ax.plot(x,y, color='blue')
        x = [self.x_bottom_middle, self.x_top_middle]
        y = [self.y_bottom_middle, self.y_top_middle]
        ax.scatter(x,y, color='black')
        # ax.scatter([self.x_bottom_middle, self.y_bottom_middle], [self.x_top_middle, self.y_top_middle], linestyle='--', color='red')
        # ax.scatter([self.x_bottom_left, self.y_bottom_left], [self.x_top_left, self.y_top_left], linestyle='--', color='blue')
        # ax.scatter([self.x_bottom_right, self.y_bottom_right], [self.x_top_right, self.y_top_right], linestyle='--', color='black')
        plt.show()

    def __init__(self, x_start, y_start, angle, length=None, area=None, volume=None):
        """ Initialize a volume.
            Based on the starting x,y coordinates, the angle, the length, and the area, determine the different points of the volume
            x_start and y_start are going to be the middle of the start of the volume
            angle will be in degrees:
                0 for a horizontal volume that is in the positive x-direction
                90 for a vertical volume pointing in the positive y-direction
                180 for a horizontal volume that is in the negative x-direction
                270 for a vertical volume pointing in the negative y-direction
                etc
        """

        # Calculate the length/area based on inputs
        if length is None:
            if area is None or volume is None:
                raise ValueError(f'Cannot calculate length. Missing area ({area}) or volume ({volume})')
            self.length = volume/area
        else:
            self.length = length
        if area is None:
            if length is None or volume is None:
                raise ValueError(f'Cannot calculate area. Missing length ({length}) or volume ({volume})')
            self.flow_area = volume/length
        else:
            self.flow_area = area
        if volume is None:
            if length is None or area is None:
                raise ValueError(f'Cannot calculate volume. Missing length ({length} or area ({area})')
            self.volume = length * area
        else:
            self.volume = volume

        # Figure out direction of angle based on cos/sin
        self.angle_deg = angle
        self.angle_rad = angle*np.pi/180

        x_new = self.length*np.cos(self.angle_rad)
        y_new = self.length*np.sin(self.angle_rad)

        if x_new > x_start:
            self.x_bottom_middle = x_start
            self.x_top_middle = x_new
        else:
            self.x_bottom_middle = x_new
            self.x_top_middle = x_start
        if y_new > y_start:
            self.y_bottom_middle = y_start
            self.y_top_middle = y_new
        else:
            self.y_bottom_middle = y_new
            self.y_top_middle = y_start

        new_angle_deg = (self.angle_deg + 90.0)
        new_angle_rad = new_angle_deg*np.pi/180.0
        half_flow_area = self.flow_area/2.0
        xdiff = half_flow_area*np.cos(new_angle_rad)
        if xdiff > 0:
            self.x_bottom_right = self.x_bottom_middle + xdiff
            self.x_top_right = self.x_top_middle + xdiff
            self.x_bottom_left = self.x_bottom_middle - xdiff
            self.x_top_left = self.x_top_middle - xdiff
        else:
            self.x_bottom_right = self.x_bottom_middle - xdiff
            self.x_top_right = self.x_top_middle - xdiff
            self.x_bottom_left = self.x_bottom_middle + xdiff
            self.x_top_left = self.x_top_middle + xdiff
        ydiff = half_flow_area*np.sin(new_angle_rad)
        if ydiff > 0:
            self.y_bottom_right = self.y_bottom_middle + ydiff
            self.y_top_right = self.y_top_middle + ydiff
            self.y_bottom_left = self.y_bottom_middle - ydiff
            self.y_top_left = self.y_top_middle - ydiff
        else:
            self.y_bottom_right = self.y_bottom_middle - ydiff
            self.y_top_right = self.y_top_middle - ydiff
            self.y_bottom_left = self.y_bottom_middle + ydiff
            self.y_top_left = self.y_top_middle + ydiff


if __name__ == '__main__':
    x = 0
    y = 0
    length = 10.0
    area = 2.0
    volume = 50.0
    angle = 15.0
    vol = Volume(x, y, angle, length=length, area=area, volume=volume)
    vol.plot_me()
