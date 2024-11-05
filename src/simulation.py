from .models import Subnet, Account, Trade
from .subtensor import Subtensor


def run_simulation(config):
    blocks = config['blocks']
    n_steps = config['n_steps']
    subnets = config['subnets']
    accounts = config['accounts']
    trades = config['trades']
    tao_supply = config['tao_supply']
    global_split = config['global_split']
    balanced = config['balanced']
    root_weight = config['root_weight']

    subtensor = Subtensor(
        subnets=subnets,
        accounts=accounts,
        trades=trades,
        tao_supply=tao_supply,
        global_split=global_split,
        balanced=balanced,
        root_weight=root_weight,
        blocks=blocks,
        n_steps=n_steps
    )

    subtensor.run_simulation()
