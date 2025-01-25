import xml.etree.ElementTree as ET
import pandas as pd

database = open("../Data/full database.xml", 'r')

tree = ET.parse(database)
root = tree.getroot()

k = 0
Data = []
sdata = []
name = None
for drug in root:
    k = k +1
    name = drug.find("{http://www.drugbank.ca}name")
    if name is not None:
        d_name = name.text
        line  = name.text

    state = drug.find("{http://www.drugbank.ca}state")
    if state is not None:
        d_state = state.text

    desc_array = ["description", "pharmacodynamics", "mechanism-of-action"] #, "toxicity", "metabolism",
                  #"absorption",  "protein-binding", "route-of-elimination", "clearance"]
                # "half-life", "volume-of-distribution",
    d_description = ""
    for desc in desc_array:
        description = drug.find("{http://www.drugbank.ca}" + desc)
        if description is not None:
            if description.text is not None:
                d_description += " " + description.text
    # classification = drug.find("{http://www.drugbank.ca}classification")
    # if classification is not None:
    #     last_desc = classification.find("{http://www.drugbank.ca}description")
    #     if last_desc is not None:
    #         if last_desc.text is not None:
    #             d_description += " " + last_desc.text

    indication =  drug.find("{http://www.drugbank.ca}indication")
    if indication is not None:
        d_indication = indication.text

    #---------dosages --------
    dosages = drug.find("{http://www.drugbank.ca}dosages")
    D = []
    for dosage in dosages:
        d = {}
        for item,n in zip(dosage,["from","route","strength"]):
            d.update({n:item.text})
        D.append(d)

    #-----------------Targets -----
    targets = drug.find("{http://www.drugbank.ca}targets")
    T = []
    for t in targets:
        T.append(t.text)

    #----------pathways ------
    pathways = drug.find("{http://www.drugbank.ca}pathways")
    P = []
    for t in pathways:
        P.append(t.text)

    #----------synonyms ----------
    synonyms = drug.find("{http://www.drugbank.ca}synonyms")
    S = []
    for t in synonyms:
        S.append(t.text)
        if len(t.text) > 3:
            line = line + "|" + t.text

    sdata.append({"name":d_name,\
                 "synonyms":S})

    Data.append({"name":d_name,\
                "description":d_description,\
                "state": d_state,\
                "indication": d_indication,\
                "dosages": D,\
                "synonyms":S})


DF = pd.DataFrame(Data)
DF = DF.set_index("name")
DF.to_excel("../Results/Drugsall_desconly.xlsx")
