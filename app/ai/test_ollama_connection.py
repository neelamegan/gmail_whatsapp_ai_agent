
import ollama

MODEL_NAME = "qwen2.5:3b"


def test_ollama_connection():
    print("Connecting Python to Ollama...")

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": (
                    "Reply with exactly: "
                    "Python connected successfully!"
                ),
            }
        ],
    )

    answer = response.message.content

    print("\nLLM Response:")
    print(answer)

    assert answer.strip(), "The model returned an empty response."

    print("\nPython and Ollama integration is working!")


if __name__ == "__main__":
    test_ollama_connection()
