from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from langchain.tools import Tool
import os
from dotenv import load_dotenv
import yaml
from crewai.project import CrewBase, agent, crew, task
from langchain_community.tools import DuckDuckGoSearchRun

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ManoonCrew():
	"""ManoonCrew crew"""
	
	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"
	
	def __init__(self):
		load_dotenv()
		self.llm = LLM(
			model="deepseek/deepseek-reasoner",
			api_key=os.getenv("DEEPSEEK_API_KEY"),
			temperature=0.7,
			base_url="https://api.deepseek.com/v1"
		)
		self.search_tool = DuckDuckGoSearchRun()
	
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[Tool(
				name="Search Tool",
				func=lambda x: self.search_tool.run(str(x)),  # Convert input to string
				description="Searches the web using DuckDuckGo. Input should be a search query string."
			)],
			llm=self.llm
		)
	
	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True,
			tools=[Tool(
				name="Search Tool",
				func=lambda x: self.search_tool.run(str(x)),  # Convert input to string
				description="Searches the web using DuckDuckGo. Input should be a search query string."
			)],
			llm=self.llm
		)
	
	@task
	def keyword_research(self) -> Task:
		return Task(
			config=self.tasks_config['keyword_research'],
			agent=self.researcher()
		)
	
	@task
	def content_writing(self) -> Task:
		return Task(
			config=self.tasks_config['content_writing'],
			agent=self.writer()
		)
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,  # Automatically created by @agent decorator
			tasks=self.tasks,    # Automatically created by @task decorator
			process=Process.sequential,
			verbose=True
		)
