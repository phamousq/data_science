# %% 
import ollama

response = ollama.chat(model='llama2', messages=[
    {
        "role": "user",
        "content": "What is the capital of France?"
    }
])
print(response)

# %%
response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'export the content of the image in markdown format with all of the text in the image',
        'images': ['SCR-20241121-nsol.png']
    }]
)

print(response)
# %%
