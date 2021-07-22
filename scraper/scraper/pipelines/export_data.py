import pathlib
import os
import csv
from datetime import datetime

class ExportDataPipeline:
    def open_spider(self, spider):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.current_data_dir = f'data/{dt_string}'
        pathlib.Path(f'{self.current_data_dir}').mkdir(parents=True, exist_ok=True)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['type'] == 'post':
            pathlib.Path(f'{self.current_data_dir}/{item["id"]}')\
            .mkdir(parents=True, exist_ok=True)

            headers = ['content', 'author_name', 'author_url', 'id', 'type']
            with open(f'{self.current_data_dir}/{item["id"]}/post.csv', 'a', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerow({
                    'content': item['content'], 
                    'author_name': item['author_name'], 
                    'author_url': item['author_url'], 
                    'id': item['id'],
                })
        elif item['type'] == 'comment':
            pathlib.Path(f'{self.current_data_dir}/{item["post_id"]}')\
            .mkdir(parents=True, exist_ok=True)
            fieldnames = ['id', 'content', 'email', 'author_name', 'author_url']
            fname = f'{self.current_data_dir}/{item["post_id"]}/comment.csv'
            has_file = os.path.isfile(fname) 

            with open(fname, 'a', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not has_file:
                    writer.writeheader()
                
                writer.writerow({
                    'id': item['id'],
                    'author_name': item['author_name'], 
                    'author_url': item['author_url'],
                    'content': item['content'], 
                    'email': item['email']
                })
            
        return item