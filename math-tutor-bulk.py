"""
Author: Bill LI
File: math-tutor-bulk.py
Created: 01/07/2024
Description: Process bulk questions at one time
"""

from openai import OpenAI
import pandas as pd
import time

api_key = "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"
client = OpenAI(api_key=api_key)

# Load the CSV file
df = pd.read_csv('./data/questions.csv')

# Upload the first file
knowledge_file = client.files.create(
    file=open("./knowledge/knowledge_1000.pdf", 'rb'),
    purpose='assistants',
)
print("knowledge_file: \t\t", knowledge_file.id)


#Create an Assistant
assistant = client.beta.assistants.create(
    name = "数学试卷解答",

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

# List to store the responses
responses = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    print("Running " + str(index))

    content = row['content']
    # print(content + "\n")

    # Create threads
    thread = client.beta.threads.create()
    print(thread)

    # Create message
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = content
    )
    print(message)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Wait for response
    start = time.time()
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        print(str(index) + " " + run.status)
        time.sleep(2)

    end = time.time()
    print("Elapsed time of " + str(index) + ": " + str(end - start))

    # Retrieve messages
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Display messages
    for message in reversed(messages.data):
        if message.role == "assistant":
            print(message.content[0].text.value)
            responses.append(message.content[0].text.value)
            print(str(index) + " done")


# Add the responses to the DataFrame
df['response'] = responses

# Save the DataFrame to a new CSV file
csv_file = './data/solutions.csv'
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print("Write to " + csv_file + " done")
