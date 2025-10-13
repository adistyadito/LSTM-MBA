# src/01_eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(input_path: str, save_fig_dir: str = "reports/figures/"):
    """
    Exploratory Data Analysis (EDA) untuk dataset molekul.
    
    Parameters
    ----------
    input_path : str
        Path ke file CSV (misal: data/raw/dataset.csv)
    save_fig_dir : str
        Folder untuk nyimpen hasil plot EDA
    """
    
    # --- Load data ---
    df = pd.read_csv(input_path)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

    # --- Preview ---
    print("Head:")
    print(df.head(), "\n")
    print("Info:")
    print(df.info(), "\n")
    
    # --- Missing values ---
    print("Missing values per column:\n", df.isnull().sum(), "\n")

    # --- Statistik dasar numeric ---
    if "acvalue" in df.columns:
        print("Descriptive statistics for 'acvalue':\n", df["acvalue"].describe(), "\n")

    # --- Unique categories ---
    if "categories" in df.columns:
        print("Unique categories:", df["categories"].unique(), "\n")
        print(df["categories"].value_counts(), "\n")

    # --- Buat folder untuk figure kalau belum ada ---
    os.makedirs(save_fig_dir, exist_ok=True)

    # --- Distribusi nilai aktivitas (acvalue) ---
    if "acvalue" in df.columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df["acvalue"], bins=30, kde=True)
        plt.title("Distribusi Nilai Aktivitas (acvalue)")
        plt.xlabel("acvalue")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(save_fig_dir, "acvalue_distribution.png"))
        plt.close()

    # --- Jumlah kategori ---
    if "categories" in df.columns:
        plt.figure(figsize=(5,4))
        sns.countplot(x="categories", data=df)
        plt.title("Distribusi Kategori Senyawa")
        plt.xlabel("Kategori")
        plt.ylabel("Jumlah")
        plt.tight_layout()
        plt.savefig(os.path.join(save_fig_dir, "category_distribution.png"))
        plt.close()

    # --- Panjang SMILES ---
    df["smiles_length"] = df["smiles"].astype(str).apply(len)
    plt.figure(figsize=(6,4))
    sns.histplot(df["smiles_length"], bins=30, kde=True)
    plt.title("Distribusi Panjang SMILES")
    plt.xlabel("Panjang SMILES")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(save_fig_dir, "smiles_length_distribution.png"))
    plt.close()

    print(f"[INFO] Figures saved to {save_fig_dir}")

    # --- Return summary info (optional) ---
    summary = {
        "n_rows": df.shape[0],
        "n_cols": df.shape[1],
        "missing": df.isnull().sum().to_dict(),
        "categories": df["categories"].value_counts().to_dict(),
        "acvalue_stats": df["acvalue"].describe().to_dict() if "acvalue" in df.columns else None
    }
    return summary

# Contoh run manual dari CLI / notebook
if __name__ == "__main__":
    summary = run_eda("data/raw/dataset.csv")
    print(summary)
