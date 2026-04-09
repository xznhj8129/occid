### Actor

[variants] by nature:
- PERSON: Person
- AGENT: Agent

#### Person

[facets]:
- role (string)
- specialty / MOS (string)
- rank (string)

#### Agent

[variants] by type:
- LLM: LLMAgent
- VISION: VisionAgent
- PLANNING: PlanningAgent
- CONTROL: ControlAgent
- FUSION: FusionAgent
- CLASSIFICATION: ClassificationAgent

[facets]:
- model identifier
- capability set (inference types)
- context capacity
- tool manifest (available actions)

[enum] AgentInferenceType:
- Text
- Vision
- Multimodal
- ToolUse
- Code

[enum] AgentSessionState:
- Active
- Suspended
- Terminated

AgentCapability [facets]:
- inference types (AgentInferenceType)
- context capacity
- response latency target

AgentConfiguration [facets]:
- model identifier
- prompt / instruction set reference
- tool manifest
- temperature
- constraints

AgentSession [facets]:
- session identifier
- agent reference
- start time
- token count
- session state (AgentSessionState)

