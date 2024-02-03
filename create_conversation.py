from zhipuai import ZhipuAI
import re
from tqdm import tqdm

def split_paragraphs(text):
    # 使用正则表达式根据句号、问号和感叹号切分文本
    # \u3002 是中文句号，\uff1f 是中文问号，\uff01 是中文感叹号
    pattern = r'\n\n\n'
    # pattern = r'。|\？|\！|\.\s|\?\s|\!\s|\n'
    sentences = re.split(pattern, text)
    paragraphs = [sentence.strip() for sentence in sentences if sentence.strip()]
    return paragraphs

client = ZhipuAI(api_key="API_KEY") # 填写您自己的APIKey
txt_file = "StartingStrengthBasic_clean.txt"
out_file = "StartingStrengthBasic_output.txt"

with open(txt_file, 'r', encoding='utf-8') as f_in:
    text = f_in.read()
    paragraphs = split_paragraphs(text)
    responses = ""
    
    for i in tqdm(range(0, len(paragraphs)-1)):
        submit_content = paragraphs[i]
        # print(submit_content)
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                response = client.chat.completions.create(
                    model="glm-4",  # 填写需要调用的模型名称
                    messages=[
                        {"role": "system", "content": "我会给你一段健身相关的资料，这段资料有一部分不通顺的地方，请你先把它按正常语序优化。 \
                        再根据优化后的资料文本，构建一些针对这些资料的问题。\
                        输出格式如下“{\n\t\"input\": \"你需要构造的问题\", \
                            \n\t\"output\": \"资料中的一部分内容\"\n},”。请严格按照以上格式输出，不要输出优化后的资料文本和其他内容。"},
                        {"role": "user", "content": submit_content}
                    ],
                )
                responses += response.choices[0].message.content + '\n'
                success = True
            except Exception as e:
                attempts += 1
                print(f'{e}\nTry again, {attempts=}')

    with open(out_file, 'w', encoding='utf-8') as f_out:
        f_out.write(responses)
