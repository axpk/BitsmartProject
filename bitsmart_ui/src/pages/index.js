import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { Button } from "@mui/material";
import Prediction from "./prediction";
import { useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [prediction, setPrediction] = useState(false);
  const [date, setDate] = useState("");
  const [result, setResult] = useState(null);

  const handleDateChange = (e) => {
    setDate(e.target.value);
  };

  const handlePredict = async () => {
    if (date) {
      console.log(date);
      try {
        const response = await fetch("http://localhost:8000/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ date }),
        });

        if (response.ok) {
          const data = await response.json();
          setResult(data);
          setPrediction(true);
        } else {
          console.error("Error: " + response.statusText);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  return (
    <>
      <Head>
        <title>BitSmart</title>
        <meta name="description" content="Bitsmart NextJS" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={`${styles.main} ${inter.className}`}>
        <div className={styles.description}>
          <h1>BitSmart Prediction Console</h1>
        </div>
        <div className={styles.description}>
          <p>
            Assume today's date is: <input type="date" onChange={handleDateChange} />
          </p>
        </div>
        <br />
        <Button variant="contained" onClick={handlePredict}>
          Predict
        </Button>
        <br />
        <br />

        {prediction && result && (
          <>
            <div>
              <h2 style={{ marginBottom: "0.25em" }}>Predicted prices (in USD) for next seven days are:</h2>
              <p>Highest Price: {result.highest_price}</p>
              <p>Lowest Price: {result.lowest_price}</p>
              <p>Average Closing Price: {result.avg_closing_price}</p>
            </div>
            <div>
              <h2 style={{ marginBottom: "0.25em" }}>Recommended swing trading strategy:</h2>
              <p>Sell All: {result.sell_date}</p>
              <p>All In: {result.load_date}</p>
            </div>
          </>
        )}
      </main>
    </>
  );
}
