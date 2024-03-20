from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fpdf import FPDF
from newspaper import Article, Config
import requests

ARTICLE_ENDPOINT = "https://codechalleng.es/api/articles/"
OUTPUT_DIR = Path("outputs")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def fetch_article_content(url):
    response = requests.get(url, headers=HEADERS)
    return response.text


def save_article_as_pdf(article):
    try:
        article_html = fetch_article_content(article["link"])

        config = Config()
        config.browser_user_agent = "Mozilla/5.0"
        news_article = Article(article["link"], config=config)
        news_article.set_html(article_html)
        news_article.parse()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        title = article["title"].encode("latin-1", "replace").decode("latin-1")
        author = article["author"].encode("latin-1", "replace").decode("latin-1")
        text = news_article.text.encode("latin-1", "replace").decode("latin-1")

        pdf.cell(0, 10, "Title: " + title, ln=True)
        pdf.cell(0, 10, "Author: " + author, ln=True)
        pdf.multi_cell(0, 10, text)

        pdf_filename = (
            OUTPUT_DIR
            / f"{article['title'][:50].replace(' ', '_').replace('/', '_')}.pdf"
        )
        pdf.output(pdf_filename)
        return f"Saved article to {pdf_filename}"

    except Exception as e:
        return f"Failed to process article {article['title']}: {e}"


def main(articles):
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_article = {
            executor.submit(save_article_as_pdf, article): article
            for article in articles
        }

        for future in as_completed(future_to_article):
            article = future_to_article[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"Article generated an exception: {article['title']}: {exc}")

    print("All articles have been processed.")


if __name__ == "__main__":
    articles = requests.get(ARTICLE_ENDPOINT).json()
    main(articles)
