import streamlit as st
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain_groq.chat_models import ChatMessage

template = """
Below is a draft text that may be poorly worded.
Your goal is to:
- Properly redact the draft text
- Convert the draft text to a specified tone
- Convert the draft text to a specified dialect

Here are some examples different Tones:
- Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
- Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

Here are some examples of words in different dialects:
- American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
- British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

Example Sentences from each dialect:
- American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
- British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

Please start the redaction with a warm introduction. Add the introduction if you need to.

Below is the draft text, tone, and dialect:
DRAFT: {draft}
TONE: {tone}
DIALECT: {dialect}

YOUR {dialect} RESPONSE:
"""

# PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)

# LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = ChatGroq(
        temperature=0.3,
        model="llama3-70b-8192",
        api_key=openai_api_key
    )
    return llm

# Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")

# Intro: instructions
st.markdown("### Re-write your text in different styles.")


# Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ", placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()

# Input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

# Output
st.markdown("### Your Re-written text:")

if draft_input and openai_api_key:
    llm = load_LLM(openai_api_key=openai_api_key)

    formatted_prompt = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    # Creating message objects
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content=formatted_prompt)
    ]

    # Debugging output to verify structure
    print("Messages to be sent to llm:")
    for msg in messages:
        print(type(msg), msg)

    # Pass the messages to the llm function
    try:
        improved_redaction = llm(messages)
        st.write(improved_redaction.content)
    except TypeError as e:
        st.error(f"TypeError: {e}")
        st.write("Messages passed to llm:")
        for msg in messages:
            st.write(type(msg), msg)
