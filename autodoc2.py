import openai
import re
import flask

# Set the OpenAI API key
openai.api_key = "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"

# Function to add inline comments to a Python script
def add_comments(code):
    # Use the OpenAI API to generate comments
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Modify this Python script so that it includes inline comments explaining what's going on, with the first comment starting at the top of the code:\n{code}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Get the first completion from the API response
    comment_text = completions.choices[0].text

    # Split the completion into individual lines
    comment_lines = comment_text.split("\n")

    # Split the code into lines
    code_lines = code.split("\n")

    # Initialize an empty list to store the commented lines
    commented_lines = []

    # Iterate over the lines of code
    for i, line in enumerate(code_lines):
        # Add the line of code to the list
        commented_lines.append(line)

        # If there is a comment for this line, add it to the list
        if i < len(comment_lines) and comment_lines[i].strip() != "":
            commented_lines.append("# " + comment_lines[i])

    # Join the commented lines and return the commented code
    return "\n".join(commented_lines)


# Initialize the Flask app
app = flask.Flask(__name__)

# Add the Access-Control-Allow-Origin header to the response
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Define the route for the API endpoint
@app.route("/add-comments", methods=["POST"])
def add_comments_api():
    # Get the code from the request data
    code = flask.request.data.decode("utf-8")

    # Add inline comments to the code
    commented_code = add_comments(code)

    # Return the commented code as the response
    return commented_code

# Run the Flask app
if __name__ == "__main__":
    app.run(port=4000)