# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:09:19 2017

--- Energy profile diagram---
This is a simple script to plot energy profile diagram using matplotlib.
E|          4__
n|   2__    /  \
e|1__/  \__/5   \
r|  3\__/       6\__
g|
y|
@author: Giacomo Marchioro giacomomarchioro@outlook.com

"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from .box_notation import plot_orbital_boxes
import math
from typing import Union, Tuple
from dataclasses import dataclass


@dataclass
class EnergyLevel:
    energy: float
    bottom_text: str
    top_text: str
    left_text: str
    right_text: str
    pos: int
    line_kw: dict
    bottom_text_kw: dict
    top_text_kw: dict
    left_text_kw: dict
    right_text_kw: dict

@dataclass
class Link:
    start_id: int
    end_id: int
    link_kw: dict
    label: str
    label_rot: Union[str, float]
    label_offset: Tuple[int, int]
    label_kwargs: dict


class ED:
    def __init__(self, **kwargs):
        # plot parameters
        self.ratio = kwargs.get('ratio', 1.6181)
        self.dimension = kwargs.get('dimension', 'auto')
        self.space = kwargs.get('space', 'auto')
        self.offset = kwargs.get('offset', 'auto')
        self.offset_ratio = kwargs.get('offset_ratio', 0.02)
        self.aspect = kwargs.get('aspect', 'equal')

        self.top_text_kwargs = kwargs.get('top_text_kwargs', {
            "fontsize": "medium",
            "color": "blue",
            "horizontalalignment": "center",
            "verticalalignment": "bottom",
        })
        self.bottom_text_kwargs = kwargs.get('bottom_text_kwargs', {
            "fontsize": "medium",
            "color": "blue",
            "horizontalalignment": "center",
            "verticalalignment": "top",
        })
        self.left_text_kwargs = kwargs.get('left_text_kwargs', {
            "fontsize": "medium",
            "color": "black",
            "horizontalalignment": "right",
            "verticalalignment": "center",
        })
        self.right_text_kwargs = kwargs.get('right_text_kwargs', {
            "fontsize": "medium",
            "color": "black",
            "horizontalalignment": "left",
            "verticalalignment": "center",
        })

        # data
        self.pos_number = 0
        self.levels = []
        self.links = []
        self.arrows = []
        self.electons_boxes = []

    def add_level(
        self, energy,
        bottom_text='', position=None, color='k',
        top_text='Energy', right_text='', left_text='',
        linestyle='solid',
        line_kwargs={}, bottom_text_kwargs={}, top_text_kwargs={},
        right_text_kwargs={}, left_text_kwargs={}
    ):
        '''
        Method of ED class
        This method add a new energy level to the plot.
        Parameters
        ----------
        energy : float
                 The energy of the level in Kcal mol-1
        bottom_text  : str
                The text on the bottom of the level (label of the level)
                (default '')
        position  : str | int
                The position of the level in the plot. Keep it empty to add
                the level on the right of the previous level use 'last' as
                argument for adding the level to the last position used
                for the level before.
                An integer can be used for adding the level to an arbitrary
                position.
                (default None)
        color  : str
                Color of the level  (default  'k')
        top_text  : str
                Text on the top of the level. By default it will print the
                energy of the level. (default  'Energy')
        right_text  : str
                Text at the right of the level. (default  '')
        left_text  : str
                Text at the left of the level. (default  '')
        linestyle  : str
                The linestyle of the level, one of the following values:
                'solid', 'dashed', 'dashdot', 'dotted' (default  'solid')
        bottom_text_kwargs : dict
                This will be passed to matplotlib.axes.Axes.text as keyword
                arguments for bottom_text
                (default {})
        top_text_kwargs : dict
                This will be passed to matplotlib.axes.Axes.text as keyword
                arguments for top_text
                (default {})
        right_text_kwargs : dict
                This will be passed to matplotlib.axes.Axes.text as keyword
                arguments for right_text
                (default {})
        left_text_kwargs : dict
                This will be passed to matplotlib.axes.Axes.text as keyword
                arguments for left_text
                (default {})
        Returns
        -------
        id of the level
        '''

        if position is None:
            position = self.pos_number
            self.pos_number += 1
        elif isinstance(position, (int, float)):
            pass
        elif position == 'last' or position == 'l':
            position = self.pos_number
        else:
            raise ValueError(
                f"Position must be None or 'last' (abrv. 'l') or in case an integer or float specifing the position. It was: {position}"
            )

        if top_text == 'Energy':
            top_text = f"{energy:.3g}"

        id = len(self.levels)
        self.levels.append(EnergyLevel(
            energy,
            bottom_text,
            top_text,
            left_text,
            right_text,
            position,
            {'color': color, 'linestyle': linestyle} | line_kwargs,
            bottom_text_kwargs,
            top_text_kwargs,
            left_text_kwargs,
            right_text_kwargs,
        ))
        return id

    def add_arrow(self, start_level_id, end_level_id):
        '''
        Method of ED class
        Add a arrow between two energy levels using IDs of the level. Use
        self.plot(show_index=True) to show the IDs of the levels.
        Parameters
        ----------
        start_level_id : int
                 Starting level ID
        end_level_id : int
                 Ending level ID
        '''
        self.arrows.append((start_level_id, end_level_id))

    def add_link(
        self, start_level_id, end_level_id,
        color='k', linestyle='dashed', linewidth=1, link_kwargs={},
        label=None, label_rot="above", label_offset=(0.,0.), label_kwargs={}
    ):
        '''
        Method of ED class
        Add a link between two energy levels using IDs of the level. Use
        self.plot(show_index=True) to show the IDs of the levels.
        Parameters
        ----------
        start_level_id : int
                 Starting level ID
        end_level_id : int
                 Ending level ID
        color : str
                color of the line
                (default 'k')
        linestyle : str
                line style
                (default 'dashed')
        linewidth : int
                line width
                (default 1)
        link_kwargs : dict
                this will be passed to matplotlib.lines.Line2D of the link
                as kwargs
                this dict will override color, linestyle, and linewidth
                (default {})
        label : str | None
                add a label in the middle of the link
                (default None)
        label_rot : str | float
                "above", "below", "vertical", "horizontal", or float
                - above: above the line, rotated parallel to the line
                - below: below the line, rotated parallel to the line
                - vertical
                - horizontal
                - float: rotation in degrees
                (default "above")
        label_offset : tuple[float, float]
                if label_rot is either "above" or "below",
                  label_offset[0] is the offset parallel to the line
                  label_offset[1] is the offset perpendicular to the line
                if label_rot is either "vertical", "horizontal", or a float
                  label_offset[0] is the horizontal offset
                  label_offset[1] is the vertical offset
        label_kwargs : dict
                this will be passed to matplotlib.axes.Axes.text
                of the label
                this must not contain "rotation", use label_rot instead
                to specify rotation
        '''
        if "rotation" in label_kwargs:
            raise ValueError("'rotation' key found in label_kwargs, use label_rot to specify rotation")
        if not(label_rot in ("above", "below", "vertical", "horizontal") or isinstance(label_rot, (float, int))):
            raise ValueError("label_rot invalid value")

        self.links.append(Link(
            start_level_id, end_level_id,
            {'color': color, 'linestyle': linestyle, 'linewidth': linewidth} | link_kwargs,
            label, label_rot, label_offset, label_kwargs
        ))

    def add_electronbox(self,
                        level_id,
                        boxes,
                        electrons,
                        side=0.5,
                        spacing_f=5):
        '''
        Method of ED class
        Add a link between two energy levels using IDs of the level. Use
        self.plot(show_index=True) to show the IDs of the levels.

        Parameters
        ----------
        start_level_id : int
                 Starting level ID
        end_level_id : int
                 Ending level ID

        Returns
        -------
        Append link to self.links

        '''
        self.__auto_adjust()
        level_pos = self.get_level_line(level_id)
        x = 0.5 * (level_pos[0] + level_pos[1])
        y = self.levels[level_id].energy
        self.electons_boxes.append((x, y, boxes, electrons, side, spacing_f))


    def get_level_line(self, id):
        start = self.levels[id].pos * (self.dimension + self.space)
        return (start, start + self.dimension)

    def plot(self, show_IDs=False, ylabel="Energy / $kcal$ $mol^{-1}$", ax: plt.Axes = None):
        '''
        Method of ED class
        Plot the energy diagram. Use show_IDs=True for showing the IDs of the
        energy levels and allowing an easy linking.
        E|          4__
        n|   2__    /  \
        e|1__/  \__/5   \
        r|  3\__/       6\__
        g|
        y|

        Parameters
        ----------
        show_IDs : bool
            show the IDs of the energy levels
        ylabel : str
            The label to use on the left-side axis. "Energy / $kcal$
            $mol^{-1}$" by default.
        ax : plt.Axes
            The axes to plot onto. If not specified, a Figure and Axes will be
            created for you.

        Returns
        -------
        fig (plt.figure) and ax (fig.add_subplot())

        '''

        # Create a figure and axis if the user didn't specify them.
        if not ax:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, aspect=self.aspect)
        # Otherwise register the axes and figure the user passed.
        else:
            self.ax = ax
            self.fig = ax.figure

            # Constrain the target axis to have the proper aspect ratio
            self.ax.set_aspect(self.aspect)

        self.ax.set_ylabel(ylabel)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        self.__auto_adjust()

        def remove_offset(inp):
            return {k: v for k, v in inp.items() if k != "offset"}

        for idx, l in enumerate(self.levels):
            line_pos = self.get_level_line(idx)
            mid = 0.5 * (line_pos[0] + line_pos[1])
            self.ax.hlines(l.energy, line_pos[0], line_pos[1], **l.line_kw)
            ttext_offset = l.top_text_kw.get('offset', (0.0, 0.0))
            ttext_kw = self.top_text_kwargs | remove_offset(l.top_text_kw)
            self.ax.text(
                mid + ttext_offset[0],
                l.energy + self.offset + ttext_offset[1],
                l.top_text, **ttext_kw
            )
            btext_offset = l.bottom_text_kw.get('offset', (0.0, 0.0))
            btext_kw = self.bottom_text_kwargs | remove_offset(l.bottom_text_kw)
            self.ax.text(
                mid + btext_offset[0],
                l.energy - 2 * self.offset + btext_offset[1],
                l.bottom_text, **btext_kw
            )
            rtext_offset = l.right_text_kw.get('offset', (0.0, 0.0))
            rtext_kw = self.right_text_kwargs | remove_offset(l.right_text_kw)
            self.ax.text(
                line_pos[1] + rtext_offset[0],
                l.energy + rtext_offset[1],
                l.right_text, **rtext_kw
            )
            ltext_offset = l.left_text_kw.get('offset', (0.0, 0.0))
            ltext_kw = self.left_text_kwargs | remove_offset(l.left_text_kw)
            self.ax.text(
                line_pos[0] + ltext_offset[0],
                l.energy + ltext_offset[1],
                l.left_text, **ltext_kw
            )
            if show_IDs:
                self.ax.text(
                    line_pos[0], l.energy + self.offset, str(idx),
                    horizontalalignment='right', color='red'
                )


        for l in self.links:
            x1 = self.get_level_line(l.start_id)[1]
            x2 = self.get_level_line(l.end_id)[0]
            y1 = self.levels[l.start_id].energy
            y2 = self.levels[l.end_id].energy
            self.ax.add_line(Line2D((x1, x2), (y1, y2), **l.link_kw))
            if l.label:
                labelpos = [0.5 * (x1 + x2), 0.5 * (y1 + y2)]
                kw = {**l.label_kwargs}
                if l.label_rot in ("vertical", "horizontal") or isinstance(l.label_rot, (float, int)):
                    kw["rotation"] = l.label_rot
                    labelpos[0] += l.label_offset[0]
                    labelpos[1] += l.label_offset[1]
                elif l.label_rot in ("above", "below"):
                    rot = math.atan2(y2-y1,x2-x1)
                    kw["rotation"] = rot / math.pi * 180.0
                    kw["horizontalalignment"] = "center"
                    kw["verticalalignment"] = "center"
                    if l.label_rot == "below":
                        labelpos[0] +=  2.0 * self.offset * math.sin(rot)
                        labelpos[1] += -2.0 * self.offset * math.cos(rot)
                    else:
                        labelpos[0] += -1.5 * self.offset * math.sin(rot)
                        labelpos[1] +=  1.5 * self.offset * math.cos(rot)
                    labelpos[0] += l.label_offset[0] * math.cos(rot) - l.label_offset[1] * math.sin(rot)
                    labelpos[1] += l.label_offset[0] * math.sin(rot) + l.label_offset[1] * math.cos(rot)
                else:
                    raise ValueError("label_rot invalid value")

                self.ax.text(labelpos[0], labelpos[1], l.label, **kw)

        for idx, (start_id, end_id) in enumerate(self.arrows):
            # by Kalyan Jyoti Kalita: put arrows between to levels
            level_pos = self.get_level_line(start_id)
            x1 = 0.5 * (level_pos[0] + level_pos[1])
            x2 = x1
            y1 = self.levels[start_id].energy
            y2 = self.levels[end_id].energy
            gap = y1-y2
            gap_fmt = f"{gap:.2f}"
            middle = y1-0.5*gap  # warning: this way works for negative HOMO/LUMO energies
            self.ax.annotate(
                "", xy=(x1, y1), xytext=(x2, middle),
                arrowprops=dict(color='green', width=2.5, headwidth=5)
            )
            self.ax.annotate(
                gap_fmt, xy=(x2, y2), xytext=(x1, middle), color='green',
                arrowprops=dict(width=2.5, headwidth=5, color='green'),
                bbox=dict(boxstyle='round', fc='white'),
                ha='center', va='center'
            )

        for box in self.electons_boxes:
            # here we add the boxes
            # x,y,boxes,electrons,side,spacing_f
            x, y, boxes, electrons, side, spacing_f = box
            plot_orbital_boxes(self.ax, x, y, boxes, electrons, side, spacing_f)

    def __auto_adjust(self):
        '''
        Method of ED class
        This method use the ratio to set the best dimension and space between
        the levels.

        Affects
        -------
        self.dimension
        self.space
        self.offset

        '''
        # Max range between the energy
        energies = [l.energy for l in self.levels]
        pos = {l.pos for l in self.levels}
        Energy_variation = abs(max(energies) - min(energies))
        if self.dimension == 'auto' or self.space == 'auto':
            # Unique positions of the levels
            positions = float(max(pos) - min(pos) + 1)
            space_for_level = Energy_variation*self.ratio/positions
            self.dimension = space_for_level*0.7
            self.space = space_for_level*0.3

        if self.offset == 'auto':
            self.offset = Energy_variation*self.offset_ratio


if __name__ == '__main__':
    a = ED()
    a.bottom_text_fontsize='xx-small'
    a.top_text_fontsize='xx-small'
    a.add_level(0, 'Separated Reactants')
    a.add_level(-5.4, 'mlC1')
    a.add_level(-15.6, 'mlC2', 'last',)
    a.add_level(28.5, 'mTS1', color='g')
    a.add_level(-9.7, 'mCARB1')
    a.add_level(-19.8, 'mCARB2', 'last')
    a.add_level(20, 'mCARBX', 'last')
    a.add_link(0, 1, color='r')
    a.add_link(0, 2)
    a.add_link(2, 3, color='b')
    a.add_link(1, 3)
    a.add_link(3, 4, color='g')
    a.add_link(3, 5)
    a.add_link(0, 6)
    a.add_electronbox(level_id=0, boxes=1, electrons=2, side=3, spacing_f=3)
    a.add_electronbox(3, 3, 1, 3, 3)
    a.add_electronbox(5, 3, 5, 3, 3)
    a.add_arrow(6, 4)
    a.offset *= 2
    a.plot(show_IDs=True)
