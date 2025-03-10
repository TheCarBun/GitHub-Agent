import requests, os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api.github.com/graphql"
TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def fetch_user_data(username: str, ):
    """
    Fetch user profile data from GitHub GraphQL API.

    Args:
        username (str): GitHub username.

    Returns:
        dict: JSON response from GitHub API containing user profile data such as:
            - name: The user's name.
            - bio: The user's bio.
            - location: The user's location.
            - createdAt: The date the user created their GitHub account.
            - avatarUrl: The URL of the user's avatar.
            - followers: The total count of followers.
            - following: The total count of users the user is following.
            - repositories: The total count of repositories owned by the user.
            - contributionsCollection: The total count of commits, pull requests, and issues contributed by the user.
        or an error message in case of a request failure.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    query = f"""
    {{
        user(login: "{username}") {{
            name
            bio
            location
            createdAt
            avatarUrl
            followers {{
                totalCount
            }}
            following {{
                totalCount
            }}
            repositories(ownerAffiliations: OWNER, isFork: false){{
                totalCount
            }}
            contributionsCollection {{
                totalCommitContributions
                totalPullRequestContributions
                totalIssueContributions
                }}
        }}
    }}
    """
    try:
        response = requests.post(BASE_URL, json={"query": query}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"errors": str(e)}

def fetch_repo_data(username: str, ):
    """
    Fetch user repository data from GitHub GraphQL API.

    Args:
        username (str): GitHub username.

    Returns:
        dict: JSON response from GitHub API containing repository data such as:
            - totalCount: The total number of repositories owned by the user.
            - edges: A list of repositories with details including:
                - name: The name of the repository.
                - primaryLanguage: The primary language used in the repository, including:
                    - name: The name of the language.
                    - color: The color associated with the language.
        or an error message in case of a request failure.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    query = f"""
    {{
        user(login: "{username}") {{
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {{
                totalCount
                edges {{
                    node {{
                        name
                        languages(first: 3) {{
                            totalCount
                            edges{{
                                node{{
                                    name
                                    color
                                }}
                                size
                            }}
                            totalSize
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    try:
        response = requests.post(BASE_URL, json={"query": query}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"errors": str(e)}

def fetch_contribution_data(username: str, ):
    """
    Fetch contribution data from GitHub GraphQL API.

    Args:
        username (str): GitHub username.

    Returns:
        dict: JSON response from GitHub API containing contribution data such as:
            - restrictedContributionsCount: The count of restricted contributions.
            - totalPullRequestContributions: The total number of pull request contributions.
            - totalIssueContributions: The total number of issue contributions.
            - contributionCalendar: The calendar of contributions including:
                - totalContributions: The total number of contributions.
                - weeks: A list of weeks containing:
                    - contributionDays: A list of days with contributions including:
                        - contributionCount: The number of contributions on that day.
                        - date: The date of the contributions.
        or an error message in case of a request failure.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    query = f"""
    {{
        user(login: "{username}") {{
            contributionsCollection {{
                restrictedContributionsCount
                totalPullRequestContributions
                totalIssueContributions
                contributionCalendar {{
                    totalContributions
                    weeks {{
                        contributionDays {{
                            contributionCount
                            date
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    try:
        response = requests.post(BASE_URL, json={"query": query}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"errors": str(e)}
    