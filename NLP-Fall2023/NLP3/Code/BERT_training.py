import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

drugbank_df = pd.read_excel("Drugsall.xlsx")
print(drugbank_df.head())
print(drugbank_df.shape)
drugbank_df.dropna(subset=["description", "indication"], how='all', inplace=True)
drugbank_df["description"] = drugbank_df.apply(lambda row: str(row["description"])
                                                           + " " + str(row["indication"]), axis=1)
print(drugbank_df.head())
print(drugbank_df.shape)


from transformers import BertTokenizer
tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')

from transformers.models.bert import BertModel

import torch


bert_model = BertModel.from_pretrained("bert-base-uncased")
sentence='I really enjoyed this movie a lot.'
#1.Tokenize the sequence:
tokens=tokenizer.tokenize(sentence)
print(tokens)
print(type(tokens))

# 2. Add [CLS] and [SEP] tokens:

tokens = ['[CLS]'] + tokens + ['[SEP]']
print(" Tokens are \n {} ".format(tokens))

# 3. Padding the input:

T=15
padded_tokens=tokens +['[PAD]' for _ in range(T-len(tokens))]
print("Padded tokens are \n {} ".format(padded_tokens))
attn_mask=[ 1 if token != '[PAD]' else 0 for token in padded_tokens  ]
print("Attention Mask are \n {} ".format(attn_mask))

# 4. Maintain a list of segment tokens:

seg_ids=[0 for _ in range(len(padded_tokens))]
print("Segment Tokens are \n {}".format(seg_ids))

# 5. Obtaining indices of the tokens in BERT’s vocabulary:

sent_ids=tokenizer.convert_tokens_to_ids(padded_tokens)
print("senetence idexes \n {} ".format(sent_ids))
token_ids = torch.tensor(sent_ids).unsqueeze(0)
attn_mask = torch.tensor(attn_mask).unsqueeze(0)
seg_ids   = torch.tensor(seg_ids).unsqueeze(0)

# Feed them to BERT

hidden_reps, cls_head = bert_model(token_ids, attention_mask = attn_mask,token_type_ids = seg_ids)
print(type(hidden_reps))
print(hidden_reps.shape ) #hidden states of each token in inout sequence
print(cls_head.shape ) #hidden states of each [cls]


