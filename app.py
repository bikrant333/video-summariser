import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



prompt_caption = """Given the transcript of a YouTube video, create an engaging and concise caption suitable for the video description section. The caption should:
Summarize the main topic: Highlight the video’s core theme or subject in an attention-grabbing way.
Capture viewer interest: Use compelling language or hooks to entice viewers to watch the video.
Include keywords: Naturally incorporate relevant keywords that can help optimize the video for search engines (SEO).
Match the video’s tone: Reflect the video's mood, whether it's informative, entertaining, inspirational, or casual.
Target the intended audience: Use language appropriate for the demographic the video is designed to attract.Video transcipt given here:  """

def get_gemini_content_summary(transcript_text,prompt):
    model= genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt+transcript_text)
    return response.text

def get_gemini_content_caption(transcript_text,prompt):
    model= genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt+transcript_text)
    return response.text

def extract_transcript(video_url):
    ''''''
    try:
        video_id = video_url.split('=')[1]
        trascript_text = YouTubeTranscriptApi.get_transcript(video_id)
        trascript = ""
        for tx in trascript_text:
            trascript += " "+ tx["text"]
        return trascript
    
    except Exception as e:
        raise e

st.markdown(
    """
    <style>
    body {
        background-color: #006400;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split('=')[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/default.jpg", use_container_width=True)

max_number_of_words = st.slider("Select Maximum Number Of Words for Summary ", min_value=50, max_value=500, value=50)
prompt_summary = f"""You are an AI assistant tasked with creating comprehensive summaries of YouTube videos contents. Your goal is to distill the key information, main ideas, and essential points from the video transcipt into a well-structured and informative summary not more than {max_number_of_words} words.Follow below guidelines:
    1. Video Overview
        Provide a brief introduction to the video's topic and main theme.
        Mention the video's title, creator (if known), and approximate length.
    2. Key Points
        Identify and list the main ideas or arguments presented in the video.
        Organize these points in order of importance or as they appear in the video.
        Aim for 3-5 key points, depending on the video's length and complexity.
    3. Supporting Details
        For each key point, include relevant supporting information, examples, or data mentioned in the video.
        Ensure these details enhance understanding without overwhelming the summary.
    4. Narrative Flow
        Maintain a logical flow in your summary, reflecting the video's structure.
        Use transitional phrases to connect different sections of the summary.
    5. Technical Information
        If applicable, include any technical terms, methodologies, or processes explained in the video.
        Briefly define or explain these terms for clarity.
    6. Visual Elements
        Mention any significant visual aids, demonstrations, or graphics used in the video.
        Describe how these elements contribute to the overall message.
    7. Quotations
        Include 1-2 direct quotes from the video if they are particularly impactful or summarize a key point well.
        Ensure quotes are brief and relevant to the main ideas.
    8. Tone and Style
        Reflect the general tone of the video (e.g., formal, casual, humorous) in your summary.
        Maintain an objective stance, avoiding personal opinions or biases.
    9. Conclusion
        Summarize the video's main takeaway or conclusion.
        If applicable, mention any call-to-action or future implications discussed.
    10. Length and Format
        Aim for a summary length of approximately 10-15% of the original transcript's word count.
        Use clear paragraphs, bullet points, or numbered lists for easy readability.
    11. Metadata
        Include the video's upload date and channel name if available.
        Mention any relevant tags or categories associated with the video.

    Remember to focus on accuracy and clarity. Your summary should provide a comprehensive overview that allows readers to grasp the video's content without watching it in full. Avoid including unnecessary details or tangential information. If the video covers multiple topics, ensure your summary reflects this diversity while maintaining coherence.
    Finally, conclude your summary with a brief statement on the video's overall value or relevance to its intended audience.
    Video transcipt given here:  """

# Create two columns
col1, col2 = st.columns(2)

# max_number_of_words = st.slider("Select Maximum Number Of Words for Summary ", min_value=50, max_value=500, value=50)

with col1:
    if st.button("Get Detailed Summary"):
        transcript_txt = extract_transcript(youtube_link)

        if transcript_txt:
            summary = get_gemini_content_summary(transcript_txt,prompt_summary)
            st.markdown('##DETAILED NOTES:')
            st.write(summary)

with col2:
    if st.button("Get Video Caption"):
        transcript_txt = extract_transcript(youtube_link)

        if transcript_txt:
            caption = get_gemini_content_caption(transcript_txt,prompt_caption)
            st.markdown('##CAPTION:')
            st.write(caption)


    

