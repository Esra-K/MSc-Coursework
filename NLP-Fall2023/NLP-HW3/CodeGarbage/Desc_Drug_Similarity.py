import csv
import xml.etree.ElementTree as ET
from lxml import etree
from collections import defaultdict
import sys
temp = sys.stdout
sys.stdout = open('../Data/Taglist.txt','wt')

def perf_func(elem, func, hierarchy_name = "", level=0):
    func(elem, hierarchy_name, level)
    for child in list(elem):
        perf_func(child, func, hierarchy_name+">"+elem.tag.replace("{http://www.drugbank.ca}", ""), level+1)

def print_level(elem, hierarchy_name, level):
    print(hierarchy_name+">"+elem.tag.replace("{http://www.drugbank.ca}", ""))


x = ET.parse("../Data/full database.xml")
root = x.getroot()
print("Start of traversing")
# i = 0
# for drug in root.findall("{http://www.drugbank.ca}drugbank"):
#     print(drug.find("{http://www.drugbank.ca}drug").text)
#     print(i)
#     i += 1
# tags = defaultdict(int)
for child in x.iter():
   print (child.tag, child.text)
# perf_func(x.getroot(), print_level)

sys.stdout = temp
