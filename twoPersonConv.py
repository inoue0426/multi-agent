import argparse

from autogen import AssistantAgent, ConversableAgent, UserProxyAgent
from openai import OpenAI


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_turns", type=int, default=5)
    parser.add_argument("--model", type=str, default="llama3")
    parser.add_argument("--temperature_cathy", type=float, default=0.9)
    parser.add_argument("--temperature_joe", type=float, default=0.7)
    return parser.parse_args()


def create_config(args):
    config = {
        "model": args.model,
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
    cathy_config = config.copy()
    cathy_config["temperature"] = args.temperature_cathy
    joe_config = config.copy()
    joe_config["temperature"] = args.temperature_joe
    return cathy_config, joe_config


def create_conversable_agent(name, system_message, llm_config, human_input_mode):
    return ConversableAgent(
        name,
        system_message=system_message,
        llm_config={"config_list": [llm_config]},
        human_input_mode=human_input_mode,
    )


args = parse_arguments()
cathy_config, joe_config = create_config(args)

cathy = create_conversable_agent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config=cathy_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = create_conversable_agent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config=joe_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=args.max_turns)
