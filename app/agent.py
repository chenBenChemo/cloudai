from google.adk import Agent
from google.adk.agents import SequentialAgent, ParallelAgent
from .tools import get_customer_history, analyze_damage_image

# Sub-Agents
history_agent = Agent(name="history_checker", tools=[get_customer_history])
vision_agent = Agent(name="vision_analyst", tools=[analyze_damage_image])

# Investigator Team (Parallel)
investigator = ParallelAgent(
    name="investigator",
    sub_agents=[history_agent, vision_agent]
)

# Final Decision Agent
decision_maker = Agent(name="decision_maker", instruction="Decide: REFUND or DENY.")

# Root Orchestrator
root_agent = SequentialAgent(name="root", sub_agents=[investigator, decision_maker])
