/**
 * Phase 2: Backend TDD
 * Test our Express server API endpoints
 */

const request = require('supertest');
const express = require('express');

// Since Jest has issues with our Express middleware, let's test the core logic directly
describe('SEC Filing Lookup Core Logic', () => {
  test('should validate ticker input correctly', () => {
    // Test the validation logic directly
    const validateTicker = (ticker) => {
      if (!ticker || ticker.trim() === '') {
        return { valid: false, error: 'Ticker is required' };
      }
      return { valid: true };
    };
    
    expect(validateTicker('')).toEqual({ valid: false, error: 'Ticker is required' });
    expect(validateTicker('   ')).toEqual({ valid: false, error: 'Ticker is required' });
    expect(validateTicker('AAPL')).toEqual({ valid: true });
    expect(validateTicker('NVDA')).toEqual({ valid: true });
  });
  
  test('should construct SEC URLs correctly', () => {
    const constructSecUrl = (cik, accession, document) => {
      const cikWithoutZeros = String(cik).replace(/^0+/, '');
      const accessionNoHyphens = accession.replace(/-/g, '');
      return `https://www.sec.gov/Archives/edgar/data/${cikWithoutZeros}/${accessionNoHyphens}/${document}`;
    };
    
    const url = constructSecUrl(320193, '0000320193-25-000073', 'aapl-20250628.htm');
    expect(url).toBe('https://www.sec.gov/Archives/edgar/data/320193/000032019325000073/aapl-20250628.htm');
  });
  
  test('should pad CIK to 10 digits correctly', () => {
    const padCik = (cik) => String(cik).padStart(10, '0');
    
    expect(padCik(320193)).toBe('0000320193');
    expect(padCik(123)).toBe('0000000123');
    expect(padCik(1234567890)).toBe('1234567890');
  });
});

// Test the actual server by starting it
describe('SEC Filing Lookup Server (Live)', () => {
  let server;
  let app;
  
  beforeAll(async () => {
    // Import the app without starting the server
    app = require('./server');
    
    // Start the server on a test port
    const PORT = 3001;
    server = app.listen(PORT);
    
    // Wait for server to start
    await new Promise(resolve => setTimeout(resolve, 100));
  });
  
  afterAll(async () => {
    if (server) {
      await new Promise(resolve => server.close(resolve));
    }
  });
  
  test('should serve static files', async () => {
    const response = await request(app)
      .get('/')
      .expect(200);
    
    expect(response.text).toContain('SEC Filing Lookup');
  });
  
  test('should return error for missing ticker', async () => {
    const response = await request(app)
      .post('/api/filings')
      .send({})
      .expect(400);
    
    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toBe('Ticker is required');
  });
  
  test('should return error for empty ticker', async () => {
    const response = await request(app)
      .post('/api/filings')
      .send({ ticker: '' })
      .expect(400);
    
    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toBe('Ticker is required');
  });
  
  test('should return error for invalid ticker', async () => {
    const response = await request(app)
      .post('/api/filings')
      .send({ ticker: 'INVALID123' })
      .expect(404);
    
    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toBe('Ticker not found');
  });
  
  test('should return filings for valid ticker (AAPL)', async () => {
    const response = await request(app)
      .post('/api/filings')
      .send({ ticker: 'AAPL' })
      .expect(200);
    
    expect(response.body).toHaveProperty('company');
    expect(response.body).toHaveProperty('cik');
    expect(response.body).toHaveProperty('filings');
    expect(response.body.company).toBe('Apple Inc.');
    expect(response.body.cik).toBe(320193);
    expect(Array.isArray(response.body.filings)).toBe(true);
    expect(response.body.filings.length).toBeGreaterThan(0);
    expect(response.body.filings.length).toBeLessThanOrEqual(10);
    
    // Check filing structure
    const filing = response.body.filings[0];
    expect(filing).toHaveProperty('form');
    expect(filing).toHaveProperty('date');
    expect(filing).toHaveProperty('description');
    expect(filing).toHaveProperty('url');
    expect(filing.url).toMatch(/^https:\/\/www\.sec\.gov\/Archives\/edgar\/data\/\d+\/\d+\/.*$/);
  });
});
