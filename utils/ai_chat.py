import requests

def get_ai_reply(user_message):
    try:
        # Example free AI API or mock response
        response = requests.get(f"https://api.popcat.xyz/chatbot?msg={user_message}&owner=TitanBot&botname=TitanAI")
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Sorry, I didn't understand that.")
        else:
            return "Hmm… I couldn't fetch a reply right now."
    except Exception as e:
        return f"Error: {str(e)}
