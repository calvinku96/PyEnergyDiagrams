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


class ED:
    def __init__(self, aspect='equal'):
        # plot parameters
        self.ratio = 1.6181
        self.dimension = 'auto'
        self.space = 'auto'
        self.offset = 'auto'
        self.offset_ratio = 0.02
        self.color_bottom_text = 'blue'
        self.color_top_text = 'blue'
        self.color_left_text = 'blue'
        self.color_right_text = 'blue'
        self.aspect = aspect
        self.round_energies_at_digit = "keep all digits"
        # data
        self.pos_number = 0
        self.energies = []
        self.positions = []
        self.colors = []
        self.top_texts = []
        self.bottom_texts = []
        self.left_texts = []
        self.right_texts = []
        self.links = []
        self.arrows = []
        self.electons_boxes = []
        self.level_hline_kwargs = []
        self.text_offsets = []

        self.plot_dots_kwargs = {
            'marker': 'o',
            'linestyle': '',
        }
        # matplotlib fiugre handlers
        self.fig = None
        self.ax = None

    def add_level(self, energy, bottom_text='', position=None, color='k',
                  top_text='', right_text='', left_text='',
                  text_offsets = {
                      'bottom': (0.,0.),
                      'top':    (0.,0.),
                      'left':   (0.,0.),
                      'right':  (0.,0.),
                  },
                  linestyle='solid', **kwargs):
        '''
        Method of ED class
        This method add a new energy level to the plot.

        Parameters
        ----------
        energy : int
                 The energy of the level in Kcal mol-1
        bottom_text  : str
                The text on the bottom of the level (label of the level)
                (default '')
        position  : str
                The position of the level in the plot. Keep it empty to add
                the level on the right of the previous level use 'last' as
                argument for adding the level to the last position used
                for the level before.
                An integer can be used for adding the level to an arbitrary
                position.
                (default  None)
        color  : str
                Color of the level  (default  'k')
        top_text  : str
                Text on the top of the level. (default '')
        right_text  : str
                Text at the right of the level. (default  '')
        left_text  : str
                Text at the left of the level. (default  '')
        text_offsets : dict
                Offsets in data coordinates to apply to the text.
                This method inserts (0.,0.) for missing key
                ('bottom', 'top', 'left', 'right')
        linestyle  : str
                The linestyle of the level, one of the following values:
                'solid', 'dashed', 'dashdot', 'dotted' (default  'solid')
        **kwargs : dict
                Arguments passed on to axhline.

        Returns
        -------
        id of energy level for add_link
        '''

        if position is None:
            position = self.pos_number + 1
            self.pos_number += 1
        elif isinstance(position, (int, float)):
            pass
        elif position == 'last' or position == 'l':
            position = self.pos_number
        else:
            raise ValueError(
                "Position must be None or 'last' (abrv. 'l') or in case an integer or float specifing the position. It was: %s" % position)
        if top_text == 'Energy':
            if self.round_energies_at_digit == "keep all digits":
                top_text = energy
            else:
                top_text = round(energy,self.round_energies_at_digit)

        offsets = {
            'bottom': (0.,0.),
            'top':    (0.,0.),
            'left':   (0.,0.),
            'right':  (0.,0.),
        }
        if text_offsets is not None:
            offsets |= text_offsets

        id = len(self.energies)
        self.colors.append(color)
        self.energies.append(energy)
        self.positions.append(position)
        self.top_texts.append(top_text)
        self.bottom_texts.append(bottom_text)
        self.left_texts.append(left_text)
        self.right_texts.append(right_text)
        self.level_hline_kwargs.append({'linestyle': linestyle} | kwargs)
        self.text_offsets.append(offsets)
        self.arrows.append([])
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

        Returns
        -------
        Append arrow to self.arrows

        '''
        self.arrows[start_level_id].append(end_level_id)

    def add_link(self, start_level_id, end_level_id,
                 color='k', ls='--', linewidth=1, **kwargs):
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
        ls : str
                line styple e.g. -- , ..
        linewidth : int
                line width
        **kwargs : dict
                Additional arguments to Line2D

        Returns
        -------
        Append link to self.links

        '''
        self.links.append((
            start_level_id, end_level_id,
            {
                'color': color,
                'ls': ls,
                'linewidth': linewidth
            } | kwargs
        ))

    def add_electronbox(self,
                        level_id,
                        boxes,
                        electrons,
                        side=0.5,
                        spacing_f=5,
                        priority='up'):
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
        x = self.positions[level_id] * \
            (self.dimension+self.space)+self.dimension*0.5
        y = self.energies[level_id]
        self.electons_boxes.append((x, y, boxes, electrons, side, spacing_f, priority))

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

        self.__create_figure_ax(ax, ylabel)
        self.__auto_adjust()

        data = zip(self.energies,
                   self.positions,
                   self.bottom_texts,
                   self.top_texts,
                   self.right_texts,
                   self.left_texts,
                   self.colors,
                   self.level_hline_kwargs,
                   self.text_offsets)

        for ener,pos,bot,top,right,left,color,kw,toff in data:
            start  = pos*(self.dimension+self.space)
            middle = start + self.dimension/2.
            end    = start + self.dimension
            self.ax.hlines(ener, start, end, color=color, **kw)
            to = toff['top']
            bo = toff['bottom']
            lo = toff['left']
            ro = toff['right']
            self.ax.text(middle+to[0], ener+self.offset+to[1], top,
                         horizontalalignment='center',
                         verticalalignment='bottom',
                         color=self.color_top_text)
            self.ax.text(end+ro[0], ener+ro[1], right,
                         horizontalalignment='left',
                         verticalalignment='center',
                         color=self.color_right_text)
            self.ax.text(start+lo[0], ener+lo[1], left,
                         horizontalalignment='right',
                         verticalalignment='center',
                         color=self.color_left_text)
            self.ax.text(middle+bo[0], ener-self.offset*2+bo[1], bot,
                         horizontalalignment='center',
                         verticalalignment='top',
                         color=self.color_bottom_text)
        if show_IDs:
            # for showing the ID allowing the user to identify the level
            for ind,(ener,pos) in enumerate(zip(self.energies,self.positions)):
                start = pos * (self.dimension + self.space)
                self.ax.text(start, ener+self.offset, str(ind),
                             horizontalalignment='right', color='red')

        for idx, arrow in enumerate(self.arrows):
            # by Kalyan Jyoti Kalita: put arrows between to levels
            # x1, x2   y1, y2
            for i in arrow:
                start = self.positions[idx]*(self.dimension+self.space)
                x1 = start + 0.5*self.dimension
                x2 = start + 0.5*self.dimension
                y1 = self.energies[idx]
                y2 = self.energies[i]
                gap = y1-y2
                gapnew = '{0:.2f}'.format(gap)
                middle = y1-0.5*gap  # warning: this way works for negative HOMO/LUMO energies
                self.ax.annotate("", xy=(x1, y1), xytext=(x2, middle), arrowprops=dict(
                    color='green', width=2.5, headwidth=5))
                self.ax.annotate(gapnew, xy=(x2, y2), xytext=(x1, middle), color='green', arrowprops=dict(width=2.5, headwidth=5, color='green'),
                            bbox=dict(boxstyle='round', fc='white'),
                            ha='center', va='center')

        for (i1,i2,kw) in self.links:
            pos1 = self.positions[i1]
            pos2 = self.positions[i2]
            ener1 = self.energies[i1]
            ener2 = self.energies[i2]

            x1 = pos1*(self.dimension+self.space) + self.dimension
            x2 = pos2*(self.dimension+self.space)
            y1 = ener1
            y2 = ener2
            self.ax.add_line(Line2D([x1,x2], [y1,y2], **kw))

        for box in self.electons_boxes:
            # here we add the boxes
            # x,y,boxes,electrons,side,spacing_f
            x, y, boxes, electrons, side, spacing_f, priority = box
            plot_orbital_boxes(self.ax, x, y, boxes, electrons, side, spacing_f, priority)

        return self.fig, self.ax

    def plot_dots(self, show_IDs=False, ylabel="Energy / $kcal$ $mol^{-1}$", ax: plt.Axes = None):
        self.__create_figure_ax(ax, ylabel)
        self.__auto_adjust()

        for (i1,i2,kw) in self.links:
            pos1 = self.positions[i1]
            pos2 = self.positions[i2]
            ener1 = self.energies[i1]
            ener2 = self.energies[i2]

            x1 = pos1*(self.dimension+self.space) + 0.5 * self.dimension
            x2 = pos2*(self.dimension+self.space) + 0.5 * self.dimension
            y1 = ener1
            y2 = ener2
            self.ax.add_line(Line2D([x1,x2], [y1,y2], **kw))

        data = zip(self.energies,
                   self.positions,
                   self.bottom_texts,
                   self.top_texts,
                   self.left_texts,
                   self.right_texts,
                   self.colors,
                   self.text_offsets)
        for ener,pos,bot,top,left,right,colors,toff in data:
            start  = pos*(self.dimension+self.space)
            middle = start + self.dimension/2.
            end    = start + self.dimension
            to = toff['top']
            bo = toff['bottom']
            lo = toff['left']
            ro = toff['right']
            hpad = self.dimension * 0.2
            self.ax.text(middle+to[0], ener+self.offset+to[1], top,
                         horizontalalignment='center',
                         verticalalignment='bottom',
                         color=self.color_top_text)
            self.ax.text(middle+hpad+ro[0], ener+ro[1], right,
                         horizontalalignment='left',
                         verticalalignment='center',
                         color=self.color_right_text)
            self.ax.text(middle-hpad+lo[0], ener+lo[1], left,
                         horizontalalignment='right',
                         verticalalignment='center',
                         color=self.color_left_text)
            self.ax.text(middle+bo[0], ener-self.offset*2+bo[1], bot,
                         horizontalalignment='center',
                         verticalalignment='top',
                         color=self.color_bottom_text)
        if show_IDs:
            for ind,(ener,pos) in enumerate(zip(self.energies,self.positions)):
                start = pos * (self.dimension + self.space)
                self.ax.text(start, ener+self.offset, str(ind),
                             horizontalalignment='right', color='red')

        x_pos = [e*(self.dimension+self.space)+self.dimension/2. for e in self.positions]
        self.ax.plot(x_pos, self.energies, **self.plot_dots_kwargs)

        return self.fig, self.ax

    def __create_figure_ax(self, ax, ylabel):
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
        Energy_variation = abs(max(self.energies) - min(self.energies))
        if self.dimension == 'auto' or self.space == 'auto':
            # Unique positions of the levels
            unique_positions = float(len(set(self.positions)))
            space_for_level = Energy_variation*self.ratio/unique_positions
            self.dimension = space_for_level*0.7
            self.space = space_for_level*0.3

        if self.offset == 'auto':
            self.offset = Energy_variation*self.offset_ratio


if __name__ == '__main__':
    a = ED()
    level0 = a.add_level(0, 'Separated Reactants')
    level1 = a.add_level(-5.4, 'mlC1')
    level2 = a.add_level(-15.6, 'mlC2', 'last',)
    level3 = a.add_level(28.5, 'mTS1', color='g')
    level4 = a.add_level(-9.7, 'mCARB1')
    level5 = a.add_level(-19.8, 'mCARB2', 'last')
    level6 = a.add_level(20, 'mCARBX', 'last')
    a.add_link(level0, level1, color='r')
    a.add_link(level0, level2)
    a.add_link(level2, level3, color='b')
    a.add_link(level1, level3)
    a.add_link(level3, level4, color='g')
    a.add_link(level3, level5)
    a.add_link(level0, level6)
    a.add_electronbox(level_id=0, boxes=1, electrons=2, side=3, spacing_f=3)
    a.add_electronbox(level3, 3, 1, 3, 3)
    a.add_electronbox(level5, 3, 5, 3, 3)
    a.add_arrow(level6, level4)
    a.offset *= 2
    a.plot(show_IDs=True)
