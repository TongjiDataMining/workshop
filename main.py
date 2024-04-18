from html import entities
from sys import prefix
from token import tok_name
from hanlp_restful import HanLPClient
HanLP = HanLPClient('https://www.hanlp.com/api', auth='NTAyN0BiYnMuaGFubHAuY29tOkw5clFLbGhTRTIyNUppUDE=', language='zh') # auth不填则匿名，zh中文，mul多语种

## 输入文本
text = "同济大学软件学院成立于2001年9月,是国家教育部与原国家计委联合批准成立的国家示范性软件学院。中国科学院院士、我国首台银河巨型计算机主机系统总设计师周兴铭教授担任首任院长，自2017年3月起担任名誉院长。学院不仅拥有一流教学和实验环境，而且拥有一支以专职教师为核心，专职与兼职相结合，高校与企业相结合，国内与国外相结合的结构多元化的特色师资队伍。同时，学院致力于国际交流和企业合作，与瑞典、丹麦、西班牙、美国、英国、法国和境外香港、台湾等高校建立合作关系。学院按照周兴铭院士提出的“前沿化、工程化、国际化、基础理论与实践技能协调发展”的办学指导思想，以“基于软件工程科学，面向国家和产业发展需求，培养基础理论扎实深厚、具有创新潜力，工程型、复合型、国际化的多层次、创新型卓越工程人才培养”为培养目标秉承“勤奋、改革、开放、创新”的学院文化，力争建设成为有一定国际知名度的软件学院。"


def get_triplegroups(sent):
    
    triple_groups = []
    doc=HanLP.parse(sent,tasks=['srl'])

    for i in range(len(doc['tok/fine'])):
        ## chunk 1
        ent1 = ""
        ent2 = ""
        relation=""
        #############################################################
  
        for j,pas in enumerate(doc['srl'][i]):
            print(f'第{j+1}个谓词论元结构')
            for form, role, begin, end in pas:
                print(f'{form} = {role} at [{begin}, {end})')
                if role == 'ARG0':
                    ent1 =  form
                if role == 'ARG1':
                    ent2 =  form
                if role == 'PRED':
                    relation = form
            triple_groups.append((ent1.strip(),relation.strip(),ent2.strip()))


    return triple_groups

for i in get_triplegroups(text):
    print(i)



