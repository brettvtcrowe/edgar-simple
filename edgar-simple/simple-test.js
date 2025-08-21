const request = require('supertest');
const app = require('./server');

// Simple test to see what's happening
console.log('Testing server import...');
console.log('App type:', typeof app);
console.log('App keys:', Object.keys(app));

// Check if routes are registered
if (app._router && app._router.stack) {
  const routes = app._router.stack
    .filter(layer => layer.route)
    .map(layer => layer.route.path);
  console.log('Available routes:', routes);
} else {
  console.log('No router stack found');
}

// Test basic endpoint
async function testEndpoint() {
  try {
    console.log('Testing /api/filings endpoint...');
    const response = await request(app)
      .post('/api/filings')
      .send({ ticker: 'AAPL' });
    
    console.log('Response status:', response.status);
    console.log('Response body:', response.body);
  } catch (error) {
    console.error('Error testing endpoint:', error.message);
  }
}

testEndpoint();
