# Latest gpt-4 topics - OpenAI Developer Community

> Notion URL: https://app.notion.com/p/Latest-gpt-4-topics-OpenAI-Developer-Community-26a7125a9c9f81c89b4df27660d91c00
> Created: 2025-09-10T21:59:00.000Z
> Last edited: 2025-09-18T19:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
Welcome to the OpenAI Developer Community, a forum for developers to meet and chat with other developers while building with OpenAI’s APIs and developer platform.
This is not a place for ChatGPT discussion (with the exception of ChatGPT developer tools, like Codex). ChatGPT discussion takes place in the OpenAI Discord community.
What to know:
1. This forum is community-run and maintained. Not all posts are monitored. To get in touch with OpenAI, reach out at https://help.openai.com/en/?q=contact.
1. Discussions related to the ChatGPT app and plans will be hidden, and your account may be suspended. (We must keep conversations focused on technical topics related to building with OpenAI, for the sake of the larger community here.)
1. Before posting a new topic, please search the forum for similar topics. This prevents duplicate discussions.
1. Your use of this forum means you agree to the community guidelines, which include being nice, productive, and constructive. Read the full community guidelines: FAQ - OpenAI Developer Community
Hello,
Hope everyone is doing well. I’ve been having some trouble with calling the GPT 4.1 mini API via my .env file.
When I hard code the API key everything works fine. Checking my directory everything is where it’s suppose to be. I even ran a separate script to check my env and the API key loads just fine.
This is the error message I’m getting:
OpenAI API error: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.
I’ve loaded money into my account. I have about $20 worth of credits. I haven’t exceeded any limits. I’ve barely got a chance to use it…
I’m confused, if anyone could aid in shining some light and giving some clarity I’d really appreciate it.
Thanks again.
This post’s script will attempt to make a “list models” call - then give you all the env variables that the client is actually detecting and using, so you can see if others are being grabbed and conflicting, such as a different organization.
  Have you tried printing the API key the code obtains, to ensure you have set the key you think you are using? Here’s a better version of finding out the credentials that are used - which are automatic and don’t need you to specify the default environment variable key. import openai def get_org_model(client, model="gpt-4o-mini"): try: return client.models.retrieve(model).id # Makes test API call except Exception as your_error: return your_error def env_info(): cl…  
