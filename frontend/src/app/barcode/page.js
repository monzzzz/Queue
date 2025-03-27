"use client";
import React, { useState } from 'react';
import axios from 'axios';
import { Html5Qrcode } from "html5-qrcode";


function Barcode() {
  const [barcode, setBarcode] = useState(""); // Store the scanned barcode
  const [isScanning, setIsScanning] = useState(false); // Toggle scanning state

  // Modified function accepts the barcode as a parameter
  const sendBarcodeToBackend = async (scannedBarcode) => {
    try {
      const response = await axios.post(`http://${process.env.NEXT_PUBLIC_HOST}:5000/upload`, { barcode: scannedBarcode });
      alert(`Price for barcode ${scannedBarcode}: ${response.data.price}`);
    } catch (error) {
      console.error("Error sending barcode to backend:", error);
      alert("Failed to process the barcode.");
    }
  };

  const startScanning = () => {
    const scannerElement = document.querySelector("#barcode-scanner");
    if (!scannerElement) {
      console.error("Scanner element not found.");
      return;
    }

    setIsScanning(true);

    const html5QrCode = new Html5Qrcode("barcode-scanner");
    html5QrCode
      .start(
        { facingMode: "environment" }, // Use the rear camera
        {
          fps: 10, // Frames per second
          qrbox: { width: 250, height: 250 }, // Scanning box size
        },
        (decodedText) => {
          // Once a barcode is detected:
          setBarcode(decodedText);
          // Stop scanning and then send the barcode automatically
          html5QrCode.stop()
            .then(() => {
              setIsScanning(false);
              sendBarcodeToBackend(decodedText);
            })
            .catch((err) => {
              console.error("Error stopping scanner:", err);
              setIsScanning(false);
            });
        },
        (errorMessage) => {
          console.warn("Scanning error:", errorMessage);
        }
      )
      .catch((err) => {
        console.error("Error initializing html5-qrcode:", err);
        setIsScanning(false);
      });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-4xl font-bold mb-6 text-center text-red-600">Queue System</h2>
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md mb-8">
        <h3 className="text-2xl font-semibold mb-4 text-gray-700">📷 Barcode Scanner</h3>
        <div id="barcode-scanner" className="w-full h-64 bg-gray-200 rounded-lg mb-4"></div>
        {isScanning ? (
          <button
            onClick={() => setIsScanning(false)}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
          >
            Stop Scanning
          </button>
        ) : (
          <button
            onClick={startScanning}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
          >
            Start Scanning
          </button>
        )}
        {barcode && (
          <div className="mt-4">
            <p className="text-lg text-gray-700">
              <strong>Scanned Barcode:</strong> {barcode}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Barcode;
