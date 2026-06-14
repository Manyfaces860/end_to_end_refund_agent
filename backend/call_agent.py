from agents import Runner, OutputGuardrailTripwireTriggered, InputGuardrailTripwireTriggered
from constants import MAX_MESSAGES_THRESHOLD
from logger import logger
from agent import *
from chat_session import ChatSession
import asyncio


async def agent_loop(query, session_key):

    logger.info(f"Received query: {query} with session key: {session_key}")

    # prepare user input to give query and session context to the agent
    session = ChatSession(query=query, chat_session_key=session_key)
    chat_session = session.chat_session
    logger.info(f"Current chat session state: {chat_session}")

    chat_session.recent_messages.append({"role": "user", "content": query})
    
    if len(chat_session.recent_messages) < MAX_MESSAGES_THRESHOLD-1:
        agent_input = session.get_agent_input()
        logger.info(f"Using full input: {agent_input}")
    else:
        agent_input =  session.get_agent_input(summarise='YES')
        logger.info(f"Using summarised input: {agent_input}")

    try:
        logger.info("Invoking agent...")
        result = await Runner.run(refund_agent, input=agent_input, max_turns=10)
    except InputGuardrailTripwireTriggered or OutputGuardrailTripwireTriggered as e:
        logger.error(f"Error during agent execution: {e, e.guardrail_result.output.output_info['reason']}")
        return fallback(e.guardrail_result.output, session.chat_session.session_key)
    finally:
        pass
    
    output: RefundAgentOutput = result.final_output
    # TESTING
    # output = RefundAgentOutput(
    #     decision="needs_more_information",
    #     customer_message="i am here",
    #     reasoning_summary="i am thinnking",
    #     conversation_summary= "summary updated" if len(chat_session.recent_messages) >= MAX_MESSAGES_THRESHOLD - 1 else None,
    #     refund_amount=None,
    #     restocking_fee=None,
    # )
    
    logger.info(f"Agent output: {output}")
    
    chat_session.recent_messages.append({"role": "agent", "content": output.customer_message})
    
    if len(chat_session.recent_messages) >= MAX_MESSAGES_THRESHOLD-1:
        session.update_recent_messages_buffer()
        logger.info(f"Updated recent messages buffer: {chat_session.recent_messages}")
        
    if output.conversation_summary:
        chat_session.conversation_summary = output.conversation_summary
        logger.info(f"Updated conversation summary: {output.conversation_summary}")
        
        print(session.chat_session)
        
    session.update_state()
    logger.info(f"Updated session state: {chat_session}")
    return {
        "message": output.customer_message,
        "refund": "pending" if output.decision == "needs_more_information" else output.decision,
        "session_key": session.chat_session.session_key
    }


if __name__ == "__main__":
    asyncio.run(agent_loop('I bought an AuraPulse Pro last week and I want to return it. Can I?', 'user_2'))