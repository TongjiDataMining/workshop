from hanlp_restful import HanLPClient
from openai import OpenAI
import os
import tqdm

client = OpenAI()

HanLP = HanLPClient('https://www.hanlp.com/api', auth='NTAyN0BiYnMuaGFubHAuY29tOkw5clFLbGhTRTIyNUppUDE=',
                    language='zh')  # auth不填则匿名，zh中文，mul多语种
SYS_PROMPT = '''
你是一名出色的语言学家，你的研究领域是自然语言处理。接下来我将给你一个中文原句与语义角色提取后的句子，你需要仔细理解句子中的各种语法关系，根据原句，
判断语义角色提取后的句子是否*完整*、*正确*与*合理*，如果是请回复“T”，否则请回复“F”，请不要回复其他内容。
'''

sents=[]
with open('./news_summary.txt', 'r', encoding='utf-8') as f:
    sents=f.readlines()

delimiters = ['。', '！', '？', '!', '?', '……']
def split_text(text, delimiters):
    text.replace('\n', '')
    sents = []
    start = 0
    for i, char in enumerate(text):
        if char in delimiters:
            sents.append(text[start:i + 1])
            start = i + 1
    return sents



def get_triplegroups(sent):
    triple_groups = []
    doc = HanLP.parse(sent, tasks=['srl'])

    for i in range(len(doc['tok/fine'])):
        ## chunk 1
        ent1 = ""
        ent2 = ""
        relation = ""
        #############################################################
        for j, pas in enumerate(doc['srl'][i]):
            for form, role, begin, end in pas:
                if role == 'ARG0':
                    ent1 = form
                if role == 'ARG1':
                    ent2 = form
                if role == 'PRED':
                    relation = form
            triple_groups.append((ent1.strip(), relation.strip(), ent2.strip()))

    return triple_groups

print(sents)

print("开始提取三元组...")
print("这可能需要一些时间，请耐心等待...")
final_result = []
for sent in tqdm.tqdm(sents):
    if len(sent) == 0:
        continue
    triples = get_triplegroups(sent)
    original_text = sent
    for i in triples:
        srl_text = ""
        srl_text += i[0] + i[1] + i[2]
        USER_INPUT = "原句：" + original_text + "\n" + "语义角色提取后的句子：" + srl_text
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": USER_INPUT}
            ],
            temperature=0.7, # 这里要结合具体模型调整
        )
        if completion.choices[0].message.content == "T":
            final_result.append(i)
print(final_result)
