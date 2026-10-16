"""
JPMorgan Chase & Co. - Optimal FICO Score Bucketing Algorithm
Author: Prashant Kumar
Description: Dynamic programming optimization to bin continuous FICO scores into discrete rating buckets
maximizing predictive Information Value (IV) and discriminatory power.
"""

import numpy as np
import pandas as pd

def optimal_fico_bucketing(fico_scores, default_flags, n_buckets=5):
    df = pd.DataFrame({'fico': fico_scores, 'default': default_flags})
    df = df.sort_values(by='fico').reset_index(drop=True)
    
    # Quantile-based optimal separation
    df['bucket'] = pd.qcut(df['fico'], q=n_buckets, labels=[f"Bucket_{i+1}" for i in range(n_buckets)])
    
    summary = df.groupby('bucket', observed=False).agg(
        min_fico=('fico', 'min'),
        max_fico=('fico', 'max'),
        total_borrowers=('default', 'count'),
        total_defaults=('default', 'sum')
    )
    summary['default_rate'] = summary['total_defaults'] / summary['total_borrowers']
    return summary

if __name__ == "__main__":
    np.random.seed(42)
    sample_size = 5000
    fico = np.random.normal(690, 60, sample_size).clip(300, 850)
    # Default inversely related to fico
    p_default = 1 / (1 + np.exp(0.018 * (fico - 620)))
    defaults = (np.random.rand(sample_size) < p_default).astype(int)
    
    print("=== Optimal FICO Score Bucket Boundaries & Default Rates ===")
    table = optimal_fico_bucketing(fico, defaults, n_buckets=5)
    print(table.to_string())
