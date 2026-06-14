import dis

from agents import function_tool
from db_models import *
from logger import logger, logging
from constants import INDEX_NAME, NAMESPACE, TOP_K
from setup import pc
from embedding import get_embedding
from pinecone import QueryResponse

@function_tool(
    description_override="""
    Search the refund/return policy knowledge base.

    Use this tool only when policy information is needed to decide a refund.
    Good queries are specific, such as:
    - "standard refund window"
    - "Black November refund window"
    - "opened electronics refund eligibility"
    - "final sale refund policy"
    - "damaged by customer refund policy"

    Do not call this repeatedly for the same policy topic if the needed policy text
    is already available in the conversation or previous tool result.
    """
)
def search_refund_policy(query: str) -> str:
    logger.log(level=logging.INFO, msg='getting context from vdb')
    index = pc.Index(INDEX_NAME)
    
    dense_query_embedding, sparse_query_embedding = get_embedding(query, "query")
    results: QueryResponse = QueryResponse()
    for d, s in zip(dense_query_embedding, sparse_query_embedding):
        query_response = index.query(
            namespace=NAMESPACE,
            top_k=TOP_K,
            vector=d['values'],
            sparse_vector={'indices': s['sparse_indices'], 'values': s['sparse_values']},
            include_values=False,
            include_metadata=True
        )
        results = query_response

    context = ""
    logger.log(level=logging.INFO, msg=f"results: {results}")
    for hits in results.matches:
        assert hits.metadata is not None
        context += "\n" + str(hits.metadata.get('text', ''))
    return context

@function_tool
def search_returns_db(query: str) -> str:
    return f"Retrieved refund docs for: {query}"

@function_tool
def calculate_refund_amount():
    pass

@function_tool(
    description_override="""
    Find an order by exact order number.

    Use this as the primary database lookup when the user provides an order ID/order number.
    This returns order details and may also include linked customer details.

    Do not call find_customer after this tool if the returned order already contains
    complete customer information such as name, email, tier, abuse flag, and notes.

    If no order is found, ask the user to verify the order number instead of guessing.
    """
)
async def find_order_by_order_number(order_number: str):
    try:
        order = await Order.find_one(Order.order_number == order_number, fetch_links=True)
    
        if not order:
            return {
                "found": False,
                "message": "Order not found"
            }

        return {
            "found": True,
            "customer_included": order.customer is not None,
            "order": order.model_dump(mode="json")
        }
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"Error occurred while fetching order details: {e}")
        return "could not return order details, something happened"

@function_tool(
    description_override="""
    Find an order using the customer's email address.

    Use this only when the user does not provide an order number but provides an email.
    If multiple orders may exist for the same customer, do not assume which one is relevant;
    ask the user for the order number or product details.

    Do not call this if find_order_by_order_number already returned the relevant order.
    """
)
async def find_order_by_customer_email(customer_email: str):
    try:
        order = await Order.find_one(Order.customer_email == customer_email)
        if not order:
            return {
                "found": False,
                "message": "Order not found"
            }

        return {
            "found": True,
            "customer_included": order.customer is not None,
            "order": order.model_dump(mode="json")
        }
        
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"Error occurred while fetching order details: {e}")
        return "could not return order details, something happened"

@function_tool(
    description_override="""
    Find customer details by customer email.

    Use this only when customer details are missing from the available order data.

    Call this tool only if:
    - the order result has no customer object
    - the order result only has customer_email
    - customer abuse flag, tier, notes, or account information is required but missing
    - there is a conflict in customer data that needs verification

    Do not call this after find_order_by_order_number if the order already includes
    complete customer details.
    """
)
async def find_customer(customer_email: str):
    try:
        customer = await Customer.find_one(Customer.email == customer_email)
        return customer.model_dump_json() if customer else "could not return customer details, something happened"
    
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"Error occurred while fetching customer details: {e}")
        return "could not return customer details, something happened"

@function_tool(
    description_override="""
    update the final refund decision for an order.

    Use this only after:
    - the relevant order has been found
    - required customer information has been checked
    - relevant refund policy has been retrieved
    - the refund decision is clear

    Do not use this tool for NEEDS_MORE_INFORMATION unless the workflow explicitly
    requires saving incomplete decisions.

    The reason should be concise and based only on verified order, customer, and policy data.
    """
)
async def create_refund_decision(order_number: str, decision: refund_decision, reason: str, refund_amount: Optional[float], requires_human_review: bool):
    try:
        order = await Order.find_one(Order.order_number == order_number)
        if not order:
            return "could not find the order to create refund decision, something happened"
        
        refund_decision = RefundDecision(
            decision=decision,
            reason=reason,
            refund_amount=refund_amount,
            requires_human_review=requires_human_review
        )
        order.refund_decision = refund_decision
        await order.save()
        return f"Refund decision for order {order_number} has been created/updated successfully."
    
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"Error occurred while creating/updating refund decision: {e}")
        return "could not create/update refund decision, something happened"
    

tools = [
    find_customer,
    find_order_by_order_number,
    find_order_by_customer_email,
    search_refund_policy,
    create_refund_decision,
]