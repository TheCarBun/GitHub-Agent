from datetime import datetime
from github_tools.fetch_data import *
from github_tools.util import format_duration, is_less_than_2_months_old, format_iso_date, format_date_ddmmyyyy, get_language_distribution, get_langugage_percent

def get_contribution_stats(username:str):
    """
    Process the contribution data from GitHub API response.

    Args:
      data (dict): JSON response from GitHub API containing contribution data.

    Returns:
      str: Formatted string containing processed contribution data including:
      - Total Contributions
      - Public Contributions
      - Private Contributions
      - Highest Contribution and its date
      - Today's Commits
      - Current Streak
      - Longest Streak
      - Active Days
      - Contribution Days

    Raises:
      KeyError: If the expected keys are not found in the input data.
      TypeError: If the input data is not of the expected type.
    """
    try:
        data = fetch_contribution_data(username)
        contributions_collection = data['data']['user']['contributionsCollection']
        calendar = contributions_collection['contributionCalendar']
        days = [day for week in calendar['weeks'] for day in week['contributionDays']]
        
        # Safely get contribution counts with fallbacks to 0
        public_contributions = calendar.get('totalContributions', 0)
        private_contributions = contributions_collection.get('restrictedContributionsCount', 0)
        total_contributions = public_contributions + private_contributions
        
        # Ensure we have valid contribution counts
        if not isinstance(public_contributions, (int, float)):
            public_contributions = 0
        if not isinstance(private_contributions, (int, float)):
            private_contributions = 0
            
        # Calculate highest contribution
        try:
            highest_day = max(days, key=lambda day: day['contributionCount'])
            highest_contribution = highest_day['contributionCount']
            highest_contribution_date = format_date_ddmmyyyy(highest_day['date'])
        except (ValueError, KeyError):
            highest_contribution = 0
            highest_contribution_date = None
        
        current_streak = 0
        longest_streak = 0
        
        # Calculate streaks with validation
        try:
            for day in days:
                if day.get('contributionCount', 0) > 0:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 0
        except (TypeError, KeyError):
            current_streak = 0
            longest_streak = 0

        # Extract contribution days
        weeks = calendar.get("weeks", [])
        contribution_days = [day["date"] for week in weeks for day in week["contributionDays"] if day["contributionCount"] > 0]
        active_days = len(set(contribution_days))  # Unique active contribution days
        
        # Today's Date in format of how it's fetched from GraohQL
        today = datetime.now().strftime("%Y-%m-%d") 

        # Find today's contributions
        today_commits = sum(
            day["contributionCount"]
            for week in weeks
            for day in week["contributionDays"]
            if day["date"] == today
        )

        return f"""
        🔢 Total Contributions: {total_contributions}
        🌐 Public Contributions: {public_contributions}
        🔒 Private Contributions: {private_contributions}
        📈 Highest Contribution: {highest_contribution} on {highest_contribution_date}
        📅 Today's Commits: {today_commits}
        🔥 Current Streak: {current_streak} days
        🏆 Longest Streak: {longest_streak} days
        📆 Active Days: {active_days}
        📜 Contribution Days: {days}
        """
    except (KeyError, TypeError) as e:
        print(f"Error processing contribution data: {str(e)}")
        return {
            "total_contributions": 0,
            "public_contributions": 0,
            "private_contributions": 0,
            "highest_contribution": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "days": []
        }

def get_repo_stats(username:str):
    """
    Process the repository data from GitHub API response.

    Args:
      data (dict): JSON response from GitHub API containing repository data.

    Returns:
      dict: Processed repository data including:
      - language_data (dict): Dictionary of languages with their usage counts and colors.

    Raises:
      KeyError: If the expected keys are not found in the input data.
      TypeError: If the input data is not of the expected type.
    """
    try:
        data = fetch_repo_data(username)
        # Get repositories from the user data
        repositories = data['data']['user']['repositories']['edges']
        
        # Process language data
        repo_language_data = {}
        
        for edge in repositories:
            repo = edge['node']
            repo_name = repo['name']
            languages_node = repo['languages']
            language_count = languages_node['totalCount']

            if language_count > 0:

                languages = languages_node['edges']
                lang_list = []
                for language in languages:
                    language_name = language['node']['name']
                    language_size = language['size']
                    lang_list.append({language_name: language_size})

                repo_language_data[repo_name] = lang_list
        
        lang_distribution = get_language_distribution(repo_language_data)
        lang_percent = get_langugage_percent(lang_distribution)

        return lang_percent

    except Exception as e:
        print(f"Error processing language data: {str(e)}")
        return None

def get_user_stats(username:str):
    """
    Process the user data from GitHub API response.

    Args:
      data (dict): JSON response from GitHub API containing user data.

    Returns:
      str: Formatted string containing processed user data including:
      - Name
      - Bio
      - Location
      - Created At
      - Avatar URL
      - Followers
      - Following
      - Repositories
      - Total Commits
      - Total Pull Requests
      - Total Issues
      - Formatted Date
      - Joined Since
      - GitHub Days
      - Less Than 2 Months Old

    Raises:
      KeyError: If the expected keys are not found in the input data.
      TypeError: If the input data is not of the expected type.
    """
    try:
        data = fetch_user_data(username)
        user_data = data['data']['user']
        
        # Calculate total GitHub days
        created_at = user_data.get("createdAt")
        formatted_date = format_iso_date(created_at) 

        less_than_2_months_old = is_less_than_2_months_old(created_at)
        github_days = (datetime.now() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days

        joined_since = format_duration(created_at)

        return f"""
        👤 Name: {user_data.get("name", "")}
        📝 Bio: {user_data.get("bio", "")}
        📍 Location: {user_data.get("location", "")}
        📅 Created At: {created_at}
        🖼️ Avatar URL: {user_data.get("avatarUrl")}
        👥 Followers: {user_data.get("followers").get("totalCount", 0)}
        👤 Following: {user_data.get("following").get("totalCount", 0)}
        📦 Repositories: {user_data.get("repositories").get("totalCount", 0)}
        📝 Total Commits: {user_data.get("contributionsCollection").get("totalCommitContributions", 0)}
        🔀 Total Pull Requests: {user_data.get("contributionsCollection").get("totalPullRequestContributions", 0)}
        🐛 Total Issues: {user_data.get("contributionsCollection").get("totalIssueContributions", 0)}
        📅 Formatted Date: {formatted_date}
        ⏳ Joined Since: {joined_since}
        📆 GitHub Days: {github_days}
        🕒 Less Than 2 Months Old: {less_than_2_months_old}
        """
    except (KeyError, TypeError) as e:
        print(f"Error processing contribution data: {str(e)}")
        return {
            "errors": str(e)
        }
    