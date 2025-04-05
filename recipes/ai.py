import ollama
import json

def get_shopping_list(ingredients: str, model: str = "llama3") -> dict:
    prompt = f"""Convert the following ingredient list into a JSON shopping cart with the format:
{{
  "items": [{{"name": <name>, "quantity": <quantity>}}, ...]
}}

Ensure the quantities are logical for shopping purposes — e.g., if the ingredient is used in small amounts like teaspoons, convert it to a typical purchase unit such as "1 small jar" or "1 bunch".

ALSO MAKE SURE THAT THE RESPONSE IS STRICTLY JSON. DON'T GIVE ANY EXPLAINATIONS.

Ingredient list:
{ingredients}
"""

    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    response_text = stream['message']['content']

    try:
        return json.loads(response_text)
    except Exception as e:
        print("Failed to parse JSON:",e)
        print("Raw response:", response_text)
        return {"error": "Failed to parse model response", "raw": response_text}


# streaming alternative
def alternative_recipe(recipe, alt_type,model = "llama3"):
    prompt = f'''Convert the following recipe into a {alt_type}.
Make sure that this is in the format: <ingredients> blank line <instructions>
{recipe}
'''
    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    for chunk in stream:
        if "content" in chunk.get("message", {}):
            yield chunk["message"]["content"]
