from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext, WorkerOptions,
    cli, llm
)

from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import google, openai
from dotenv import load_dotenv
from api import AssistanceFnc
import os

load_dotenv()


async  def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe = AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        instrctions = "",
        voice = "shimmer",
        temperatur = 0.8,
        modalities = ["audio", "text"]
    )

    assistant_fun = AssistanceFnc()
    assistant = MultimodalAgent(model = model, fnc_ctx = assistant_fun)
    assistant.start(ctx.rooom)

    session = model.session[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role = "assistant",
            content = ""
        )
    )

    session.response.create()

    if __name__ == "__main__":
        cli.run_app(WorkerOptions(entrypoint_fnc = entrypoint))



    # session = AgentSession(
    # llm = google.LLM(model = "gemini-2.0-flash-001", api_key = "YOUR_GOOGLE_API_KEY"),)
