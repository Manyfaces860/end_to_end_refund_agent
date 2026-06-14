from agents import input_guardrail, GuardrailFunctionOutput, output_guardrail, Runner, Agent, OpenAIChatCompletionsModel
from prompts import REFUND_INPUT_GUARDRAIL_PROMPT, REFUND_OUTPUT_GUARDRAIL_PROMPT
from constants import MODEL_NAME
from setup import client
from schema import InputGuardrailOutput, OutputGuardrailOutput

# =========================================================
# INPUT GUARDRAIL AGENT
# =========================================================

input_guardrail_agent = Agent(
    name="InputGuardrailAgent",
    instructions=REFUND_INPUT_GUARDRAIL_PROMPT,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=InputGuardrailOutput,
)

# =========================================================
# OUTPUT GUARDRAIL AGENT
# =========================================================

output_guardrail_agent = Agent(
    name="OutputGuardrailAgent",
    instructions=REFUND_OUTPUT_GUARDRAIL_PROMPT,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=OutputGuardrailOutput,
)

@input_guardrail
async def refund_input_guardrail(
    _ctx,
    _agent,
    input,
) -> GuardrailFunctionOutput:

    result = await Runner.run(
        input_guardrail_agent,
        input=input,
    )

    output: InputGuardrailOutput = result.final_output

    return GuardrailFunctionOutput(
        output_info=output.model_dump(),
        tripwire_triggered=not output.is_safe,
    )

@output_guardrail
async def refund_output_guardrail(
    _ctx,
    _agent,
    output,
) -> GuardrailFunctionOutput:

    result = await Runner.run(
        output_guardrail_agent,
        input=output.model_dump_json(),
    )

    validation: OutputGuardrailOutput = result.final_output

    return GuardrailFunctionOutput(
        output_info=validation.model_dump(),
        tripwire_triggered=not validation.is_valid,
    )

