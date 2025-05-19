import pandas as pd
from sympy import latex
from typing import Tuple, Dict
import sympy as sp

def generate_markdown_report(
    original_df: pd.DataFrame,
    transformed_df: pd.DataFrame,
    formulas: Tuple[sp.Expr, sp.Expr, sp.Expr],
    params: Dict[str, float]
) -> str:
    X_new, Y_new, Z_new = formulas
    first_point = original_df.iloc[0]
    
    report = "# Отчет о преобразовании координат\n\n"
    
    report += "## Параметры преобразования\n\n"
    report += "```\n"
    for key, value in params.items():
        report += f"{key}: {value}\n"
    report += "```\n\n"
    
    report += "## Формула преобразования\n\n"
    report += f"$$ X_{{r}} = {latex(X_new)} $$\n\n"
    report += f"$$ Y_{{r}} = {latex(Y_new)} $$\n\n"
    report += f"$$ Z_{{r}} = {latex(Z_new)} $$\n\n"
    
    report += "## Пример вычисления\n\n"
    report += f"Для точки {first_point['Name']}:\n"
    report += f"X = {first_point['X']}\n"
    report += f"Y = {first_point['Y']}\n"
    report += f"Z = {first_point['Z']}\n\n"
    
    report += "## Преобразованные координаты\n\n"
    report += "| Name | X | Y | Z |\n"
    report += "| --- | --- | --- | --- |\n"
    for _, row in transformed_df.iterrows():
        report += f"| {row['Name']} | {row['X']:.6f} | {row['Y']:.6f} | {row['Z']:.6f} |\n"
    report += "\n"
    
    report += "## Статистика\n\n"
    numeric_cols = ['X', 'Y', 'Z']
    stats = transformed_df[numeric_cols].agg(['count', 'mean', 'std', 'min', 'max'])
    report += "```\n"
    report += stats.to_markdown()
    report += "\n```\n"
    
    return report 