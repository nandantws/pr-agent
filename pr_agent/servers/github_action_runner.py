import asyncio
import json
import os
import logging
import time
from typing import Any, Dict


from pr_agent.agent.pr_agent import PRAgent
from pr_agent.config_loader import get_settings
from pr_agent.git_providers import get_git_provider
from pr_agent.tools.pr_code_suggestions import PRCodeSuggestions
from pr_agent.tools.pr_description import PRDescription
from pr_agent.tools.pr_reviewer import PRReviewer
from pr_agent.algo.utils import update_settings_from_args


async def run_action():
    agent = PRAgent()
    # Get environment variables
    GITHUB_EVENT_NAME = os.environ.get('GITHUB_EVENT_NAME')
    GITHUB_EVENT_PATH = os.environ.get('GITHUB_EVENT_PATH')
    OPENAI_KEY = os.environ.get('OPENAI_KEY') or os.environ.get('OPENAI.KEY')
    OPENAI_ORG = os.environ.get('OPENAI_ORG') or os.environ.get('OPENAI.ORG')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    get_settings().set("CONFIG.PUBLISH_OUTPUT_PROGRESS", False)


    # Check if required environment variables are set
    if not GITHUB_EVENT_NAME:
        print("GITHUB_EVENT_NAME not set")
        return
    if not GITHUB_EVENT_PATH:
        print("GITHUB_EVENT_PATH not set")
        return
    if not OPENAI_KEY:
        print("OPENAI_KEY not set")
        return
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set")
        return

    # Set the environment variables in the settings
    get_settings().set("OPENAI.KEY", OPENAI_KEY)
    if OPENAI_ORG:
        get_settings().set("OPENAI.ORG", OPENAI_ORG)
    get_settings().set("GITHUB.USER_TOKEN", GITHUB_TOKEN)
    get_settings().set("GITHUB.DEPLOYMENT_TYPE", "user")

    # Load the event payload
    try:
        with open(GITHUB_EVENT_PATH, 'r') as f:
            event_payload = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return
    
    _duplicate_requests_cache = {}

    # if get_settings().github_app.override_deployment_type:
    #     # Override the deployment type to app
    #     get_settings().set("GITHUB.DEPLOYMENT_TYPE", "app")
    
    # def _is_duplicate_request(body: Dict[str, Any]) -> bool:
    #     print('================================================')
    #     """
    #     In some deployments its possible to get duplicate requests if the handling is long,
    #     This function checks if the request is duplicate and if so - ignores it.
    #     """
    #     request_hash = hash(str(body))
    #     print('request_hash: ', request_hash)
    #     logging.info(f"request_hash: {request_hash}")
    #     request_time = time.monotonic()
    #     ttl = get_settings().github_app.duplicate_requests_cache_ttl  # in seconds
    #     to_delete = [key for key, key_time in _duplicate_requests_cache.items() if request_time - key_time > ttl]
    #     for key in to_delete:
    #         del _duplicate_requests_cache[key]
    #     is_duplicate = request_hash in _duplicate_requests_cache
    #     _duplicate_requests_cache[request_hash] = request_time
    #     if is_duplicate:
    #         logging.info(f"Ignoring duplicate request {request_hash}")
    #     return is_duplicate

    
    # print('get_settings().github_app.duplicate_requests_cache: ', get_settings().github_app.duplicate_requests_cache)
    # if get_settings().github_app.duplicate_requests_cache and _is_duplicate_request(body):
    #     return {}
    # print('_is_duplicate_request(body): ', _is_duplicate_request(body))

    # Handle pull request event
    # if GITHUB_EVENT_NAME == "pull_request":
    #     print('===================================================ddddddddd===============================')
    #     action = event_payload.get("action")
    #     print('action: ', action)
    #     if action in ["opened", "reopened"]:
    #         pr_url = event_payload.get("pull_request", {}).get("url")
    #         print('pr_url: ', pr_url)
    #         if pr_url:
    #             auto_review = os.environ.get('github_action.auto_review', None)
    #             print('auto_review: ', auto_review)
    #             if auto_review is None or (isinstance(auto_review, str) and auto_review.lower() == 'true'):
    #                 await PRReviewer(pr_url).run()
    #             auto_describe = os.environ.get('github_action.auto_describe', None)
    #             print('auto_describe: ', auto_describe)
    #             if isinstance(auto_describe, str) and auto_describe.lower() == 'true':
    #                 await PRDescription(pr_url).run()
    #             auto_improve = os.environ.get('github_action.auto_improve', None)
    #             print('auto_improve: ', auto_improve)
    #             if isinstance(auto_improve, str) and auto_improve.lower() == 'true':
    #                 await PRCodeSuggestions(pr_url).run()

    if GITHUB_EVENT_NAME == "pull_request":
        print(event_payload, '=-=-=-=-=-=-=-=-=-=-=----')
        action = event_payload.get("action")
        if action in get_settings().github_action.handle_pr_actions:
            pr_url = event_payload.get("pull_request", {}).get("url")
            logging.info(f"Performing review because of event={GITHUB_EVENT_NAME} and action={action}")
            for command in get_settings().github_action.pr_commands:
                split_command = command.split(" ")
                command = split_command[0]
                args = split_command[1:]
                other_args = update_settings_from_args(args)
                new_command = ' '.join([command] + other_args)
                logging.info(f"Performing command: {new_command}")
                await agent.handle_request(pr_url, new_command)

    # Handle issue comment event
    elif GITHUB_EVENT_NAME == "issue_comment":
        print('===================================================ffffffffffff==============================')
        action = event_payload.get("action")
        if action in ["created", "edited"]:
            comment_body = event_payload.get("comment", {}).get("body")
            if comment_body:
                is_pr = False
                # check if issue is pull request
                if event_payload.get("issue", {}).get("pull_request"):
                    url = event_payload.get("issue", {}).get("pull_request", {}).get("url")
                    is_pr = True
                else:
                    url = event_payload.get("issue", {}).get("url")
                if url:
                    body = comment_body.strip().lower()
                    comment_id = event_payload.get("comment", {}).get("id")
                    provider = get_git_provider()(pr_url=url)
                    if is_pr:
                        await PRAgent().handle_request(url, body, notify=lambda: provider.add_eyes_reaction(comment_id))
                    else:
                        await PRAgent().handle_request(url, body)


if __name__ == '__main__':
    asyncio.run(run_action())