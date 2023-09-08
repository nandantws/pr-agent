import os
from pr_agent.agent.pr_agent import PRAgent
from pr_agent.tools.pr_reviewer import PRReviewer

for key, value in os.environ.items():
    print(f"{key}: {value}==================")
    print('PR ID found')
    pr_url = f"https://bitbucket.org/tejinder22/blog/pull-requests/11"
    print(f"PR URL: {pr_url}")
    PRReviewer(pr_url).run()

