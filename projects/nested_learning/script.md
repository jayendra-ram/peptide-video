# Nested Learning: The Illusion of Deep Learning Architecture — Video Script

> **Edit this file** to change narration, timing, visuals, and text overlays.
> Run `python scripts/make_video.py projects/nested_learning` to build the video.

---

## Scene 1: The Illusion
<!-- id: scene_01_intro -->
<!-- render: manim:IntroScene -->

**Duration:** 20s

### Narration

What if the way we think about deep learning is an illusion? We stack a hundred layers and call it a deep network. But what if it is not one model at all — but dozens of small learning systems, nested inside each other? Each with its own objective, its own memory, and its own update speed. This paper reframes deep learning entirely, starting from a single, surprisingly simple idea.

### Visuals

- Show a standard deep network: a column of rectangular blocks labeled "Layer 1" through "Layer N", connected by arrows. This is the conventional "deep learning" view — opaque and flat.
- Animate the blocks sliding apart and revealing nested colored boxes within each layer. Inner boxes pulse fast, outer boxes pulse slowly. Gradient flow arrows appear within each nested level.
- Title text: "Nested Learning" fades in at bottom.

### Text Overlays

- [0s–4s] "The Deep Learning View" — size 0.28, position (0, 3, 0)
- [5s–end] "The Nested Learning View" — size 0.28, position (0, 3, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 2: Associative Memory
<!-- id: scene_02_assoc_memory -->
<!-- render: manim:AssocMemoryScene -->

**Duration:** 35s

### Narration

Think about how memory works. You see a friend's face, and their name comes to mind. You hear a melody and recall the lyrics. In each case, an input maps to an output. This is an associative memory. Now generalize: given any set of keys and values, can we find an operator M that best maps each key to its corresponding value? Formally, M-star equals argmin over M of the sum of losses between M of k-i and v-i. This is Definition 1 of the paper. And here is the key insight: any learning process that solves this optimization — whether gradient descent, attention, or a Hopfield network — is building an associative memory. This abstraction is the foundation of everything that follows.

### Visuals

- Animate key-value pairs appearing: k1→v1, k2→v2, k3→v3, k4→v4
- Show the central box labeled "M" with arrows flowing from keys through M to values
- Display Definition 1 equation with MathTex
- Highlight: "This formulation is equivalent to data compression and dimensionality reduction."

### Text Overlays

- [0s–end] "Definition 1: Associative Memory" — size 0.22, position (0, 3.2, 0)
- [8s–end] "M* = argmin_M Σ L(M(k_i), v_i)" — size 0.26, position (0, 2.4, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 3: Backprop as Surprise Memory
<!-- id: scene_03_surprise -->
<!-- render: manim:SurpriseMemoryScene -->

**Duration:** 40s

### Narration

When you study for an exam, you don't re-read everything equally. You focus on what surprised you — the questions you got wrong. Neural networks do exactly the same thing. Consider a single linear layer training with backpropagation. The standard objective is W-star equals argmin of the loss over the training data. But the paper shows you can reformulate this. The gradient of the loss with respect to the output measures how surprising each data point is — this is the Local Surprise Signal. So the weight update becomes an associative memory problem: the key is the input x, and the value is the surprise. Formally, the weight update minimizes the inner product of the surprise signal with the prediction, plus a proximal term that keeps weights close to their previous values. Backpropagation is memorizing surprises. The same Definition 1 from before, applied to gradient updates.

### Visuals

- Show a single linear layer: input x flowing through weight matrix W to output y.
- Display Eq. 7: "W* = argmin L(W; D_train)"
- For each data point, show the output, then the error/surprise as a colored bar.
- Transform Eq. 7 into Eq. 9: the associative memory formulation with LSS.
- Build a key-value table: x_t → ∇_y L (the surprise).
- Box highlight: "Backpropagation is memorizing surprises."

### Text Overlays

- [0s–12s] "Eq. 7: W* = argmin L(W; D_train)" — size 0.24, position (0, 3.2, 0)
- [13s–end] "Eq. 9: Backprop = Surprise Memory" — size 0.22, position (0, 3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 4: Nested Systems
<!-- id: scene_04_nested_systems -->
<!-- render: manim:NestedSystemsScene -->

**Duration:** 45s

### Narration

Your brain doesn't learn everything at the same speed. You pick up a new word in seconds, but mastering a language takes years. Fast adaptation and slow consolidation happen at different timescales. The nested learning framework formalizes this. A nested system is a set of K ordered levels. Each level k has its own optimization problem with objective L-k, its own parameters theta-k, and crucially, its own update frequency f-k. Higher levels have lower frequency — they update slowly and store persistent knowledge. Lower levels update fast, adapting to immediate context. This is Definition 3 of the paper. Each level's optimization includes a proximal regularizer that controls how far parameters can move in a single step. The key insight: well-known architectures are already nested systems. In a Transformer, attention heads update their key-value associations at every token — that is a fast inner level. The MLP weights update via backpropagation across batches — that is a slower outer level. The embeddings update most slowly of all. Different components, different timescales, nested optimization.

### Visuals

- Build concentric rounded rectangles: Level 1 (innermost, red border pulsing fast), Level 2 (middle, yellow border pulsing medium), Level 3 (outermost, blue border pulsing slowly).
- Inside each level, show the optimization: θ, L_k, C_k, f_k labels.
- Display Eq. 19 with color-coded terms matching the levels.
- Animate a Transformer decomposition: show attention (high frequency, inner) vs. MLP weights (low frequency, outer) vs. embeddings (lowest frequency, outermost).

### Text Overlays

- [0s–end] "Definition 3: Nested System" — size 0.22, position (0, 3.2, 0)
- [10s–end] "K levels, each with (L_k, C_k, Θ_k, f_k)" — size 0.20, position (0, -3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 5: Knowledge Transfer Between Levels
<!-- id: scene_05_knowledge_transfer -->
<!-- render: manim:KnowledgeTransferScene -->

**Duration:** 40s

### Narration

If you have systems learning at different speeds, how do they share what they know? Think of a company: junior employees learn fast from daily work, senior leaders update strategy slowly. But knowledge needs to flow between them. The paper identifies three mechanisms for inter-level transfer. First, direct connections: the output of one level conditions the input of another. In a Transformer, the attention output feeds directly into the MLP — that is a direct connection between levels. Second, backpropagation: gradient information flows backward across levels during training, letting slow levels influence fast ones. Third, meta-learning: one level learns the initialization for another, as in MAML, where a slow outer loop learns a starting point that a fast inner loop can quickly adapt from. The choice of transfer mechanism fundamentally shapes a model's learning dynamics and determines whether it can learn continually without forgetting.

### Visuals

- Show two nested boxes: Level 1 (fast, inner) and Level 2 (slow, outer).
- Mechanism 1 — Direct Connection: animate forward arrows from Level 1 to Level 2. Display equation.
- Mechanism 2 — Backprop: animate backward gradient arrows.
- Mechanism 3 — Meta-Learning (MAML): animate Level 2 setting the initial state of Level 1. Display Eq. 28.
- Side-by-side comparison: "Transformers → Direct Connection" vs "MAML → Initialization Transfer"

### Text Overlays

- [0s–end] "Knowledge Transfer Between Levels" — size 0.22, position (0, 3.2, 0)
- [6s–14s] "1. Direct Connections" — size 0.20, position (-4, -3, 0)
- [15s–25s] "2. Backpropagation" — size 0.20, position (0, -3, 0)
- [26s–end] "3. Meta-Learning (MAML)" — size 0.20, position (4, -3, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 6: Optimizers as Associative Memories
<!-- id: scene_06_optimizers -->
<!-- render: manim:OptimizersScene -->

**Duration:** 45s

### Narration

Here is something surprising: the optimizer itself is an associative memory. Consider momentum. At each step, it takes a weighted average of past gradients. That weighted average is compressing a history of gradient signals into a single vector — it is memorizing a summary of past updates. But standard momentum with beta equals 0.9 has very limited capacity. The contribution of a gradient from 43 steps ago has decayed to just one percent of its original magnitude. Earlier information is exponentially forgotten. Can we do better? The paper introduces Delta Gradient Descent. Instead of the momentum being a simple weighted average, the update rule now includes the current gradient, the previous momentum, and higher-order features from the loss landscape. The momentum becomes a self-referential memory — it uses its own past state as input to decide what to store next. This is the same associative memory pattern again: keys are gradient features, values are update directions, and the optimizer is the memory operator M.

### Visuals

- Show gradient vectors accumulating into momentum with exponential decay.
- Display the exponential decay curve: contribution drops as β^(t-i). Mark the "50% capacity" line at ~43 steps.
- Transition to Delta Momentum: show the enriched update rule.
- Display Eq. 46 (momentum as associative memory) and Eq. 50 (Delta Momentum).
- Visual contrast: standard momentum (simple weighted sum) vs. Delta Momentum (self-referential loop).

### Text Overlays

- [0s–18s] "Momentum as Associative Memory (Eq. 46)" — size 0.22, position (0, 3.2, 0)
- [19s–end] "Delta Gradient Descent (Eq. 50)" — size 0.22, position (0, 3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 7: Continuum Memory System
<!-- id: scene_07_cms -->
<!-- render: manim:CMSScene -->

**Duration:** 40s

### Narration

Your computer has RAM for instant access and a hard drive for permanent storage. What if a neural network had the same hierarchy of memory speeds? This is the Continuum Memory System, or CMS. CMS chains K MLP blocks together. Block 1 updates its parameters on every token — this is the fastest working memory. Block 2 updates every C tokens. Block 3 updates every C-squared tokens. Block K updates every C-to-the-K tokens — this is the most persistent, long-term memory. Each block compresses its context into parameters at its own timescale. What makes this efficient is that at each step, only one block actually updates. And Equation 71 shows that updates within each block are independent across chunks of the input, enabling full sequence parallelism. The result is a memory hierarchy that spans from millisecond working memory to long-term knowledge — all learned end-to-end.

### Visuals

- Build a horizontal chain of K=4 MLP blocks, color-coded from red (fast) to blue (slow).
- Tokens stream in from the left. Block 1 flashes on every token. Block 2 flashes every C tokens.
- Display Eq. 70: the chained output.
- Display Eq. 71: the conditional update rule.
- Animate knowledge consolidation: information flows from fast blocks to slow blocks over time.

### Text Overlays

- [0s–end] "Continuum Memory System (CMS)" — size 0.22, position (0, 3.2, 0)
- [8s–end] "Eq. 70–71: Multi-frequency MLP chain" — size 0.20, position (0, -3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 8: Generalized Gradient Descent
<!-- id: scene_08_ggd -->
<!-- render: manim:GGDScene -->

**Duration:** 40s

### Narration

In school, the teacher provides the answers. But the best students test themselves — they generate their own problems and learn from the results. This is the idea behind Generalized Gradient Descent, or GGD. In standard backpropagation, the target values come from the training data — externally provided. But in GGD, the model generates its own targets. The update rule is: W at t plus 1 equals argmin of the loss on input x and self-generated value u, plus a retention term that controls how much past memory to preserve. What is u? It is f of W-t applied to x-t — the model's own output becomes its learning signal. The model decides what to memorize based on what it itself produces. This makes the entire training process self-referential. And the retention function Ret controls the balance between plasticity — learning new things — and stability — remembering old ones.

### Visuals

- Show standard backprop: data x → model → output y → compare with external target → gradient → update.
- Transform into GGD: the output loops back as the self-generated value u.
- Display Eq. 59: GGD update rule with the retention term highlighted.
- Display Eq. 60: u_t = f_{W_t}(x_t).
- Box: "Backpropagation is a self-referential process."

### Text Overlays

- [0s–15s] "Standard Backprop: External Targets" — size 0.22, position (0, 3.2, 0)
- [16s–end] "GGD (Def. 5): Self-Referential Learning" — size 0.22, position (0, 3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 9: HOPE Architecture
<!-- id: scene_09_hope -->
<!-- render: manim:HOPEScene -->

**Duration:** 40s

### Narration

Everything we have built leads to one architecture: HOPE. HOPE starts with a self-modifying Titan backbone. Each block has its own local objective function — it does not wait for end-to-end backpropagation. Instead, it generates its own update values using the GGD framework from the previous scene. Next, HOPE wraps this backbone in the Continuum Memory System. Each block is replicated at multiple frequency levels — fast blocks for working memory, slow blocks for long-term knowledge. The result is a fully self-referential architecture where every component continuously learns at its own timescale. For efficient training, HOPE processes the input in chunks. Each block updates independently within a chunk, and state transfers between chunks. This makes training parallelizable, unlike recurrent models that must process tokens sequentially.

### Visuals

- Step 1: Self-Modifying Titans with loop arrow.
- Step 2: CMS wrapping with 3 frequency-level blocks.
- Step 3: Parallelizable training via chunking.
- Show the complete HOPE diagram.

### Text Overlays

- [0s–end] "HOPE: Self-Referential Learning + Continuum Memory" — size 0.22, position (0, 3.2, 0)
- [0s–12s] "Step 1: Self-Modifying Titans" — size 0.20, position (0, -3.2, 0)
- [13s–25s] "Step 2: Add CMS" — size 0.20, position (0, -3.2, 0)
- [26s–end] "Step 3: Parallelizable Training" — size 0.20, position (0, -3.2, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60

---

## Scene 10: Results and Big Picture
<!-- id: scene_10_results -->
<!-- render: manim:ResultsScene -->

**Duration:** 35s

### Narration

The experiments validate nested learning across multiple axes. On continual learning, HOPE with CMS outperforms Transformers and Mamba, significantly reducing catastrophic forgetting. On long-context understanding at 128K to 256K tokens, standard Transformers degrade while HOPE maintains stable performance. On language modeling, HOPE achieves competitive perplexity while being fully parallelizable. The deeper message of this paper is a shift in how we think about architecture. True computational depth is not the number of layers you stack. It is nested optimization at multiple timescales — each level learning, memorizing, and consolidating at its own frequency. Depth is not layers. Depth is nesting.

### Visuals

- Left panel: Bar chart comparing HOPE vs Transformer vs Mamba on continual learning.
- Right panel: Line chart of accuracy vs context length.
- Transition to final visual: paper title and concluding message.

### Text Overlays

- [0s–12s] "Continual Learning" — size 0.22, position (-3.5, 3.2, 0)
- [0s–12s] "Long-Context Understanding" — size 0.22, position (3.5, 3.2, 0)
- [15s–end] "Nested Learning: The Illusion of Deep Learning Architecture" — size 0.26, position (0, 0, 0)

### Camera

- Static: (0, 0, 10) looking at (0, 0, 0), FOV 60
