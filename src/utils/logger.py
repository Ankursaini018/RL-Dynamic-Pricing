"""
logger.py
=========
Simple logging utility for
tracking experiment progress.

Infotact DS/ML Internship — Project 2
"""

import os
import json
from datetime import datetime


class ExperimentLogger:
    """
    Logs experiment results to file.

    Parameters
    ----------
    experiment_name : str
        Name of the experiment.
    log_dir : str
        Directory to save logs.
    """

    def __init__(self,
                 experiment_name: str,
                 log_dir: str = '../results/'):
        self.name     = experiment_name
        self.log_dir  = log_dir
        self.logs     = []
        self.start_time = datetime.now()

        os.makedirs(log_dir, exist_ok=True)
        print(f"✅ Logger started: {experiment_name}")

    def log(self, metrics: dict,
            step: int = None):
        """
        Log metrics at a step.

        Parameters
        ----------
        metrics : dict
            Metrics to log.
        step : int
            Current step/episode.
        """
        entry = {
            'timestamp' : datetime.now().strftime(
                '%H:%M:%S'
            ),
            'step'      : step,
            **metrics
        }
        self.logs.append(entry)

    def save(self):
        """Save logs to JSON file."""
        filepath = os.path.join(
            self.log_dir,
            f'{self.name}_log.json'
        )
        output = {
            'experiment'  : self.name,
            'start_time'  : str(self.start_time),
            'end_time'    : str(datetime.now()),
            'total_steps' : len(self.logs),
            'logs'        : self.logs[-100:]
        }
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=4)
        print(f"✅ Logs saved: {filepath}")

    def summary(self):
        """Print experiment summary."""
        if not self.logs:
            print("No logs yet!")
            return

        print(f"\n=== {self.name} SUMMARY ===")
        print(f"Total steps : {len(self.logs)}")

        # Get last log
        last = self.logs[-1]
        print("Last metrics:")
        for k, v in last.items():
            if k not in ['timestamp', 'step']:
                print(f"  {k:<20}: {v}")


if __name__ == "__main__":
    logger = ExperimentLogger('test_run')
    logger.log({'revenue': 1500, 'epsilon': 0.5},
               step=100)
    logger.log({'revenue': 1800, 'epsilon': 0.3},
               step=200)
    logger.summary()
    logger.save()
    print("✅ Logger working correctly!")