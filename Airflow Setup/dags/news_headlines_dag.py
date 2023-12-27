from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os

print(f'current wd = {os.getcwd()}')

news_api = '85194d9ee83f4474b57f0c9718a5a319'
base_url = 'https://newsapi.org/v2/'
country = 'us'
query = 'stock market'
version = '_14'

default_args = {
    'owner': 'news_dag' + version,
    'start_date': datetime(2023, 12, 11),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'news_dag' + version,
    default_args=default_args,
    description='Fetch top news headlines and store in PostgreSQL',
    schedule_interval='@daily',  # adjust as needed
)

def get_news_data(daily):
    url = base_url + daily

    params = {
        'apiKey': news_api,
        'country': country
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def scrape_text_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lines = soup.get_text().splitlines()
        long_lines = [line.strip() for line in lines if len(line.strip()) >= 300]
        result = '\n'.join(long_lines)
        return result
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return None

def gather_news(**kwargs):
    ti = kwargs['ti']
    news_data = get_news_data(daily="top-headlines")['articles']
    news_articles = []

    for news in news_data:
        article_url = news['url']
        article_source = news['source']['name']
        article_author = news['author']
        article_title = news['title']
        article_content = scrape_text_from_url(article_url)
        if all(value is not None and value is not "None" and value is not "" for value in news.values()):
            article = {
                "url": article_url,
                "source": article_source,
                "author": article_author,
                "title": article_title,
                "content": article_content
            }
            news_articles.append(article)

    ti.xcom_push(key='news_articles', value=news_articles)
    print(f'fetched and stored {len(news_data)} articles to news_articles({len(news_articles)})')

def load_news_to_database(**kwargs):
    ti = kwargs['ti']
    news_articles = ti.xcom_pull(task_ids='fetch_news', key='news_articles')

    # Connect to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='news_headlines')

    # Iterate through the news articles and insert into PostgreSQL
    for news in news_articles:
        # Replace single quotes with double quotes in the content
        if news['content'] is not None: news['content'] = news['content'].replace("'", '"')
        if news['title'] is not None: news['title'] = news['title'].replace("'", '"')
        pg_hook.run(
            f"INSERT INTO news_headlines (url, publisher, author, title, article_text) "
            f"VALUES ('{news['url']}', '{news['source']}', '{news['author']}', '{news['title']}', '{news['content']}');"
        )
        print(f'Inserted into DB')
    print(f'Inserted {len(news_articles)} rows into table')

# Define tasks
fetch_news_task = PythonOperator(
    task_id='fetch_news',
    python_callable=gather_news,
    provide_context=True,
    dag=dag,
)

store_in_postgres_task = PythonOperator(
    task_id='store_in_postgres',
    python_callable=load_news_to_database,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_news_task >> store_in_postgres_task
