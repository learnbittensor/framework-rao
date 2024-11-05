from src.plotting import BasePlot, PlotStyle
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, List, Union

class AccountValuePlot(BasePlot):
    def plot(self, account_ids: Optional[Union[int, List[int]]] = None):
        fig = PlotStyle.setup_plot_style()
        
        if account_ids is None:
            account_ids = self.accounts_df['account_id'].unique()
        elif isinstance(account_ids, int):
            account_ids = [account_ids]
        
        colors = PlotStyle.get_colors(
            self.accounts_df[self.accounts_df['account_id'].isin(account_ids)],
            'account_id',
            'Set2'
        )
        
        ax = PlotStyle.setup_axis(
            plt.subplot(1, 1, 1),
            'Account Balances Over Time',
            'Block Number',
            'Full Balance'
        )
        
        for idx, account_id in enumerate(account_ids):
            account_data = self.accounts_df[self.accounts_df['account_id'] == account_id]
            ax.plot(account_data['block'], 
                    account_data['market_value'],
                    color=colors[idx],
                    label=f'Account {account_id}')
        
        PlotStyle.create_legend(ax)
        plt.tight_layout()
