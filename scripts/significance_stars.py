# significance_stars.py
import pandas as pd

def add_significance_stars(p_values):
    """
    Add significance stars to p-values.

    Parameters:
    p_values (pd.Series): The p-values of the coefficients

    Returns:
    pd.Series: The p-values with significance stars
    """
    stars = pd.Series([""] * len(p_values), index=p_values.index)
    stars[p_values < 0.10] = "*"
    stars[p_values < 0.05] = "**"
    stars[p_values < 0.01] = "***"
    return stars
