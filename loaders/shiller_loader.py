from pathlib import Path

import pandas as pd


def load_shiller_data():
    """
    Carga el fichero oficial de Robert Shiller
    y devuelve únicamente las observaciones válidas.
    """

    file_path = Path("data/raw/shiller.xlsx")

    if not file_path.exists():
        print(f"❌ No existe el fichero: {file_path}")
        return None

    df = pd.read_excel(
        file_path,
        sheet_name="Data",
        header=7
    )

    # ---------------------------------------------------------
    # Limpiar datos
    # ---------------------------------------------------------

    # Convertimos Date y P a numérico.
    # Las filas con texto pasan a NaN.
    df["Date"] = pd.to_numeric(df["Date"], errors="coerce")
    df["P"] = pd.to_numeric(df["P"], errors="coerce")

    # Eliminamos filas sin datos válidos
    df = df.dropna(subset=["Date", "P"])

    # Reiniciamos índice
    df = df.reset_index(drop=True)

    return df