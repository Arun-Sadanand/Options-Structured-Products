# Creating Structured Products by Combining European Options

## 1. Introduction

As per the Black-Scholes model,
The value of a European call option on a single underlying asset can be computed as,
$$
C(S, \tau) = S e^{-d\tau}  \Phi(d_1) - K e^{-r\tau} \Phi(d_2)
$$
And the value of a put option is,
$$
P(S,\tau) = -S e^{-d\tau} \Phi(-d_1) + K e^{-r\tau} \Phi(-d_2)
$$
Where,
$$
d_1 = \frac{log(\frac{S}{K}) + \bigl(r-d + \frac{1}{2}\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}
$$
And,
$$
\begin{aligned}
d_2 &= \frac{log(\frac{S}{K}) + \bigl(r-d - \frac{1}{2}\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}\\
&= d_1 - \sigma\sqrt{\tau}
\end{aligned}
$$

Where each symbol is defined as,

- $S$ is the price of the underlying stock
- $K$ is the strike price of the option
- $\tau$ is the time remaining to maturity of the option
- $\sigma$ is the volatility of the underlying stock; the Black-Scholes framework assumes flat volatility across strikes
- $r$ is the risk-free interest rate
- $d$ is the annual dividend rate of the underlying stock
- $\Phi$ is the standard normal distribution function

If we are long a call option and short a put option, the resulting value of this package becomes:

$$
\begin{aligned}
C(S, \tau) - P(S,\tau) &= S e^{-d\tau}  \Phi(d_1) - K e^{-r\tau} \Phi(d_2) - \bigl(-S e^{-d\tau} \Phi(-d_1) + K e^{-r\tau} \Phi(-d_2) \bigr)\\
&= S e^{-d\tau} \Phi(d_1) + S e^{-d\tau} \Phi(-d_1) - K e^{-r\tau} \Phi(d_2) - K e^{-r\tau} \Phi(-d_2)\\
&= S e^{-d\tau}\bigl(\Phi(d_1) + \Phi(-d_1)\bigr) - K e^{-r\tau}\bigl(\Phi(d_2) + \Phi(-d_2)\bigr)\\
&= S e^{-d\tau} - K e^{-r\tau}. \qquad\because \Phi(x) + \Phi(-x) = 1
\end{aligned}
$$

$S e^{-d\tau} - K e^{-r\tau}$ is exactly the payoff of a forward contract on a single underlying stock with forward price $K$ and with $\tau$ years to maturity, given the continuously compouned interest rate $r$ and dividend yield $d$.

Just like combining a call and put to create a forward, it is possible to combine these options in different way to create different 'unique' synthetic payoffs. These simple structured products typically have names that correspond to the shape of their payoff diagram (eg. butterfly, straddle, condor), but they can be conceptualized as simply combinations of calls and puts on the same underlying stock, with different strike prices.

In this project, I create some common structured products by combining call and put options, and visualize their price evolution and greeks.

## 2. Design Framework

My object-oriented appraoch is this project intended to closely follow the financial framework described above.

In [`options.py`](/options.py), I define a class (`StructuredProduct`) that represents a generic structured product. This product is a combination of long and short positions in underlying elements (options), where each underlying position has a corresponding 'weight'.

The total payoff of the product is the sum of the payoffs of the underlying elements, scaled by thier weights. The underlying elements can be European call or put options defined as per the class `OptionElement`.

The `OptionElement` class provides a method (called `bs_price()`) which calculates the Black-Shcoles price of the option. The `StructuredProdcut` class is then able to take the prices of each `OptionElement`, multiply them by their `weights`, and return a single price for the combined product.

With the price in hand, the greeks (partial derivatives of price) for a `StructuredProduct` is calculated by finite differening, using defined methods for each greek.

Creating unique structured products is made possible through the class `StructuredProductFactory` in [`optionsfactory.py`](\optionsfactory.py). This class provides functions that each correspond to special types of structured product (like a bear spread or a butterfly). These special constructors contstruct and return a `StructuredProduct` for a given set of input parameters.

To create any new type of structured product, we only need to know its underlying options positions. Knowing this allows us to add another special constructor to the `StructuredProductFactory` class as required.

## 3. Visualizations

Visializtions of the evolution of product price and greeks at varying underlying spot prices $S$ and at varying time remaing to expiry $\tau$ are shown in in the Python notebook [`charts.ipynb`](\charts.ipynb).

## 4. Observations

- Visualizing payoff diagrams in this way makes clear which products are **short volatility** (eg. butterfly) and which ones are **long volatility** (eg. straddle).
- Short volatility trades benefit from time decay, they have positve **theta** near the strike.
- If we are short volatility (eg. we are long the butterfly), then we have negative gamma near the strike. If we were dynamically **delta-hedging our position**, the negative gamma indicates that delta decreases as the stock prices moves higher. The charts tell us that delta swings from close to $+1$ to close to $-1$ as the stock price $S$ moves from slightly below the center strike price $K_2$ to slightly above. This means that in order to keep our delta hedge, would be *buying shares* as the stock price rises, and *selling shares* as the stock price falls.
- The opposite would be true if we are long volatility (eg. we are long the straddle). In this case gamma is positive near the strike, indicating that delta increases as the stock price moves higher. To keep our delta hedge, would be *selling shares* as the stock price rises, and *buying shares* as the stock price falls.
