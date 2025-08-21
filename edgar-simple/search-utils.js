/**
 * Search Utilities for Enhanced SEC Filing Search
 * Phase 2: Enhanced Foundation
 */

/**
 * Validate search criteria
 * @param {Object} criteria - Search criteria object
 * @returns {Object} Validation result with valid flag and optional error message
 */
function validateSearchCriteria(criteria) {
  // Check if at least one criteria is provided
  const hasCriteria = Object.keys(criteria).some(key => 
    criteria[key] && criteria[key].toString().trim() !== ''
  );
  
  if (!hasCriteria) {
    return { 
      valid: false, 
      error: 'At least one search criteria required' 
    };
  }

  // Validate date range if provided
  if (criteria.dateRange) {
    const validDateRanges = ['1year', '2years', '3years', '5years', '6months'];
    if (!validDateRanges.includes(criteria.dateRange)) {
      return { 
        valid: false, 
        error: 'Invalid date range. Must be one of: 1year, 2years, 3years, 5years, 6months' 
      };
    }
  }

  // Validate form type if provided
  if (criteria.formType) {
    const validFormTypes = ['8-K', '10-K', '10-Q', 'S-1', 'S-3', '424B3'];
    if (!validFormTypes.includes(criteria.formType)) {
      return { 
        valid: false, 
        error: 'Invalid form type. Must be one of: 8-K, 10-K, 10-Q, S-1, S-3, 424B3' 
      };
    }
  }

  return { valid: true };
}

/**
 * Construct search query object
 * @param {Object} criteria - Search criteria
 * @returns {Object} Processed search query
 */
function constructSearchQuery(criteria) {
  const query = {};
  
  if (criteria.formType) {
    query.formType = criteria.formType;
  }
  
  if (criteria.sector) {
    query.sector = criteria.sector;
  }
  
  if (criteria.keywords) {
    query.keywords = criteria.keywords.toLowerCase().trim();
  }
  
  if (criteria.dateRange) {
    query.dateRange = criteria.dateRange;
  }
  
  return query;
}

/**
 * Calculate date range from criteria
 * @param {string} dateRange - Date range string
 * @returns {Object} Start and end dates
 */
function calculateDateRange(dateRange) {
  const endDate = new Date();
  const startDate = new Date();
  
  switch (dateRange) {
    case '6months':
      startDate.setMonth(endDate.getMonth() - 6);
      break;
    case '1year':
      startDate.setFullYear(endDate.getFullYear() - 1);
      break;
    case '2years':
      startDate.setFullYear(endDate.getFullYear() - 2);
      break;
    case '3years':
      startDate.setFullYear(endDate.getFullYear() - 3);
      break;
    case '5years':
      startDate.setFullYear(endDate.getFullYear() - 5);
      break;
    default:
      startDate.setFullYear(endDate.getFullYear() - 1); // Default to 1 year
  }
  
  return { startDate, endDate };
}

/**
 * Filter filings by search criteria
 * @param {Array} filings - Array of filing objects
 * @param {Object} criteria - Search criteria
 * @returns {Array} Filtered filings
 */
function filterFilings(filings, criteria) {
  let filtered = [...filings];
  
  // Filter by form type
  if (criteria.formType) {
    filtered = filtered.filter(filing => filing.form === criteria.formType);
  }
  
  // Filter by date range
  if (criteria.dateRange) {
    const { startDate, endDate } = calculateDateRange(criteria.dateRange);
    filtered = filtered.filter(filing => {
      const filingDate = new Date(filing.date);
      return filingDate >= startDate && filingDate <= endDate;
    });
  }
  
  // Filter by keywords (if description contains keywords)
  if (criteria.keywords) {
    const keywords = criteria.keywords.toLowerCase().split(' ');
    filtered = filtered.filter(filing => {
      const description = (filing.description || '').toLowerCase();
      return keywords.some(keyword => description.includes(keyword));
    });
  }
  
  return filtered;
}

module.exports = {
  validateSearchCriteria,
  constructSearchQuery,
  calculateDateRange,
  filterFilings
};
