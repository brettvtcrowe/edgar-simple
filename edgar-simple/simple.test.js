/**
 * Simple test to verify our approach
 */

describe('Basic Functionality', () => {
  test('should work with basic logic', () => {
    const validateTicker = (ticker) => {
      if (!ticker || ticker.trim() === '') {
        return { valid: false, error: 'Ticker is required' };
      }
      return { valid: true };
    };
    
    expect(validateTicker('')).toEqual({ valid: false, error: 'Ticker is required' });
    expect(validateTicker('AAPL')).toEqual({ valid: true });
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
});
