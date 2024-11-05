from src.plotting import BasePlot, PlotStyle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class SubnetDividendsPlot(BasePlot):
    def plot(self, subnet_id: int = 1):
        fig = PlotStyle.setup_plot_style()
        
        checkpoints = np.linspace(0, self.blocks, int(self.n_steps) + 1, dtype=int)[:-1]
        interval_labels = [str(i) for i in range(len(checkpoints))]
        
        subnet_data = self.subnets_df[self.subnets_df['subnet_id'] == subnet_id]
        
        dividends_df = pd.DataFrame(subnet_data['dividends'].tolist(), 
                                  index=subnet_data['block'])
        
        ax1 = PlotStyle.setup_axis(plt.subplot(1, 1, 1), f'Dividends Over Time for Subnet {subnet_id}')
        
        u_colors = PlotStyle.get_colors(
            pd.DataFrame({'account_id': dividends_df.columns}), 
            'account_id', 
            'Set2'
        )
        
        for i, account_id in enumerate(dividends_df.columns):
            ax1.plot(dividends_df.index, dividends_df[account_id],
                    label=f'User {account_id}', color=u_colors[i])
        
        PlotStyle.create_legend(ax1)
        ax1.set_xticks(checkpoints)
        ax1.set_xticklabels(interval_labels)
        ax1.set_ylabel('Dividend Value')
        
        plt.tight_layout()
