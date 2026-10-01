# Day 4 Task – Will It Fit, and May I Use It?

## 1. My Scenario

I want to run an open-weight AI model locally on my laptop as a personal
coding assistant. The model will be used by me for learning, programming
practice, code explanation and general coding help.

### Machine

- RAM: 8 GB
- GPU: No dedicated GPU
- Memory budget: 8 GB
- Purpose: Personal coding assistant
- Users: Myself
- Operating environment: Windows laptop

### Licensing Situation

The intended use is personal/student use. However, the licence must still be
checked before using a model in a public project, redistributing it, or using
it commercially.

I will compare three model families: Qwen, Mistral and IBM Granite.

---

## 2. Model Weights

Model weights are the learned parameters of a language model. The amount of
memory required by the weights depends mainly on the number of parameters and
the number of bytes used to store each parameter.

The formula used in this task is:

Weights (GB) = Parameters in billions × Bytes per parameter

For example, an 8B model using Q4_K_M requires approximately:

8 × 0.57 = 4.56 GB

An FP16 version of the same 8B model requires:

8 × 2.00 = 16.00 GB

Therefore, increasing the parameter count increases memory requirements.
Changing the precision or quantization changes the memory required by the
weights.

If the weight memory is underestimated, the model may not fit into the
available memory even before considering the KV cache and runtime overhead.

---

## 3. Quantization

Quantization stores model parameters using fewer bits or bytes.

The bytes-per-parameter values used in this task are:

| Precision | Bytes per parameter |
|---|---:|
| FP16 | 2.00 |
| Q8_0 | 1.00 |
| Q6_K | 0.81 |
| Q5_K_M | 0.68 |
| Q4_K_M | 0.57 |
| Q3_K_M | 0.43 |

Q4_K_M is useful for local models because it requires much less memory than
FP16. However, lower-bit quantization can introduce some quality loss.

For example, for an 8B model:

- FP16 weights = 16.00 GB
- Q8_0 weights = 8.00 GB
- Q5_K_M weights = 5.44 GB
- Q4_K_M weights = 4.56 GB
- Q3_K_M weights = 3.44 GB

Therefore, quantization is mainly important for the memory-fit decision.

If quantization is ignored, I may select a model whose full-precision version
cannot fit on my laptop.

---

## 4. KV Cache and Context Length

The KV cache stores information from previous tokens so that the model can
continue processing a conversation without recomputing everything.

The approximate formula used in this task is:

KV Cache (GB) = Parameters in billions × Context in K tokens × 0.02

Unlike the model weights, the KV cache grows as the context length grows.

For example, for an 8B model:

At 4K context:

8 × 4 × 0.02 = 0.64 GB

At 8K context:

8 × 8 × 0.02 = 1.28 GB

At 32K context:

8 × 32 × 0.02 = 5.12 GB

Therefore, a model can fit at a short context but stop fitting at a longer
context.

This is particularly important for an AI coding assistant or an agent because
the conversation can become longer as more code, instructions and tool
results are added.

---

## 5. Memory Formula

The complete estimate used in the Day 4 lab is:

Weights = Parameters × Bytes per parameter

KV Cache = Parameters × Context(K) × 0.02

Total = (Weights + KV Cache) × 1.10

The 1.10 factor represents approximately 10% additional runtime overhead,
activations and fragmentation.

These calculations are estimates. They are intended to decide whether a model
is likely to fit rather than predict actual memory usage to the exact
megabyte.

Actual memory usage can differ because of model architecture, runtime,
context defaults, memory reservation and other implementation details.

---

## 6. Memory Estimate Table

My available memory is 8 GB.

The following table uses the Day 4 estimation formula.

| Model | Parameters | Quantization | Context | Weights | KV Cache | Total | Fits in 8 GB? |
|---|---:|---|---:|---:|---:|---:|---|
| Small model | 1.5B | Q4_K_M | 8K | 0.85 GB | 0.24 GB | 1.20 GB | Yes |
| 8B model | 8.0B | Q4_K_M | 8K | 4.56 GB | 1.28 GB | 6.42 GB | Yes, but tight |
| 8B model | 8.0B | FP16 | 8K | 16.00 GB | 1.28 GB | 19.01 GB | No |
| 30B model | 30.0B | Q4_K_M | 8K | 17.10 GB | 4.80 GB | 24.09 GB | No |

The 1.5B Q4_K_M model leaves substantial memory available for the operating
system and other applications.

The 8B Q4_K_M model has an estimated requirement of about 6.42 GB at 8K
context. It therefore fits according to the formula, but the remaining memory
is limited.

The 8B FP16 and 30B Q4_K_M configurations do not fit within an 8 GB memory
budget.

---

## 7. Model Comparison

I compared three different model families:

1. Qwen
2. Mistral
3. IBM Granite

The model-card and Ollama information was checked on 1 October 2026.

### Model 1 – Qwen3-8B

- Full model name: Qwen3-8B
- Publisher: Qwen / Alibaba
- Parameters: 8.2B
- Model type: Dense
- Native context length: 32,768 tokens
- Extended context: 131,072 tokens with YaRN
- Licence: Apache License 2.0
- Commercial use: Permitted under the Apache 2.0 licence, subject to its
  conditions
- Tool calling: Supported; the model card describes agent capabilities and
  integration with external tools
- Ollama availability: Yes
- Ollama Q4_K_M size: 5.2 GB
- Ollama Q4_K_M context listing: 40K
- Model selected for memory estimate: Q4_K_M

The Qwen3-8B model card states that the model has 8.2B parameters and a
32,768-token native context length. It also describes extension to 131,072
tokens using YaRN. The model card lists Apache 2.0 as the licence.

### Model 2 – Mistral-7B-Instruct-v0.3

- Full model name: Mistral-7B-Instruct-v0.3
- Publisher: Mistral AI
- Parameters: approximately 7.2B
- Model type: Dense
- Context window: 32,768 tokens
- Licence: Apache License 2.0
- Commercial use: Permitted under the Apache 2.0 licence, subject to its
  conditions
- Tool calling: Yes, function calling is documented on the model card
- Ollama availability: Yes
- Ollama Q4_K_M size: approximately 4.4 GB
- Model selected for memory estimate: Q4_K_M

The Mistral model card states that Mistral-7B-Instruct-v0.3 supports function
calling. It is released under Apache 2.0 and has a 32,768-token context
window.

### Model 3 – IBM Granite-3.3-8B-Instruct

- Full model name: Granite-3.3-8B-Instruct
- Publisher: IBM Granite Team / IBM
- Parameters: approximately 8B
- Model type: Dense
- Context window: 128,000 tokens
- Licence: Apache License 2.0
- Commercial use: Permitted under the Apache 2.0 licence, subject to its
  conditions
- Tool calling: Yes; function-calling tasks are listed as a capability
- Ollama availability: Yes
- Ollama Q4_K_M size: approximately 4.9 GB
- Model selected for memory estimate: Q4_K_M

The Granite model card states that Granite-3.3-8B-Instruct is an 8-billion
parameter model with a 128K context length and lists function-calling tasks
among its capabilities.

### Comparison Table

| Basis | Qwen3-8B | Mistral-7B-Instruct-v0.3 | Granite-3.3-8B-Instruct |
|---|---|---|---|
| Publisher | Qwen / Alibaba | Mistral AI | IBM |
| Parameters | 8.2B | ~7.2B | ~8B |
| MoE? | No, dense | No, dense | No, dense |
| Context window | 32K native; 131K with YaRN | 32K | 128K |
| Licence | Apache License 2.0 | Apache License 2.0 | Apache License 2.0 |
| Commercial use | Yes, subject to licence | Yes, subject to licence | Yes, subject to licence |
| Extra conditions | Apache 2.0 conditions | Apache 2.0 conditions | Apache 2.0 conditions |
| Tool/function calling | Yes | Yes | Yes |
| GGUF/Ollama available | Yes | Yes | Yes |
| Ollama Q4_K_M size | 5.2 GB | 4.4 GB | 4.9 GB |
| Date checked | 1 Oct 2026 | 1 Oct 2026 | 1 Oct 2026 |

---

## 8. Memory Estimate for the Compared Models

Using the approximate parameter counts and the same Day 4 formula at Q4_K_M
and 8K context gives:

| Model | Parameters | Q4_K_M Weights | KV Cache at 8K | Estimated Total | Fits 8 GB? |
|---|---:|---:|---:|---:|---|
| Qwen3-8B | 8.2B | ~4.67 GB | ~1.31 GB | ~6.58 GB | Yes, but tight |
| Mistral-7B-Instruct-v0.3 | ~7.2B | ~4.13 GB | ~1.16 GB | ~5.81 GB | Yes |
| Granite-3.3-8B-Instruct | ~8.2B | ~4.66 GB | ~1.31 GB | ~6.56 GB | Yes, but tight |

These are formula-based estimates. They should not be confused with actual
runtime memory measurements.

---

## 9. Context Length Experiment

For this experiment, I kept the model at 8B parameters and Q4_K_M
quantization and changed only the context length.

| Context | Weights | KV Cache | Total | Fits in 8 GB? |
|---:|---:|---:|---:|---|
| 4K | 4.56 GB | 0.64 GB | 5.72 GB | Yes, but tight |
| 8K | 4.56 GB | 1.28 GB | 6.42 GB | Yes, but tight |
| 32K | 4.56 GB | 5.12 GB | 10.65 GB | No |
| 128K | 4.56 GB | 20.48 GB | 27.54 GB | No |

The weights stayed constant at 4.56 GB because the parameter count and
quantization did not change.

The KV cache increased from 0.64 GB at 4K to 20.48 GB at 128K. Therefore,
the total memory requirement increased with context length.

For my 8 GB machine, the largest tested context that fits for this 8B
Q4_K_M estimate is 8K. At 32K the estimated requirement is already above
the available memory.

This demonstrates why long-context agents can require much more memory even
when the model weights remain unchanged.

---

## 10. Quantization Experiment

For this experiment, I kept the model at 8B parameters and the context at 8K
and changed only the quantization.

| Quantization | Weights | KV Cache | Total | Fits in 8 GB? |
|---|---:|---:|---:|---|
| Q3_K_M | 3.44 GB | 1.28 GB | 5.19 GB | Yes |
| Q4_K_M | 4.56 GB | 1.28 GB | 6.42 GB | Yes, but tight |
| Q5_K_M | 5.44 GB | 1.28 GB | 7.39 GB | Yes, but tight |
| Q8_0 | 8.00 GB | 1.28 GB | 10.21 GB | No |
| FP16 | 16.00 GB | 1.28 GB | 19.01 GB | No |

The KV cache remained approximately 1.28 GB because the model size and context
length were unchanged.

The weight memory changed significantly because quantization changes the
number of bytes used for each parameter.

For an 8 GB laptop, Q4_K_M is a reasonable balance for this memory estimate.
Q3_K_M uses less memory, but it gives up more model precision and can cause
more noticeable quality loss. Q5_K_M gives more weight precision but leaves
less memory headroom.

---

## 11. Estimate vs Reality

Ollama is not installed on my laptop. When I tried to run:

    ollama run qwen2.5:1.5b

Windows reported that the `ollama` command was not recognized.

Therefore, I could not honestly record an `ollama list` or `ollama ps`
measurement from my own machine.

The estimate-versus-reality section is therefore limited to the formula-based
estimate in this submission.

If Ollama is later installed or a neighbour's machine is used, the following
comparison can be performed:

    ollama list

This shows the model size on disk.

Then, while a model is running:

    ollama ps

This shows the memory used by the running model and whether it is using the
CPU, GPU or a split between them.

The real runtime value can differ from the formula estimate because of
runtime overhead, context defaults, architecture and other implementation
details.

---

## 12. Open-Weight vs Open-Source

An open-weight model provides access to its model weights, but this does not
automatically mean that every aspect of the model is open-source.

For this task, the exact licence is important because it determines the
conditions under which the model can be used, modified and redistributed.

The three compared models use Apache License 2.0 according to their current
official model cards. Apache 2.0 is a permissive licence, but it still has
conditions such as retaining the licence and applicable notices when
redistributing the software or other covered material.

Therefore, I should not decide whether a model can be used only by looking at
its parameter count or download size. The licence must also be checked.

---

## 13. Model Card

A model card is documentation supplied with a model that describes important
information such as:

- Model name and version
- Publisher
- Parameter count
- Intended use
- Context length
- Capabilities
- Limitations
- Licence
- Tool/function-calling support
- Usage information

I used model cards to identify the licence, context length, parameter count
and capabilities of the three models.

The model card is therefore important for both the technical fit decision and
the permission/licensing decision.

---

## 14. Suitability Analysis

My scenario is a personal coding assistant running on an 8 GB laptop without
a dedicated GPU.

Based on the memory estimate, a small Q4_K_M model has the most memory
headroom. An 8B Q4_K_M model is estimated at about 6.42 GB at 8K context,
which fits within the 8 GB budget according to the formula but leaves only
limited memory for the operating system and other applications.

For the coding-assistant scenario, tool calling is also important because an
agent may need to interact with external tools.

Among the compared models, Qwen3-8B, Mistral-7B-Instruct-v0.3 and
Granite-3.3-8B-Instruct all have documented support related to tool or
function calling. However, their context capabilities differ.

For my 8 GB machine, I would use a Q4_K_M configuration and keep the context
moderate rather than attempting to use the maximum advertised context.

### Recommended configuration

Model: Mistral-7B-Instruct-v0.3

Size: approximately 7.2B parameters

Quantization: Q4_K_M

Context: 8K for my memory experiment

Licence: Apache License 2.0

Estimated memory: approximately 5.81 GB using the Day 4 formula at 8K
context.

The main reason for selecting this configuration for my scenario is that its
estimated memory requirement is lower than the approximately 8B alternatives
while remaining within the memory budget. The model card also documents
function calling, which is relevant to a coding assistant.

### Runner-up

Runner-up: Qwen3-8B at Q4_K_M.

Qwen3-8B has strong documented agent/tool capabilities and a longer native
context than the 8K context used in my experiment. However, its approximately
8.2B parameters give a slightly higher estimated memory requirement than
Mistral-7B-Instruct-v0.3 on my 8 GB machine.

### What would change my choice?

My choice could change if:

1. I had a laptop or server with more memory.
2. I needed a very long context for large documents or long codebases.
3. I required a particular tool-calling feature.
4. I needed to redistribute the model as part of a public project.
5. The licence or its conditions changed.
6. I needed higher model quality and had enough memory to use a larger model
   or higher precision.

---

## 15. Limitations of My Analysis

The memory formula is an approximation and does not predict actual memory use
to the exact megabyte.

The KV-cache formula used in this task assumes a modern grouped-query
attention architecture with an FP16 cache. Different architectures can have
different KV-cache requirements.

The 8 GB figure represents the machine's memory budget used for this
exercise. The operating system and other applications also consume memory,
so an estimate that technically fits into 8 GB may still be impractical if
there is insufficient free memory.

The Ollama runtime comparison could not be completed locally because Ollama
was not installed on my machine.

The model-card and licence information was checked on 1 October 2026 and may
change in the future. Therefore, the licence and capability statements in
this report represent the information available on the date checked.

---

## 16. Conclusion

This task demonstrated that selecting an open model requires considering both
memory fit and permission to use the model.

Model size is important when the available RAM or VRAM is limited. A larger
number of parameters increases the weight memory requirement.

Quantization can reduce weight memory significantly. For example, the 8B
model in this experiment requires about 16 GB for FP16 weights but only about
4.56 GB for Q4_K_M weights. The reduction in memory comes with a possible
quality trade-off.

Context length is also important because the model weights remain unchanged
while the KV cache grows with context. In the experiment, the 8B Q4_K_M
model increased from about 5.72 GB at 4K context to about 27.54 GB at 128K
context according to the estimation formula.

Licence becomes especially important when a model is going to be redistributed,
published in a project, or used commercially. A model should not be selected
only because it is small enough to fit.

For my personal 8 GB laptop coding-assistant scenario, a quantized model with
a moderate context is more practical than a larger or full-precision model.
Before deploying the model in a public or commercial project, I would check
the current model card and licence again.

---

## 17. Sources Checked

### Qwen

Official model card:
Qwen/Qwen3-8B

Ollama:
qwen3:8b

Date checked: 1 October 2026

### Mistral

Official model card:
mistralai/Mistral-7B-Instruct-v0.3

Ollama:
mistral:7b-instruct-v0.3-q4_K_M

Date checked: 1 October 2026

### IBM Granite

Official model card:
ibm-granite/granite-3.3-8b-instruct

Ollama:
granite3.3:8b

Date checked: 1 October 2026