from selenium.webdriver                                      import Chrome,Firefox,ChromeOptions,FirefoxOptions
from selenium.webdriver.common.by                            import By
from selenium.webdriver.support.ui                           import WebDriverWait
from selenium.webdriver.support                              import expected_conditions as EC
from selenium.webdriver.common.keys                          import Keys
from scrapy                                                  import Selector
from datetime                                                import datetime,timedelta
import html2text as H2T,pandas,time,os,json


def readJSONfiles(fdir): return {  
	    j.split('.')[0] : json.loads(open(fdir+j).read()) 
	    for j in os.listdir(fdir) 
	    if j.endswith('.json')
	    }
def compute_intervals(start_date,
					  end_date,
					  search_range,**_):
        start_date,end_date,search_range                     = datetime.fromisoformat(start_date),\
        														datetime.fromisoformat(end_date),\
        														int(search_range)
        intervals                                            = []
        interval_start_date                                  = start_date
        while interval_start_date                            < end_date:
                interval_end_date                            = min(interval_start_date + timedelta(days=search_range), end_date)
                intervals.append(
            [interval_start_date.isoformat()[:10], 
            interval_end_date.isoformat()[:10]]
                    )
                interval_start_date                          = interval_end_date
        return intervals
class SearchAuto:
	"""
	This class was designed \
		to collect tweets on twitter using webdrivers
	"""
	def __init__(self,**kwargs):
		self.twitter_explore_url                            = 'https://twitter.com/explore'
		self.BrowserJSON                                    = kwargs['Browser']
		self.CssJSON                                        = kwargs['Css']
		self.SearchJSON                                     = kwargs['Search']
		self.ShakeJSON                                      = kwargs['Shake']
		self.TimeoutJSON                                    = kwargs['Timeout']
		self.output                                         = kwargs['output']
		self.cfd                                            = os.getcwd()
		self.driver_path                                    = os.path.join(self.cfd,'data','drivers')
		self.browsers_objects                               = {
					 'Chrome'                               : [Chrome,ChromeOptions],
					 'Firefox'                              : [Firefox,FirefoxOptions]}
		self.max_height_new                                 = lambda : self.driver.execute_script("return document.body.scrollHeight")
	def safe_css_element_finder(self,css_selector,timeout) :
		ok,element                                          = False,[]
		try:
			element                                         = WebDriverWait(
																self.driver,
																timeout).until(
																EC.presence_of_element_located(
																	(By.CSS_SELECTOR, 
																	 css_selector)))
			ok                                              = True
		except:pass
		return(ok,element)
	def initialize_browser(self):
		browser_name                                        = self.BrowserJSON['browser']
		browser_object                                      = self.browsers_objects[browser_name]
		#setting options          
		options                                             = browser_object[1]()
		if self.BrowserJSON['headless']                     : options.add_argument('--headless')
		if self.BrowserJSON['no_sandbox']                   : options.add_argument('--no-sandbox')
		if self.BrowserJSON['no_images']    and\
			            browser_name == 'Chrome'            : options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
		height,width                                        = self.BrowserJSON["hheight"], self.BrowserJSON["wwidth"]
		options.add_argument("--width=%d"%width)
		options.add_argument("--height=%d"%height)
		driver_name                                         = list(filter(lambda x : browser_name.lower() in x.lower(),os.listdir(self.driver_path)))[0]
		self.driver                                         = browser_object[0](executable_path=os.path.join(self.driver_path,driver_name),options=options)
	def go_to_search_page(self):
		self.driver.get(
		   self.twitter_explore_url)
		ok                                                 = False
		ok,self.search_bar                                 = self.safe_css_element_finder(
																self.CssJSON["search_bar"],
																self.TimeoutJSON["search_bar"])
		return ok
	def post_query(self):
		self.query_syntax                                  = "{query} until:{end_date} since:{start_date}".format(**self.SearchJSON)
		if self.SearchJSON['filters']                      : self.query_syntax += 'filter:%s'%self.SearchJSON['filters']
		self.search_bar.send_keys(self.query_syntax)
		self.search_bar.send_keys(Keys.RETURN)
		if self.SearchJSON['recent']:
			ok,nav_bar_recent                              = self.safe_css_element_finder(
																self.CssJSON["recent"],
																self.TimeoutJSON["recent"])
			if ok:
				nav_bar_recent.click()		
	def collect_articles_and_scroll_to_last(self):
		time.sleep(3)
		self.articles                                       = self.driver.find_elements_by_css_selector(self.CssJSON["article"]["list"])
		self.articles_data_df_dynamic                       = pandas.DataFrame([{ 
							                **{ k           : article.css(v).extract_first() for k,v in self.CssJSON["article"]['user'].items()},
							                **{ k           : article.css(v).extract_first() if k != 'status_text' else H2T.html2text('\n'.join(article.css(v).extract())) for k,v in self.CssJSON["article"]['status_text'].items()},
							                **{ k           : article.css(v).extract_first() for k,v in self.CssJSON["article"]['status_info'].items()},
							                **{ 'raw_html'  : article.getall()[0],
							                    'tags'      : article.css(self.CssJSON["article"]['status_text']['status_text']).re('(@.+)</.*') }}
                    										  for article in map(lambda a: Selector(text=a.get_attribute('outerHTML')),self.articles)])
		self.max_height_old                                 = self.driver.execute_script("return document.body.scrollHeight")
		if len(self.articles)>0:
			last_article                                    = self.articles[-1]
			last_article.\
				location_once_scrolled_into_view
		else:
			self.scrollable                                 = False
	def save_df(self,df):
		storage_path                                        = os.path.join(self.output,'start_date={start_date}','end_date={end_date}').format(**self.SearchJSON)
		#print(storage_path)
		os.makedirs(storage_path,exist_ok                   = True)
		df.to_csv(os.path.join(storage_path,'data.zip'),
				                             sep            = ';',
				                           index            = None,
				                     compression            = dict(method='zip',archive_name='data.csv') )
	def shake_browser(self):
		for i in range(
	self.ShakeJSON['iterations'][self.shaken]['n_shake']+1):
			self.driver.execute_script(
			"window.scrollTo(0,0);") #UP
			time.sleep(3)
			self.driver.execute_script(
			"window.scrollTo(0,document.body.\
							 scrollHeight);")#DOWN
			time.sleep(3)
		time.sleep(
	self.ShakeJSON['iterations'][self.shaken]['sleep'])
		self.shaken += 1

	def scroll(self):
		 scrollable                                         = True #we assume new data is available
		 browser_shake_params                               = self.ShakeJSON['iterations']
		 #first launch
		 self.initialize_browser()
		 ok                                                 = self.go_to_search_page()
		 if ok:
			 self.post_query()
			 self.collect_articles_and_scroll_to_last()
			 articles_data_df_persistent                    = self.articles_data_df_dynamic.copy()
			 self.save_df(                   df             = self.articles_data_df_dynamic)
			 #then loop
			 while scrollable:
			 	self.collect_articles_and_scroll_to_last()
			 	articles_data_df_persistent                 = pandas.concat([
			 												  articles_data_df_persistent,
			 												  self.articles_data_df_dynamic]).drop_duplicates('status_url')
			 	self.save_df(
			 										df      = articles_data_df_persistent)
			 	if self.max_height_new() == \
			 							self.max_height_old :
			 		self.shaken = 0
			 		self.shake_browser()
			 		if self.max_height_new() \
			 						== self.max_height_old  :
			 			self.shake_browser()
			 			if self.max_height_new()   ==\
			 				          self.max_height_old   : scrollable = False; #no more available data, we hope!
		 #finally 
		 self.driver.close()