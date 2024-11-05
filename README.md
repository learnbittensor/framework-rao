## RAO Simulation - "Framework"

![Thumbail of RAO Simulation](media/thumbnail.png)

A simulation framework for modeling and analyzing subnet interactions, account balances, and trade activities within the RAO network. The project includes modules for running simulations, storing results, and visualizing outcomes through plots.

## Requirements

- **Python 3.7+**
- `matplotlib`
- `numpy`
- `pandas`

## Installation

1. **Clone the Repository:**
```bash
git clone https://github.com/learnbittensor/rao-simulation.git
cd rao-simulation
```

2. **Install Dependencies:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Basic Simulation Example

Create a simple simulation in `simulations/simple.py`:

```python
from src.models import Subnet, Account, Trade
from src.simulation import run_simulation
import argparse

blocks = 1000  # Run for 1000 blocks
n_steps = 10   # Log data every 100 blocks

# Create two subnets: one root and one regular
subnets = [
    Subnet(id=0, tao_in=100.0, alpha_in=100.0, alpha_out=100.0, is_root=True),
    Subnet(id=1, tao_in=100.0, alpha_in=100.0, alpha_out=100.0)
]

# Create two accounts with initial stake
accounts = [
    Account(id=1, free_balance=50.0, alpha_stakes={0: 50.0}, registered_subnets=[0, 1]),
    Account(id=2, free_balance=0.0, alpha_stakes={1: 100.0}, registered_subnets=[1])
]

# Define some trades
trades = [
    Trade(block=500, account_id=1, subnet_id=0, action='sell', amount='50%'),
    Trade(block=750, account_id=2, subnet_id=1, action='sell', amount='all')
]

config = {
    "blocks": blocks,
    "n_steps": n_steps,
    "subnets": subnets,
    "accounts": accounts,
    "trades": trades,
    "tao_supply": 200.0,
    "global_split": 0.5,
    "balanced": True,
    "root_weight": 0.5
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--plots', nargs='+', help='List of plot modules to run')
    args = parser.parse_args()

    run_simulation(config, args.plots if args.plots else [])
```

### Basic Plot Example

Create a simple plot in `plots/account_value.py`:

```python
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
            'Account Values Over Time',
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
```

### Running Simulations and Plots

1. **Run simulation only:**
```bash
python3 -m simulations.simple
```

2. **Run simulation with specific plot:**
```bash
python3 -m simulations.simple --plots plots.dashboard
```

3. **Run simulation with plot parameters (in this example the account id to be
   tracked):**
```bash
python3 -m simulations.simple --plots 'plots.account_value[1]'
```

4. **Run simulation with multiple plots:**
```bash
python3 -m simulations.simple --plots 'plots.account_value[1]' 'plots.account_value[2]'
```
**Note***: When using plot parameters (square brackets), wrap the argument in quotes to prevent shell interpretation.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Modified and reused code from the simulation notebook of Const. (Thank you) <3
