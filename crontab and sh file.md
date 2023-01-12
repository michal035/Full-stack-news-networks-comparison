
.sh file

```
#!/bin/bash
cd  //path/crawling
scrapy crawl stvp
scrapy crawl stvn-e
cd data
python  proccesing\ data
python adding\ data\ to\ db.py
```

cronatab

```
50 23 * * * /home/user/scripts/job.sh
```
