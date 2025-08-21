/**
 * Debug test to isolate the 404 issue
 */

const request = require('supertest');
const express = require('express');

// Test 1: Simple Express app
describe('Debug: Simple Express App', () => {
  test('should work with basic Express app', async () => {
    const app = express();
    app.get('/test', (req, res) => {
      res.json({ message: 'Hello World' });
    });
    
    const response = await request(app)
      .get('/test')
      .expect(200);
    
    expect(response.body.message).toBe('Hello World');
  });
});

// Test 2: Import our actual server
describe('Debug: Import Our Server', () => {
  test('should import server without error', () => {
    expect(() => {
      const app = require('./server');
      expect(app).toBeDefined();
      expect(typeof app.use).toBe('function');
    }).not.toThrow();
  });
  
  test('should have /api/filings endpoint', () => {
    const app = require('./server');
    const routes = app._router.stack
      .filter(layer => layer.route)
      .map(layer => layer.route.path);
    
    console.log('Available routes:', routes);
    expect(routes).toContain('/api/filings');
  });
});

// Test 3: Test our actual server endpoints
describe('Debug: Test Our Server Endpoints', () => {
  let app;
  
  beforeAll(() => {
    app = require('./server');
  });
  
  test('should serve static files', async () => {
    const response = await request(app)
      .get('/')
      .expect(200);
    
    expect(response.text).toContain('SEC Filing Lookup');
  });
  
  test('should handle missing ticker', async () => {
    const response = await request(app)
      .post('/api/filings')
      .send({})
      .expect(400);
    
    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toBe('Ticker is required');
  });
});
