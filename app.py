import streamlit as st
from github_agent import github_main_agent

# Streamlit App
def main():

  st.set_page_config(
    page_title="Agno GitHub Chat",
    page_icon="👽",
    layout="centered"
  )

  with st.sidebar:
    st.title("🚀Agno GitHub Agent\n**GitHub AI Agent** is an intelligent assistant designed to help you analyze and interpret GitHub data effortlessly.  ")
    with st.expander("🔹 How It Works"):
      st.write("""

  This AI-powered agent operates as a **team of specialized processors**, each handling different aspects of GitHub data:  

  **👑 Main GitHub Agent (Leader)**:  
    - Oversees the entire workflow.  
    - Uses **Agno's GitHub tools** for interacting with the GitHub API.  
    - Delegates tasks to specialized agents for data fetching and processing.  
  
  **📊 GitHub Stats Agent** 
    - Retrieves user contributions, repositories, and profile details.  
    - Computes **streaks, trends, burnouts, and predictions**.  
    - Identifies most-used languages, top repositories, and engagement insights.  
    - Uses both **Agno's GitHub tools** and **custom functions** for deeper analysis.  

  ### **⚡ What You Can Do**  
    ✅ View **GitHub activity trends** (streaks, weekly/monthly contributions).  
    ✅ Analyze **repositories** (most-used languages, top starred repos).  
    ✅ Detect **burnout patterns** and predict future activity.  
    ✅ Get a **comprehensive GitHub profile summary** with AI insights.  

  This AI agent is designed to provide **fast, insightful, and structured GitHub analysis** using **state-of-the-art tools and custom algorithms**. 🎯  

  Let's dive into your GitHub stats! 🚀
  """)

  prompt = st.chat_input("Type something...")

  if prompt:
    with st.chat_message('user'):
      st.write(prompt)

    response = github_main_agent.run(prompt) #Agent Response

    with st.chat_message('ai'):
      st.write(response.content)

if __name__ == "__main__":
  main()