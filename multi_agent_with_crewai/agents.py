import os
from crewai import Agent
from tools import yt_tool
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'



#create a blog content reseacher
blog_researcher = Agent(
    role='Blog Reseacher from Youtube videos',
    goal='get the relevant video transcription for the topic {topic} from the youtube channel',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos in AI Data Science , MAchine Learning And GEN AI and providing suggestion"
    ),
    tools=[yt_tool],
    allow_delegation=True,
)

#create a blog writer agent with YT tool
blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YT video',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False,
)
