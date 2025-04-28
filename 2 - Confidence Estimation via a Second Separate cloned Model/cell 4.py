# Cell 4: Confidence Estimation (Approach 2)

# ( THEN HERE THE PROPOSED APPROACH, IN THE 2.)

# Craft the evaluation prompt for the confidence estimation model
# This prompt should instruct the second model to evaluate the initial_response

evaluation_prompt = f"""
Original Query: {user_query}

Primary Model's Response: "{initial_response}"

Evaluate the Primary Model's Response for accuracy and consistency with the Original Query.
Provide a confidence score between 0 and 100 percent.
Respond ONLY with the confidence score as a number followed by a percentage sign (e.g., "95%").
"""

# {here is your logic to run the second model in parallel, with just milliseconds of delay}

# {Pass the evaluation_prompt to the confidence estimation model}

# {Capture the output which should be the confidence score}

# Example (conceptual):

# confidence_output = model_confidence.generate(tokenizer_confidence.encode(evaluation_prompt, return_tensors="pt"), max_length=10) # Keep max_length small as we only expect a percentage
# confidence_score_text = tokenizer_confidence.decode(confidence_output[0], skip_special_tokens=True).strip()

# # Extract the numerical score
# try:
#     confidence_score = int(confidence_score_text.replace('%', ''))
#     print(f"\nConfidence Score (from separate model): {confidence_score}%")
# except ValueError:
#     print("\nCould not parse confidence score from separate model output.")
#     print(f"Confidence model raw output: {confidence_score_text}")