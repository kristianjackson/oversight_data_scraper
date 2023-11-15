import time
import gradio as gr
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Replace with your actual Assistant ID
ASSISTANT_ID = "asst_G9Y2sXKVPc38IJFLptZ9hlKd"

def ask_openai(user_message):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    # Wait for the run to complete
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)

    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    response = "\n".join([m.content[0].text.value for m in messages])
    return response


# Gradio Interface
with gr.Blocks() as demo:
    with gr.Row():
        input_query = gr.Textbox(
            label="Your Query", placeholder="Type your question here..."
        )
        submit_btn = gr.Button("Submit")
    output_response = gr.Textbox(label="OpenAI Response", interactive=False)

    submit_btn.click(fn=ask_openai, inputs=input_query, outputs=output_response)

demo.launch()
