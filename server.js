const express = require('express');
const app = express();

// Serve the HTML file
app.use(express.static('.'));
app.use(express.json());

// Single endpoint that does everything
app.post('/api/filings', async (req, res) => {
  try {
    const { ticker } = req.body;

    // Validation: Check if ticker is provided
    if (!ticker || ticker.trim() === '') {
      return res.status(400).json({ error: 'Ticker is required' });
    }

    // Step 1: Get the list of all companies from SEC
    // This is a public file the SEC provides with all tickers
    const tickersResponse = await fetch('https://www.sec.gov/files/company_tickers.json', {
      headers: {
        'User-Agent': 'SimpleEdgarApp/1.0 (brett.vantil@crowe.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
      }
    });
    const tickers = await tickersResponse.json();

    // Step 2: Find the company by ticker
    // The SEC file has entries like { "ticker": "AAPL", "cik_str": 320193, ... }
    const company = Object.values(tickers).find(c => c.ticker === ticker.toUpperCase());
    if (!company) {
      return res.status(404).json({ error: 'Ticker not found' });
    }

    // Step 3: Get the company's filings
    // CIK must be padded to 10 digits with leading zeros
    const cik = String(company.cik_str).padStart(10, '0');
    const filingsResponse = await fetch(`https://data.sec.gov/submissions/CIK${cik}.json`, {
      headers: {
        'User-Agent': 'SimpleEdgarApp/1.0 (brett.vantil@crowe.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
      }
    });
    const data = await filingsResponse.json();

    // Step 4: Build the response with the 10 most recent filings
    const filings = [];
    const recent = data.filings.recent;

    for (let i = 0; i < Math.min(10, recent.accessionNumber.length); i++) {
      // Build the SEC URL
      // Format: https://www.sec.gov/Archives/edgar/data/{CIK}/{ACCESSION}/{DOCUMENT}
      const cikWithoutZeros = cik.replace(/^0+/, '');
      const accessionNoHyphens = recent.accessionNumber[i].replace(/-/g, '');
      const document = recent.primaryDocument[i];

      filings.push({
        form: recent.form[i],
        date: recent.filingDate[i],
        description: recent.primaryDocDescription[i] || recent.form[i],
        url: `https://www.sec.gov/Archives/edgar/data/${cikWithoutZeros}/${accessionNoHyphens}/${document}`
      });
    }

    res.json({
      company: data.name,
      cik: company.cik_str,
      filings
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to fetch data from SEC' });
  }
});

// Only start the server if this file is run directly
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('Enter a ticker and click "Get Filings" to test');
  });
}

module.exports = app;
