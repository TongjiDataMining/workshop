# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
CTB_SPECIFICATION = '''
|Tag| Description| Chinese Description|
|---|---|---|
| AD | adverb | 副词 |
| AS | aspect marker | 助词 |
| BA | bǎ in ba-construction | 当“把”、“将”出现在结构“NP0 + BA + NP1+VP”时的词性 |
| CC | coordinating conjunction | 并列连词 |
| CD | cardinal number | 数词或表达数量的词 |
| CS | subordinating conjunction | 从属连词 |
| DEC | de as a complementizer or a nominalizer | 当“的”或“之”作补语标记或名词化标记时的词性，其结构为：S/VP DEC {NP}，如，喜欢旅游的大学生 |
| DEG | de as a genitive marker and an associative marker | 当“的”或“之”作所有格时的词性，其结构为:NP/PP/JJ/DT DEG {NP}， 如，他的车、经济的发展 |
| DER | resultative de, de in V-de const and V-de-R | 当“得”出现在结构“V-得-R”时的词性，如，他跑得很快 |
| DEV | manner de, de before VP | 当“地”出现在结构“X-地-VP”时的词性，如，高兴地说 |
| DT | determiner | 代冠词，通常用来修饰名词 |
| ETC | etc | “等”、“等等”的词性 |
| FW | foreign word | 外来语 |
| IJ | interjection | 感叹词 |
| JJ | adjective | 形容词 |
| LB | biao in bei-construction | 当“被”、“让”出现在结构“NP0 + LB + NP1+VP”时的词性 |
| LC | localizer | 方位词以及表示范围的限定词 |
| M | measure word | 量词 |
| MSP | aspect marker | 其他虚词，包括“所”、“以”、“来”和“而”等出现在VP前的词 |
| NN | common noun | 普通名词 |
| NR | proper noun | 专有名词 |
| NT | temporal noun | 时间名词 |
| OD | ordinal number | 序数词 |
| ON | onomatopoeia | 拟声词 |
| P | preposition | 介词 |
| PN | pronoun | 代词 |
| PU | punctuation | 标点符号 |
| SB | bèi in short bei-const | 当“被”、“让”出现在结构“NP0 + SB + NP1+VP”时的词性 |
| SP | sentence final particle | 句末助词 |
| URL | url | 网址 |
| VA | copula, be words | 系动词，表示“是”或“非”概念的动词 |
| VC | copula | 系动词 |
| VE | yǒu as the main verb | 表示“有”或“无”概念的动词 |
| VV | other verb | 其他普通动词，包括情态词、控制动词、动作动词、心理动词等等 |
'''
MSRA_SPECIFICATION = '''
|Category| Subcategory| Tag|
|---|---|---|
|NAMEX| Person| P|
|| Location| L|
|| Organization| O|
|TIMEX| Date| dat|
|| Duration| dur|
|| Time| tim|
|NUMEX| Percent| per|
|| Money| mon|
|| Frequency| fre|
|| Integer| int|
|| Fraction| fra|
|| Decimal| dec|
|| Ordinal| ord|
|| Rate| rat|
| MEASUREX | Age | age |
|| Weight | wei |
|| Length | len |
|| Temperature | tem |
|| Angle | ang |
|| Area | are |
|| Capacity | cap |
|| Speed | spe |
|| Acceleration | acc |
|| Other measures | mea |
ADDREX| Email| ema|
|| Phone| pho|
|| Fax| fax|
|| Mobile| mob|
|| Telex| tel|
|| WWW| www|
'''


system_prompt = """
You are an excellent linguist. You are good at NLP in Chinese such as Word Segmentation, Named Entity Recognition.
Here is MSRA specification for your reference.
""" + MSRA_SPECIFICATION + """
The task is to segment using ctb specification and label entities using msra specification in the text. Below are some example sentences in Chinese.
Example:
Input : 同济大学软件学院 成立于2001年9月，是国家教育部与原国家计委联合批准成立的国家示范性软件学院。
Output : 同济大学软件学院(ORG)|成立(VV)|于(P)|2001年9月(DT)|，(PU)|是(VC)|国家教育部(ORG)|与(CC)|原(JJ)|国家计委(ORG)|联合(AD)|批准(VV)|成立(VV)|的(DEC)|国家(NN)|示范性(JJ)|软件学院(NN)|(PU)
Input : 同时，学院致力于国际交流和企业合作，与瑞典、丹麦、西班牙、美国、英国、法国和境外香港、台湾等高校建立合作关系。
Output : 同时(AD)|，(PU)|学院(NN)|致力于(VV)|国际(NN)|交流(NN)|和(CC)|企业(NN)|合作(NN)|，(PU)|与(P)|瑞典(LOC)|、(PU)|丹麦(LOC)|、(PU)|西班牙(LOC)|、(PU)|美国(LOC)|、(PU)|英国(LOC)|、(PU)|法国(LOC)|和(CC)|境外(LOC)|香港(LOC)|、(PU)|台湾(LOC)|等(ETC)|高校(NN)|建立(VV)|合作关系(NN)|(PU)
Input : 中国科学院院士、我国首台银河巨型计算机主机系统总设计师周兴铭教授担任首任院长，自2017年3月起担任名誉院长。
Output : 中国科学院(ORG)|院士(NN)|、(PU)|我国(NR)|首台(OD)|银河(NN)|巨型(JJ)|计算机(NN)|主机(NN)|系统(NN)|总设计师(NN)|周兴铭教授(PER)|担任(VV)|首任(OD)|院长(NN)|，(PU)|自(P)|2017年3月(DT)|起(LC)|担任(VV)|名誉院长(NN)|(PU)
Here is a sentence in Chinese. Please segment and label entities using msra specification in the text.
"""
user_input = "中国科学院院士、我国首台银河巨型计算机主机系统总设计师周兴铭教授担任首任院长，自2017年3月起担任名誉院长。"
completion = client.chat.completions.create(
    model="Qwen/Qwen1.5-14B-Chat-GGUF",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ],
    temperature=0,
)


print(completion.choices[0].message)