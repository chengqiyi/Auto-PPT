import uuid

from readconfig.myconfig import MyConfig
from chain.gpt_memory import GptChain


# 抽象父类
class Gen:
    config: MyConfig = None
    GptChain: GptChain = None

    def __init__(self, session_id):
        self.config = MyConfig()
        self.GptChain = GptChain(openai_api_key=self.config.OPENAI_API_KEY, session_id=session_id,
                                 redis_url=self.config.REDIS_URL)


# ----------------------------------------------------------------
# 生成标题
class GenTitle(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_title(self, query):
        text = f"""我希望你帮助我以```{query}```为题生成3个PPT的标题.要求能吸引人的注意
        """
        self.GptChain.predict(text)


class GenOutline(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_outline(self, query):
        text = f"""我选择的标题是第```{query}```个标题,我希望你用markdown的格式生成一个只有标题的大纲,并且请遵循以下要求:
        1.如果要创建标题，请在单词或短语前面添加井号 (#) 。# 的数量代表了标题的级别。
        2.不能使用无序或者有序列表,必须全部使用添加井号 (#)的方式表示大纲结构.
        3.第一级(#)表示大纲的标题,第二级(##)表示章节的标题,第三级(###)表示章节的重点.
        """
        self.GptChain.predict(text)


class GenBody(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def predict_body(self, fix_outline):
        if fix_outline == "":
            text = f"""请根据大纲生成的PPT文本的正文内容,我希望你同样以markdown的格式返回,并且请遵循以下要求:
            1.不要丢失原有的大纲markdown信息
            2.你需要根据每一个标题的信息,结合上下文在标题的下一行新增一个或者多个段落,每个段落必须使用<p></p>标签包围
            """
        else:
            text = f"""我对大纲进行了如下修改,这是修改后的大纲:
            ```{fix_outline}``` 
            请根据大纲生成的PPT文本的正文内容,我希望你同样以markdown的格式返回,并且请遵循以下要求:
            1.不要丢失原有的大纲markdown信息
            2.你需要根据每一个标题的信息,结合上下文在标题的下一行新增一个或者多个段落,每个段落必须使用<p></p>标签包围
            """
        self.GptChain.predict(text)


if __name__ == '__main__':
    session_id = str(uuid.uuid4())

    title = GenTitle(session_id)
    title.predict_title("如何健身")

    outline = GenOutline(session_id)
    outline.predict_outline("1")

    body = GenBody(session_id)
    body.predict_body("")

# 将一个问题拆分成多个子问题解决,可以大大提高AI对问题的理解,从而提高程序的速度和准确性
