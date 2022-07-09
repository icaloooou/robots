from scrapy.cmdline import execute
try:
    execute(
        [
            'scrapy',
            'crawl',
            'yamaha',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass
