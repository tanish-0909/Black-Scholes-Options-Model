from BlackScholesCalc import BlackScholesCalculator
from utils import run_interactive_calculator

run_interactive_calculator()

# # Example: Apple-like stock option
# print("EXAMPLE 1: Technology Stock Call Option")
# print("="*50)
#
# # Parameters typical for a tech stock
# apple_calc = BlackScholesCalculator(
#     S=150,      # Current stock price
#     K=155,      # Strike price (slightly out-of-the-money)
#     T=45/365,   # 45 days to expiration
#     r=0.045,    # 4.5% risk-free rate
#     sigma=0.25, # 25% volatility (typical for tech stocks)
#     option_type='call'
# )
#
# apple_calc.summary()
#
# # Example: Utility stock with dividend
# print("\nEXAMPLE 2: Dividend-Paying Stock Put Option")
# print("="*50)
#
# utility_calc = BlackScholesCalculator(
#     S=45,       # Current stock price
#     K=50,       # Strike price (in-the-money put)
#     T=0.25,     # 3 months to expiration
#     r=0.035,    # 3.5% risk-free rate
#     sigma=0.15, # 15% volatility (lower for utilities)
#     option_type='put',
#     q=0.04      # 4% dividend yield
# )
#
# utility_calc.summary()


