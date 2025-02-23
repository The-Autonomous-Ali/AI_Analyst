from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from config import Config

class GroqAnalyst:
    def __init__(self):
        self.cfg = Config()
        self.llm = ChatGroq(
            model_name=self.cfg.GROQ_MODEL,
            temperature=self.cfg.TEMPERATURE,
            max_tokens=self.cfg.MAX_TOKENS,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_insights(self, analysis_report, user_query):
        """Generate textual insights from data analysis"""
        template = """
        Dataset Analysis Report:
        {report}

        User Question: {query}

        Generate detailed insights with:
        - Key statistical findings
        - Important patterns/trends
        - Business implications
        - Recommendations

        Use markdown formatting with headings and bullet points.
        """

        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        
        return chain.invoke({
            "report": analysis_report,
            "query": user_query
        }).content