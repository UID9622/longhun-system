# google/tunix：JAX 原生的 LLM 后训练库

> Notion URL: https://app.notion.com/p/google-tunix-JAX-LLM-2807125a9c9f81b2919bf41b3224963d
> Created: 2025-10-02T12:53:00.000Z
> Last edited: 2026-07-01T13:25:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
https://github.com/google/tunix
# Tunix: A JAX-native LLM Post-Training Library
Tunix(Tune-in-JAX) is a JAX based library designed to streamline the post-training of Large Language Models. It provides efficient and scalable supports for:
- Supervised Fine-Tuning
- Reinforcement Learning (RL)
- Knowledge Distillation
Tunix leverages the power of JAX for accelerated computation and seamless integration with JAX-based modeling framework Flax NNX.
Current Status: Early Development
Tunix is in early development. We're actively working to expand its capabilities, usability and improve its performance. Stay tuned for upcoming updates and new features!
## Key Features & Highlights
Tunix is still under development, here's a glimpse of the current features:
- Supervised Fine-Tuning: 
- Reinforcement Learning (RL): 
- Preference Fine-Tuning: 
- Knowledge Distillation: 
- Modularity: 
- Efficiency: 
## Upcoming
- Agentic RL Training: 
- Advanced Algorithms: 
- Scalability: 
- User Guides: 
## Installation
You can install Tunix in several ways:
1. From PyPI (recommended):
```plain text
pip install "tunix[prod]"
```
1. Directly from GitHub (latest main branch)
```plain text
pip install git+https://github.com/google/tunix
```
1. From source (editable install) If you plan to modify the codebase and run it in development mode:
```plain text
git clone https://github.com/google/tunix.git
cd tunix
pip install -e ".[dev]"

```
## Getting Started
To get started, we have a bunch of detailed examples and tutorials.
- PEFT Gemma with QLoRA
- Training Gemma on grade school Math problems using GRPO
- Logit Distillation using Gemma models
To setup Jupyter notebook on single host GCP TPU VM, please refer to the setup script.
We plan to provide clear, concise documentation and more examples in the near future.
## Contributing and Feedbacks
We welcome contributions! As Tunix is in early development, the contribution process is still being formalized. A rough draft of the contribution process is present here. In the meantime, you can make feature requests, report issues and ask questions in our Tunix GitHub discussion forum.
## Collaborations and Partnership
GRL (Game Reinforcement Learning), developed by Hao AI Lab from UCSD, is an open-source framework for post-training large language models through multi-turn RL on challenging games. In collaboration with Tunix, GRL integrates seamless TPU support—letting users quickly run scalable, reproducible RL experiments (like PPO rollouts on Qwen2.5-0.5B-Instruct) on TPU v4 meshes with minimal setup. This partnership empowers the community to push LLM capabilities further, combining Tunix’s optimized TPU runtime with GRL’s flexible game RL pipeline for cutting-edge research and easy reproducibility.
## Stay Tuned!
Thank you for your interest in Tunix. We're working hard to bring you a powerful and efficient library for LLM post-training. Please follow our progress and check back for updates!
## Acknowledgements
Thank you to all our wonderful contributors!
