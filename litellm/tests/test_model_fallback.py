#### What this tests ####
#    This tests error handling + logging (esp. for sentry breadcrumbs)

import sys, os
import traceback
sys.path.insert(0, os.path.abspath('../..'))  # Adds the parent directory to the system path
import litellm
from litellm import embedding, completion

litellm.success_callback = ["posthog"]
litellm.failure_callback = ["slack", "sentry", "posthog"]

litellm.set_verbose = True

model_fallback_list = ["replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1", "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1", "chatgpt-test"]

user_message = "Hello, how are you?"
messages = [{ "content": user_message,"role": "user"}]

for model in model_fallback_list:
    try:
        response = embedding(model="text-embedding-ada-002", input=[user_message])
        response = completion(model=model, messages=messages)
        print(response)
    except Exception as e:
        print(f"error occurred: {traceback.format_exc()}") 