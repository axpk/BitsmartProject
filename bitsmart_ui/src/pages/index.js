import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { Button } from "@mui/material";
import Prediction from "./prediction";
import { useEffect, useState, useRef } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [prediction, setPrediction] = useState(false);
  const [date, setDate] = useState("");
  const [result, setResult] = useState(null);
  const [skeleton, setSkeleton] = useState(false);
  const initMount = useRef(true);

  const handleDateChange = (e) => {
    setDate(e.target.value);
  };

  const handlePredict = async () => {
    if (date) {
      setSkeleton(true);
      console.log(date);
      try {
        const response = await fetch("https://bitsmart-backend-2b0b46a4c9ee.herokuapp.com/predict", {
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
    } else {
      alert("You must input a date!");
    }
  };

  // Skeleton for loading prediction results
  useEffect(() => {
    if (initMount.current) {
      initMount.current = false;
    } else {
      setSkeleton(false);
    }
  }, [result]);

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

        {skeleton && <div>Loading...</div>}

        {prediction && result && (
          <>
            <div>
              <h2 style={{ marginBottom: "0.25em" }}>Predicted prices (in USD) for next seven days are:</h2>
              <p>Highest Price: {result.highest_price}</p>
              <p>Lowest Price: {result.lowest_price}</p>
              <p>Average Closing Price: {result.avg_closing_price}</p>
            </div>
            <br />
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
