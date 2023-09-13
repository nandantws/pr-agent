import os
from starlette_context import context
from pr_agent.tools.pr_reviewer import PRReviewer
import asyncio

async def run_action():
    pull_request_id = os.environ.get("BITBUCKET_PR_ID", '')
    slug = os.environ.get("BITBUCKET_REPO_SLUG", '')
    workspace = os.environ.get("BITBUCKET_WORKSPACE", '')
    context['bitbucket_bearer_token'] = os.environ.get('BITBUCKET_BEARER_TOKEN', None)
    if pull_request_id and slug and workspace:
        pr_url = f"https://bitbucket.org/{workspace}/{slug}/pull-requests/{pull_request_id}"
        print(f"PR URL: {pr_url}===================================================================")
        await PRReviewer(pr_url).run()

if __name__ == "__main__":
    asyncio.run(run_action())

