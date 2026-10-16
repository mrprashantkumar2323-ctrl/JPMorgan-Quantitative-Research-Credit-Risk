"""
JPMorgan Chase & Co. - Natural Gas Commodity Storage Contract Valuation
Author: Prashant Kumar
"""

import numpy as np

def price_storage_contract(injection_dates, withdrawal_dates, purchase_prices, sale_prices, 
                           injection_rate, withdrawal_rate, max_storage_capacity, storage_fee_rate):
    """
    Prices a natural gas storage contract based on scheduled injection and withdrawal dates,
    commodity forward prices, capacity limits, and injection/storage costs.
    """
    total_revenue = 0.0
    total_cost = 0.0
    current_stored_gas = 0.0
    
    cash_flows = []
    
    print("[+] Simulating Commodity Storage Injection & Withdrawal Schedule:")
    for (inj_date, with_date, buy_p, sell_p) in zip(injection_dates, withdrawal_dates, purchase_prices, sale_prices):
        # Inject gas
        injected = min(injection_rate, max_storage_capacity - current_stored_gas)
        current_stored_gas += injected
        gas_cost = injected * buy_p
        
        # Withdraw gas
        withdrawn = min(withdrawal_rate, current_stored_gas)
        current_stored_gas -= withdrawn
        gas_revenue = withdrawn * sell_p
        
        # Operational storage fee
        storage_fee = (inj_date + with_date) * 0.5 * storage_fee_rate * injected
        
        net_cf = gas_revenue - (gas_cost + storage_fee)
        cash_flows.append(net_cf)
        print(f"  Cycle {len(cash_flows)} | Buy: ${buy_p:.2f} | Sell: ${sell_p:.2f} | Net Profit: ${net_cf:,.2f}")
    
    contract_npv = sum(cash_flows)
    return contract_npv

if __name__ == "__main__":
    inj_d = [10, 15, 20]
    with_d = [120, 150, 180]
    buy_prices = [2.85, 3.10, 2.95]
    sell_prices = [4.40, 4.85, 4.60]
    
    npv = price_storage_contract(
        inj_d, with_d, buy_prices, sell_prices,
        injection_rate=500000,
        withdrawal_rate=500000,
        max_storage_capacity=2000000,
        storage_fee_rate=0.0005
    )
    print("=" * 55)
    print(f"Total Contract Valuation (NPV): ${npv:,.2f}")
    print("=" * 55)
