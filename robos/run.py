from scrapy.cmdline import execute
try:
    execute(
        [
            'scrapy',
            'crawl',
            'nacional_super',
            #'-o',
            #'out.json',
        ]
    )
except SystemExit:
    pass
