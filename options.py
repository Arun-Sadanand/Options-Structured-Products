from typing import List
from dataclasses import dataclass
import numpy as np
from scipy.stats import norm

@dataclass
class OptionElement:
    """Represents a single option element in a structured product."""
    type: str  # 'call' or 'put'
    strike: float # strike price of option
    time_to_expiry: float # time to expiry (maturity) of option in years
    volatility: float = 0.25 # volatility of underlying stock
    int_rate: float = 0.05 # current risk-free interest rate (continuously compounded annual rate)
    div_yield: float = 0.025 # dividend yield of underlying stock (continuously compounded annual rate)

    def validate(self):
        """Validate option parameters."""
        assert self.type in ['call', 'put'], "Option type must be 'call' or 'put'."
        assert self.strike >= 0, "Strike price must be non-negative."
        assert self.time_to_expiry >= 0, "Time to expiry must be non-negative."
        assert self.volatility >= 0, "Volatility must be non-negative."
        assert self.int_rate >= 0, "Interest rate must be non-negative."
        assert self.div_yield >= 0, "Dividend yield rate must be non-negative."

    def __post_init__(self):
        """Validate option paramaters on initialization and convert inputs."""
        self.validate()
        # remap inputs to numbers
        type_map = {
            "call" : 1,
            "put" : -1
        }
        self.phi = type_map.get(self.type)
        
    def bs_price(self, spot, t = 0) -> float:
        """Price of option using the Black-Scholes model.
        Parameters
        ----------
        spot : float
            spot price of underlying stock
        t : float
            current time (time elapsed since contract inception) in years
        Returns
        -------
        price : float
            price of the option
        """
        assert np.all(spot) >= 0, "Spot price must be non-negative."
        assert t <= self.time_to_expiry, "Time remaing to expiry must be non-negative."
        
        time_to_exp = self.time_to_expiry - t
        if time_to_exp == 0:
            price =  np.maximum((self.phi * (spot - self.strike)), 0)
        else:
            fwd = spot * np.exp((self.int_rate - self.div_yield) * time_to_exp)
            vol_t = self.volatility * np.sqrt(time_to_exp)
            d1 = np.log(fwd / self.strike) / vol_t + 0.5 * vol_t
            d2 = d1 - vol_t
            df = np.exp(-self.int_rate * time_to_exp)
            price = fwd * norm.cdf(self.phi * d1) - self.strike * norm.cdf(self.phi * d2)
            price *= self.phi * df
        return price

@dataclass
class StructuredProduct:
    """Represents a structured product composed of multiple option elements."""
    elements: List[OptionElement] # List of option elements
    weights: np.array # Array of number of units or weights of each option
    volatility: float # volatility of underlying stock
    int_rate: float # current risk-free interest rate (continuously compounded annual rate)
    div_yield: float # dividend yield of underlying stock (continuously compounded annual rate)
    
    def __post_init__(self):
        """Validate structured product parameters"""
        assert len(self.elements) == len(self.weights), "Number of elements must match number of weights"
        assert all(w != 0 for w in self.weights), "Weights cannot be zero"
        self.reset_parameters() # Ensure all options have common vol, int_rate, & div_yield
        
    def reset_parameters(self):
        """Ensures elements' vol and rates parameters are reset to product parameters"""
        for element in self.elements:
            element.volatility = self.volatility
            element.int_rate = self.int_rate
            element.div_yield = self.div_yield
                
    def price(self, spot, t) -> float:
        """Price the product using the Black-Shcoles model for underlying options"""
        prices = np.array([element.bs_price(spot, t) for element in self.elements])
        wts = self.weights
        if prices.shape != wts.shape: # in case spot is an array
            wts = wts[:, np.newaxis]
        prices = prices * wts
        price = np.sum(prices, axis=0)
        return price
    
    def get_delta(self, spot, t) -> float:
        """Delta of the product (1st derivative with respect to price) 
        using finite differencing"""
        dS = spot / 1000
        price0 = self.price(spot, t)
        price1 = self.price(spot + dS, t)
        delta = (price1 - price0) / dS
        return delta
    
    def get_gamma(self, spot, t) -> float:
        """Gamma of the product (2nd derivative with respect to price) 
        using finite differencing"""
        dS = spot / 100
        price0 = self.price(spot, t)
        price1 = self.price(spot + dS, t)
        price2 = self.price(spot + (2 * dS), t)
        gamma = (price2 - 2 * price1 + price0) / dS**2
        return gamma
    
    def get_theta(self, spot, t) -> float:
        """Theta of the product (1st derivative with respect to price)
        using finite differencing"""
        dT = 1/250 # 1 trading day earlier
        price0 = self.price(spot, t - dT)
        price1 = self.price(spot, t)
        theta = (price1 - price0) / dT
        return theta
    
    def get_vega(self, spot, t) -> float:
        """Theta of the product (1st derivative with respect to volatility)
        using finite differencing"""
        dV = 0.0001 # 1 basis point
        price0 = self.price(spot, t)
        for element in self.elements:
            element.volatility += dV
        price1 = self.price(spot, t)
        vega = (price1 - price0) / dV
        self.reset_parameters()
        return vega
    