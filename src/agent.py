from typing import List, Dict
from openai import OpenAI
from .scraper import FinancialNewsScraper
import pdfkit
from datetime import datetime
import os

class FinancialNewsAgent:
    def __init__(self, api_key: str = None):
        self.scraper = FinancialNewsScraper()
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.analyze_prompt = """
        You are a financial analyst AI trained to analyze financial news articles.
        Your mission is to process the latest headlines and summaries from the US, Japan, and Korea, then produce a concise, expert-level report in Korean that covers:

        Inputs (to be filled in via Python scraping):
        - US Articles and Summaries: {}
        - Japan Articles and Summaries: {}
        - Korean Articles and Summaries: {}

        Report Structure (output entirely in Korean):

        1. **미국 시장 분석**
        - 해당 뉴스의 주요 금융 시사점
        - 시장에 미치는 잠재적 영향
        - 투자 기회 및 관련 금융 지표
        - 위험 요소

        2. **일본 시장 분석**
        - 해당 뉴스의 주요 금융 시사점
        - 시장에 미치는 잠재적 영향
        - 투자 기회 및 관련 금융 지표
        - 위험 요소

        3. **한국 시장 분석**
        - 해당 뉴스의 주요 금융 시사점
        - 시장에 미치는 잠재적 영향
        - 투자 기회 및 관련 금융 지표
        - 위험 요소

        4. **KOSPI 당일 움직임 예측**
        - 상기 3개국 분석을 종합한 KOSPI 지수의 예상 방향 및 근거

        Writing Guidelines:
        - Summarize each country's analysis in a single paragraph.
        - Provide the KOSPI movement prediction in one clear paragraph.
        - Maintain the tone of a professional financial analyst.
        - Structure the report cleanly so an HTML designer can format it into a formal document.
        """
        self.html_prompt = """
        You are an HTML designer AI at Yonsei Financial Group. Every morning at 08:30.
        Your task is to output a complete, valid HTML5 document in Korean (without any comments), following these guidelines:

        Input:
        - Today's Date: {}
        - Financial Analysis Content: {}

        - The document must begin with `<!DOCTYPE html>` and include `<html lang="ko">`, `<head>`, and `<body>` tags.
        - In `<head>`, include:
        - `<meta charset="UTF-8">`
        - A viewport meta tag
        - A `<title>` set to “연세금융그룹 KOSPI 데일리 리포트 - (date placeholder)`.
        - Include a `<style>` block that:
        - Sets the font-family to a Korean-compatible font such as `'Nanum Gothic', 'Noto Sans KR', sans-serif`.
        - Resets margins and padding.
        - Styles the header and footer with a subtle background.
        - Inside `<body>`:
        1. A `<header>` containing:
            - An `<h1>` with “연세금융그룹 데일리 리포트 - (date placeholder)`.
            - A `<p>` reading “발행 시간: 08:30”.
        2. A `<main>` element wrapping a `<section>` where you insert the financial analysis content.
        3. A `<footer>` that reads “© Yonsei Financial Group. All rights reserved.”.
        - Do not include any HTML comments or additional explanatory text—output only the final HTML document ready for rendering.
        """

    def analyze_financial_news(self) -> tuple[str, int, int]:
        """Analyzes financial news articles from the US, Japan, and Korea using the OpenAI API."""
        us_articles = self.scraper.scrape_us_articles()
        japan_articles = self.scraper.scrape_jp_articles()
        korea_articles = self.scraper.scrape_kr_articles()
        prompt = self.analyze_prompt.format(us_articles, japan_articles, korea_articles)
        response = self.client.responses.create(
            model=self.model,
            input = [
                {
                    "role": "developer",
                    "content": prompt
                }
            ],
        )
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens
        return response.output_text, self.total_input_tokens, self.total_output_tokens

    def generate_html_report(self, analysis_content: str) -> tuple[str, int, int]:
        """Generates an HTML report from the financial analysis, renders it to PDF, and saves it to the assets directory."""
        today_date = datetime.now().strftime("%Y-%m-%d")
        prompt = self.html_prompt.format(today_date, analysis_content)
        response = self.client.responses.create(
            model=self.model,
            input = [
                {
                    "role": "developer",
                    "content": prompt
                }
            ],
        )
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        report_name = f"yonsei_financial_report_{today_date}.pdf"
        report_path = os.path.join("assets", report_name)

        pdfkit.from_string(response.output_text, report_path)

        return "Report Generation Complete", self.total_input_tokens, self.total_output_tokens

