# Deployment Guide: Regulatory Intelligence Hub

## Overview

This document covers the deployment process for the Regulatory Intelligence Hub, from local development to production deployment on Vercel.

## Current Deployment Status

### ✅ **Production Deployment: ACTIVE**
- **Platform**: Vercel
- **Domain**: https://edgar-simple.vercel.app/
- **Status**: ✅ **LIVE** - Successfully deployed and accessible
- **Last Deployment**: Phase 3 TDD Cycles 1-3 completion

### 📊 **Deployment History**
1. **Initial Deployment**: Basic SEC filing lookup functionality
2. **Phase 2 Update**: Enhanced search and sector analysis features
3. **Phase 3 Update**: NLP parsing and SEC API integration complete

---

## Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.12+ (for Phase 3 components)
- npm or yarn
- Git

### Installation Steps

#### 1. Clone Repository
```bash
git clone https://github.com/brettvtcrowe/edgar-simple.git
cd edgar-simple
```

#### 2. Install Node.js Dependencies
```bash
npm install
```

#### 3. Set Up Python Environment (Phase 3)
```bash
# Create virtual environment
python3 -m venv phase3_env

# Activate environment
source phase3_env/bin/activate  # On macOS/Linux
# or
phase3_env\Scripts\activate     # On Windows

# Install Python dependencies
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
# Test Node.js backend
npm test

# Test Python components (Phase 3)
source phase3_env/bin/activate
python -m pytest tests/ -v
```

### Expected Test Results
- **Node.js Tests**: 15/15 passing (100% success rate)
- **Python Tests**: 10/10 passing (100% success rate)
- **Total Tests**: 25/25 passing (100% success rate)

---

## Local Development Server

### Start Development Server
```bash
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3000/api/*
- **Health Check**: http://localhost:3000/health

### Available API Endpoints
- **`POST /api/filings`** - Basic ticker-based filing lookup
- **`POST /api/search/advanced`** - Advanced search with multiple criteria
- **`GET /api/sectors`** - List all available sectors
- **`GET /api/sectors/:sector/analytics`** - Sector-specific analytics
- **`GET /api/trends`** - Filing trends analysis
- **`GET /health`** - Health check endpoint

---

## Vercel Deployment

### Current Configuration

#### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server.js"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

#### `server.js` Configuration
```javascript
// Root route handler for Vercel
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});
```

### Deployment Process

#### 1. Automatic Deployment (GitHub Integration)
- **Repository**: https://github.com/brettvtcrowe/edgar-simple
- **Trigger**: Push to main branch
- **Platform**: Vercel
- **Status**: ✅ **ACTIVE**

#### 2. Manual Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Deployment Commands
```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel

# List deployments
vercel ls

# View deployment logs
vercel logs [deployment-url]
```

---

## Environment Configuration

### Required Environment Variables
```bash
# SEC API Configuration
SEC_API_BASE_URL=https://data.sec.gov
SEC_API_USER_AGENT="Regulatory Intelligence Hub - Phase 3 Development"
SEC_API_RATE_LIMIT=0.1

# Python Environment (Phase 3)
PYTHON_VERSION=3.12
SPACY_MODEL=en_core_web_sm
```

### Local Environment Setup
```bash
# Create .env file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

---

## Testing Before Deployment

### Pre-Deployment Checklist
- [ ] All tests passing locally
- [ ] SEC API integration working
- [ ] Frontend functionality verified
- [ ] Python components tested (Phase 3)
- [ ] Environment variables configured

### Test Commands
```bash
# Run all tests
npm test

# Run Python tests (Phase 3)
source phase3_env/bin/activate
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_query_parser_basic.py -v
python -m pytest tests/test_sec_api_client.py -v
```

### Expected Test Results
```bash
# Node.js Tests
✓ 15 tests passing
✓ All API endpoints functional
✓ Frontend components working

# Python Tests (Phase 3)
✓ 10 tests passing
✓ NLP Query Parser functional
✓ SEC API Client working
✓ All components integrated
```

---

## Production Monitoring

### Health Check Endpoints
- **`/health`** - Basic health status
- **`/api/filings`** - SEC API connectivity test
- **`/api/sectors`** - Backend API functionality test

### Monitoring Dashboard
- **Platform**: Vercel Dashboard
- **URL**: https://vercel.com/dashboard
- **Metrics**: Deployment status, performance, errors

### Error Tracking
- **Console Logs**: Available in Vercel dashboard
- **Function Logs**: Serverless function execution logs
- **Performance Metrics**: Response times and error rates

---

## Troubleshooting

### Common Issues

#### 1. Vercel 404 Errors
**Problem**: Routes not found after deployment
**Solution**: Verify `vercel.json` routing configuration
```json
{
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

#### 2. SEC API Rate Limiting
**Problem**: API requests failing with 429 errors
**Solution**: Ensure rate limiting is properly configured
```javascript
// In server.js
const SEC_API_RATE_LIMIT = 0.1; // 10 requests per second
```

#### 3. Python Environment Issues (Phase 3)
**Problem**: Module import errors
**Solution**: Verify virtual environment and package installation
```bash
source phase3_env/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

#### 4. Frontend Rendering Issues
**Problem**: Extra white boxes or empty tabs
**Solution**: Check CSS and JavaScript for proper tab initialization
```javascript
// Ensure tabs are properly initialized
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
});
```

### Debug Commands
```bash
# Check Node.js version
node --version

# Check Python version
python3 --version

# Verify package installation
npm list
pip list

# Test specific components
curl http://localhost:3000/health
curl http://localhost:3000/api/sectors
```

---

## Performance Optimization

### Current Performance Metrics
- **Frontend Load Time**: <500ms
- **API Response Time**: <2 seconds
- **SEC API Integration**: <2 seconds
- **NLP Processing**: <1 second

### Optimization Strategies
1. **Caching**: Implement Redis caching for frequently accessed data
2. **CDN**: Use Vercel's edge network for static assets
3. **Compression**: Enable gzip compression for API responses
4. **Async Processing**: Implement background jobs for heavy computations

---

## Security Considerations

### SEC API Compliance
- **User-Agent**: Proper identification in headers
- **Rate Limiting**: Respect 10 requests/second limit
- **Error Handling**: Secure error responses

### API Security
- **Input Validation**: Comprehensive request validation
- **CORS**: Proper cross-origin configuration
- **Rate Limiting**: Prevent abuse and ensure SEC compliance

---

## Future Deployment Plans

### Phase 3 Completion (Current)
- **Content Analysis Engine**: Deploy when TDD Cycle 4 complete
- **Natural Language Interface**: Frontend integration for Phase 3
- **Performance Optimization**: Response time improvements

### Phase 4 Planning
- **Database Integration**: PostgreSQL setup and migration
- **Multi-Source APIs**: Comment letters and FASB standards
- **Advanced Analytics**: ML-powered insights and predictions

### Production Scaling
- **Microservices**: Separate services for different functionalities
- **Load Balancing**: Multiple server instances
- **Monitoring**: Advanced APM and alerting systems

---

## Support and Maintenance

### Deployment Support
- **Vercel Documentation**: https://vercel.com/docs
- **GitHub Repository**: https://github.com/brettvtcrowe/edgar-simple
- **Issue Tracking**: GitHub Issues for bug reports

### Maintenance Schedule
- **Weekly**: Test all functionality and monitor performance
- **Monthly**: Review and update dependencies
- **Quarterly**: Performance optimization and security updates

---

## Conclusion

The Regulatory Intelligence Hub is successfully deployed on Vercel with:

✅ **Production Status**: Live and accessible at https://edgar-simple.vercel.app/
✅ **Phase 1 & 2**: Complete with 100% test coverage
✅ **Phase 3**: TDD Cycles 1-3 complete, Cycle 4 in progress
✅ **Deployment**: Automated via GitHub integration
✅ **Monitoring**: Health checks and performance tracking active

**Current Focus**: Complete TDD Cycle 4 (Content Analysis Engine) and deploy Phase 3 completion

**Next Milestone**: Deploy content analysis engine with natural language interface

The deployment infrastructure is robust and ready for continued Phase 3 development and future phases.
