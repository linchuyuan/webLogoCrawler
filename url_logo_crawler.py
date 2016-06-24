import requests;
import threading;
import csv
import time
import argparse

crawl_target=[]
report_stack = [];

#crawl_target=[];
#f = open("top.csv",'r');
#reader = csv.reader(f,delimiter=',');
#for row in reader:
#	temp = row;
#	crawl_target.append("https://www.%s"%(temp[1]));
	#crawl_target.append("http://www.%s"%(temp[1]));

def crawl_mixrank(size):
	#only work n mixrank.com/web/sites
	return_me = [];
	stepping = 250
	i = 0;
	while i < size:	
		k = 0
		html = requests.get("https://mixrank.com/web/sites?page_size=%s&offset=%s" %(size,i));
		html = html.text;
		while k < stepping:
			k = k + 1;
			html = strstr(html[1:],"list-result-link");
			url = recorder(html,">","<");
			crawl_target.append("https://www.%s/"%(url));
		i = i + stepping;
	print crawl_target;
def recorder(html,starter,stopper):
	flag = False;
	return_me = ""
	for i in html:
		if flag:
                        return_me = return_me + i;
		if i == starter and flag == False:
			flag = True;
		if i == stopper and flag == True:
			flag = False;
			return return_me[:-1];
	return return_me[:-1];
			

def str_replace(string,target,replace,reset=None,reset_count=1):
        string = string + target;
        temp = '';
        temp_count = 0;
        count = 0;
        for i in range(len(string)):
                if string[i:i+len(target)] == target and count < reset_count:
                        temp = temp + string[temp_count:i] + replace;
                        temp_count = i+len(target);
                        if not reset:
                                pass;
                        else:
                                count = count + 1;
                elif string[i:i+len(target)] == target:
                        count = 0;
        string = temp[:len(temp)-len(replace)];
        return string;

def strstr(base,target):
	m = len(base);
	n = len(target);
	if n > m:
		return "";
	i = 0;
	k = 0;
	while i < m - n + 1:
		k = 0;
		while k < n:
			if target[k] != base[i+k]:
				break;
			k = k + 1;
			if k == n:
				return base[i:];
		i = i + 1;
	return "";
def get(url):
	try:
		r = requests.get(url,timeout=5);
	except:
		return "None";
	html = r.text;
	html = html.lower();
	return html;
def get_url_logo(url):
	try:
		icon_link_indicator = False;
		html = get(url);
		if html == "None":
			url = str_replace(url,"https","http")
			html = get(url);
		while not icon_link_indicator:
        		html = strstr(html[1:],"<link");
        		i = 0;
        		while i < 99:
                		temp = html[:i];
				if "shortcut icon" in temp:
                	        	icon_link_indicator = True;
                        		break;
                		if html[i] == ">":
                        		break;
                		i = i + 1;
		html = strstr(html,"href=");
		logo = get_logo(html);
		if not (".com" in logo or ".net" in logo or ".org" in logo or ".edu" in logo):
			return url + logo;
		else:
			return logo;
	except:
		icon_link_indicator = False;
                html = get(url);
                while not icon_link_indicator:
                        html = strstr(html[1:],"<link");
                        i = 0;
                        while i < 99:
                                temp = html[:i];
                                if "image/x-icon" in temp:
                                        icon_link_indicator = True;
                                        break;
                                if html[i] == ">":
                                        break;
                                i = i + 1;
                html = strstr(html,"href=");
                logo = get_logo(html);
                test_logo = strstr(logo,"http");
                if test_logo == "":
                        return url + logo;
                else:
                        return logo;
def get_logo(html):
	start = False;
	return_me = "";
	for i in html:
		if i == "\"" and start == False:
			start = True;
		elif i =="\"" and start == True:
			return return_me[1:];
		if start:
			return_me = return_me + i;
	return return_me;
class worker(threading.Thread):
	global crawl_target;
	global report_stack;
	def __init__(self,ID):
		threading.Thread.__init__(self);
		self.worker_ID = ID;
		self._stop = threading.Event()
	def run(self):
		try:
                        i = crawl_target.pop();
                except:
                        i = None;
                while i:
			print "working on %s" %i;
                        try:
                                logo_url = get_url_logo(i);
                        except:
                                logo_url = i + "favicon.ico" ;
                        report_stack.append([i,"=HYPERLINK(\"%s\")" %(logo_url),logo_url]);
			try:
                                i = crawl_target.pop();
                        except:
                                i = None;
		return 0;
    	def stop(self):
        	self._stop.set()

	def stopped(self):
        	return self._stop.isSet()
def parse_cmdline_args():
        parser = argparse.ArgumentParser(description='super web crawler');
        parser.add_argument('--length', dest='size',default=None, help='How long does the list need to be');
	parser.add_argument('--worker', dest='worker_count',default=None, help='Total number of worker for crawl');
        args = parser.parse_args();
        return args;	

def main():
	together_conquer = [];
	worker_count = int(args.worker_count);
	size = int(args.size);
	crawl_mixrank(size);
	with open("logo_url.csv","w+") as fp:
		file = csv.writer(fp,delimiter = ',');
		file.writerows([["website","Hyperlink","URL in raw"]]);
		for i in range(worker_count):
			together_conquer.append(worker(i));
			together_conquer[i].start();
			time.sleep(0.5);
		while crawl_target:
			time.sleep(5);
		for i in range(worker_count):
			together_conquer[i].stop();
		time.sleep(30);
		file.writerows(report_stack);



if __name__ == '__main__':
	args = parse_cmdline_args();
	main();







	

