from crewai import Crew, Process
from agents import blog_writer, blog_researcher
from tasks import research_task, writing_task

#forming the tech-focused crew with some enhenced configurations
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

#start the task execution process
res = crew.kickoff(inputs={'topic':'AI VS ML VS DL vs Data Science'})
print(res)