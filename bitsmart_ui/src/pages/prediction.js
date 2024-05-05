import React, { useEffect } from "react";

const Prediction = (props) => {
  useEffect(() => {
    console.log("Rendering Prediction...");
  }, []);
  return (
    <div>
      <p>You have selected today as . Bitsmart has made the following predictions.</p>
      <h3>Predicted prices (USD) for the next seven days are:</h3>
      <table>
        <tbody>
          <tr>
            <td>Highest Price</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Lowest Price</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Average Closing Price</td>
            <td>N/A</td>
          </tr>
        </tbody>
      </table>
      <h3>Recommended swing trading strategy</h3>
      <table>
        <tbody>
          <tr>
            <td>Sell All</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>All in</td>
            <td>N/A</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Prediction;
