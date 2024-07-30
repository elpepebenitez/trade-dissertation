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

# import pandas as pd

# def add_significance_stars(p_values):
#     # Ensure p_values is a pandas Series
#     if not isinstance(p_values, pd.Series):
#         p_values = pd.Series(p_values)
        
#     # Adding debug statement
#     print(f"p_values: {p_values}")
    
#     # Ensure index is not None or invalid
#     if p_values.index is None:
#         raise ValueError("p_values must have an index")

#     stars = pd.Series([""] * len(p_values), index=p_values.index)
#     stars[p_values < 0.1] = "*"
#     stars[p_values < 0.05] = "**"
#     stars[p_values < 0.01] = "***"
#     return stars