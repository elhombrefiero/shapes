#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import numpy as np


def calculate_length_area_volume(length=None, area=None, volume=None):
    if length is None:
        if area is None or volume is None:
            raise ValueError(f'Cannot calculate length. Missing area ({area}) or volume ({volume})')
        new_length = volume / area
    else:
        new_length = length
    if area is None:
        if length is None or volume is None:
            raise ValueError(f'Cannot calculate area. Missing length ({length}) or volume ({volume})')
        new_flow_area = volume / length
    else:
        new_flow_area = area
    if volume is None:
        if length is None or area is None:
            raise ValueError(f'Cannot calculate volume. Missing length ({length} or area ({area})')
        new_volume = length * area
    else:
        new_volume = volume

    return new_length, new_flow_area, new_volume


class Volume:
    """ Volume comprises a starting elevation, a delta Z, an angle, and a flow area

    Input angle is in degrees
    The x_start and y_start are the inlet coordinates.

    This will be translated to a version that corresponds to the equivalent rectangle in matplotlib.
     MATPLOTLIB uses the bottom left corner as the input to the Rectangle class
    """

    inlet_coordinates = (None, None)
    outlet_coordinates = (None, None)

    vol_no = None
    angle_deg = 0
    angle_rad = 0
    flow_area = 0
    length = 0.0

    rect = None

    def rel_to_mtplt(self, x_start, y_start, r_angle):
        """ Converts the R inputs into a format for the Matplotlib plot rectangle.

            Also calculates the inlet and outlet coordinates"""
        # The angle used in matplotlib is 90 degrees off in the clockwise direction
        # The angle of rotation will be based on the r_angle
        r_angle_rad = math.radians(r_angle)
        m_angle = r_angle - 90.0
        m_angle_rad_180 = math.radians(m_angle + 180.0)

        # The starting position is the inlet of the volume.
        self.inlet_coordinates = (x_start, y_start)
        # The outlet coordinates use the length
        x_outlet = x_start + self.length*np.cos(r_angle_rad)
        y_outlet = y_start + self.length*np.sin(r_angle_rad)
        self.outlet_coordinates = (float(x_outlet), float(y_outlet))

        # Matplotlib needs the corner.
        # These need an additional 90-degree angle
        x1 = x_start + 0.5*self.flow_area*np.cos(m_angle_rad_180)
        y1 = y_start + 0.5*self.flow_area*np.sin(m_angle_rad_180)

        self.rect = Rectangle((x1, y1), self.flow_area, self.length, angle=m_angle,
                              rotation_point=(x1, y1))

    def plot_me(self, show_inlet_outlet=False):

        fig, ax = plt.subplots()
        ax.add_patch(self.rect)
        if show_inlet_outlet:
            ax.plot((self.inlet_coordinates[0], self.outlet_coordinates[0]), (self.inlet_coordinates[1],  self.outlet_coordinates[1]), 'o')
        plt.autoscale()
        plt.show()

    def return_figure(self):
        return self.rect

    def return_inlet_coordinates(self):
        return self.inlet_coordinates

    def return_outlet_coordinates(self):
        return self.outlet_coordinates

    def __init__(self, x_start, y_start, angle, length=None, area=None, volume=None, vol_no=None):
        """ Initialize a volume.
            Input starting x,y coordinates, the angle, the length, and the area
            x_start and y_start are going to be the coordinates of the inlet of the volume
            angle will be in degrees:
                0 for a horizontal volume that is in the positive x-direction
                90 for a vertical volume pointing in the positive y-direction
                180 for a horizontal volume that is in the negative x-direction
                270 for a vertical volume pointing in the negative y-direction
                etc
        """

        # Calculate the length/area based on inputs
        self.length, self.flow_area, self.volume = calculate_length_area_volume(length, area, volume)

        if vol_no:
            self.vol_no = vol_no

        # Figure out direction of angle based on cos/sin
        self.angle_deg = angle

        self.rel_to_mtplt(x_start, y_start, angle)


class Junction:
    pass


if __name__ == '__main__':
    x = 0
    y = 0
    length = 10.0
    area = 2.0
    volume = 50.0
    angle = 60.0
    vol = Volume(x, y, angle, length=length, area=area, volume=volume)
    vol.plot_me()

