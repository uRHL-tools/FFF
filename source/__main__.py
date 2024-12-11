from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path
from tqdm import tqdm

import utils as ut
import argparse
import re

class Puppet:
	def __init__(self, headless: bool = False):
		if headless:
			opts = webdriver.FirefoxOptions()
			opts.add_argument('--headless')
		else:
			opts = None
		self._driver = webdriver.Firefox(options=opts)
	
	
	def find_font_families(self, *args, path: str | Path = None, cache: bool = True) -> dict | None:
		targets = set()
		if path:
			if Path(path).exists():
				with open(path, 'r') as file:
					for ln in file.readlines():
						if re.match(r'^http(s)://', ln):
							targets.add(ln.strip())
			else:
				print(f"[!] Input file not found ({path})")
				return None
		elif len(args) > 0:
			targets = args
		else:
			print("[!] Bad usage. Either URLs list or input file must be specified")
			return None
		db = ut.load_db()
		all_ff = dict()
		
		# return {url: self._get_font_families(url) for url in tqdm(targets)}
		print(f"[*] Starting analysis (cache {'enabled' if cache else 'disabled'})...")
		for url in tqdm(targets):
			if cache and url in db:
				tqdm.write(f"[+] Cached resource {url}")
				all_ff[url] = db[url]
			else:
				all_ff[url] = self._analyze_url(url)
		print(f"[+] Analysis completed")
		return all_ff
	
	def _analyze_url(self, url) -> dict:
		tqdm.write(f"[*] Analyzing {url}")
		page_ff = {'__all__': set()}
		try:
			self._driver.get(url)
		except Exception as e:
			tqdm.write(f"{type(e)} {e}")
			tqdm.write(f"[!] Error retrieving resource {url}")
		else:
			for elem in ut.on_load_all(self._driver, by=By.CSS_SELECTOR, value='*', timeout=5):
				try:
					if elem.tag_name in page_ff:
						page_ff[elem.tag_name].add(elem.value_of_css_property('font-family'))
						page_ff['__all__'].add(elem.value_of_css_property('font-family'))
					else:
						page_ff[elem.tag_name] = {elem.value_of_css_property('font-family')}
						page_ff['__all__'].add(elem.value_of_css_property('font-family'))
				except ut.ignored_exceptions:
					continue
			return page_ff
	
	def close(self):
		self._driver.close()



def _parse_args():
	parser = argparse.ArgumentParser(
		prog=__file__,
		description='Font-Family-Finder gets and categorize all different font-families used in web pages'
	)
	parser.add_argument(
		'--no-cache',
		action='store_true',
		default=False,
		help='Disables caches, forcing all target URLs to be requested again'
	)
	parser.add_argument(
		'-u', '--urls',
		# required=False,
		metavar='URLs',
		nargs='+',
		help='Targeted URL, sepparated by blanks'
	)
	parser.add_argument(
		'-f', '--file',
		type=Path,
		# default=DEF_INPUT_FILE,
		default=None,
		help='Read target URLs from file instead of CLI arguments.'
	)
	_args = parser.parse_args()
	if _args.file is None and _args.urls is None:
		print(f"[!] Bad usage. Either URL list or input file must be specified")
		parser.print_usage()
		exit(1)
	return _args

if __name__ == '__main__':
	ARGS = _parse_args()
	ut.print_banner()
	# print("[#] CLI", ARGS)
	p = Puppet(headless=True)
	ut.save_db(p.find_font_families(ARGS.urls, path=ARGS.file, cache=not ARGS.no_cache))
	p.close()
	
