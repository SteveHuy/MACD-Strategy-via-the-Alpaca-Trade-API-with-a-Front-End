import Dropdown from "./Dropdown.js"
import Plot from  "./Plot.js"
import "./Styles.css"
import Stats from "./Stats.js"
import Execute from "./Execute.js"

const App = () =>{

  return(
    <div>
    <h1>Trading Bot!</h1>
    <div className="describe">
      <p>The MACD (Moving Average Convergence Divergence) strategy is a popular tool used by traders to identify potential buying and selling opportunities. It involves calculating the MACD line by subtracting the 26-day exponential moving average from the 12-day EMA, and then plotting it alongside a 9-day EMA called the signal line. When the MACD line crosses above the signal line, it suggests a bullish signal for buying, and when it crosses below, it indicates a bearish signal for selling. Traders often use the histogram representation and look for confirmation from price action and other indicators to increase the reliability of signals.</p>
    </div>
    <Dropdown/>
    <h2>Plots</h2>
    <Plot />
    <h2>Stats of Chosen Stocks</h2>
    <Stats />
    <h2>Execute the Program</h2>
    <Execute />
  </div>
    );
};







export default App;