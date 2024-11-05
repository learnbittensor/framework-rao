from src.plotting import BasePlot, PlotStyle
import matplotlib.pyplot as plt
import numpy as np

class DashboardPlot(BasePlot):
    def plot(self):
        fig = PlotStyle.setup_plot_style()
        
        checkpoints = np.linspace(0, self.blocks, int(self.n_steps) + 1, dtype=int)[:-1]
        interval_labels = [str(i) for i in range(len(checkpoints))]
        
        non_root_subnets_df = self.subnets_df[self.subnets_df['subnet_id'] != 0]
        non_root_subnets = non_root_subnets_df['subnet_id'].unique()

        s_colors = PlotStyle.get_colors(non_root_subnets_df, 'subnet_id', 'Set1')
        a_colors = PlotStyle.get_colors(self.accounts_df, 'account_id', 'Set2')

        ax1 = PlotStyle.setup_axis(plt.subplot(2, 2, 1), 'Exchange Rates Over Time')
        exchange_rates_pivot = non_root_subnets_df.pivot(index='block', 
                                                        columns='subnet_id', 
                                                        values='exchange_rate')
        for i, subnet in enumerate(non_root_subnets):
            ax1.plot(exchange_rates_pivot.index, 
                    exchange_rates_pivot[subnet],
                    label=f'Subnet {subnet}', 
                    color=s_colors[i])
        PlotStyle.create_legend(ax1)

        ax2 = PlotStyle.setup_axis(plt.subplot(2, 2, 2), 'User Balances Over Time')
        balances_pivot = self.accounts_df.pivot(index='block', 
                                              columns='account_id', 
                                              values='market_value')
        for i, account in enumerate(balances_pivot.columns):
            ax2.plot(balances_pivot.index, 
                    balances_pivot[account],
                    label=f'User {account}', 
                    color=a_colors[i])
        PlotStyle.create_legend(ax2)

        ax3 = PlotStyle.setup_axis(plt.subplot(2, 2, 3), 
                                 'Emission Rates Over Time',
                                 'Blocks', 
                                 'Emission Rate')
        emission_data = non_root_subnets_df.pivot(index='block', 
                                                 columns='subnet_id',
                                                 values='emission_rate').fillna(0)
        emission_data.plot(kind='bar', 
                         stacked=True, 
                         ax=ax3, 
                         color=s_colors, 
                         legend=False)
        ax3.tick_params(axis='x', rotation=45)

        ax4 = PlotStyle.setup_axis(plt.subplot(2, 2, 4), 
                                 'Sum of Subnet Exchange Rates Over Time',
                                 'Interval', 
                                 'Sum of Exchange Rates')
        ax4.plot(self.subtensor_df['block'], 
                self.subtensor_df['sum_prices'],
                color='cyan', 
                label='Sum of Exchange Rates')

        for ax in [ax1, ax2, ax4]:
            ax.set_xticks(checkpoints)
            ax.set_xticklabels(interval_labels)

        plt.tight_layout()
