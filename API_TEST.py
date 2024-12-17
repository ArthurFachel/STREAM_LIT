from openai import OpenAI
import streamlit as st

st.title("STREAMLIT API TEST")

client = OpenAI(
    api_key=st.secrets["DEEPINFRA_TOKEN"], 
    base_url="https://api.deepinfra.com/v1/openai"
)

if "deepinfra_model" not in st.session_state:
    st.session_state["deepinfra_model"] = "meta-llama/Meta-Llama-3-8B-Instruct"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = True  

        completion = client.completions.create(
            model=st.session_state["deepinfra_model"],
            prompt=f'<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n',
            stop=['<|eot_id|>'],
            stream=stream,
        )

        response_text = ""
        for event in completion:
            if not event.choices[0].finish_reason:
                response_text += event.choices[0].text

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
