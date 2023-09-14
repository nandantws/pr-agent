import os
from pr_agent.config_loader import get_settings
from pr_agent.tools.pr_reviewer import PRReviewer
import asyncio

async def run_action():
    pull_request_id = os.environ.get("BITBUCKET_PR_ID", '')
    slug = os.environ.get("BITBUCKET_REPO_SLUG", '')
    workspace = os.environ.get("BITBUCKET_WORKSPACE", '')
    bearer_token = os.environ.get('BITBUCKET_BEARER_TOKEN', None)
    get_settings().set(bearer_token)
    if pull_request_id and slug and workspace:
        pr_url = f"https://bitbucket.org/{workspace}/{slug}/pull-requests/{pull_request_id}"
        await PRReviewer(pr_url, env_vars={'bearer_token':bearer_token}).run()

if __name__ == "__main__":
    asyncio.run(run_action())

