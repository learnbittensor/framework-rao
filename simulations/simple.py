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
