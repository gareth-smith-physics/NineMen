from database import Database
import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == "__main__":

    dname = sys.argv[1] if len(sys.argv)>=2 else "positions.db"

    d = Database(db_name=dname)
    id = 1
    go = True

    ss = 40
    dd = 130

    # Define bins for outcomes and depths
    outcome_bins = np.arange(-1-ss, 2+ss, 2)  # Bins in steps of 2
    depth_bins = np.arange(0, 1+dd, 1)         # Bins for depths 
    outcome_hist = np.zeros(len(outcome_bins) - 1, dtype=float)
    depth_hist = np.zeros(len(depth_bins) - 1, dtype=float)

    while go:
        result = d.get_entry_by_id(id)
        if result is None:
            print(f'End of database reached! {id} entries.')
            go = False
            break

        x, o, k_move = result
        k_start, k_end, k_removal, outcome, depth = d.deintify(k_move)
        if outcome>0:
            outcome -= 100
            outcome += ss
        elif outcome<0:
            outcome += 100
            outcome -= ss
        
        # Update outcome histogram
        outcome_idx = np.digitize([outcome], outcome_bins) - 1
        if 0 <= outcome_idx[0] < len(outcome_hist):
            outcome_hist[outcome_idx[0]] += 1

        # Update depth histogram only if outcome is 0
        if outcome == 0:
            depth_idx = np.digitize([depth], depth_bins) - 1
            if 0 <= depth_idx[0] < len(depth_hist):
                depth_hist[depth_idx[0]] += 1

        # Increment id for the next database entry
        id += 1

    # Close the database
    d.close()

    # Normalize
    total_outcome = sum(outcome_hist)
    outcome_hist *= 1./total_outcome
    #total_depth = sum(depth_hist)
    #depth_hist *= 1./depth_hist

    # Plotting the histograms
    plt.figure(figsize=(10, 5))

    # Histogram of outcomes
    plt.subplot(1, 2, 1)
    plt.bar(outcome_bins[:-1], outcome_hist, width=2, color='blue', alpha=0.7, edgecolor='black', align='edge')
    plt.title("Histogram of Outcomes")
    plt.xlabel("Outcome")
    plt.ylabel("Frequency")

    # Histogram of depths for outcome == 0
    plt.subplot(1, 2, 2)
    plt.bar(depth_bins[:-1], depth_hist, width=1, color='green', alpha=0.7, edgecolor='black', align='edge')
    plt.title("Histogram of Depths (Outcome = 0)")
    plt.xlabel("Depth")
    plt.ylabel("Frequency")

    # Show plots
    plt.tight_layout()
    plt.show()
