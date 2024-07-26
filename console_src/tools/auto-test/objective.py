import argparse
import json
import random

from src import detect
from src.prompt import alex_incoherent_prompt, alex_prompt, maria_prompt


def somesome(use_base_model):
    model_type = use_base_model if use_base_model in ["base", "fine-tuned"] else "base"

    # Loading a variety of queries
    with open("data/detect/queries.json", "r") as file:
        queries = json.load(file)

    # Loading a variety of agent prompts
    with open("data/detect/prompts.json", "r") as file:
        prompts = json.load(file)

    # Loop through all the conversation phases
    for k in queries:

        # Randomize prompt for sale, as well as initial query from the sale
        sales_prompt = random.choice(prompts.get(k))
        customer_prompt = maria_prompt
        initial_query = random.choice(queries.get(k))

        # Diverse model provides diverse chatting experience
        sales_model_name = random.choice(model_names)

        # Create the detector
        detector = Detector.make(
            use_customer_base=use_base_model,
            sales_model_name=sales_model_name,
            customer_prompt=customer_prompt,
            sales_prompt=sales_prompt,
            initial_query=initial_query,
        )

        # Run the detection
        issue_history, conversation_history = detector.run()

        # Construct the output file name
        output_file = f"{args.o}_{model_type}_model_{args.v}_{k}_{sales_model_name.split('/')[-1]}_{initial_query[:20]}.json"

        # Store Detection Results
        detector.store_detected_issue(
            {
                "issue_history": issue_history,
                "conversation_history": conversation_history,
            },
            file_name=output_file,
        )
