class Config:
    # Visualization
    MAX_PREVIEW_ROWS = 5
    MAX_CATEGORIES = 10
    PLOT_THEME = "plotly_white"
    
    # Data Analysis
    SUPPORTED_FILE_TYPES = [".csv", ".xlsx"]
    NUMERIC_LIMIT = 5  # Max numeric cols for auto-analysis
    
    # Groq API
    GROQ_MODEL = "deepseek-r1-distill-llama-70b"
    MAX_TOKENS = 4096
    TEMPERATURE = 0.3