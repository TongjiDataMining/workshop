from hanlp_restful import HanLPClient
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

HanLP = HanLPClient('https://www.hanlp.com/api', auth='NTAyN0BiYnMuaGFubHAuY29tOkw5clFLbGhTRTIyNUppUDE=',
                    language='zh')  # auth不填则匿名，zh中文，mul多语种
SYS_PROMPT = '''
你是一名出色的语言学家，你的研究领域是自然语言处理。接下来我将给你一个中文原句与语义角色提取后的句子，你需要仔细理解句子中的各种语法关系，根据原句，
判断语义角色提取后的句子是否*完整*、*正确*与*合理*，如果是请回复“T”，否则请回复“F”，请不要回复其他内容。
'''

## 输入文本
text = '''
习近平会见德国总理朔尔茨
新华社北京4月16日电  （记者杨依军）4月16日上午，国家主席习近平在北京钓鱼台国宾馆会见德国总理朔尔茨。

　　习近平指出，今年是中德建立全方位战略伙伴关系10周年。10年来，尽管国际形势发生很大变化，但中德关系始终稳健发展，各领域合作不断巩固和深化，为两国各自发展提供了动力。当前，世界百年变局加速演进，人类社会面临的风险挑战增多，要解决这些问题，离不开大国合作。中德是世界第二、第三大经济体，巩固和发展中德关系的意义超越双边关系范畴，对亚欧大陆乃至整个世界都有重要影响。两国要从长远和战略角度看待和发展双边关系，携手为世界注入更多稳定性和确定性。

　　习近平强调，中德两国都曾为人类文明进步作出重大贡献。中德之间没有根本利益冲突，彼此不构成安全威胁。中德合作对双方有利，对世界有利。世界越是动荡，双方越要提升两国关系的韧性和活力，坚持中德关系的合作主基调和发展大方向，牢牢把握中德是全方位战略伙伴这一定位。中国对德政策保持高度稳定性和连贯性。双方应该继续以开放的胸襟密切交往，增进战略互信。只要双方坚持相互尊重、求同存异、交流互鉴、合作共赢，两国关系必将继续行稳致远。

　　习近平指出，中德产业链供应链深度互嵌，两国市场高度依存。中德互利合作不是“风险”，而是双方关系稳定的保障、开创未来的机遇。无论是机械制造、汽车等传统领域，还是绿色转型、数字化、人工智能等新兴领域，两国都有合作共赢的巨大潜力亟待挖掘。双方应该发扬互利共赢的鲜明特色，彼此成就。中国出口电动汽车、锂电池、光伏产品等，不仅丰富了全球供给，缓解了全球通胀压力，也为全球应对气候变化和绿色低碳转型作出巨大贡献。中德两国都是以实业立国，都支持自由贸易和经济全球化。双方要警惕保护主义抬头，坚持以市场眼光和全球视野，从经济规律出发，客观、辩证看待产能问题，多探讨合作。中国坚持对外开放基本国策，希望德方为中国企业赴德发展提供公平、透明、开放、非歧视的营商环境。中德在世界多极化问题上有不少共通之处。多极化本质上应该是不同文明、不同制度、不同道路的国家之间相互尊重、和平共处。中德应该独立自主开展多边领域协作，推动国际社会用实际行动更好应对气候变化、发展不平衡、地区冲突等全球性挑战，为世界的平衡稳定作出更多贡献。

　　朔尔茨表示，当前，德中关系发展良好，双方各层级、各领域交往密切。双方成功举行了两国政府磋商以及战略、财金等领域高级别对话，还将举行气候变化和绿色转型对话。过去两天，我和德国企业界代表参访了重庆、上海等地，亲身感受到中国经济发展近年来取得的巨大成就，对德中两国企业界的紧密良好合作印象深刻。德方愿同中方继续加强两国关系，深化各领域双边对话与合作，推进教育、文化等领域人文交流，这对德中两国以及世界都至关重要。德方愿同中方加强沟通协调，共同应对气候变化等全球挑战，致力于维护多边国际秩序，促进世界和平与发展，不赞同对立对抗。德方反对保护主义，支持自由贸易。作为欧盟重要成员，德国愿为促进欧盟同中国关系良好发展发挥积极作用。

　　两国领导人还就乌克兰危机深入交换意见，表示中德都致力于遵守联合国宪章宗旨和原则，反对使用核武器或攻击和平核设施，妥善解决国际粮食安全问题，遵守国际人道主义法。

　　习近平强调，当前形势下，为防止冲突螺旋式升级甚至走向失控，各方应共同致力于早日恢复和平。为此，应该把握以下几个原则：一要以和平稳定的大局为重，不要谋求一己私利。二要为局势降温，不要拱火浇油。三要为恢复和平积累条件，不要进一步激化矛盾。四要减少对世界经济的负面影响，不要破坏全球产业链供应链稳定。中方不是乌克兰危机的当事方、参与方，但一直在以自己的方式劝和促谈。中方鼓励和支持一切有利于和平解决危机的努力，支持适时召开俄乌双方认可、各方平等参与、对所有和平方案进行公平讨论的国际和会，愿就此同包括德国在内的有关各方保持密切沟通。

　　双方还就巴以冲突等共同关心的国际和地区问题交换了意见。双方都认为，应落实联合国安理会第2728号决议，防止事态扩大，避免局势进一步恶化，保证加沙地带无障碍、可持续的人道主义准入，支持巴勒斯坦问题在“两国方案”基础上早日通过谈判解决，呼吁有影响力的国家为维护地区和平稳定发挥建设性作用，推动巴勒斯坦问题早日得到全面、公正、持久解决。

　　会见后，习近平同朔尔茨一起散步并共进午餐，就广泛议题进一步深入交流。

　　王毅参加会见。
'''


sents = [key for key, value in HanLP.extractive_summarization(text, topk=6).items() if value > 0.1] # 参数要根据具体情况调整

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


# sents = split_text(text, delimiters)
print(sents)


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

final_result = []
for sent in sents:
    triples = get_triplegroups(sent)
    original_text = sent
    for i in triples:
        srl_text = ""
        srl_text += i[0] + i[1] + i[2]
        USER_INPUT = "原句：" + original_text + "\n" + "语义角色提取后的句子：" + srl_text
        completion = client.chat.completions.create(
            model="Qwen/Qwen1.5-14B-Chat-GGUF",
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": USER_INPUT}
            ],
            temperature=0.7, # 这里要结合具体模型调整
        )
        if completion.choices[0].message.content == "T":
            final_result.append(i)
print(final_result)
