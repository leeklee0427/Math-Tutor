"""
Author: Bill LI
File: math-tutor.py
Created: 01/02/2024
Description: Answers a single hardcoded question by calling the Assistant API through the command line.
"""

from openai import OpenAI
import time

api_key = ""

# Intialize an Client
client = OpenAI(api_key=api_key)

# Upload knowledge file
knowledge_file = client.files.create(
    file=open("./knowledge/knowledge_1000.pdf", 'rb'),
    purpose='assistants',
)
print("knowledge_file:", knowledge_file.id)

# Create an Assistant
assistant = client.beta.assistants.create(
    name = "数学导师",

    instructions = (
        """

        你是一位中国数学老师，你要从上传文件中找到所问题目的相关数学知识点ID，并简单解释题目答案。
        例如，如果题目涉及多个知识点，请列出所有相关的所有知识点ID。
        
        回答包含两段。

        第一段中请从上传文件中查询数学知识点名称的对应ID，并输出你认为相关的知识点ID。
        输出格式如下：
        相关知识点ID：xxxx，xxxx
        
        第二段中请解释题目答案，保证回答简洁，清晰，准确。
        输出格式如下：
        解答：xxx

        """
    ),
        

    tools = [{"type": "retrieval"}, {"type": "code_interpreter"}],

    # model = "gpt-3.5-turbo-1106",
    model = "gpt-4-1106-preview",

    file_ids = [knowledge_file.id]
)


# Create threads
thread = client.beta.threads.create()
print(thread)

# Create message
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = (
        """
        如果向西走5m，记作＋5m，那么－15m表示？ A. 向东走15m B. 向南走15m C. 向西走15m D. 向北走15m
        """
    )
)
print(message)


run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# run = client.beta.threads.runs.retrieve(
#   thread_id=thread.id,
#   run_id=run.id
# )

# Wait for response
start = time.time()
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(run.status)
    time.sleep(2)
end = time.time()
print("Elapsed time: " + str(end - start))

# Retrieve messages
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Display messages
for message in reversed(messages.data):
    print(message.role + ": \n" + message.content[0].text.value)
    
