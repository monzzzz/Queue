 
const fs = require('fs');
const https = require('https');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  const server = https.createServer(
    {
      key: fs.readFileSync('../server.key'),  // Path to your private key
      cert: fs.readFileSync('../server.crt'), // Path to your certificate
    },
    (req, res) => {
      handle(req, res); // Handle requests to Next.js
    }
  );

  server.listen(3000, '192.168.1.220', (err) => {
    if (err) throw err;
    console.log('> Ready on https://localhost:3000');
  });
});
