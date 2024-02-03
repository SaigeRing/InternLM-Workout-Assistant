# InternLM-Workout-Assistant
# 书生·浦语 健身助手
## 简介
第一届“书生·浦语大模型实战营”大项目仓库。尝试利用 InternLM/Xtuner/Langchain 等工具创建一个健身小助手。

- 大语言基座模型 - [InternLM2-7b-chat](https://github.com/InternLM/InternLM)
- 数据 - 健身相关中文书籍
- 词嵌入模型 - [bge-large-zh-1.5](https://huggingface.co/BAAI/bge-large-zh-v1.5)

首先调用 LLM API 根据健身书籍内容生成对话数据，利用 Xtuner 微调 InternLM2-7b-chat。再利用词嵌入模型，构建向量数据库，用 Langchain 构建检索问答链。最后尝试在 OpenXLab 上部署。

## 数据
### 原始数据
1. 《力量训练基础》PDF
2. 《无器械健身-用自重锻炼身体》PDF
3. 《别让不懂营养学的医生害了你》TXT
1 和 2 为图片 PDF 版本，因此利用 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 提取其中文字，保存成 TXT 文件。调用代码见 [pdf2txt.py](./pdf2txt.py)。

### 生成对话数据
利用智谱 GLM-4 API 根据健身书籍内容生成对话数据。调用代码见 [create_conversation.py](./create_conversation.py)。直接生成的数据格式不对，无法被正确读取，手动清洗数据至标准 JSON 格式。由于书籍 2&3 生成的问答数据效果不行，故下一步微调只选择了书籍 1 生成的问答数据。

## 微调
参考配置 [internlm2_chat_7b_qlora_oasst1_e3.py](https://github.com/InternLM/xtuner/blob/main/xtuner/configs/internlm/internlm2_chat_7b/internlm2_chat_7b_qlora_oasst1_e3.py)，用生成的对话数据进行微调。

## RAG

## 参考
`requirements.txt` 参考自 [Law_InternLM](https://github.com/Aitejiu/Law_InternLM/blob/main/requirements.txt)
