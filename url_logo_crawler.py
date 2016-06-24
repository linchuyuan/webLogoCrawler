import requests;
import time;
import csv

crawl_target=["http://www.dnvod.eu/","https://www.airbnb.com/","https://gopro.com/","https://twitter.com/","https://intl.alipay.com/","https://www.periscope.tv/","http://www.yahoo.com","https://www.google.com","http://mixrank.com"];

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
	r = requests.get(url);
	html = r.text;
	return html;
def get_url_logo(url):
	try:
		icon_link_indicator = False;
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
		test_logo = strstr(logo,"http");
		if test_logo == "":
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

stack = [];
with open("logo_url.csv","w+") as fp:
	file = csv.writer(fp,delimiter = ',');
	file.writerows([["website","Hyperlink","URL in raw"]]);
	for i in crawl_target:
		try:
			logo_url = get_url_logo(i);
		except:
			logo_url = "NULL";
		stack.append([i,"=HYPERLINK(\"%s\")" %(logo_url),logo_url]);
	file.writerows(stack);











	

