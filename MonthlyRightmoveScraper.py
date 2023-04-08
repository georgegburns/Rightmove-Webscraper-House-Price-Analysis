import time

from RightmoveScraper import RightmoveScraper

num = 0
st = time.time()

RightmoveScraper('Isle of Man', 'rent')

ed = time.time()
el =  round(ed - st, 0)

print(f'Completed in {el} seconds')
