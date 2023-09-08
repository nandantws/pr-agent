import os
from pr_agent.agent.pr_agent import PRAgent
from pr_agent.tools.pr_reviewer import PRReviewer
import asyncio

async def run_action():
    for key, value in os.environ.items():
        print(f"{key}: {value}==================")
        print('PR ID found')
        pr_url = f"https://bitbucket.org/tejinder22/blog/pull-requests/11"
        if  "BITBUCKET_PR_ID" in key:
            print(f"PR URL: {pr_url}")
            await PRReviewer(pr_url).run()

if __name__ == "__main__":
    asyncio.run(run_action())

