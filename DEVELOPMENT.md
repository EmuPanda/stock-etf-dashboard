# 🛠️ Development Guide

This guide helps developers contribute to and extend the Stock/ETF Dashboard.

## 🚀 **Getting Started**

### **Prerequisites**
- **Python 3.9+**
- **Git**
- **VS Code** (recommended) or your preferred IDE
- **Supabase account** (for portfolio storage)

### **Local Setup**
```bash
# Clone repository
git clone <your-repo-url>
cd stock-etf-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env

# Run the dashboard
cd app
python3 -m streamlit run main.py --server.port=8501
```

## 🏗️ **Project Architecture**

### **Core Structure**
```
app/
├── main.py              # 🚀 Application entry point
├── pages/               # 📱 Individual dashboard pages
│   ├── dashboard.py     # Main dashboard view
│   ├── stock_browser.py # Stock screening
│   ├── portfolio.py     # Portfolio simulation
│   └── market_analysis.py # Market insights
├── components/          # 🔧 Reusable UI components
├── utils/               # ✨ Utilities & styling
│   └── styles.py        # Custom CSS
└── requirements.txt     # 📦 Dependencies
```

### **Service Layer**
```
├── data_service.py      # 📊 Stock data & API management
├── portfolio_service.py # 💼 Portfolio calculations
└── config.py            # ⚙️ Configuration management
```

## 🔧 **Development Workflow**

### **1. Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Test locally
python3 -m streamlit run app/main.py --server.port=8501

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature
```

### **2. Bug Fixes**
```bash
# Create bugfix branch
git checkout -b fix/bug-description

# Fix the issue
# Test thoroughly
# Commit with conventional commit message
git commit -m "fix: resolve issue with stock data loading"
```

### **3. Code Review Process**
1. **Create Pull Request** with clear description
2. **Self-review** your code before requesting review
3. **Address feedback** from reviewers
4. **Merge** after approval

## 📝 **Coding Standards**

### **Python Style Guide**
- **PEP 8** compliance
- **Type hints** for function parameters and returns
- **Docstrings** for all functions and classes
- **Maximum line length**: 88 characters (Black formatter)

### **Example Function**
```python
def calculate_portfolio_metrics(portfolio: List[Dict]) -> Dict[str, float]:
    """
    Calculate portfolio risk and return metrics.
    
    Args:
        portfolio: List of portfolio holdings with ticker and value
        
    Returns:
        Dictionary containing risk metrics (volatility, sharpe_ratio, etc.)
        
    Raises:
        ValueError: If portfolio is empty or invalid
    """
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")
    
    # Implementation here
    return metrics
```

### **Streamlit Best Practices**
- **Use columns** for responsive layouts
- **Implement caching** for expensive operations
- **Handle errors gracefully** with try-catch blocks
- **Use session state** for persistent data

### **CSS/Styling Guidelines**
- **Consistent color scheme** (#00D4AA primary)
- **Responsive design** for mobile and desktop
- **Accessibility** considerations (contrast, font sizes)
- **Component-based styling** in `app/utils/styles.py`

## 🧪 **Testing**

### **Running Tests**
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov=app

# Run specific test file
pytest tests/test_data_service.py -v
```

### **Test Structure**
```
tests/
├── test_data_service.py
├── test_portfolio_service.py
├── test_pages/
│   ├── test_dashboard.py
│   └── test_portfolio.py
└── conftest.py
```

### **Writing Tests**
```python
import pytest
from app.data_service import StockDataService

def test_get_stock_data_success():
    """Test successful stock data retrieval."""
    service = StockDataService()
    data = service.get_stock_data("AAPL")
    
    assert data is not None
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "current_price" in data
    assert data["current_price"] > 0

def test_get_stock_data_invalid_ticker():
    """Test handling of invalid ticker symbols."""
    service = StockDataService()
    
    with pytest.raises(ValueError):
        service.get_stock_data("INVALID_TICKER")
```

## 📊 **Data Management**

### **Adding New Data Sources**
1. **Create new service class** in `app/services/`
2. **Implement interface** methods
3. **Add fallback logic** in main data service
4. **Update configuration** for API keys

### **Example: Adding Alpha Vantage**
```python
class AlphaVantageService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_stock_data(self, ticker: str) -> Dict:
        """Fetch stock data from Alpha Vantage."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        return self._parse_response(response.json())
```

### **Caching Strategy**
- **TTL-based caching** for stock data (5 minutes)
- **Size-based cache eviction** (max 1000 entries)
- **Cache warming** for frequently accessed data
- **Cache invalidation** on data updates

## 🎨 **UI/UX Development**

### **Adding New Pages**
1. **Create page file** in `app/pages/`
2. **Import in main.py** and add to navigation
3. **Follow existing patterns** for consistency
4. **Add to documentation**

### **Example New Page**
```python
import streamlit as st
from utils.styles import get_custom_css

def show_new_page():
    """New page functionality."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    st.header("🆕 New Feature")
    
    # Page content here
    st.write("This is a new page!")
```

### **Adding New Components**
1. **Create component file** in `app/components/`
2. **Design reusable interface**
3. **Add proper error handling**
4. **Include documentation and examples**

## 🔒 **Security Development**

### **Input Validation**
```python
def validate_ticker(ticker: str) -> str:
    """Validate and sanitize ticker symbol."""
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    # Remove any dangerous characters
    clean_ticker = re.sub(r'[^A-Za-z.]', '', ticker.upper())
    
    if len(clean_ticker) > 10:
        raise ValueError("Ticker too long")
    
    return clean_ticker
```

### **API Rate Limiting**
```python
import time
from functools import wraps

def rate_limit(calls: int, period: int):
    """Rate limiting decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            # Implementation here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 📈 **Performance Optimization**

### **Caching Best Practices**
```python
@st.cache_data(ttl=300)  # 5 minutes
def get_market_overview():
    """Cache market overview data."""
    return data_service.get_market_overview()

@st.cache_resource
def get_data_service():
    """Cache service instance."""
    return StockDataService()
```

### **Data Processing**
- **Use pandas efficiently** (vectorized operations)
- **Implement lazy loading** for large datasets
- **Optimize database queries** with proper indexing
- **Use async operations** where appropriate

## 🐛 **Debugging**

### **Streamlit Debug Mode**
```bash
# Run with debug logging
streamlit run app/main.py --logger.level=debug

# Check browser console for errors
# Use st.write() for temporary debugging
```

### **Common Issues**
1. **Import errors**: Check file paths and `__init__.py` files
2. **Environment variables**: Verify `.env` file and variable names
3. **API limits**: Check rate limiting and error handling
4. **Memory issues**: Monitor cache sizes and data processing

### **Debugging Tools**
```python
# Temporary debugging
st.write("Debug info:", variable)

# Check data types
st.write("Type:", type(data))

# Inspect objects
st.json(data)
```

## 📚 **Documentation**

### **Code Documentation**
- **Docstrings** for all functions and classes
- **Type hints** for better IDE support
- **Inline comments** for complex logic
- **README updates** for new features

### **API Documentation**
- **Function signatures** with examples
- **Parameter descriptions** and types
- **Return value explanations**
- **Error handling documentation**

## 🚀 **Deployment Preparation**

### **Pre-deployment Checklist**
- [ ] **All tests pass**
- [ ] **Environment variables** configured
- [ ] **Dependencies** updated in requirements.txt
- [ ] **Documentation** updated
- [ ] **Security review** completed
- [ ] **Performance testing** done

### **Version Management**
```bash
# Update version in README.md
# Tag release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# Create release notes
# Update CHANGELOG.md
```

## 🤝 **Contributing Guidelines**

### **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Local testing completed
- [ ] Unit tests added/updated
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### **Code Review Checklist**
- [ ] **Functionality** works as expected
- [ ] **Code quality** meets standards
- [ ] **Security** considerations addressed
- [ ] **Performance** impact evaluated
- [ ] **Documentation** updated
- [ ] **Tests** added/updated

---

**Happy Coding! 🚀**
