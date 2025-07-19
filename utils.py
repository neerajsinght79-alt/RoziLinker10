import requests

# Dummy movie search function
def get_movie_results(query):
    # Normally you'd fetch from @Premiummovies0_bot or a database
    # For demo purposes:
    return [
        {"title": f"{query} HD", "quality": "1080p", "file_id": "FILE_ID_1080"},
        {"title": f"{query} HD", "quality": "720p", "file_id": "FILE_ID_720"},
    ]


# ShrinkMe shortlink generator
def generate_verification_link(user_id, file_id):
    api_key = "32974302f4ff563e2a8a47e2b60c1e2e8161c503"
    url_to_shorten = f"https://t.me/rozimoviebot?start=verify_{user_id}_{file_id}"
    res = requests.get(f"https://shrinkme.io/api?api={api_key}&url={url_to_shorten}")
    data = res.json()
    return data["shortenedUrl"]


# Dummy in-memory store
user_verification_status = {}

def verify_user(user_id):
    # In production, check actual verification status
    # For now we assume they are verified after clicking link
    if str(user_id) in user_verification_status:
        return True, user_verification_status[str(user_id)]
    return False, None


def send_movie_file(bot, chat_id, file_id):
    return bot.send_document(chat_id, file_id)
