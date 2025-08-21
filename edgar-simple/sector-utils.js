/**
 * Sector Utilities for Enhanced SEC Filing Search
 * Phase 2: Enhanced Foundation
 */

/**
 * Sector classification based on SIC and NAICS codes
 * @param {Object} company - Company object with SIC and NAICS codes
 * @returns {string} Sector name
 */
function classifySector(company) {
  const sicCode = company.sic_code;
  const naicsCode = company.naics_code;
  
  // Technology sector
  if (sicCode === '7372' || sicCode === '7373' || sicCode === '7374' ||
      naicsCode === '511210' || naicsCode === '541511' || naicsCode === '541512') {
    return 'Technology';
  }
  
  // Healthcare sector
  if (sicCode === '2834' || sicCode === '2835' || sicCode === '2836' ||
      naicsCode === '325400' || naicsCode === '339100' || naicsCode === '541715') {
    return 'Healthcare';
  }
  
  // Financial sector
  if (sicCode === '6021' || sicCode === '6022' || sicCode === '6025' ||
      naicsCode === '522110' || naicsCode === '522120' || naicsCode === '522130') {
    return 'Financial';
  }
  
  // Energy sector
  if (sicCode === '1311' || sicCode === '2911' || sicCode === '4922' ||
      naicsCode === '211110' || naicsCode === '221100' || naicsCode === '486200') {
    return 'Energy';
  }
  
  // Consumer sector
  if (sicCode === '5411' || sicCode === '5412' || sicCode === '5413' ||
      naicsCode === '445100' || naicsCode === '446100' || naicsCode === '447100') {
    return 'Consumer';
  }
  
  // Industrial sector
  if (sicCode === '3511' || sicCode === '3523' || sicCode === '3531' ||
      naicsCode === '332300' || naicsCode === '333200' || naicsCode === '334500') {
    return 'Industrial';
  }
  
  // Default to Other if no match
  return 'Other';
}

/**
 * Get sector information and statistics
 * @param {string} sectorName - Sector name
 * @returns {Object} Sector information
 */
function getSectorInfo(sectorName) {
  const sectors = {
    'Technology': {
      name: 'Technology',
      description: 'Software, hardware, and technology services companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K'],
      riskFactors: ['Cybersecurity', 'Regulatory changes', 'Competition']
    },
    'Healthcare': {
      name: 'Healthcare',
      description: 'Pharmaceutical, biotech, and healthcare services companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K', 'S-1'],
      riskFactors: ['FDA approval', 'Clinical trials', 'Patent expiration']
    },
    'Financial': {
      name: 'Financial',
      description: 'Banks, insurance, and financial services companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K', '424B3'],
      riskFactors: ['Interest rates', 'Regulatory compliance', 'Credit risk']
    },
    'Energy': {
      name: 'Energy',
      description: 'Oil, gas, and renewable energy companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K', 'S-1'],
      riskFactors: ['Commodity prices', 'Environmental regulations', 'Geopolitical risk']
    },
    'Consumer': {
      name: 'Consumer',
      description: 'Retail, consumer goods, and services companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K'],
      riskFactors: ['Consumer spending', 'Supply chain', 'Competition']
    },
    'Industrial': {
      name: 'Industrial',
      description: 'Manufacturing, construction, and industrial services companies',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K'],
      riskFactors: ['Economic cycles', 'Raw material costs', 'Labor costs']
    },
    'Other': {
      name: 'Other',
      description: 'Companies not fitting into major sector categories',
      count: 0,
      topForms: ['10-K', '10-Q', '8-K'],
      riskFactors: ['Sector-specific', 'General market', 'Regulatory']
    }
  };
  
  return sectors[sectorName] || sectors['Other'];
}

/**
 * Calculate sector analytics
 * @param {Array} filings - Array of filing objects
 * @param {string} sector - Sector name
 * @returns {Object} Sector analytics
 */
function calculateSectorAnalytics(filings, sector) {
  const sectorFilings = filings.filter(filing => filing.sector === sector);
  
  // Count filings by form type
  const formCounts = {};
  sectorFilings.forEach(filing => {
    formCounts[filing.form] = (formCounts[filing.form] || 0) + 1;
  });
  
  // Sort forms by count
  const topForms = Object.entries(formCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)
    .map(([form, count]) => ({ form, count }));
  
  // Calculate risk score based on filing patterns
  let riskScore = 50; // Base risk score
  
  // Increase risk for high frequency of 8-K filings (material events)
  const eightKCount = formCounts['8-K'] || 0;
  if (eightKCount > 10) riskScore += 20;
  else if (eightKCount > 5) riskScore += 10;
  
  // Increase risk for recent filings (potential issues)
  const recentFilings = sectorFilings.filter(filing => {
    const filingDate = new Date(filing.date);
    const oneMonthAgo = new Date();
    oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
    return filingDate > oneMonthAgo;
  });
  
  if (recentFilings.length > 5) riskScore += 15;
  
  // Cap risk score at 100
  riskScore = Math.min(riskScore, 100);
  
  return {
    sector,
    filingCount: sectorFilings.length,
    topForms,
    riskScore,
    recentActivity: recentFilings.length,
    trends: {
      totalFilings: sectorFilings.length,
      eightKPercentage: ((eightKCount / sectorFilings.length) * 100).toFixed(1)
    }
  };
}

/**
 * Get all available sectors
 * @returns {Array} Array of sector objects
 */
function getAllSectors() {
  const sectors = ['Technology', 'Healthcare', 'Financial', 'Energy', 'Consumer', 'Industrial', 'Other'];
  
  return sectors.map(sector => {
    const info = getSectorInfo(sector);
    return {
      name: info.name,
      description: info.description,
      count: 0, // Will be populated with actual data
      riskFactors: info.riskFactors
    };
  });
}

module.exports = {
  classifySector,
  getSectorInfo,
  calculateSectorAnalytics,
  getAllSectors
};
