'use client';

import React from 'react';
import Link from 'next/link';

function App() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>ยินดีต้อนรับสู่เว็บไซต์ร้านเล็ก</h1>

      <div style={styles.buttonGroup}>
        <Link href="/barcode">
          <button style={styles.button}>สแกนบาร์โค้ด</button>
        </Link>
        <Link href="/order">
          <button style={styles.button}>รายการคำสั่งซื้อ</button>
        </Link>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: '100vh',
    background: 'linear-gradient(to bottom right, #f8fafc, #dbeafe)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: "'Prompt', sans-serif", // Thai-friendly font if loaded
  },
  title: {
    fontSize: '2.5rem',
    color: '#1e293b',
    marginBottom: '40px',
  },
  buttonGroup: {
    display: 'flex',
    gap: '20px',
    flexWrap: 'wrap',
  },
  button: {
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    padding: '12px 24px',
    fontSize: '1.1rem',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
  },
};

export default App;
