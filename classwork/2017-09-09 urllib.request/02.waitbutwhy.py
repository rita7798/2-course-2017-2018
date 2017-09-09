import re
import urllib.request


def getting_code():
    request = urllib.request.Request('https://waitbutwhy.com')
    with urllib.request.urlopen(request) as response:
       code = response.read().decode('utf-8')
    return code

def extracting_names(code):
    regName = re.compile('<h5>\s*.*\s*(\w.*)\s*</a>\s?')
    name = regName.findall(code)
    regN = re.compile('<i class=\"icon-comments\"></i>\s*(.*)</a>\s*&nbsp;&nbsp;&nbsp;')
    n = regN.findall(code)
    j = -1
    for i in range (len(name)):
        if len(name[i]) > 7:
            for l in range (len(n)):
                j+=1
                template = "{}\t{}\n"
                print(template.format(name[i], n[l+j]))
                break
        else:
            continue
    

def main():
    code = getting_code()
    extracting_names(code)

main()
