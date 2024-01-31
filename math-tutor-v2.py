"""
Author: Bill LI
File: math-tutor-v2.py
Created: 01/07/2024
Description: Allows users to input questions one at a time, preventing uploading duplicated knowledge files.
"""

from openai import OpenAI
import time

assistant_id = ""
api_key = ""

# Intialize an Client
client = OpenAI(api_key=api_key)

def initialize():
    # Upload knowledge file
    knowledge_file = client.files.create(
        file=open("./knowledge/knowledge_1000.pdf", 'rb'),
        purpose='assistants',
    )
    print("knowledge_file: \t\t", knowledge_file.id)


    # Create an Assistant
    assistant = client.beta.assistants.create(
        name = "数学导师",

        instructions = (
            """
            你是一位中国数学老师，你要从上传文件中找到所问题目的相关数学知识点ID，并简单解释题目答案。
            例如，如果题目涉及多个知识点，请列出所有相关的所有知识点ID。
        
            请从上传文件中查询数学知识点名称的对应ID，并输出你认为相关的知识点ID。
            输出格式如下：
            相关知识点ID：xxxx，xxxx
            """
        ),
            
        tools = [{"type": "retrieval"}, {"type": "code_interpreter"}],

        # model = "gpt-3.5-turbo-1106",
        model = "gpt-4-1106-preview",

        file_ids = [knowledge_file.id]
    )

    global assistant_id
    assistant_id = str(assistant.id)
    print("assistant_id: \t\t" + str(assistant.id))


def chat(user_input):
    # Create threads
    thread = client.beta.threads.create()
    print(thread)

    # Create message
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content=user_input
    )
    #print(message)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

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
    

if __name__ == "__main__":
    initialize()
    
    while True:
        user_input = input("Please enter your question below (or type '0' to exit): ")

        if user_input == '0':
            print("Exiting.")
            break
        else:
            print("You entered: ", user_input)
            chat(user_input)
