from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Subnet:
    id: int
    tao_in: float
    alpha_in: float
    alpha_out: float
    is_root: bool = False
    k: float = field(init=False)

    def __post_init__(self):
        self.k = self.tao_in * self.alpha_in if not self.is_root else 0.0

    def alpha_price(self) -> float:
        return 1.0 if self.is_root or self.alpha_in == 0 else self.tao_in / self.alpha_in

    def weight(self, alpha_amount: float) -> float:
        return alpha_amount if self.is_root else (
            0.0 if self.alpha_out == 0 else (alpha_amount / self.alpha_out) * self.tao_in
        )

    def stake(self, tao_amount: float) -> float:
        if self.is_root:
            self.alpha_out += tao_amount
            return tao_amount
        new_tao_in = self.tao_in + tao_amount
        new_alpha_in = self.k / new_tao_in
        alpha_bought = self.alpha_in - new_alpha_in
        self.alpha_out += alpha_bought
        self.alpha_in = new_alpha_in
        self.tao_in = new_tao_in
        return alpha_bought

    def unstake(self, alpha_amount: float) -> float:
        if self.is_root:
            self.alpha_out -= alpha_amount
            return alpha_amount
        new_alpha_in = self.alpha_in + alpha_amount
        new_tao_in = self.k / new_alpha_in
        tao_bought = self.tao_in - new_tao_in
        self.alpha_out -= alpha_amount
        self.alpha_in = new_alpha_in
        self.tao_in = new_tao_in
        return tao_bought

    def inject(self, tao_amount: float, alpha_amount: float, alpha_out: float):
        self.tao_in += tao_amount
        self.alpha_in += alpha_amount
        self.alpha_out += alpha_out
        self.k = self.tao_in * self.alpha_in


@dataclass
class Account:
    id: int
    free_balance: float
    registered_subnets: List[int]
    alpha_stakes: Dict[int, float]  # = field(default_factory=dict)


@dataclass
class Trade:
    block: int
    account_id: int
    subnet_id: int
    action: str
    amount: str
