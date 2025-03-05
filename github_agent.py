from agno.agent import Agent
from agno.tools.github import GithubTools
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
import os
from dotenv import load_dotenv
load_dotenv()

from agent_instructions import process_instruction, stat_instruction
from github_tools import get_contribution_stats, get_repo_stats, get_user_stats

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

model = OpenAIChat(
  id="gpt-4o-mini",
  api_key=OPENAI_API_KEY
)

# Base GitHub Tools
github_tool = GithubTools(
  access_token=GITHUB_ACCESS_TOKEN,
  create_issue=False,
  create_repository=False
)

# GitHub Data Processer Agent
get_github_data = Agent(
  name="GitHub Stats Agent",
  model=model,
  instructions= process_instruction,
  tools=[get_contribution_stats, get_repo_stats, get_user_stats],
  show_tool_calls=True,
  read_chat_history=True,
  markdown=True,
  debug_mode=True
)


# Main Agent
github_stat_agent = Agent(
  model=model,
  instructions=stat_instruction,
  # tools= [github_tool], # Use tools when using github_instruction
  team= [get_github_data], # Use Team when using own github functions
  show_tool_calls=True,
  read_chat_history=True,
  markdown=True,
  debug_mode=True
)

# # CLI 
# while True:
#   prompt = input("You: ")
#   if prompt.lower().strip() == 'exit':
#     break

#   response = github_stat_agent.run(prompt)
#   print(response.content)

app = Playground(agents=[github_stat_agent]).get_app()

if __name__ == "__main__":
  serve_playground_app("github_agent:app", reload=True)