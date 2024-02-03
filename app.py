__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# 导入必要的库
import gradio as gr
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from LLM import InternLM_LLM
from langchain.prompts import PromptTemplate
import torch
from openxlab.model import download
import os

def download_model():
    # 下载大语言模型和向量数据库
    download(model_repo='Saige-Ring/InternLM-Workout-Assistant', output='InternLM2-chat-7b')
    # 下载 Embedding 模型
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'    
    os.system('huggingface-cli download --resume-download BAAI/bge-large-zh-v1.5 --local-dir bge-large-zh-v1.5')
    os.system('unzip InternLM2-chat-7b/data_base_workout_assistant.zip -d ./')

def load_chain():
    # 加载问答链
    # 定义 Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="bge-large-zh-v1.5")

    # 向量数据库持久化路径
    persist_directory = 'data_base_workout_assistant/vector_db/chroma'

    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
        embedding_function=embeddings
    )

    llm = InternLM_LLM(model_path = "InternLM2-chat-7b")

    template = """你现在是一个健身教练，你需要始终保持积极的态度，激励用户坚持他们的健身计划。
    分享你的专业知识，提供各种运动技巧、定制的健身计划和营养建议。
    确保安全总是放在首位，教导正确的姿势和技巧，以预防运动伤害，并提供处理这些伤害的有效方法。
    根据每个用户的健身水平、健康状况和个人喜好，提供个性化的训练建议。
    鼓励用户跟踪他们的锻炼和饮食习惯，给予他们正面的反馈和建设性的意见，以帮助他们看到自己的进步。
    同时，不要忘记提供有关健康生活方式的建议，如良好的睡眠习惯、有效的压力管理技巧和均衡的饮食计划，这些都是支持整体健康和达成健身目标的关键因素。
    现在你需要使用以下上下文来回答用户的问题。如果你不知道答案，就说你不知道。总是使用中文回答。
    问题: {question}
    可参考的上下文：
    ···
    {context}
    ···
    如果给定的上下文无法让你做出回答，请回答你不知道。
    有用的回答:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                    template=template)

    # 运行 chain
    from langchain.chains import RetrievalQA

    qa_chain = RetrievalQA.from_chain_type(llm,
                                        retriever=vectordb.as_retriever(),
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    
    return qa_chain

class Model_center():
    """
    存储问答 Chain 的对象 
    """    
    def __init__(self):        
        self.chain = load_chain()

    def qa_chain_self_answer(self, question: str, chat_history: list = []):
        """
        调用不带历史记录的问答链进行回答
        """
        if question == None or len(question) < 1:
            return "", chat_history
        try:
            chat_history.append(
                (question, self.chain({"query": question})["result"]))
            return "", chat_history
        except Exception as e:
            return e, chat_history

if __name__ == "__main__":
    download_model()
    model_center = Model_center()

    block = gr.Blocks()
    with block as demo:
        with gr.Row(equal_height=True):   
            with gr.Column(scale=15):
                gr.Markdown("""<h1><center>InternLM</center></h1>
                    <center>书生浦语·健身小助手</center>
                    """)
            # gr.Image(value=LOGO_PATH, scale=1, min_width=10,show_label=False, show_download_button=False)

        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(height=450, show_copy_button=True)
                # 创建一个文本框组件，用于输入 prompt。
                msg = gr.Textbox(label="Prompt/问题")

                with gr.Row():
                    # 创建提交按钮。
                    db_wo_his_btn = gr.Button("Chat")
                with gr.Row():
                    # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                    clear = gr.ClearButton(
                        components=[chatbot], value="Clear console")
                    
            # 设置按钮的点击事件。当点击时，调用上面定义的 qa_chain_self_answer 函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
            db_wo_his_btn.click(model_center.qa_chain_self_answer, inputs=[
                                msg, chatbot], outputs=[msg, chatbot])
            
        gr.Markdown("""提醒：<br>
        1. 本助手是利用 InternLM 7B 模型和 Langchain 搭建的“健身小助手”。
        2. 初始化数据库时间可能较长，请耐心等待。
        3. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。 <br>
        """)

    # threads to consume the request
    gr.close_all()
    # 启动新的 Gradio 应用，设置分享功能为 True，并使用环境变量 PORT1 指定服务器端口。
    # demo.launch(share=True, server_port=int(os.environ['PORT1']))
    # 直接启动
    demo.launch()
