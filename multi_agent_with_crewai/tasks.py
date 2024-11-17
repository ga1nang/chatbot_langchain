from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

#research task
research_task = Task(
    description=(
        "Identify the video {topic}."
        "Get detailed information about the video from the channel video."
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',
    tools=[yt_tool],
    agent=blog_researcher,
)


#writing task with language model
writing_task = Task(
    description=(
        "get the info from the youtube channel on the topic {topic}."
    ),
    expected_output='Summarize the info from the youtube channel video on the topic{topic} and create the content for the blog',
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file='multi_agent_with_crewai/new_blog_post.md'
)