/**
 * Phase 2: Backend TDD
 * Test our Express server API endpoints
 */

const request = require('supertest');
const express = require('express');

// We'll import our server once we create it
// const app = require('./server');

describe('SEC Filing Lookup API', () => {
  let app;
  
  // Setup test app before each test
  beforeEach(() => {
    app = express();
    app.use(express.json());
    
    // TODO: Add our /api/filings endpoint here
    // app.post('/api/filings', require('./server').handleFilings);
  });
  
  describe('POST /api/filings', () => {
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
    
    test('should handle SEC API errors gracefully', async () => {
      // TODO: Mock SEC API failure and test error handling
      const response = await request(app)
        .post('/api/filings')
        .send({ ticker: 'AAPL' })
        .expect(500);
      
      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toBe('Failed to fetch data from SEC');
    });
  });
  
  describe('Server Configuration', () => {
    test('should serve static files', async () => {
      // TODO: Test that index.html is served
      const response = await request(app)
        .get('/')
        .expect(200);
      
      expect(response.text).toContain('SEC Filing Lookup');
    });
  });
});
