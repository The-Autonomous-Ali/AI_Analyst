import pandas as pd
import logging
import plotly.express as px
from io import BytesIO
from config import Config

class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.logger = logging.getLogger(__name__)
        self.cfg = Config()

    def load_data(self):
        """Load and validate data"""
        try:
            if self.file_path.name.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            else:
                self.df = pd.read_excel(self.file_path)
            self.logger.info(f"Loaded {len(self.df)} rows")
            return True
        except Exception as e:
            self.logger.error(f"Load failed: {str(e)}")
            return False

    def analyze_dataset(self):
        """Generate complete analysis report"""
        return {
            "stats": self._get_statistical_summary(),
            "visualizations": self.generate_visualizations(),
            "data_sample": self.df.head(self.cfg.MAX_PREVIEW_ROWS).to_dict()
        }

    def _get_statistical_summary(self):
        """Generate numerical summary"""
        return {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "description": self.df.describe().to_dict(),
            "missing_values": self.df.isna().sum().to_dict()
        }

    def generate_visualizations(self):
        """Automatically generate key visualizations"""
        viz = {}
        
        try:
            # Numeric Features
            numeric_cols = self._get_numeric_columns()
            if numeric_cols:
                viz.update(self._numeric_analysis(numeric_cols))

            # Categorical Features
            categorical_cols = self._get_categorical_columns()
            if categorical_cols:
                viz.update(self._categorical_analysis(categorical_cols))

            # Time Series
            datetime_cols = self._get_datetime_columns()
            if datetime_cols:
                viz.update(self._time_analysis(datetime_cols))

        except Exception as e:
            self.logger.error(f"Visualization error: {str(e)}")
            
        return viz

    def _get_numeric_columns(self):
        return self.df.select_dtypes(include='number').columns.tolist()

    def _get_categorical_columns(self):
        return self.df.select_dtypes(include=['object', 'category']).columns.tolist()

    def _get_datetime_columns(self):
        return self.df.select_dtypes(include='datetime').columns.tolist()

    def _numeric_analysis(self, cols):
        """Handle numeric column visualizations"""
        analysis = {}
        cols = cols[:self.cfg.NUMERIC_LIMIT]  # Limit number of cols
        
        # Distribution Plots
        analysis['distributions'] = [
            px.histogram(self.df, x=col, title=f'Distribution of {col}')
            for col in cols
        ]

        # Correlation Matrix
        if len(cols) > 1:
            analysis['correlation'] = px.imshow(
                self.df[cols].corr(),
                title="Feature Correlation Matrix"
            )

        # Pair Plot
        if len(cols) > 2:
            analysis['pair_plot'] = px.scatter_matrix(
                self.df[cols[:3]],
                title="Numerical Relationships"
            )

        return analysis

    def _categorical_analysis(self, cols):
        """Handle categorical data visualizations"""
        analysis = {}
        cols = cols[:self.cfg.MAX_CATEGORIES]
        
        # Modified bar chart code
        analysis['category_dist'] = [
            px.bar(
                self.df[col].value_counts().reset_index(name='count'), 
                x=col, 
                y='count',
                title=f'Distribution of {col}'
            )
            for col in cols
        ]
        
        # Rest of the code remains same
        analysis['pie_charts'] = [
            px.pie(self.df, names=col, title=f'Proportion of {col}')
            for col in cols[:3]
        ]

        return analysis

    def _time_analysis(self, cols):
        """Generate time series visualizations"""
        analysis = {}
        primary_date_col = cols[0]
        numeric_cols = self._get_numeric_columns()
        
        if numeric_cols:
            # Time Series Line Plot
            analysis['time_series'] = px.line(
                self.df, 
                x=primary_date_col, 
                y=numeric_cols[0],
                title=f"{numeric_cols[0]} Over Time"
            )

            # Seasonal Decomposition
            if len(self.df) > 100:  # Only for sufficient data
                analysis['seasonality'] = px.scatter(
                    self.df.set_index(primary_date_col).resample('M').mean(),
                    title="Monthly Trends"
                )

        return analysis

    def plot_custom(self, plot_type, **kwargs):
        """Handle user-requested visualizations"""
        plot_func = {
            'scatter': px.scatter,
            'line': px.line,
            'bar': px.bar,
            'histogram': px.histogram,
            'box': px.box,
            'violin': px.violin,
            'heatmap': px.density_heatmap,
            '3d': px.scatter_3d
        }.get(plot_type.lower())

        if not plot_func:
            raise ValueError(f"Unsupported plot type: {plot_type}")

        return plot_func(self.df, **kwargs)