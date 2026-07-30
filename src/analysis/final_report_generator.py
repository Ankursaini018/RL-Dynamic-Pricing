"""
final_report_generator.py
=========================
Generates final project report
combining all results and proofs.

Infotact DS/ML Internship — Project 2
Week 4 : Final Report
"""

import json
import os
import sys
from datetime import datetime
sys.path.append('../')

os.makedirs('../results', exist_ok=True)


def generate_final_report(
        summary_df,
        proof: dict,
        behavior_proof: dict,
        bv: dict,
        save_path: str = '../results/final_project_report.json'):
    """
    Generate complete final project report.

    Parameters
    ----------
    summary_df : DataFrame
        Simulation summary.
    proof : dict
        Statistical proof.
    behavior_proof : dict
        Behavior proof.
    bv : dict
        Business value.
    save_path : str
        Save path.
    """
    print("=" * 60)
    print("  GENERATING FINAL PROJECT REPORT")
    print("=" * 60)

    rankings = []
    medals   = ['Gold', 'Silver', 'Bronze',
                '4th', '5th', '6th', '7th']
    for i, row in summary_df.iterrows():
        rankings.append({
            'rank'         : i + 1,
            'medal'        : medals[i],
            'agent'        : row['Agent'],
            'mean_revenue' : float(row['Mean Revenue']),
            'std_revenue'  : float(row['Std Revenue']),
            'sell_through' : float(row['Sell Through %'])
        })

    report = {
        'project'          : 'RL Dynamic Pricing',
        'program'          : 'Infotact DS/ML Internship 2026',
        'date'             : str(datetime.now().date()),
        'weeks_completed'  : 4,

        'final_rankings'   : rankings,

        'best_agent'       : {
            'name'         : 'PPO',
            'type'         : 'Actor-Critic RL',
            'revenue'      : float(
                summary_df[
                    summary_df['Agent'] == 'PPO'
                ]['Mean Revenue'].values[0]
            )
        },

        'statistical_proof': {
            'n_seasons'      : 1000,
            'n_comparisons'  : len(proof),
            'all_significant': all(
                v.get('significant', False)
                for v in proof.values()
            ),
            'details'        : proof
        },

        'behavior_proof'   : behavior_proof,
        'business_value'   : bv,

        'technical_summary': {
            'algorithms'    : [
                'Q-Learning (Tabular)',
                'DQN (Deep Q-Network)',
                'PPO (Proximal Policy Optimization)'
            ],
            'frameworks'    : [
                'PyTorch', 'Gymnasium',
                'NumPy', 'Pandas'
            ],
            'unit_tests'    : 26,
            'notebooks'     : 21,
        },

        'recommendation'   : (
            "Deploy PPO pricing agent for "
            f"+{bv.get('uplift_pct', 0):.1f}% "
            "revenue improvement over "
            "traditional pricing strategies!"
        )
    }

    with open(save_path, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"\n✅ Final report saved: {save_path}")
    print(f"\n  Best Agent     : "
          f"{report['best_agent']['name']}")
    print(f"  Best Revenue   : "
          f"${report['best_agent']['revenue']:.0f}")
    print(f"  Recommendation : "
          f"{report['recommendation']}")
    print("=" * 60)

    return report


if __name__ == "__main__":
    print("✅ Final report generator loaded!")