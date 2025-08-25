def get_custom_css():
    """Return custom CSS styles for the dashboard"""
    return """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00D4AA;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .metric-card {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #333333;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
        }
        
        .positive-change {
            color: #00FF88;
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .negative-change {
            color: #FF6B6B;
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .stock-lookup-card {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 2rem;
            border-radius: 1rem;
            border: 1px solid #333333;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            margin: 1rem 0;
        }
        
        .stock-metric {
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #00D4AA;
            margin: 0.5rem 0;
        }
        
        .mover-card {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 1rem;
            border-radius: 0.75rem;
            border: 1px solid #333333;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0.5rem;
        }
        
        .mover-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            border-color: #00D4AA;
        }

        .portfolio-card {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #333333;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
        }
        
        .portfolio-summary {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 1rem;
            border-radius: 0.75rem;
            border: 1px solid #333333;
            margin: 0.5rem 0;
        }
        
        .portfolio-holdings {
            background: rgba(255,255,255,0.02);
            padding: 1rem;
            border-radius: 0.75rem;
            border: 1px solid #444444;
            margin: 1rem 0;
        }
        
        .performance-comparison {
            background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #333333;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #00D4AA 0%, #00B894 100%);
            color: #000000;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,212,170,0.4);
        }
        
        .stTextInput > div > div > input {
            background-color: #2D2D2D;
            border: 1px solid #333333;
            color: #FFFFFF;
            border-radius: 0.5rem;
            padding: 0.75rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #00D4AA;
            box-shadow: 0 0 0 2px rgba(0,212,170,0.2);
        }
    </style>
    """
