import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

def setup_directories():
    """Create a directory to save plots."""
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    return plot_dir

def save_bar_plot(data, title, xlabel, ylabel, filename, plot_dir, rotation=45):
    """Saves a styled bar plot for the given data."""
    if data.empty:
        print(f"✗ Plot not generated for '{title}': No data.")
        return
        
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
    bars = plt.bar(range(len(data)), data.values, color=colors, alpha=0.9, edgecolor='black', linewidth=0.5)
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(range(len(data)), data.index, rotation=rotation, ha='right')
    plt.grid(axis='y', alpha=0.4, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
        
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, filename), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Plot saved: {filename}")

def summarize_numeric(series, name, plot_dir):
    """Generates and prints a detailed summary for a numeric series, including a count of zeros."""
    non_null = series.dropna()
    if non_null.empty:
        print(f"\n--- {name} (Numeric) ---\n[No valid data to summarize]\n")
        return

    N, miss = len(series), series.isna().sum()
    zeros = (non_null == 0).sum()
    lo, hi = non_null.min(), non_null.max()
    mean, median, mode_val = non_null.mean(), non_null.median(), non_null.mode().iloc[0] if not non_null.mode().empty else np.nan
    
    pctiles = [0, 1, 5, 25, 50, 75, 95, 99, 100]
    pct_vals = np.percentile(non_null, pctiles)

    bin_count = min(len(non_null.unique()), 20)
    freq = pd.cut(non_null, bins=bin_count, include_lowest=True).value_counts().sort_index()

    print(f"\n--- {name} (Numeric) ---")
    print(f"Stats: Obs={N}, Missing={miss}, Zeros={zeros}, Mean={mean:.2f}, Median={median:.2f}, Mode={mode_val}")
    print(f"Range: {lo} – {hi}")

    print("\nPercentiles:")
    for p, v in zip(pctiles, pct_vals):
        label = {0: "Min", 25: "Q1", 50: "Median", 75: "Q3", 100: "Max"}.get(p, f"{p}%")
        print(f"  {label:<7} {v:,.2f}")
    
    print("\nFrequency Bins:")
    print(freq.to_frame("Count"))
    
    plot_filename = f"{name.replace(' ', '_').lower()}_distribution.png"
    save_bar_plot(freq, f"{name} Distribution", name, "Count", plot_filename, plot_dir)

def summarize_categorical(series, name, plot_dir):
    """Generates a summary for a categorical series with conditional truncation."""
    counts = series.value_counts()
    
    print(f"\n--- {name} (Categorical) ---")
    print(f"Unique Categories: {len(counts)}")
    print("\nFrequency:")
    
    # Conditional truncation based on the number of unique categories
    if len(counts) > 50:
        print(counts.to_frame("Count").head(10))
        print(f"... and {len(counts)-10} more categories.")
    else:
        # Display all categories if 50 or fewer
        with pd.option_context('display.max_rows', None):
            print(counts.to_frame("Count"))
        
    if not counts.empty:
        mf, lf = counts.idxmax(), counts.idxmin()
        print(f"\nMost Frequent: {mf} ({counts.loc[mf]})")
        print(f"Least Frequent: {lf} ({counts.loc[lf]})")

    if len(counts) > 50:
        print("\nNote: Plot not generated (more than 50 unique categories).")
        return
        
    plot_filename = f"{name.replace(' ', '_').lower()}_distribution.png"
    save_bar_plot(counts, f"{name} Distribution", name, "Count", plot_filename, plot_dir)

def univariate_analysis(df, plot_dir):
    """Performs univariate analysis on all columns of a DataFrame."""
    print(f"=== Starting Univariate Analysis: {df.shape[1]} columns, {df.shape[0]} rows ===")
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            summarize_numeric(df[col], col, plot_dir)
        else:
            summarize_categorical(df[col].astype(str), col, plot_dir)
    print("\n=== Analysis Complete ===")
    print(f"All plots have been saved in the '{plot_dir}/' directory.")

def main():
    parser = argparse.ArgumentParser(description="Perform universal univariate analysis on a CSV file.")
    parser.add_argument("filepath", type=str, help="Path to the input CSV file.")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at '{args.filepath}'")
        return

    try:
        df = pd.read_csv(args.filepath, low_memory=False)
        plot_dir = setup_directories()
        univariate_analysis(df, plot_dir)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

