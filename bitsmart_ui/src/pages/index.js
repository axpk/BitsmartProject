import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { Button } from "@mui/material";
import Prediction from "./prediction";
import { useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [prediction, setPrediction] = useState(false);
  const handlePredict = () => {
    if (!prediction) {
      setPrediction(true);
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
            Assume today's date is: <input type="date" />
          </p>
        </div>
        <br />
        <Button variant="contained" onClick={handlePredict}>
          Predict
        </Button>
        <br />
        <br />
        {prediction ? <Prediction /> : <></>}
      </main>
    </>
  );
}
