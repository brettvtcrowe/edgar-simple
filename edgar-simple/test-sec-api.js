#!/usr/bin/env node

/**
 * Phase 1: Core API Testing
 * Test SEC API endpoints directly to ensure our understanding is correct
 */

// Test 1: Company Tickers Endpoint
async function testCompanyTickers() {
  console.log('🧪 Testing SEC Company Tickers Endpoint...');
  
  try {
    const data = await fetch('https://www.sec.gov/files/company_tickers.json', {
      headers: {
        'User-Agent': 'SimpleEdgarApp/1.0 (brett.vantil@crowe.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
      }
    });
    
    const tickers = await data.json();
    
    // Test: Can we find Apple?
    const apple = Object.values(tickers).find(c => c.ticker === 'AAPL');
    if (apple) {
      console.log('✅ Company Tickers API: SUCCESS');
      console.log(`   Found Apple: ${apple.title} (CIK: ${apple.cik_str})`);
      return apple.cik_str;
    } else {
      console.log('❌ Company Tickers API: FAILED - Could not find AAPL');
      return null;
    }
  } catch (error) {
    console.log('❌ Company Tickers API: FAILED -', error.message);
    return null;
  }
}

// Test 2: Company Filings Endpoint
async function testCompanyFilings(cik) {
  if (!cik) {
    console.log('⏭️  Skipping filings test - no CIK available');
    return;
  }
  
  console.log('🧪 Testing SEC Company Filings Endpoint...');
  
  try {
    // CIK must be padded to 10 digits with leading zeros
    const paddedCik = String(cik).padStart(10, '0');
    const url = `https://data.sec.gov/submissions/CIK${paddedCik}.json`;
    
    const data = await fetch(url, {
      headers: {
        'User-Agent': 'SimpleEdgarApp/1.0 (brett.vantil@crowe.com)',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
      }
    });
    
    const filings = await data.json();
    
    if (filings.filings && filings.filings.recent) {
      console.log('✅ Company Filings API: SUCCESS');
      console.log(`   Company: ${filings.name}`);
      console.log(`   Recent filings: ${filings.filings.recent.accessionNumber.length}`);
      
      // Test URL construction
      if (filings.filings.recent.accessionNumber.length > 0) {
        const firstFiling = {
          cik: cik,
          accession: filings.filings.recent.accessionNumber[0],
          document: filings.filings.recent.primaryDocument[0]
        };
        
        const secUrl = `https://www.sec.gov/Archives/edgar/data/${firstFiling.cik}/${firstFiling.accession.replace(/-/g, '')}/${firstFiling.document}`;
        console.log(`   Sample SEC URL: ${secUrl}`);
        
        return true;
      }
    } else {
      console.log('❌ Company Filings API: FAILED - Invalid response structure');
      return false;
    }
  } catch (error) {
    console.log('❌ Company Filings API: FAILED -', error.message);
    return false;
  }
}

// Test 3: Rate Limiting Awareness
function testRateLimiting() {
  console.log('🧪 Testing Rate Limiting Awareness...');
  console.log('✅ Rate Limiting: REMEMBER - 10 requests per second maximum');
  console.log('   This test made 2 requests - we\'re well within limits');
}

// Main test runner
async function runTests() {
  console.log('🚀 Phase 1: Core SEC API Testing\n');
  
  const cik = await testCompanyTickers();
  const filingsWork = await testCompanyFilings(cik);
  testRateLimiting();
  
  console.log('\n📊 Test Results Summary:');
  console.log(`   Company Tickers: ${cik ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`   Company Filings: ${filingsWork ? '✅ PASS' : '❌ FAIL'}`);
  
  if (cik && filingsWork) {
    console.log('\n🎉 ALL TESTS PASSED! SEC API integration is working.');
    console.log('   Ready to proceed to Phase 2: Backend TDD');
  } else {
    console.log('\n⚠️  Some tests failed. Need to investigate before proceeding.');
  }
}

// Run the tests
runTests().catch(console.error);
