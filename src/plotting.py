import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .utils import read_json


def setup_plot_style():
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(15, 10))
    fig.patch.set_facecolor('black')
    return fig


def get_colors(df, id_column, cmap_name):
    num_items = df[id_column].nunique()
    return [plt.get_cmap(cmap_name)(i) for i in range(num_items)]


def setup_axis(ax, title, xlabel=None, ylabel=None):
    ax.set_facecolor('black')
    ax.set_title(title, color='white', fontsize=14)
    if xlabel:
        ax.set_xlabel(xlabel, color='white', fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, color='white', fontsize=12)
    ax.tick_params(colors='white')
    return ax


def create_legend(ax, **kwargs):
    return ax.legend(loc='upper right', facecolor='black', edgecolor='black',
                    labelcolor='white', fontsize=10, **kwargs)


def plot_simulation_results(data_dir, blocks, n_steps):
    subnets_data = read_json(f"{data_dir}/subnets.json")
    accounts_data = read_json(f"{data_dir}/accounts.json")
    subtensor_data = read_json(f"{data_dir}/subtensor.json")
    trades_data = read_json(f"{data_dir}/trades.json")

    subnets_df = pd.DataFrame(subnets_data)
    accounts_df = pd.DataFrame(accounts_data)
    subtensor_df = pd.DataFrame(subtensor_data)
    trades_df = pd.DataFrame(trades_data)

    fig = setup_plot_style()

    checkpoints = np.linspace(0, blocks, (int(blocks / n_steps)) + 1, dtype=int)[:-1]
    day_labels = [str(i) for i in range(len(checkpoints))]
    non_root_subnets = [s for s in subnets_df['subnet_id'].unique() if s != 0]

    s_colors = get_colors(subnets_df[subnets_df['subnet_id'].isin(non_root_subnets)], 'subnet_id', 'Set1')
    a_colors = get_colors(accounts_df, 'account_id', 'Set2')

    ax1 = setup_axis(plt.subplot(2, 2, 1), 'Exchange Rates Over Time')
    for i, subnet in enumerate(non_root_subnets):
        subnet_data = subnets_df[subnets_df['subnet_id'] == subnet]
        ax1.plot(subnet_data['block'], subnet_data['exchange_rate'],
                 label=f'Subnet {subnet}', color=s_colors[i])
    create_legend(ax1)

    ax2 = setup_axis(plt.subplot(2, 2, 2), 'User Balances Over Time')
    for i, account in enumerate(accounts_df['account_id'].unique()):
        account_data = accounts_df[accounts_df['account_id'] == account]
        ax2.plot(account_data['block'], account_data['market_value'],
                 label=f'User {account}', color=a_colors[i])
    create_legend(ax2)

    ax3 = setup_axis(plt.subplot(2, 2, 3), 'Emission Rates Over Time',
                     'Blocks', 'Emission Rate')
    filtered_df = subnets_df[subnets_df['subnet_id'] != 0]
    emission_data = filtered_df.pivot(index='block', columns='subnet_id',
                                      values='emission_rate').fillna(0)
    emission_data.plot(kind='bar', stacked=True, ax=ax3, color=s_colors, legend=False)
    ax3.tick_params(axis='x', rotation=45)

    ax4 = setup_axis(plt.subplot(2, 2, 4), 'Sum of Subnet Exchange Rates Over Time',
                     'Days', 'Sum of Exchange Rates')
    ax4.plot(subtensor_df['block'], subtensor_df['sum_prices'],
             color='cyan', label='Sum of Exchange Rates')
    create_legend(ax4)

    for ax in [ax1, ax2, ax4]:
        ax.set_xticks(checkpoints)
        ax.set_xticklabels(day_labels)

    plt.tight_layout()
    plt.show()
