from langchain.agents import AgentState, create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch


def get_response_from_agent(
    llm_id: str, human_query: str, allow_websearch: bool, system_prompt: str = None
):

    llm = ChatGroq(model=llm_id)

    tools = [TavilySearch(max_results=2)] if allow_websearch else []

    agent = create_agent(llm, tools=tools, system_prompt=system_prompt)

    state: AgentState = {"messages": [HumanMessage(content=human_query)]}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [
        message.content for message in messages if isinstance(message, AIMessage)
    ]

    return ai_messages[-1]
