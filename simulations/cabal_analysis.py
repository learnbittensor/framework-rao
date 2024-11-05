from src.models import Subnet, Account, Trade
from src.simulation import run_simulation
from src.plotting import plot_simulation_results

blocks = 13140000
n_steps = 547500


subnets = [
    Subnet(id=1, tao_in=100000, alpha_in=100000, alpha_out=100000),
    Subnet(id=2, tao_in=100000, alpha_in=100000, alpha_out=100000)
]

accounts = [
    Account(id=1, free_balance=350000, alpha_stakes={}, registered_subnets=[1, 2]),
    Account(id=2, free_balance=650000, alpha_stakes={}, registered_subnets=[1, 2])
]

trades = [
    Trade(block=0, account_id=1, subnet_id=1, action='stake', amount='all'),
    Trade(block=0, account_id=2, subnet_id=2, action='stake', amount='all'),
]

for block in range(blocks):
    trades.append(Trade(
        block=block,
        account_id=1,
        subnet_id=2,
        action='unstake',
        amount='all'
    ))

    trades.append(Trade(
        block=block,
        account_id=2,
        subnet_id=1,
        action='unstake',
        amount='all'
    ))

    trades.append(Trade(
        block=block,
        account_id=1,
        subnet_id=1,
        action='stake',
        amount='all'
    ))

    trades.append(Trade(
        block=block,
        account_id=2,
        subnet_id=2,
        action='stake',
        amount='all'
    ))

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
    run_simulation(config)
    plot_simulation_results("data", blocks, n_steps)
