/**
 * Enhanced Search Functionality Tests
 * Phase 2: Enhanced Foundation
 * 
 * Following TDD: Write tests first, then implement
 */

const request = require('supertest');
const app = require('./server');

describe('Enhanced Search API', () => {
  describe('POST /api/search/advanced', () => {
    test('should search by form type', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          formType: '8-K',
          dateRange: '3years',
          keywords: 'restatement'
        })
        .expect(200);

      expect(response.body).toHaveProperty('results');
      expect(response.body.results).toBeInstanceOf(Array);
      expect(response.body.results.length).toBeGreaterThan(0);
      
      // Verify all results are 8-K forms
      response.body.results.forEach(filing => {
        expect(filing.formType).toBe('8-K');
      });
    });

    test('should search by date range', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          dateRange: '1year',
          keywords: 'revenue recognition'
        })
        .expect(200);

      expect(response.body).toHaveProperty('results');
      expect(response.body.results).toBeInstanceOf(Array);
      
      // Verify dates are within 1 year
      const oneYearAgo = new Date();
      oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
      
      response.body.results.forEach(filing => {
        const filingDate = new Date(filing.filingDate);
        expect(filingDate.getTime()).toBeGreaterThanOrEqual(oneYearAgo.getTime());
      });
    });

    test('should search by keywords', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          keywords: 'ASC 606 principal agent'
        })
        .expect(200);

      expect(response.body).toHaveProperty('results');
      expect(response.body.results).toBeInstanceOf(Array);
      
      // Verify results contain relevant keywords
      const hasRelevantResults = response.body.results.some(filing => 
        filing.description.toLowerCase().includes('asc 606') ||
        filing.description.toLowerCase().includes('principal') ||
        filing.description.toLowerCase().includes('agent')
      );
      expect(hasRelevantResults).toBe(true);
    });

    test('should search by sector', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          sector: 'Technology',
          keywords: 'revenue recognition'
        })
        .expect(200);

      expect(response.body).toHaveProperty('results');
      expect(response.body.results).toBeInstanceOf(Array);
      
      // Verify all results are from technology sector
      response.body.results.forEach(filing => {
        expect(filing.sector).toBe('Technology');
      });
    });

    test('should combine multiple search criteria', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          formType: '10-K',
          sector: 'Healthcare',
          dateRange: '2years',
          keywords: 'milestone method'
        })
        .expect(200);

      expect(response.body).toHaveProperty('results');
      expect(response.body.results).toBeInstanceOf(Array);
      
      // Verify all criteria are met
      response.body.results.forEach(filing => {
        expect(filing.formType).toBe('10-K');
        expect(filing.sector).toBe('Healthcare');
        
        const filingDate = new Date(filing.filingDate);
        const twoYearsAgo = new Date();
        twoYearsAgo.setFullYear(twoYearsAgo.getFullYear() - 2);
        expect(filingDate.getTime()).toBeGreaterThanOrEqual(twoYearsAgo.getTime());
      });
    });

    test('should return error for invalid date range', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({
          dateRange: 'invalid'
        })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('Invalid date range');
    });

    test('should return error for missing search criteria', async () => {
      const response = await request(app)
        .post('/api/search/advanced')
        .send({})
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('At least one search criteria required');
    });
  });

  describe('GET /api/sectors', () => {
    test('should return list of available sectors', async () => {
      const response = await request(app)
        .get('/api/sectors')
        .expect(200);

      expect(response.body).toHaveProperty('sectors');
      expect(response.body.sectors).toBeInstanceOf(Array);
      expect(response.body.sectors.length).toBeGreaterThan(0);
      
      // Verify sector structure
      response.body.sectors.forEach(sector => {
        expect(sector).toHaveProperty('name');
        expect(sector).toHaveProperty('count');
        expect(sector).toHaveProperty('description');
      });
    });
  });

  describe('GET /api/sectors/:sector/analytics', () => {
    test('should return sector analytics', async () => {
      const response = await request(app)
        .get('/api/sectors/Technology/analytics')
        .expect(200);

      expect(response.body).toHaveProperty('sector');
      expect(response.body.sector).toBe('Technology');
      expect(response.body).toHaveProperty('filingCount');
      expect(response.body).toHaveProperty('trends');
      expect(response.body).toHaveProperty('riskScore');
      expect(response.body).toHaveProperty('topForms');
    });

    test('should return 404 for non-existent sector', async () => {
      await request(app)
        .get('/api/sectors/NonExistentSector/analytics')
        .expect(404);
    });
  });

  describe('GET /api/trends', () => {
    test('should return filing trends', async () => {
      const response = await request(app)
        .get('/api/trends')
        .query({ period: '6months' })
        .expect(200);

      expect(response.body).toHaveProperty('trends');
      expect(response.body.trends).toBeInstanceOf(Array);
      expect(response.body.trends.length).toBeGreaterThan(0);
      
      // Verify trend structure
      response.body.trends.forEach(trend => {
        expect(trend).toHaveProperty('date');
        expect(trend).toHaveProperty('filingCount');
        expect(trend).toHaveProperty('sectorBreakdown');
      });
    });

    test('should return error for invalid period', async () => {
      const response = await request(app)
        .get('/api/trends')
        .query({ period: 'invalid' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('Invalid period');
    });
  });
});

describe('Enhanced Search Core Logic', () => {
  test('should validate search criteria', () => {
    const { validateSearchCriteria } = require('./search-utils');
    
    // Valid criteria
    const validCriteria = {
      formType: '8-K',
      dateRange: '3years',
      keywords: 'restatement'
    };
    expect(validateSearchCriteria(validCriteria)).toEqual({ valid: true });

    // Invalid criteria
    const invalidCriteria = {
      dateRange: 'invalid'
    };
    const result = validateSearchCriteria(invalidCriteria);
    expect(result.valid).toBe(false);
    expect(result.error).toContain('Invalid date range');
  });

  test('should construct advanced search query', () => {
    const { constructSearchQuery } = require('./search-utils');
    
    const criteria = {
      formType: '8-K',
      sector: 'Technology',
      keywords: 'revenue recognition'
    };
    
    const query = constructSearchQuery(criteria);
    expect(query).toHaveProperty('formType', '8-K');
    expect(query).toHaveProperty('sector', 'Technology');
    expect(query).toHaveProperty('keywords', 'revenue recognition');
  });

  test('should classify company sector', () => {
    const { classifySector } = require('./sector-utils');
    
    const company = {
      sic_code: '7372',
      naics_code: '511210',
      name: 'Microsoft Corporation'
    };
    
    const sector = classifySector(company);
    expect(sector).toBe('Technology');
  });
});
