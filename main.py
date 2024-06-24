import streamlit as st
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain_groq.chat_models import ChatMessage

template = """
Below is a draft text that may be poorly worded
Your goal is to:
- Properly redact the draft text
- Convert the draft text to a specified tone
- Convert the draft text for a specified target audience
- Convert the draft text to the specified level of formality
- Convert the draft text to a specified length in words
- Convert the draft text with the stylistic preferences

Here are some examples different Tones:
- Formal: Greetings! After a period of five days of conversations, discussions, and deliberations, the decision to implement the new corporate strategy has been made. We are delighted to announce this development.
- Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - we're launching a new team initiative. After a bunch of intense talks, debates, and convincing, we're finally moving forward with it.

Here are some examples different Target Audience:
- Teacher: Dear Mr. Smith, I wanted to inform you that the school board has decided to implement a new curriculum after a series of thorough discussions.
- Boss: Ms. Johnson, I am pleased to share that our department will be adopting a new project management tool following extensive deliberations.
- Professor: Professor Davis, I wanted to update you that the university has approved the new research guidelines after a period of comprehensive discussions.

Here are some examples different Level of Formality:
- Low: Hey everyone, just a heads up that we're launching a new team initiative after some intense talks!
- Medium: Hi team, I'm excited to announce that after several days of discussions, we are implementing a new office policy.
- High: Greetings, I am delighted to inform you that after a thorough deliberation process, we will be introducing a new corporate strategy.

Here are some examples different Stylistic Preferences:
- Friendly: Hey folks, great news! After a week of talks, we're rolling out a new company perk.
- Assertive: Attention team, after decisive discussions, we will be enforcing the new security protocols immediately.
- Professional - Dear colleagues, I am pleased to announce that following our recent meetings, we have finalized the decision to adopt new industry standards.
- Empathetic: Hi team, I understand there have been many questions, so I wanted to personally inform you that after careful consideration, we will be updating our health benefits package.

Please start the redaction with a warm introduction. Add the introduction if you need to.

Below is the draft text, tone, and dialect:
DRAFT: {draft}
TONE: {tone}
TARGET AUDIENCE: {audience}
LEVEL OF FORMALITY: {formality}
LENGTH: {length}
STYLISTIC PREFERENCES: {style}

YOUR RESPONSE:
"""

# PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["draft", "tone", "audience", "formality", "length", "style"],
    template=template,
)

# LLM and key loading function
def load_LLM(groq_api_key):
    llm = ChatGroq(
        temperature=0.2,
        model="llama3-70b-8192",
        api_key=groq_api_key
    )
    return llm

# Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")

# Intro: instructions
st.markdown("Re-write your text in different styles.")


# Input OpenAI API Key
st.markdown("## Enter Your Groq API Key")

def get_groq_api_key():
    input_text = st.text_input(label="Groq API Key ", placeholder="Ex: sk-2twmA8tfCb8un4...", key="groq_api_key_input", type="password")
    return input_text

groq_api_key = get_groq_api_key()

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
    
    option_formality = st.selectbox(
        'What formality level would you prefer?',
        ('Low', 'Medium', 'High'))
    
    option_style = st.selectbox(
        'What kind of style do you want the response in?',
        ('Friendly', 'Assertive', 'Professional', 'Empathetic'))
    
with col2:   
    option_audience = st.selectbox(
        'Who is your target audience?',
        ('Teacher', 'Boss', 'Professor'))
    
    option_length = st.selectbox(
        'How long should the response be?',
        ('100 words', '200 words', '500 words'))

# Output
st.markdown("### Your Re-written text:")

if draft_input and groq_api_key:
    llm = load_LLM(groq_api_key)

    formatted_prompt = prompt.format(
        tone=option_tone, 
        audience=option_audience,
        formality=option_formality,
        length=option_length,
        style=option_style, 
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
