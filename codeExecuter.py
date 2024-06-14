#!/usr/bin/env python
# coding: utf-8

import tempfile

from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

temp_dir = tempfile.TemporaryDirectory()
executor = LocalCommandLineCodeExecutor(timeout=10, work_dir=temp_dir.name)
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
)

message_with_code_block = """This is a message with code block.
The code block is below:
```python
import numpy as np
import matplotlib.pyplot as plt
x = np.random.randint(0, 100, 100)
y = np.random.randint(0, 100, 100)
plt.scatter(x, y)
plt.savefig('scatter.png')
print('Scatter plot saved to scatter.png')
```
This is the end of the message.
"""

reply = code_executor_agent.generate_reply(
    messages=[{"role": "user", "content": message_with_code_block}]
)
print(reply)

import os

print(os.listdir(temp_dir.name))
temp_dir.cleanup()
