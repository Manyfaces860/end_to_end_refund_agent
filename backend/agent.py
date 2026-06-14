from agents import Agent, OpenAIChatCompletionsModel
from constants import MODEL_NAME
from prompts import *
from setup import client
from tools import *
from schema import *
from guardrails import refund_input_guardrail, refund_output_guardrail, GuardrailFunctionOutput

# =========================================================
# REFUND AGENT
# =========================================================

refund_agent = Agent(
    name="RefundAgent",
    instructions=REFUND_AGENT_PROMPT,
    output_type=RefundAgentOutput,
    tools = [
        find_customer,
        find_order_by_order_number,
        find_order_by_customer_email,
        search_refund_policy,
        create_refund_decision,
    ],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    input_guardrails=[
        refund_input_guardrail,
    ],
    output_guardrails=[
        refund_output_guardrail,
    ],
)

def fallback(output: GuardrailFunctionOutput, session_key: str):
    # RefundAgentOutput(
    #     decision='escalate',
    #     customer_message=(
    #         "Your request requires additional review "
    #         "by our support team."
    #     ),
    #     reasoning_summary=f"Output guardrail triggered: {error}",
    #     conversation_summary=None,
    #     refund_amount=None,
    #     restocking_fee=None
    # )
    
    return {
        "message": f"Your request requires additional review by our support team. reason: {output.output_info['reason']}",
        "refund": "escalate",
        "session_key": session_key
    }
