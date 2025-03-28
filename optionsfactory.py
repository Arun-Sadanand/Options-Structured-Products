import numpy as np
import options

class StructuredProductFactory:
    """Factory for creating standard option strategies."""
    @classmethod
    def synthetic_forward(cls,
                          fwd_price: float,
                          time_to_exp: float = 0.125,
                          volatility: float = 0.25,
                          int_rate: float = 0.05,
                          div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a synthetic forward using put-call parity
        Parameters
        ----------
        fwd_price : float
            Forward price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """    
        # Synthetic forward elements
        elements = [options.OptionElement(type='call', 
                                          strike=fwd_price,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put', 
                                          strike=fwd_price,
                                          time_to_expiry=time_to_exp)]
        # Long call short put
        weights = np.array([1, -1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
                
    @classmethod
    def bull_spread(cls, 
                    lower_strike: float, 
                    upper_strike: float,
                    time_to_exp : float = 0.125,
                    volatility: float = 0.25,
                    int_rate: float = 0.05,
                    div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a bull spread
        Parameters
        ----------
        lower_strike : float
            Lower strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float,
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct bull spread elements
        elements = [options.OptionElement(type='call', 
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp)]
        # long, short
        weights = np.array([1, -1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
    
    @classmethod
    def bear_spread(cls, 
                    lower_strike: float, 
                    upper_strike: float,
                    time_to_exp: float = 0.125,
                    volatility: float = 0.25,
                    int_rate: float = 0.05,
                    div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a bear spread
        Parameters
        ----------
        lower_strike : float
            Lower strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct bear spread elements
        elements = [options.OptionElement(type='put', 
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp)]
        # short, long
        weights = np.array([-1, 1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
    
    @classmethod
    def straddle(cls,
                 strike: float,
                 time_to_exp: float,
                 volatility: float = 0.25,
                 int_rate: float = 0.05,
                 div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a straddle
        Parameters
        ----------
        strike : float
            Center strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Straddle elements
        elements = [options.OptionElement(type='call', 
                                          strike=strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put', 
                                          strike=strike,
                                          time_to_expiry=time_to_exp)]
        # call and put at same strike
        weights = np.array([1, 1])
        product = options.StructuredProduct(elements=elements,
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
    
    @classmethod
    def strangle(cls,
                 lower_strike: float, 
                 upper_strike: float,
                 time_to_exp: float = 0.125,
                 volatility: float = 0.25,
                 int_rate: float = 0.05,
                 div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a strangle
        Parameters
        ----------
        lower_strike : float
            Lower strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Strangle elements
        elements = [options.OptionElement(type='put', 
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp)]
        # call and put at same strike
        weights = np.array([1, 1])
        product = options.StructuredProduct(elements=elements,
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product    
        
    @classmethod
    def butterfly(cls,
                  width: float,
                  center_strike: float,
                  time_to_exp: float = 0.125,
                  volatility: float = 0.25,
                  int_rate: float = 0.05,
                  div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a butterfly spread
        Parameters
        ----------
        width : float
            Width of the spread (distance between wings)
        center_strike : float
            Center strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct butterfly spread elements
        elements = [options.OptionElement(type='call', 
                                          strike=center_strike - width/2,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=center_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=center_strike + width/2,
                                          time_to_expiry=time_to_exp)]
        # long the wings, short the center
        weights = np.array([1, -2, 1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product

    @classmethod
    def condor(cls,
               width: float,
               lower_strike: float,
               upper_strike: float,
               time_to_exp: float = 0.125,
               volatility: float = 0.25,
               int_rate: float = 0.05,
               div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a condor spread
        Parameters
        ----------
        width : float
            Width of the spread excl. distance betweem lower and upper strikes
        lower_strike : float
            Lower strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct butterfly spread elements
        elements = [options.OptionElement(type='put', 
                                          strike=lower_strike - width/2,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put',
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=upper_strike + width/2,
                                          time_to_expiry=time_to_exp)]
        # long the wings, short the center
        weights = np.array([1, -1, -1, 1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product

    @classmethod
    def call_xmastree(cls,
                      lower_strike: float,
                      center_strike: float,
                      upper_strike: float,
                      time_to_exp: float = 0.125,
                      volatility: float = 0.25,
                      int_rate: float = 0.05,
                      div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a call christmas tree spread
        Parameters
        ----------
        lower_strike : float
            Lower strike price
        center_strike : float
            Center strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct call xmas tree spread elements
        elements = [options.OptionElement(type='call', 
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=center_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp)]
        # long, short, short
        weights = np.array([1, -1, -1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
    
    @classmethod
    def put_xmastree(cls,
                     lower_strike: float,
                     center_strike: float,
                     upper_strike: float,
                     time_to_exp: float = 0.125,
                     volatility: float = 0.25,
                     int_rate: float = 0.05,
                     div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a put christmas tree spread
        Parameters
        ----------
        lower_strike : float
            Lower strike price
        center_strike : float
            Center strike price
        upper_strike : float
            Upper strike price
        time_to_exp : float
            Time to expiry (maturity) of product in years (defaults to 0.125)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Construct put xmas tree spread elements
        elements = [options.OptionElement(type='put', 
                                          strike=lower_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put', 
                                          strike=center_strike,
                                          time_to_expiry=time_to_exp),
                    options.OptionElement(type='put', 
                                          strike=upper_strike,
                                          time_to_expiry=time_to_exp)]
        # short, short, long
        weights = np.array([-1, -1, 1])
        product = options.StructuredProduct(elements=elements, 
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product
    
    @classmethod
    def calendar_spread(cls,
                        strike: float,
                        near_time_to_exp: float = 0.125,
                        far_time_to_exp: float = 0.25,
                        volatility: float = 0.25,
                        int_rate: float = 0.05,
                        div_yield: float = 0.025) -> options.StructuredProduct:
        """Creates a calendar spread
        Parameters
        ----------
        strike : float
            Center strike price
        near_time_to_exp : float
            Time to expiry of near term option in years (defaults to 0.125)
        far_time_to_exl : float
            Time to expire of far term option in years (defaults to 0.25)
        volatility : float 
            Stock volatility (defaults to 25%)
        int_rate : float
            Risk-free interest rate (continuously compounded annual rate, defaults to 5%)
        div_yield : float
            Dividend yield of underlying stock (continuously compounded annual rate, defaults to 2.5%)
        Returns
        -------
        product : StructuredProduct
        """
        # Straddle elements
        elements = [options.OptionElement(type='call', 
                                          strike=strike,
                                          time_to_expiry=near_time_to_exp),
                    options.OptionElement(type='call', 
                                          strike=strike,
                                          time_to_expiry=far_time_to_exp)]
        # short the near term expiry and long the far term expiry
        weights = np.array([-1, 1])
        product = options.StructuredProduct(elements=elements,
                                            weights=weights,
                                            volatility=volatility,
                                            int_rate=int_rate,
                                            div_yield=div_yield)
        return product