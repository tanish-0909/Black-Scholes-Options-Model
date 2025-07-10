import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
from datetime import datetime, timedelta
import math


class BlackScholesCalculator:
    """
    A comprehensive Black-Scholes options pricing calculator with Greeks.

    This class implements the Black-Scholes-Merton model for European options
    and calculates all major Greeks (Delta, Gamma, Theta, Vega, Rho).
    """

    def __init__(self, S, K, T, r, sigma, option_type='call', q=0.0):
        """
        Initialize the Black-Scholes calculator.

        Parameters:
        -----------
        S : float
            Current stock price (spot price)
        K : float
            Strike price
        T : float
            Time to expiration in years
        r : float
            Risk-free interest rate (annual)
        sigma : float
            Volatility (annual)
        option_type : str
            'call' or 'put'
        q : float
            Dividend yield (annual, default 0.0)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
        self.q = q

        # Calculate d1 and d2
        self.d1 = self._calculate_d1()
        self.d2 = self._calculate_d2()

    def _calculate_d1(self):
        """Calculate d1 parameter for Black-Scholes formula."""
        if self.T == 0:
            return 0 if self.S == self.K else (float('inf') if self.S > self.K else float('-inf'))

        return (np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))

    def _calculate_d2(self):
        """Calculate d2 parameter for Black-Scholes formula."""
        if self.T == 0:
            return self.d1
        return self.d1 - self.sigma * np.sqrt(self.T)

    def option_price(self):
        """Calculate the option price using Black-Scholes formula."""
        if self.T == 0:
            # At expiration
            if self.option_type == 'call':
                return max(self.S - self.K, 0)
            else:
                return max(self.K - self.S, 0)

        if self.option_type == 'call':
            price = (self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1) -
                     self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:
            price = (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) -
                     self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1))

        return price

    def delta(self):
        """Calculate Delta - sensitivity to underlying price changes."""
        if self.T == 0:
            if self.option_type == 'call':
                return 1.0 if self.S > self.K else 0.0
            else:
                return -1.0 if self.S < self.K else 0.0

        if self.option_type == 'call':
            return np.exp(-self.q * self.T) * norm.cdf(self.d1)
        else:
            return -np.exp(-self.q * self.T) * norm.cdf(-self.d1)

    def gamma(self):
        """Calculate Gamma - rate of change of Delta."""
        if self.T == 0:
            return 0.0

        return (np.exp(-self.q * self.T) * norm.pdf(self.d1)) / (self.S * self.sigma * np.sqrt(self.T))

    def theta(self):
        """Calculate Theta - time decay."""
        if self.T == 0:
            return 0.0

        if self.option_type == 'call':
            theta = (-(self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T)) +
                     self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1) -
                     self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:
            theta = (-(self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T)) -
                     self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1) +
                     self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2))

        return theta / 365  # Convert to per-day theta

    def vega(self):
        """Calculate Vega - sensitivity to volatility changes."""
        if self.T == 0:
            return 0.0

        return self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * np.sqrt(self.T) / 100

    def rho(self):
        """Calculate Rho - sensitivity to interest rate changes."""
        if self.T == 0:
            return 0.0

        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100

    def get_all_greeks(self):
        """Return all Greeks in a dictionary."""
        return {
            'Price': self.option_price(),
            'Delta': self.delta(),
            'Gamma': self.gamma(),
            'Theta': self.theta(),
            'Vega': self.vega(),
            'Rho': self.rho()
        }

    def summary(self):
        """Print a comprehensive summary of the option and its Greeks."""
        print("=" * 60)
        print("BLACK-SCHOLES OPTION PRICING SUMMARY")
        print("=" * 60)
        print(f"Option Type: {self.option_type.upper()}")
        print(f"Current Stock Price (S): ${self.S:.2f}")
        print(f"Strike Price (K): ${self.K:.2f}")
        print(f"Time to Expiration (T): {self.T:.4f} years")
        print(f"Risk-free Rate (r): {self.r:.2%}")
        print(f"Volatility (σ): {self.sigma:.2%}")
        print(f"Dividend Yield (q): {self.q:.2%}")
        print("-" * 60)
        print("OPTION PRICING RESULTS:")
        print("-" * 60)

        greeks = self.get_all_greeks()
        for name, value in greeks.items():
            if name == 'Price':
                print(f"{name}: ${value:.4f}")
            elif name == 'Delta':
                print(f"{name}: {value:.4f} (${value * 100:.2f} per $1 move)")
            elif name == 'Gamma':
                print(f"{name}: {value:.6f} (Delta change per $1 move)")
            elif name == 'Theta':
                print(f"{name}: {value:.4f} (${value:.4f} per day)")
            elif name == 'Vega':
                print(f"{name}: {value:.4f} (per 1% volatility change)")
            elif name == 'Rho':
                print(f"{name}: {value:.4f} (per 1% rate change)")

        print("-" * 60)

        # Moneyness analysis
        if self.S > self.K:
            print(f"Option is IN-THE-MONEY (S > K)")
        elif self.S < self.K:
            print(f"Option is OUT-OF-THE-MONEY (S < K)")
        else:
            print(f"Option is AT-THE-MONEY (S = K)")

        # Intrinsic and Time Value
        if self.option_type == 'call':
            intrinsic_value = max(self.S - self.K, 0)
        else:
            intrinsic_value = max(self.K - self.S, 0)

        time_value = self.option_price() - intrinsic_value

        print(f"Intrinsic Value: ${intrinsic_value:.4f}")
        print(f"Time Value: ${time_value:.4f}")
        print("=" * 60)
