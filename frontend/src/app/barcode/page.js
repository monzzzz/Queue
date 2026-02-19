"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";

const BarcodeInput = () => {
  const [barcode, setBarcode] = useState("");
  const [message, setMessage] = useState("");
  const [typingTimeout, setTypingTimeout] = useState(null);

  const handleInputChange = (e) => {
    const value = e.target.value;

    setBarcode(value);

    // Clear previous timeout
    if (typingTimeout) clearTimeout(typingTimeout);

    // Start a new timeout to detect end of scanning (e.g., 300ms after last character)
    const timeoutId = setTimeout(() => {
      if (value) {
        sendToBackend(value);
        setBarcode(""); // Clear the barcode input after sending
      }
    }, 300);  // Adjust this delay as needed (300ms is usually good for scanners)

    setTypingTimeout(timeoutId);
  };

  const sendToBackend = async (barcode) => {
    try {
      const response = await axios.post(`https://${process.env.NEXT_PUBLIC_HOST}:5000/upload`, { barcode }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setMessage(response.data.message);
    } catch (error) {
      console.error("Error sending barcode to backend:", error);
      setMessage("Failed to send barcode to backend.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Barcode Scanner Input</h1>
      <input
        type="text"
        value={barcode}
        onChange={handleInputChange}
        style={{ width: "300px", padding: "10px" }}
        autoFocus
      />
      <p>Scanned Barcode: {barcode}</p>
      <p>Server Message: {message}</p>
    </div>
  );
};

export default BarcodeInput;
