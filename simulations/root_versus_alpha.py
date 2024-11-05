from src.models import Subnet, Account, Trade
from src.simulation import run_simulation
from src.plotting import plot_simulation_results

blocks = 3600
n_steps = 10

subnets = [
    Subnet(id=0, tao_in=100.0, alpha_in=100.0, alpha_out=100.0, is_root=True),
    Subnet(id=1, tao_in=100.0, alpha_in=100.0, alpha_out=100.0)
]

accounts = [
    Account(id=1, free_balance=0.0, alpha_stakes={0: 100.0}, registered_subnets=[0, 1]),
    Account(id=2, free_balance=0.0, alpha_stakes={1: 100.0}, registered_subnets=[1]),
]

#trades = []
trades = [
    Trade(block=blocks, account_id=1, subnet_id=0, action='sell', amount='all'),
    Trade(block=blocks, account_id=1, subnet_id=1, action='sell', amount='all'),

    Trade(block=blocks, account_id=2, subnet_id=1, action='sell', amount='all'),
]

config = {
    "blocks": blocks + 1,
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
    run_simulation(config)
    plot_simulation_results("data", blocks, n_steps)
