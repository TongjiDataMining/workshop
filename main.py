from hanlp_restful import HanLPClient
from openai import OpenAI
import tqdm
from database import NDB

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
HanLP = HanLPClient('https://www.hanlp.com/api', auth='NTAyN0BiYnMuaGFubHAuY29tOkw5clFLbGhTRTIyNUppUDE=',
                    language='zh')  # auth不填则匿名，zh中文，mul多语种
SYS_PROMPT = '''
你是一名出色的语言学家，你的研究领域是自然语言处理。接下来我将给你一个中文原句与语义角色提取后的句子，你需要仔细理解句子中的各种语法关系，根据原句，
判断语义角色提取后的句子是否*完整*、*正确*与*合理*，如果是请回复“T”，否则请回复“F”，请不要回复其他内容。
'''
NDB = NDB("bolt://localhost:7687", "neo4j", "dry330500")

sents = []
with open('./news_summary.txt', 'r', encoding='utf-8') as f:
    sents = f.readlines()


def summarize(text):
    sents = [key for key, value in HanLP.extractive_summarization(text, topk=6).items() if value > 0.1]  # 参数要根据具体情况调整
    return sents


def get_triples(sent):
    triple_groups = []
    doc = HanLP.parse(sent, tasks=['srl'])

    for i in range(len(doc['tok/fine'])):
        ent1 = ""
        ent2 = ""
        relation = ""
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


def filter_triples(sent, triples):
    results = []
    for i in triples:
        srl_text = ""
        if i[0] == "" or i[1] == "" or i[2] == "":
            continue
        # srl_text += i[0] + i[1] + i[2]
        # USER_INPUT = "原句：" + sent + "\n" + "语义角色提取后的句子：" + srl_text
        # completion = client.chat.completions.create(
        #     model="Qwen/Qwen1.5-7B-Chat-GGUF",
        #     messages=[
        #         {"role": "system", "content": SYS_PROMPT},
        #         {"role": "user", "content": USER_INPUT}
        #     ],
        #     temperature=0.7,  # 这里要结合具体模型调整
        # )
        # if completion.choices[0].message.content == "T":
        results.append(i)
    return results


def get_triple_groups(sents):
    final_result = []
    for sent in tqdm.tqdm(sents):
        triples = get_triples(sent)
        results = filter_triples(sent, triples)
        final_result.extend(results)
    return final_result


def execute_write(tx, subject, relation, object):
    # 如果节点不存在，则创建节点，如果关系不存在，则创建关系
    query = (
        "MERGE (e1:Entity {name: $subject}) "
        "MERGE (e2:Entity {name: $object}) "
        "MERGE (e1)-[r:RELATIONSHIP {type: $relation}]->(e2)"
    )
    tx.run(query, subject=subject, relation=relation, object=object)


def find_triplets(tx, subject):
    query = (
        "MATCH (e1:Entity {name: $subject})-[r:RELATIONSHIP]->(e2:Entity) "
        "RETURN e1.name, r.type, e2.name"
    )
    result = tx.run(query, subject=subject)
    return [(record["e1.name"], record["r.type"], record["e2.name"]) for record in result]


result = get_triple_groups(sents)
print(result)

for i in result:
    NDB.add_triplet(i[0], i[1], i[2])

print(NDB.find_triplets("北京"))
