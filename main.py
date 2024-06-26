import streamlit as st
from langchain.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
from langchain_groq.chat_models import ChatMessage
from langchain.chains import LLMChain


prompt_template = """
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

Please start the redaction with a warm introduction. Add the introduction if you need to. The response should only contain the changed message and nothing else.

Example:
- Draft: Do i have to be present on Saturday, because i am going to attend a competition about some robot building ?
- Output: Hey teacher, hope you're doing great! I just wanted to check in with you about Saturday's schedule. I've got a super cool robot building competition that I'm really excited to attend, and I was wondering if I need to be present in class that day. I've been working hard on my robot and I'd love to show it off! If it's okay with you, I'd really appreciate it if I could take the day off to focus on the competition. Let me know either way, thanks so much!

Below is the draft text, tone, and dialect:
DRAFT: {draft}
TONE: {tone}
TARGET AUDIENCE: {audience}
LEVEL OF FORMALITY: {formality}
LENGTH: {length}
STYLISTIC PREFERENCES: {style}

YOUR RESPONSE:
"""

# output_template = """
# Given is a draft text that is poorly generated and has some additional content
# Your goal is to:
# - Removed the additional content
# - Keep the core message as it is

# The input generally consists of some starting directive like 
# "Here is the rewritten text:" 
# and some ending points like 
# "This rewritten text meets the specified requirements:

# Tone: Informal
# Target Audience: Teacher
# Level of Formality: Low
# Length: 100 words
# Stylistic Preferences: Assertive"

# A simple example is as follows:
# - Input
# Here is the rewritten text:

# Hey [Teacher's Name], hope you're doing well! I've got a question about Saturday's schedule. I'm actually participating in a robot-building competition that day and I was wondering if I really need to be present in class. I've been working hard on this project and it's a great opportunity for me to showcase my skills. I'll make sure to catch up on any material I miss, but I'd really appreciate it if I could take the day off. Let me know either way, thanks!

# This rewritten text meets the specified requirements:

# Tone: Informal
# Target Audience: Teacher
# Level of Formality: Low
# Length: 100 words
# Stylistic Preferences: Assertive

# - Required Output
# Hey [Teacher's Name], hope you're doing well! I've got a question about Saturday's schedule. I'm actually participating in a robot-building competition that day and I was wondering if I really need to be present in class. I've been working hard on this project and it's a great opportunity for me to showcase my skills. I'll make sure to catch up on any material I miss, but I'd really appreciate it if I could take the day off. Let me know either way, thanks!
# """

# PromptTemplate variables definition
prompt1 = PromptTemplate(
    input_variables=["draft", "tone", "audience", "formality", "length", "style"],
    template=prompt_template,
)
# prompt2 = PromptTemplate(
#     # input_variables=["input"],
#     template=output_template,
# )

# LLM and key loading function
def load_LLM():
    llm = ChatGroq(
        temperature=0.2,
        model="llama3-70b-8192",
        api_key=st.secrets["GROQ_API_KEY"]
    )
    return llm

# def createChain(llm):
#     chain_one = LLMChain(
#         llm=llm, 
#         prompt=prompt1, 
#         output_key="input"
#     )
#     chain_two = LLMChain(
#         llm=llm, 
#         prompt=prompt2, 
#         output_key="final"
#     )
    
#     overall_chain = SequentialChain(
#         chains=[chain_one, chain_two, chain_three, chain_four],
#         input_variables=["draft", "tone", "audience", "formality", "length", "style"],
#         output_variables=["input"],
#     )
    
#     return overall_chain
    
    
# Page title and header
st.set_page_config(page_title="ReWriteAI")
st.markdown("<h1 style='text-align: center; font-size:5rem;'>ReWriteAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:1rem; font-weight: 200;'>Re-write your text using various customisations and the power of LLM's</p>", unsafe_allow_html=True)

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
        'Which tone would you like to have?',
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
    
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 0.7em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    submit = st.button('Submit')
    
# Output
def runQuery():
    llm = load_LLM()

    formatted_prompt1 = prompt1.format(
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
        ChatMessage(role="user", content=formatted_prompt1)
    ]

    # Debugging output to verify structure
    print("Messages to be sent to llm:")
    for msg in messages:
        print(type(msg), msg)

    # Pass the messages to the llm function
    try:
        improved_redaction = llm(messages)
        message_content = improved_redaction.content
        
        st.write(message_content)       
            
    except TypeError as e:
        st.error(f"TypeError: {e}")
        st.write("Messages passed to llm:")
        for msg in messages:
            st.write(type(msg), msg)
            
            
st.markdown("### Your Re-written text:")
if(submit):
    runQuery()
    
