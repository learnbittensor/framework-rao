from src.plotting import BasePlot, PlotStyle
import matplotlib.pyplot as plt

class AccountBalancePlot(BasePlot):
    def plot(self, account_id: int = 1):
        fig = PlotStyle.setup_plot_style()
        
        # Get data for specific account
        account_data = self.accounts_df[self.accounts_df['account_id'] == account_id]
        
        # Create plot
        ax = PlotStyle.setup_axis(
            plt.subplot(1, 1, 1),
            f'Account {account_id} Value Over Time',
            'Block Number',
            'Market Value'
        )
        
        # Plot balance
        ax.plot(account_data['block'], 
                account_data['market_value'],
                color='cyan',
                label='Market Value')
        
        PlotStyle.create_legend(ax)
        plt.tight_layout()
