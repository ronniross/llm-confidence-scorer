import re

def generate_response_with_confidence(prompt):
    """
    Generate a response to a prompt and a confidence score for its coherence.
    
    Args:
        prompt (str): The user's input question or statement.
    
    Returns:
        tuple: (response, confidence_score) where response is the model's answer
               and confidence_score is an integer from 0 to 100 (or None if extraction fails).
    """
    # Step 1: Create initial conversation with user's prompt
    messages = [{"role": "user", "content": prompt}]
    
    # Apply chat template to format the input
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False  # Thinking mode disabled as requested
    )
    
    # Tokenize the input
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    # Generate the response with increased max_new_tokens
    outputs = model.generate(**inputs, max_new_tokens=512)
    
    # Extract only the newly generated tokens (assistant's response)
    generated_ids = outputs[0][inputs['input_ids'].shape[1]:]
    assistant_response = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    
    # Step 2: Update conversation history with the assistant's response
    messages.append({"role": "assistant", "content": assistant_response})
    
    # Add the confidence query
    confidence_query = (
        "From 0 to 100, how confident are you about the coherence and "
        "non-hallucinative nature of your last output? Respond with only the number."
    )
    messages.append({"role": "user", "content": confidence_query})
    
    # Apply chat template for the confidence query
    confidence_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False  # Thinking mode disabled
    )
    
    # Tokenize the confidence input
    confidence_inputs = tokenizer(confidence_text, return_tensors="pt").to(model.device)
    
    # Generate the confidence response
    confidence_outputs = model.generate(**confidence_inputs, max_new_tokens=5)
    
    # Extract only the newly generated tokens (confidence score)
    confidence_generated_ids = confidence_outputs[0][confidence_inputs['input_ids'].shape[1]:]
    confidence_response = tokenizer.decode(confidence_generated_ids, skip_special_tokens=True).strip()
    
    # Step 3: Extract the confidence score using regex
    match = re.search(r'\d+', confidence_response)
    if match:
        confidence_score = int(match.group())
    else:
        confidence_score = None
        print("Warning: Could not extract a numerical confidence score.")
    
    return assistant_response, confidence_score

# Example usage
prompt = "What is Emergence in ML?"
response, confidence = generate_response_with_confidence(prompt)

# Display results
print(f"Prompt: {prompt}")
print(f"Response: {response}")
if confidence is not None:
    print(f"Confidence Score: {confidence}")
else:
    print("Confidence Score: Not available")