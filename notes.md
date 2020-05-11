1. Create project
   ```shell script
   scrapy startproject <project_name>
   ```

2. To create new spider use:
   ```shell script
   scrapy genspider <spider_name> <site_url_for_scraping>
   ```
   
3. Run crawlers:
   ```shell script
   scrapy crawl <spider_name> -o <result_name>.json
   ```