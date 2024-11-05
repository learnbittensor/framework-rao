from typing import List, Dict
from collections import defaultdict
from .models import Subnet, Account, Trade
from .utils import write_json


class Subtensor:
    def __init__(self, subnets: List[Subnet], accounts: List[Account],
                 trades: List[Trade], tao_supply: float, global_split: float,
                 balanced: bool, root_weight: float, blocks: int,
                 n_steps: int):
        self.subnets = {s.id: s for s in subnets}
        self.accounts = {a.id: a for a in accounts}
        self.trade_blocks = self._organize_trades(trades)
        self.tao_supply = tao_supply
        self.global_split = global_split
        self.balanced = balanced
        self.initial_root_weight = root_weight
        self.root_weight = root_weight
        self.blocks = blocks
        self.log_interval = int(blocks/n_steps)

    def _organize_trades(self, trades: List[Trade]) -> Dict[int, List[Trade]]:
        trade_dict = defaultdict(list)
        for trade in trades:
            trade_dict[trade.block].append(trade)
        return dict(trade_dict)

    def _parse_amount(self, amount: str, total: float) -> float:
        if amount == 'all':
            return total
        if '%' in amount:
            return total * float(amount.strip('%')) / 100
        return float(amount)

    def _update_root_weight(self, current_block: int):
        weight_decrease_per_block = self.initial_root_weight / self.blocks
        self.root_weight = max(0.0, self.initial_root_weight - (current_block * weight_decrease_per_block))

    def run_simulation(self):
        accounts_data = []
        subnets_data = []
        trades_data = []
        subtensor_data = []

        for block in range(self.blocks):
            #self._update_root_weight(block)

            if block in self.trade_blocks:
                for trade in self.trade_blocks[block]:
                    self._execute_trade(trade)
                    trades_data.append({
                        "block": block,
                        "account_id": trade.account_id,
                        "subnet_id": trade.subnet_id,
                        "action": trade.action,
                        "amount": trade.amount
                    })

            self._process_block_step()

            if block % self.log_interval == 0 or block == self.blocks - 1:
                self._log_state(block, accounts_data, subnets_data, subtensor_data)

        write_json("data/accounts.json", accounts_data)
        write_json("data/subnets.json", subnets_data)
        write_json("data/trades.json", trades_data)
        write_json("data/subtensor.json", subtensor_data)

    def _process_block_step(self):
        emit = self._calculate_emission()
        sum_prices = sum(s.alpha_price() for s in self.subnets.values() if not s.is_root)
        emission_val = 1

        if sum_prices < 1.0 or not self.balanced:
            self.tao_supply += emission_val

        for subnet in self.subnets.values():
            if subnet.is_root:
                continue

            tao_amount = emit.get(subnet.id, 0.0) * emission_val \
                if sum_prices < 1.0 or not self.balanced else 0.0
            alpha_amount = emission_val if sum_prices >= 1.0 and self.balanced else 0.0

            subnet.inject(tao_amount, alpha_amount, emission_val)

            dividends = self._calculate_dividends(subnet.id)
            for acc_id, div in dividends.items():
                self.accounts[acc_id].alpha_stakes[subnet.id] = \
                    self.accounts[acc_id].alpha_stakes.get(subnet.id, 0.0) + \
                    div * emission_val

    def _execute_trade(self, trade: Trade):
        account = self.accounts.get(trade.account_id)
        subnet = self.subnets.get(trade.subnet_id)
        if not account or not subnet:
            return

        if trade.action == 'buy':
            tao_amount = self._parse_amount(trade.amount, account.free_balance)
            alpha_bought = subnet.stake(tao_amount)
            account.alpha_stakes[trade.subnet_id] = account.alpha_stakes.get(trade.subnet_id, 0.0) + alpha_bought
            account.free_balance -= tao_amount
        elif trade.action == 'sell':
            alpha_amount = self._parse_amount(trade.amount, account.alpha_stakes.get(trade.subnet_id, 0.0))
            tao_bought = subnet.unstake(alpha_amount)
            account.alpha_stakes[trade.subnet_id] = account.alpha_stakes.get(trade.subnet_id, 0.0) - alpha_amount
            account.free_balance += tao_bought

    def _calculate_emission(self) -> Dict[int, float]:
        emission = {s.id: s.tao_in for s in self.subnets.values() if not s.is_root}
        total = sum(emission.values())
        return {sid: e / total if total else 0.0 for sid, e in emission.items()}

    def _calculate_dividends(self, subnet_id: int) -> Dict[int, float]:
        subnet = self.subnets.get(subnet_id)
        if not subnet:
            return {}

        weights = self._calculate_weights()
        local_weights = {
            acc_id: subnet.weight(account.alpha_stakes.get(subnet_id, 0.0))
            for acc_id, account in self.accounts.items()
            if subnet_id in account.alpha_stakes
        }

        total_local = sum(local_weights.values())
        total_global = sum(weights.values())

        return {
            acc_id: (
                self.global_split * (weights.get(acc_id, 0.0) / total_global if total_global else 0.0) +
                (1 - self.global_split) * (local_weights.get(acc_id, 0.0) / total_local if total_local else 0.0)
            )
            for acc_id in self.accounts
        }

    def _calculate_weights(self) -> Dict[int, float]:
        weights = defaultdict(float)
        for subnet in self.subnets.values():
            for acc_id, account in self.accounts.items():
                if subnet.id in account.alpha_stakes:
                    alpha = account.alpha_stakes[subnet.id]
                    weight = subnet.weight(alpha * self.root_weight if subnet.is_root else alpha)
                    weights[acc_id] += weight
        return dict(weights)

    def _log_state(self, block: int, accounts_data: List, subnets_data: List, subtensor_data: List):
        for account in self.accounts.values():
            market_value = (
                account.free_balance +
                sum(
                    account.alpha_stakes.get(subnet.id, 0.0) if subnet.is_root
                    else (subnet.tao_in - (subnet.k / (subnet.alpha_in + account.alpha_stakes.get(subnet.id, 0.0))))
                    for subnet in self.subnets.values()
                    if account.alpha_stakes.get(subnet.id, 0.0) > 0
                )
            )

            accounts_data.append({
                "block": block,
                "account_id": account.id,
                "free_balance": account.free_balance,
                "market_value": market_value,
                "alpha_stakes": account.alpha_stakes.copy(),
            })

        current_emissions = self._calculate_emission()

        for subnet in self.subnets.values():
            if not subnet.is_root:
                dividends = self._calculate_dividends(subnet.id)
            else:
                dividends = {}
            
            subnets_data.append({
                "block": block,
                "subnet_id": subnet.id,
                "tao_in": subnet.tao_in,
                "alpha_in": subnet.alpha_in,
                "alpha_out": subnet.alpha_out,
                "exchange_rate": subnet.alpha_price(),
                "emission_rate": current_emissions.get(subnet.id, 0.0),
                "dividends": dividends
            })

            sum_prices = sum(s.alpha_price() for s in self.subnets.values() if not s.is_root)
            subtensor_data.append({
                "block": block,
                "tao_supply": self.tao_supply,
                "sum_prices": sum_prices
            })
