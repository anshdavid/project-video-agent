from __future__ import annotations as _annotations

import asyncio
import json
import os
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from rich.prompt import Prompt

from pydantic_graph.persistence.file import FileStatePersistence
from pydantic_ai import Agent, format_as_xml


from pydantic_graph import (
    BaseNode,
    End,
    Graph,
    GraphRunContext,
)

from models import DirectorEdit, Inceptions, POVGenState, Scripts

with open(r"key", "r", encoding="utf-8") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()

INCEPTION_PROMPT = ""
with open(r"prompts/1. inception.md", "r", encoding="utf-8") as file:
    INCEPTION_PROMPT = file.read()

WRITER_PROMPT = ""
with open(r"prompts/2. writer.md", "r", encoding="utf-8") as file:
    WRITER_PROMPT = file.read()

PRODUCER_PROMPT = ""
with open(r"prompts/3. director.md", "r", encoding="utf-8") as file:
    PRODUCER_PROMPT = file.read()


inception_agent = Agent("openai:gpt-4o", result_type=Inceptions, instrument=True, system_prompt=INCEPTION_PROMPT)

writer_agent = Agent("openai:o3-mini", result_type=Scripts, instrument=True, system_prompt=WRITER_PROMPT)

director_agent = Agent("openai:gpt-4o", result_type=DirectorEdit, instrument=True, system_prompt=PRODUCER_PROMPT)


@dataclass
class UserPrompt(BaseNode[POVGenState, None, str]):
    async def run(self, ctx: GraphRunContext[POVGenState]) -> InceptionNode:
        question_ = Prompt.ask("Instructions")
        ctx.state.user_prompt = question_
        # gaurdrail
        return InceptionNode(question_)


@dataclass
class InceptionNode(BaseNode[POVGenState]):
    user_prompt: str

    async def run(self, ctx: GraphRunContext[POVGenState]) -> WriterNode:
        result = await inception_agent.run(self.user_prompt, message_history=ctx.state.inception_agent_messages)
        ctx.state.inception_agent_messages = result.all_messages()
        ctx.state.inceptions = result.data
        return WriterNode(result.data)


@dataclass
class WriterNode(BaseNode[POVGenState]):
    ideas: Inceptions

    async def run(self, ctx: GraphRunContext[POVGenState]) -> DirectorNode:
        result = await writer_agent.run(
            format_as_xml.format_as_xml(
                {
                    "Instruction": "convert the ideas to production ready scripts",
                    "ideas": self.ideas.model_dump_json(),
                },
                include_root_tag=False,
            ),
            message_history=ctx.state.writer_agent_messages,
        )
        ctx.state.writer_agent_messages = result.all_messages()
        return DirectorNode(result.data)


@dataclass
class DirectorNode(BaseNode[POVGenState, None, str]):
    scripts: Scripts

    async def run(self, ctx: GraphRunContext[POVGenState]) -> End[str]:
        result = await director_agent.run(
            format_as_xml.format_as_xml(
                {
                    "Instruction": "convert the scripts to video storyboard. Provided a trailing list of ideas and user prompt used earlier",
                    "scripts": self.scripts.model_dump_json(),
                    "ideas": ctx.state.inceptions,
                    "original_user_prompt": ctx.state.user_prompt,
                }
            ),
            message_history=ctx.state.director_agent_messages,
        )
        ctx.state.director_agent_messages = result.all_messages()

        file = rf"./storyboard/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"

        with open(file, "w") as f:
            json.dump(result.data.model_dump(), f)

        return End("done!")


question_graph = Graph(nodes=(UserPrompt, InceptionNode, WriterNode, DirectorNode), state_type=POVGenState)


async def main():
    file = rf"./state-history/{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"

    persistence = FileStatePersistence(Path(file))
    persistence.set_graph_types(question_graph)

    state = POVGenState()
    node = UserPrompt()

    async with question_graph.iter(node, state=state, persistence=persistence) as run:
        while True:
            node = await run.next()
            if isinstance(node, End):
                break


asyncio.run(main())
