import matplotlib.pyplot as plt
import pandas as pd
from .utils import read_json

class PlotStyle:
    @staticmethod
    def setup_plot_style():
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(7.5, 5))
        fig.patch.set_facecolor('black')
        return fig

    @staticmethod
    def get_colors(df, id_column, cmap_name):
        num_items = df[id_column].nunique()
        return [plt.get_cmap(cmap_name)(i) for i in range(num_items)]

    @staticmethod
    def setup_axis(ax, title, xlabel=None, ylabel=None):
        ax.set_facecolor('black')
        ax.set_title(title, color='white', fontsize=14)
        if xlabel:
            ax.set_xlabel(xlabel, color='white', fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, color='white', fontsize=12)
        ax.tick_params(colors='white')
        return ax

    @staticmethod
    def create_legend(ax, **kwargs):
        return ax.legend(loc='upper right', facecolor='black', edgecolor='black',
                        labelcolor='white', fontsize=10, **kwargs)

class BasePlot:
    def __init__(self, data_dir, blocks, n_steps):
        self.data_dir = data_dir
        self.blocks = blocks
        self.n_steps = n_steps
        self.load_data()
        
    def load_data(self):
        self.subnets_data = read_json(f"{self.data_dir}/subnets.json")
        self.accounts_data = read_json(f"{self.data_dir}/accounts.json")
        self.subtensor_data = read_json(f"{self.data_dir}/subtensor.json")
        self.trades_data = read_json(f"{self.data_dir}/trades.json")

        self.subnets_df = pd.DataFrame(self.subnets_data)
        self.accounts_df = pd.DataFrame(self.accounts_data)
        self.subtensor_df = pd.DataFrame(self.subtensor_data)
        self.trades_df = pd.DataFrame(self.trades_data)

    def plot(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement plot method")
