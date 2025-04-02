import os
import groq

groq_api_key = os.environ.get("GROQ_API_KEY")

client = groq.Client(api_key=groq_api_key)

def query_llm(input_text, video_file=None):
    """
    Handles user queries about workouts. If a video is uploaded, it acknowledges video analysis.
    """
    if video_file:
        return f"Received your workout video ({video_file}). Analyzing your form... (Pose detection coming soon)"
    
    if any(keyword in input_text.lower() for keyword in ["workout", "exercise", "training", "fitness"]):
        input_text = "Give a concise and actionable tip for performing this workout correctly in one sentence."
    
    response = client.chat.completions.create(
        model="Llama-3.3-70b-Versatile",
        messages=[
            {"role": "system", "content": "You are a helpful fitness assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    user_input = "I am performing squats."
    response = query_llm(user_input)
    print("LLaMA Response:", response)
    
    # Simulating video upload
    video_response = query_llm("", video_file="squats.mp4")
    print("LLaMA Video Analysis Response:", video_response)
