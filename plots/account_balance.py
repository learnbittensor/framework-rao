from src.plotting import BasePlot, PlotStyle
import matplotlib.pyplot as plt
import numpy as np

class AccountBalancePlot(BasePlot):
    def plot(self, account_id: int = 1):
        fig = PlotStyle.setup_plot_style()
        
        # Get data for specific account
        account_data = self.accounts_df[self.accounts_df['account_id'] == account_id]
        
        # Create plot
        ax = PlotStyle.setup_axis(
            plt.subplot(1, 1, 1),
            f'Account {account_id} Balance Over Time',
            'Block Number',
            'Full Balance'
        )
        
        # Plot balance
        ax.plot(account_data['block'], 
                account_data['market_value'],
                color='cyan',
                label='Full Balance')
        
        PlotStyle.create_legend(ax)
        plt.tight_layout()
