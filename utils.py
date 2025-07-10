from BlackScholesCalc import BlackScholesCalculator
import numpy as np

def get_user_input():
    """
    Interactive function to get user input for Black-Scholes parameters.
    """
    print("\n" + "=" * 70)
    print("INTERACTIVE BLACK-SCHOLES OPTIONS PRICING CALCULATOR")
    print("=" * 70)
    print("Please enter the following parameters for your option:")
    print("(Enter 'q' at any time to quit)")

    try:
        # Get stock price
        S = float(input("\n1. Current Stock Price (S): $"))

        # Get strike price
        K = float(input("2. Strike Price (K): $"))

        # Get time to expiration
        print("\n3. Time to Expiration:")
        print("   You can enter this in:")
        print("   - Years (e.g., 0.25 for 3 months)")
        print("   - Days (we'll convert to years)")

        time_input = input("   Enter time value: ")
        time_unit = input("   Is this in (d)ays or (y)ears? [d/y]: ").lower()

        if time_unit == 'd':
            T = float(time_input) / 365
        else:
            T = float(time_input)

        # Get risk-free rate
        r_input = input("\n4. Risk-free Interest Rate (as %): ")
        r = float(r_input) / 100

        # Get volatility
        sigma_input = input("5. Volatility (as %): ")
        sigma = float(sigma_input) / 100

        # Get dividend yield (optional)
        # q_input = input("6. Dividend Yield (as %, press Enter for 0): ")
        q_input = 0.0
        q = float(q_input) / 100 if q_input else 0.0

        # Get option type
        option_type = input("\n7. Option Type - (c)all or (p)ut? [c/p]: ").lower()
        if option_type == 'c':
            option_type = 'call'
        elif option_type == 'p':
            option_type = 'put'
        else:
            option_type = 'call'  # default

        return S, K, T, r, sigma, q, option_type

    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return None
    except KeyboardInterrupt:
        print("\nExiting...")
        return None


def run_interactive_calculator():
    """Run the interactive Black-Scholes calculator."""

    while True:
        user_input = get_user_input()

        if user_input is None:
            break

        S, K, T, r, sigma, q, option_type = user_input

        # Create calculator and show results
        calculator = BlackScholesCalculator(S, K, T, r, sigma, option_type, q)
        calculator.summary()

        # Ask if user wants to continue
        continue_choice = input("\nWould you like to calculate another option? (y/n): ").lower()
        if continue_choice != 'y':
            break

    print("\nThank you for using the Black-Scholes Calculator!")


def scenario_analysis(base_S, base_K, base_T, base_r, base_sigma, base_q, base_option_type):
    """
    Perform comprehensive scenario analysis showing how Greeks change with different inputs.
    """
    print("\n" + "=" * 80)
    print("SCENARIO ANALYSIS: How Parameter Changes Affect Option Pricing")
    print("=" * 80)

    # Base case
    base_calc = BlackScholesCalculator(base_S, base_K, base_T, base_r, base_sigma, base_option_type, base_q)
    base_greeks = base_calc.get_all_greeks()

    print(f"\nBase Case Results:")
    print(f"Stock: ${base_S}, Strike: ${base_K}, Time: {base_T:.3f}yr, Rate: {base_r:.1%}, Vol: {base_sigma:.1%}")
    print(f"Option Price: ${base_greeks['Price']:.4f}")

    # Scenario 1: Stock Price Changes
    print(f"\n1. STOCK PRICE SENSITIVITY ANALYSIS:")
    print(f"{'Stock Price':<12} {'Option Price':<12} {'Delta':<8} {'Gamma':<8}")
    print("-" * 50)

    for multiplier in [0.9, 0.95, 1.0, 1.05, 1.1]:
        new_S = base_S * multiplier
        calc = BlackScholesCalculator(new_S, base_K, base_T, base_r, base_sigma, base_option_type, base_q)
        greeks = calc.get_all_greeks()
        print(f"${new_S:<11.2f} ${greeks['Price']:<11.4f} {greeks['Delta']:<8.4f} {greeks['Gamma']:<8.6f}")

    # Scenario 2: Volatility Changes
    print(f"\n2. VOLATILITY SENSITIVITY ANALYSIS:")
    print(f"{'Volatility':<12} {'Option Price':<12} {'Vega':<8} {'Delta':<8}")
    print("-" * 50)

    for vol_change in [-0.1, -0.05, 0.0, 0.05, 0.1]:
        new_sigma = base_sigma + vol_change
        if new_sigma > 0:  # Ensure positive volatility
            calc = BlackScholesCalculator(base_S, base_K, base_T, base_r, new_sigma, base_option_type, base_q)
            greeks = calc.get_all_greeks()
            print(f"{new_sigma:<11.1%} ${greeks['Price']:<11.4f} {greeks['Vega']:<8.4f} {greeks['Delta']:<8.4f}")

    # Scenario 3: Time Decay Analysis
    print(f"\n3. TIME DECAY ANALYSIS:")
    print(f"{'Days Left':<12} {'Option Price':<12} {'Theta':<8} {'Delta':<8}")
    print("-" * 50)

    for days in [90, 60, 30, 15, 7]:
        new_T = days / 365
        if new_T > 0:
            calc = BlackScholesCalculator(base_S, base_K, new_T, base_r, base_sigma, base_option_type, base_q)
            greeks = calc.get_all_greeks()
            print(f"{days:<12} ${greeks['Price']:<11.4f} {greeks['Theta']:<8.4f} {greeks['Delta']:<8.4f}")


def compare_call_vs_put(S, K, T, r, sigma, q=0.0):
    """
    Compare call and put options side by side.
    """
    print("\n" + "=" * 80)
    print("CALL vs PUT COMPARISON")
    print("=" * 80)

    call_calc = BlackScholesCalculator(S, K, T, r, sigma, 'call', q)
    put_calc = BlackScholesCalculator(S, K, T, r, sigma, 'put', q)

    call_greeks = call_calc.get_all_greeks()
    put_greeks = put_calc.get_all_greeks()

    print(f"{'Metric':<15} {'Call Option':<15} {'Put Option':<15}")
    print("-" * 50)

    for metric in ['Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']:
        call_val = call_greeks[metric]
        put_val = put_greeks[metric]

        if metric == 'Price':
            print(f"{metric:<15} ${call_val:<14.4f} ${put_val:<14.4f}")
        else:
            print(f"{metric:<15} {call_val:<15.4f} {put_val:<15.4f}")

    # Put-Call Parity Check
    print(f"\n{'PUT-CALL PARITY CHECK:'}")
    print(f"Call - Put = {call_greeks['Price'] - put_greeks['Price']:.4f}")
    print(f"S - K*e^(-rT) = {S - K * np.exp(-r * T):.4f}")
    print(f"Difference = {abs((call_greeks['Price'] - put_greeks['Price']) - (S - K * np.exp(-r * T))):.6f}")
