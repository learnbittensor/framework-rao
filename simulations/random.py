from src.models import Subnet, Account, Trade
from src.simulation import run_simulation
import argparse

from typing import List
from collections import defaultdict
import random

def generate_trades(
    subnets: List[Subnet],
    accounts: List[Account], 
    blocks: int,
) -> List[Trade]:
    trades = []
    
    account_states = {
        account.id: {
            'free_balance': account.free_balance,
            'staked_alpha': defaultdict(float)
        } for account in accounts
    }

    for account in accounts:
        if account_states[account.id]['free_balance'] > 0 and account.registered_subnets:
            valid_subnets = [s for s in account.registered_subnets if any(sub.id == s for sub in subnets)]
            if valid_subnets:
                num_initial_stakes = random.randint(1, min(3, len(valid_subnets)))
                selected_subnets = random.sample(valid_subnets, num_initial_stakes)

                for subnet_id in selected_subnets:
                    try:
                        subnet = next(s for s in subnets if s.id == subnet_id)
                        stake_percentage = random.uniform(0.1, 0.5)
                        amt = account_states[account.id]['free_balance'] * stake_percentage
                        if amt > 0:
                            trades.append(Trade(
                                block=0,
                                account_id=account.id,
                                subnet_id=subnet.id,
                                action='buy',
                                amount=str(amt)
                            ))
                            account_states[account.id]['free_balance'] -= amt
                            account_states[account.id]['staked_alpha'][subnet.id] += amt
                    except StopIteration:
                        continue

    target_blocks = int(blocks * random.uniform(0.8, 0.9))
    trading_blocks = sorted(random.sample(range(1, blocks-1), target_blocks))
    account_frequencies = {account.id: random.randint(1, max(2, blocks // 20)) for account in accounts}

    for block in trading_blocks:
        active_accounts = [account for account in accounts if block % account_frequencies[account.id] == 0]

        for account in active_accounts:
            available_subnets = [
                subnet_id for subnet_id in account.registered_subnets
                if account_states[account.id]['staked_alpha'][subnet_id] > 0 and
                any(s.id == subnet_id for s in subnets)
            ]

            if account_states[account.id]['free_balance'] < 1.0 and available_subnets:
                subnet_id = random.choice(available_subnets)
                staked = account_states[account.id]['staked_alpha'][subnet_id]
                percentage = random.uniform(0.3, 0.7)
                amt = staked * percentage

                trades.append(Trade(
                    block=block,
                    account_id=account.id,
                    subnet_id=subnet_id,
                    action='sell',
                    amount=f"{percentage*100}%"
                ))
                account_states[account.id]['staked_alpha'][subnet_id] -= amt
                account_states[account.id]['free_balance'] += amt

            else:
                action = 'buy' if random.random() < 0.6 and account_states[account.id]['free_balance'] > 0 else 'sell'

                if action == 'buy' and account_states[account.id]['free_balance'] > 0:
                    valid_subnets = [s for s in account.registered_subnets if any(sub.id == s for sub in subnets)]
                    if valid_subnets:
                        subnet_id = random.choice(valid_subnets)
                        try:
                            subnet = next(s for s in subnets if s.id == subnet_id)
                            percentage = random.uniform(0.1, 0.5)
                            amt = account_states[account.id]['free_balance'] * percentage

                            trades.append(Trade(
                                block=block,
                                account_id=account.id,
                                subnet_id=subnet.id,
                                action='buy',
                                amount=str(amt)
                            ))
                            account_states[account.id]['free_balance'] -= amt
                            account_states[account.id]['staked_alpha'][subnet.id] += amt
                        except StopIteration:
                            continue

                elif action == 'sell' and available_subnets:
                    subnet_id = random.choice(available_subnets)
                    staked = account_states[account.id]['staked_alpha'][subnet_id]
                    percentage = random.uniform(0.1, 0.5)
                    amt = staked * percentage

                    trades.append(Trade(
                        block=block,
                        account_id=account.id,
                        subnet_id=subnet_id,
                        action='sell',
                        amount=f"{percentage*100}%"
                    ))
                    account_states[account.id]['staked_alpha'][subnet_id] -= amt
                    account_states[account.id]['free_balance'] += amt

    return sorted(trades, key=lambda x: (x.block, x.account_id))

blocks = 216000
n_steps = 12

subnets = [
    Subnet(id=0, tao_in=1000.0, alpha_in=1000.0, alpha_out=1000.0, is_root=True),
    *[Subnet(id=i, tao_in=1000.0, alpha_in=1000.0, alpha_out=1000.0)
      for i in range(1, 4)],
]

subnet_ids = [subnet.id for subnet in subnets]

accounts = [
    *[Account(id=i, free_balance=100, alpha_stakes={},
              registered_subnets=subnet_ids) for i in range(1, 3)],
]

trades = generate_trades(subnets, accounts, blocks)

config = {
    "blocks": blocks,
    "n_steps": n_steps,
    "subnets": subnets,
    "accounts": accounts,
    "trades": trades,
    "tao_supply": 1000000.0,
    "global_split": 0.5,
    "balanced": True,
    "root_weight": 0.5
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--plots', nargs='+', help='List of plot modules to run')
    args = parser.parse_args()

    run_simulation(config, args.plots if args.plots else [])
