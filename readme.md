## To run the crawler you need:
1. Create virtual environment
    ```bash
    # via pyenv - https://github.com/pyenv/pyenv#installation
    pyenv virtualenv 3.8.0 scrapy_tut
    pyenv activate scrapy_tut
    # or via venv
    python -m venv venv
    source ./venv/bin/activate
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Setup splash-server
    ```bash
    docker pull scrapinghub/splash
    docker run -p 8050:8050 scrapinghub/splash
    ```

4. Run crawler
    ```bash
    scrapy crawl tweets -o tweets.json
    ```