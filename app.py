import streamlit as st
import logging
from data_analyzer import DataAnalyzer
from llm_client import GroqAnalyst
from config import Config
from dotenv import load_dotenv

# Initialize
load_dotenv()
logging.basicConfig(level=logging.INFO)
cfg = Config()

# Streamlit App
def main():
    st.title("AI Data Analyst")
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Upload Your Data File", 
        type=cfg.SUPPORTED_FILE_TYPES
    )
    
    if uploaded_file:
        # Reset analysis if new file is uploaded
        if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file.name:
            st.session_state.uploaded_file = uploaded_file.name
            if 'analysis' in st.session_state:
                del st.session_state['analysis']
        
        analyzer = DataAnalyzer(uploaded_file)
        if analyzer.load_data():
            st.success("Data loaded successfully!")
            
            # Analysis Trigger Section
            st.header("Data Analysis Actions")
            
            # Basic Analysis Trigger
            if st.button("Run Basic Analysis"):
                with st.spinner("Analyzing dataset..."):
                    st.session_state.analysis = analyzer.analyze_dataset()
                st.success("Basic analysis completed!")
            
            # Show analysis results only if available
            if 'analysis' in st.session_state:
                # Visualization Section
                st.header("Automated Visualizations")
                _display_visualizations(st.session_state.analysis['visualizations'])

            # User Query Section
            st.header("Ask Questions")
            user_query = st.text_area("Enter your analysis question:")
            
            if st.button("Generate Insights"):
                if 'analysis' not in st.session_state:
                    st.info("Running Basic Analysis first...")
                    with st.spinner("Analyzing dataset..."):
                        st.session_state.analysis = analyzer.analyze_dataset()
                        st.success("Basic analysis completed!")
                
                try:
                    groq_client = GroqAnalyst()
                    insights = groq_client.generate_insights(
                        st.session_state.analysis['stats'], 
                        user_query
                    )
                    st.markdown(insights)
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

            # Custom Visualization
            st.header("Custom Visualization")
            _custom_viz_interface(analyzer)

def _display_visualizations(viz_dict):
    """Display automated visualizations"""
    for viz_type, visuals in viz_dict.items():
        st.subheader(viz_type.replace('_', ' ').title())
        
        if isinstance(visuals, list):
            cols = st.columns(2)
            for idx, fig in enumerate(visuals):
                cols[idx % 2].plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(visuals, use_container_width=True)

def _custom_viz_interface(analyzer):
    """Handle custom visualization requests"""
    col1, col2 = st.columns(2)
    
    with col1:
        plot_type = st.selectbox(
            "Select Visualization Type",
            ["scatter", "line", "bar", "histogram", "box", "heatmap", "3d"]
        )
        
        x_axis = st.selectbox("X-Axis", analyzer.df.columns)
        y_axis = st.selectbox("Y-Axis", analyzer.df.columns) if plot_type not in ['histogram', 'box'] else None
        color = st.selectbox("Color By", [None] + analyzer.df.columns.tolist())

    with col2:
        try:
            fig = analyzer.plot_custom(
                plot_type,
                x=x_axis,
                y=y_axis,
                color=color,
                title=f"{plot_type.title()} Plot of {x_axis}" + 
                      (f" vs {y_axis}" if y_axis else "")
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Couldn't create visualization: {str(e)}")

if __name__ == "__main__":
    main()