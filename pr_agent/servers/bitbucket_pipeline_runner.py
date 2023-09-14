import os
from pr_agent.agent.pr_agent import PRAgent
from pr_agent.config_loader import get_settings
from pr_agent.tools.pr_reviewer import PRReviewer
import asyncio

async def run_action():
    pull_request_id = os.environ.get("BITBUCKET_PR_ID", '')
    slug = os.environ.get("BITBUCKET_REPO_SLUG", '')
    workspace = os.environ.get("BITBUCKET_WORKSPACE", '')
    bearer_token = os.environ.get('BITBUCKET_BEARER_TOKEN', None)
    print(bearer_token, '=-=-=-=-=-=-=-=-=-=-=')

    # Check if required environment variables are set
    if not bearer_token:
        print("BITBUCKET_BEARER_TOKEN not set")

    # Set the environment variables in the settings
    get_settings().set("BITBUCKET.BEARER_TOKEN", bearer_token)
    print(get_settings, '=-=-=-=-=-=-=--=-=-ff')

    if pull_request_id and slug and workspace:
        pr_url = f"https://bitbucket.org/{workspace}/{slug}/pull-requests/{pull_request_id}"
        await PRReviewer(pr_url, env_vars=[bearer_token]).run()

if __name__ == "__main__":
    asyncio.run(run_action())

