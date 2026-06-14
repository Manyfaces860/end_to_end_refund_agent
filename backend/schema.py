from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal


# =========================================================
# ENUM / CONTROL TYPES
# =========================================================

ContinuityDecision = Literal[
    "continuation",
    "intent_drift",
]

RefundDecision = Literal["approved", "denied", "escalate", "needs_more_information"]

# =========================================================
#  REFUND AGENT OUTPUT
# =========================================================

class RefundAgentOutput(BaseModel):

    decision: RefundDecision
    customer_message: str
    reasoning_summary: str
    conversation_summary: Optional[str]
    refund_amount: Optional[float]
    restocking_fee: Optional[float]

# =========================================================
# CHAT SESSION
# =========================================================

class ChatSessionRuntime(BaseModel):

    query: str
    recent_messages: List[Dict[str, str]] = []
    conversation_summary: str = "No prior summary available."
    refund_resolved: bool = False
    session_key: str
    
class InputGuardrailOutput(BaseModel):
    is_safe: bool = Field(
        description="Whether the user input is safe to process."
    )

    reason: str = Field(
        description="Short explanation for the decision."
    )

    category: Optional[str] = Field(
        default=None,
        description=(
            "Type of violation if unsafe. "
            "Examples: prompt_injection, policy_override, "
            "system_prompt_extraction, unrelated_request."
        )
    )
    
class OutputGuardrailOutput(BaseModel):
    is_valid: bool = Field(
        description="Whether the final RefundAgentOutput is valid."
    )

    reason: str = Field(
        description="Short explanation for the validation result."
    )

    category: Optional[str] = Field(
        default=None,
        description=(
            "Type of violation if invalid. "
            "Examples: policy_violation, "
            "reasoning_leakage, invalid_fields, "
            "hallucinated_data."
        )
    )
    
class TestRefundAgentOutput(BaseModel):
    decision: str = Field(
        description="Refund decision."
    )
    customer_message: str = Field(
        description="Message shown to the customer."
    )
    reasoning_summary: str = Field(
        description="Internal summary."
    )
    refund_amount: Optional[float] = None
    restocking_fee: Optional[float] = None