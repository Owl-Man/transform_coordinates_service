import pandas as pd
import numpy as np
from sympy import Matrix, symbols, N
import sympy as sp
from typing import Tuple, Dict, Any
import json

def load_parameters() -> Dict[str, Dict[str, float]]:
    with open('parameters.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def transform_coordinates(df: pd.DataFrame, source_system: str) -> Tuple[pd.DataFrame, Tuple[sp.Expr, sp.Expr, sp.Expr], Dict[str, float]]:
    all_params = load_parameters()
    if source_system not in all_params:
        raise ValueError(f"Unknown coordinate system: {source_system}")
    
    params = all_params[source_system]
    
    ΔX, ΔY, ΔZ, ωx, ωy, ωz, m_sym = symbols('ΔX ΔY ΔZ ωx ωy ωz m')
    X, Y, Z = symbols('X Y Z')
    
    formula = (1 + m_sym) * Matrix([
        [1, ωz, -ωy],
        [-ωz, 1, ωx],
        [ωy, -ωx, 1]
    ]) @ Matrix([[X], [Y], [Z]]) + Matrix([[ΔX], [ΔY], [ΔZ]])
    
    elements_const = {
        ΔX: params['ΔX'],
        ΔY: params['ΔY'],
        ΔZ: params['ΔZ'],
        ωx: params['ωx'],
        ωy: params['ωy'],
        ωz: params['ωz'],
        m_sym: params['m']
    }
    
    transformed = []
    for _, row in df.iterrows():
        elements = {
            **elements_const,
            X: row['X'],
            Y: row['Y'],
            Z: row['Z']
        }
        results_vector = formula.subs(elements).applyfunc(N)
        transformed.append([
            row['Name'],
            float(results_vector[0]),
            float(results_vector[1]),
            float(results_vector[2])
        ])
    
    df_result = pd.DataFrame(transformed, columns=['Name', 'X', 'Y', 'Z'])
    
    X_new = formula[0].subs(elements_const)
    Y_new = formula[1].subs(elements_const)
    Z_new = formula[2].subs(elements_const)
    
    return df_result, (X_new, Y_new, Z_new), params

def generate_markdown_report(df: pd.DataFrame) -> str:
    report = "# Отчет о преобразовании координат\n\n"
    
    report += "## Формула преобразования\n\n"
    report += "```\n"
    report += "X' = X * cos(30°) - Y * sin(30°)\n"
    report += "Y' = X * sin(30°) + Y * cos(30°)\n"
    report += "Z' = Z + 100\n"
    report += "```\n\n"
    
    report += "## Пример вычисления\n\n"
    report += "```\n"
    first_row = df.iloc[0]
    report += f"Для точки {first_row['Name']}:\n"
    report += f"X = {first_row['X']:.3f}\n"
    report += f"Y = {first_row['Y']:.3f}\n"
    report += f"Z = {first_row['Z']:.3f}\n\n"
    report += f"X' = {first_row['X']:.3f} * cos(30°) - {first_row['Y']:.3f} * sin(30°) = {first_row['X_transformed']:.3f}\n"
    report += f"Y' = {first_row['X']:.3f} * sin(30°) + {first_row['Y']:.3f} * cos(30°) = {first_row['Y_transformed']:.3f}\n"
    report += f"Z' = {first_row['Z']:.3f} + 100 = {first_row['Z_transformed']:.3f}\n"
    report += "```\n\n"
    
    report += "## Исходные координаты\n\n"
    report += "```\n"
    original_cols = ['Name', 'X', 'Y', 'Z']
    report += df[original_cols].to_markdown(index=False)
    report += "\n```\n\n"
    
    report += "## Преобразованные координаты\n\n"
    report += "```\n"
    transformed_cols = ['Name', 'X_transformed', 'Y_transformed', 'Z_transformed']
    report += df[transformed_cols].to_markdown(index=False)
    report += "\n```\n\n"
    
    report += "## Статистика\n\n"
    report += "```\n"
    numeric_cols = ['X', 'Y', 'Z', 'X_transformed', 'Y_transformed', 'Z_transformed']
    report += df[numeric_cols].describe().to_markdown()
    report += "\n```\n"
    
    return report 