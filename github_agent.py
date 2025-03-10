from agno.agent import Agent
from agno.tools.github import GithubTools
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from instructions.main_agent_instructions import main_agent, stat_agent
from github_tools.github_tools import get_contribution_stats, get_repo_stats, get_user_stats
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

model = OpenAIChat(
  id="gpt-4o-mini",
  api_key=OPENAI_API_KEY
)

# Agno GitHub Tools
github_tools = GithubTools(
  access_token=GITHUB_ACCESS_TOKEN,
  create_issue=False,
  create_repository=False
)

# GitHub Stats Agent
github_stats_agent = Agent(
  name="GitHub Stats Agent",
  model=model,
  instructions= stat_agent,
  tools=[get_contribution_stats, get_repo_stats, get_user_stats],
  show_tool_calls=True,
  read_chat_history=True,
  markdown=True,
  debug_mode=True
)


# Main GitHub Agent
github_main_agent = Agent(
  name="GitHub Agent",
  model=model,
  instructions=main_agent,
  tools= [github_tools], # Use tools when using github_instruction
  team= [github_stats_agent], # Use Team when using own github functions
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

app = Playground(agents=[github_main_agent]).get_app()

if __name__ == "__main__":
  serve_playground_app("github_agent:app", reload=True)