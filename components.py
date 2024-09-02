#!/usr/bin/env python3

import re

import matplotlib.pyplot as plt

from shapes import Volume, Junction

def process_cmp_info(cmp_lines:list):
    """ Function will read in component input lines and return a processed component."""

    component = dict()

    component['type'] = 'PIPE'
    component['name'] = 'NAME'

    return component


class Pipe:
    """ A pipe comprises one or more volumes with junctions between them."""

    name = None
    num_vols = None
    num_juns = None
    volumes = list()
    junctions = list()

    # TODO: Add black lines around the volumes
    def __init__(self, pipe_info: dict):
        """ pipe_info is a dictionary that has the information necessary to process a pipe component

            nv is the number of volumes
            pipe_info['vol_info'] is a dictionary that contains read information for every volume
                x_start
                y_start
                flow_area
                length
                volume
                inclination_angle
                volume_number
            pipe_info['jun_info'] is a dictionary that contains read information for every junction
                from_component
                to_component
            """
        x_start = 0.0
        if 'x_start' in pipe_info:
            x_start = pipe_info['x_start']
        y_start = 0.0
        if 'y_start' in pipe_info:
            y_start = pipe_info['y_start']

        self.num_vols = 0
        if 'name' in pipe_info:
            self.name = pipe_info['name']
        if 'vol_info' in pipe_info:
            for vol in pipe_info['vol_info']:
                self.num_vols += 1
                flow_area = vol['flow_area']
                length = vol['length']
                volume = vol['volume']
                inclination_angle = vol['inclination_angle']
                volume_number = vol['volume_number']
                new_vol = Volume(x_start, y_start, inclination_angle,
                                 vol_length=length, vol_volume=volume,
                                 vol_area=flow_area, vol_no=volume_number)
                self.volumes.append(new_vol)
                x_start, y_start = new_vol.return_outlet_coordinates()

        self.num_juns = self.num_vols - 1
        # Iterate through the volumes to
        for i, vol in enumerate(self.volumes):
            if i < len(self.volumes)-1:
                from_cmp = int(vol.vol_no)
                to_cmp = int(self.volumes[i+1].vol_no)
                new_jun = Junction(from_cmp, to_cmp)
                self.junctions.append(new_jun)

    def return_outlet_coordinates(self):
        if len(self.volumes) <= 0:
            raise Exception(f'Pipe {self.name} has no volumes!')
        return self.volumes[-1].get_outlet_coordinates()

    def return_inlet_coordinates(self):
        if len(self.volumes) <= 0:
            raise Exception(f'Pipe {self.name} has no volumes!')
        return self.volumes[0].get_inlet_coordinates()

    def plot_me(self, show_inner_junctions=False):
        patches = list()
        fig, ax = plt.subplots()
        for i, vol in enumerate(self.volumes):
            patches.append(vol.return_figure())
            if show_inner_junctions:
                if (i > 0) and (i < len(self.volumes)-1):
                    ax.plot((vol.inlet_coordinates[0], vol.outlet_coordinates[0]),
                            (vol.inlet_coordinates[1],  vol.outlet_coordinates[1]), 'o')
        for patch in patches:
            ax.add_patch(patch)

        plt.autoscale()
        plt.show()


if __name__ == '__main__':
    pipe_info = dict()
    pipe_info['name'] = 'TEST'
    pipe_info['type'] = 'PIPE'
    pipe_info['vol_info'] = list()
    start_x = 0.0
    start_y = 0.0
    for i in range(1, 6):
        flow_area = 2.0
        length = i*2.0
        volume = None
        inclination_angle = 90.0
        volume_number = f'101{i:02}0000'
        pipe_info['vol_info'].append({
            'flow_area': flow_area,
            'length': length,
            'volume': volume,
            'inclination_angle': inclination_angle,
            'volume_number': volume_number
        })
    pipe = Pipe(pipe_info)
    pipe.plot_me(show_inner_junctions=True)

