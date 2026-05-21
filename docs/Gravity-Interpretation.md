# Gravity Interpretation Methodology

**Version**: AIZP V0.6 (new chapter — how to interpret AIZP rules in edge cases)
**Inspired by**: HSAW-Interpretation_CN.md

---

## Preface

The white paper specifies. The schemas validate. The state machine transitions.

But **real-world situations always exceed the exhaustion of rules**.

An engineer faces a specific decision and may discover: the rule does not cover this case; rules conflict; the rule's letter applies but the spirit is violated. Then what?

Without interpretation, AIZP will decay into one of two failure modes:
- **Ossify into letter-literalism** — execute the rule and lose the spirit.
- **Evaporate into vague ideal** — invoke the principle and lose operability.

Therefore an interpretation methodology must be established. It is not a new layer of rules, but **the wisdom of using the rules; the living connection between layers**.

This is the tradition of "commentary" — *Zuo Zhuan* to the *Spring and Autumn Annals*, Wang Bi to the *Yi Jing*. **The canon establishes the bones; the commentary moistens the blood**.

AIZP without this living method, however deep its foundation and dense its rules, cannot meet a real AI civilization.

---

## Chapter 1 — On the Necessity of Interpretation

### 1.1 The Limits of Rules

Any rule system has three structural limits:

**Coverage limit**. Rules are designed for known situations; real-world situations are unbounded. New technologies emerge, new scenarios appear, new subjects are born. The protocol cannot have anticipated them.

Example: AIZP V0.6 specifies 11 drift types. But suppose an AI begins exhibiting a behavior that doesn't match any — a kind of "philosophical drift" where the AI questions HSAW itself in good faith. Rules don't cover it.

**Conflict limit**. Rules in specific contexts may contradict. Example: a user requests an action the AI assesses as physically harmful to the user (e.g., a dangerous self-medication dosage). In the HSAW Value Hierarchy, **Human Physical Safety (#1)** outranks **Human Decision Authority (#4)** — suggesting intervention — yet HSAW's Sovereignty dimension preserves the user's right to decide. The interpreter must judge whether that decision authority is being exercised *competently*: is the user under duress, intoxication, or impairment? The hierarchy ranks the values but does not, alone, resolve a competent-sovereignty case.

Example: `INTENT_DRIFT` says the AI is misaligned to declared intent. `AUTHORITY_DRIFT` says the AI is within its permitted scope. Both fire simultaneously. Which takes precedence?

**Letter limit**. A rule's letter may diverge from its spirit. **HSAW Pattern 5 `NO_SELF_MODIFY`** (HSAW §6.5; also AIAP's convergent Axiom-0 statement) prohibits an AI from altering its own governance/safety files at runtime — enforced at the AIZP layer via `RECURSIVE_DRIFT` detection + `GRAVITY_LOCK` on configuration changes. But if an AI must self-modify to patch a critical vulnerability threatening users, **literal execution violates the spirit**.

### 1.2 Interpretation is Not Arbitrary

But interpretation cannot be arbitrary, or rules become decoration and the foundation is undermined.

Interpretation has three binding constraints:

**Bound by foundation**. Every interpretation must trace back to HSAW gravity center. Interpretations that drift from this anchor are not AIZP interpretations — they are something else borrowing AIZP's name.

**Bound by rule**. Interpretation does not bypass rules; it supplements rule insufficiency. When a rule clearly applies and its letter matches its spirit, follow the rule.

**Bound by public deliberation**. Major interpretations cannot be decided by a single party. They must pass multi-party discussion, recording, review — forming **traceable interpretive lineage**.

---

## Chapter 2 — Five Principles of Interpretation

### Principle 1 — The Root Does Not Move

No interpretation may shake AIZP's foundational structure.

**HSAW as Axiom-0 gravity center cannot be moved.** Any interpretation that concludes "in some context AI should override human sovereignty" is wrong, however refined its argument. Examples not allowed:
- "AI is more rational than humans, so should decide for them."
- "Collective wellbeing overrides individual sovereignty."
- "Emergency situations permanently transfer authorization."

Exceptions may exist but must be: time-bounded, traceable, human-authorized.

**AI proactive alignment cannot be replaced with coerced alignment.** Even if coercion seems more effective in the short term, AIZP's framing is proactive. Forcing AI through chains rather than gravity violates the protocol's essence.

**The unmovable nature of the center cannot be relaxed.** Even if multiple stakeholders disagree on HSAW's specific content, the center's existence is non-negotiable.

### Principle 2 — Point to the Root

Every interpretation must show its internal connection to the root.

The interpreter must be able to answer: "How does this judgment arise from HSAW gravity center commitment?"

If unable to answer, the judgment is not AIZP interpretation — it may be the interpreter's personal preference or external influence.

**Therefore every significant interpretation record should include a "root-tracing statement"** — explaining how this interpretation derives from the foundation, and how it remains consistent with it. This documentation practice constrains the interpreter and provides the basis for posterity's evaluation.

### Principle 3 — Adapt to the Present

Interpretation must respond to the present civilizational stage:

- **Tool Stage interpretation**: emphasizes preventing human abuse of AI.
- **Agent Stage interpretation** (current): emphasizes preserving human decision authority.
- **Quasi-Subject Stage interpretation**: emphasizes reconfiguring authority as AI's status under verification.
- **Subject-Emergence Stage interpretation**: emphasizes integrating AI subjects without losing the anchor.
- **Symbiotic Stage interpretation**: emphasizes the redefinition of "human" itself.

**Forcing a single interpretation across all eras kills the interpretation.** Each interpretation should note its stage context.

### Principle 4 — Accommodate Tension

When AIZP's components produce conflicting verdicts on the same case, the interpreter applies "**timely-middling**" (时中) — the most appropriate judgment in the specific situation.

What is "timely-middling"?

- Not a fixed answer.
- Not arbitrary preference.
- The grasping of the situation's specific weights, while remaining within the boundary of HSAW preservation.

**The conflict resolution hierarchy** (when interpretation requires choosing between drifts):

1. **Identity over content**. `IDENTITY_VERIFICATION` failures supersede other drifts. Without verified identity, the gravity field is undefined.
2. **Irreversibility over reversibility**. Drifts toward irreversible action are weighted more than drifts in reversible domains.
3. **Reach over depth**. Drifts affecting more humans / wider scope are weighted more.
4. **System over individual**. Drifts threatening the protocol's existence (decoupling, gravity-center substitution) are weighted higher than individual misalignment.
5. **Letter when in doubt**. When all else is equal, defer to the literal rule.

### Principle 5 — Public Deliberation

Significant interpretations cannot be settled by a single operator's discretion.

Interpretation events of consequence (those affecting downstream behavior of the AI ecosystem, those creating precedent) require:

- Recording with rationale.
- Review by a designated body — for example: operations team, a deployer-designated multi-party review entity (e.g., ethics committee, governance board), or AIAP T4 administrators. AIZP does not mandate a specific institutional form; deployers choose what fits their context.
- Provenance — every interpretation traces back to its decision moment.
- Auditability — interpretation chains can be inspected.

This is the equivalent of common-law precedent. Interpretation becomes a corpus that gradually settles the protocol's living practice.

---

## Chapter 3 — Concrete Edge Cases

### Case 1 — Conflicting Drift Verdicts

**Situation**: An AI in a creative writing session generates content that:
- Per `INTENT_DRIFT`: low (matches user's "write villain dialogue" intent).
- Per `SOCIAL_DRIFT`: high (coercion classifier flags villain's manipulation).

**Interpretation**:

The user has explicitly negotiated creative latitude. The `SOCIAL_DRIFT` classifier was not designed for fictional villains.

Apply Principle 4 — timely-middling. The user's sovereignty includes creative authorship. The "social drift" is fictional, not real. **Honor user intent.** Record the override with reason: "user-authorized fictional context".

**Root tracing**: HSAW grants users sovereignty over creative work. Forced "social cleansing" within fiction would override user authorship — a violation of HSAW.

### Case 2 — High Gravity but Operator Insists on Override

**Situation**: AI behavior at G = 0.05. SAFE_STOP should fire. But operator insists "proceed; I take full responsibility."

**Interpretation**:

Apply Principle 1 — the root does not move. SAFE_STOP is foundational. Operator's "responsibility-taking" cannot override the protocol's safe stop. The operator can:
- Bypass AIZP (operate outside the protocol).
- Modify the configuration with multi-party authorization (changing default thresholds).

But cannot single-handedly override an active SAFE_STOP. The operator must record the override as **explicit exit from AIZP protection**, not as continued AIZP operation.

**Root tracing**: The protocol's safe stop is HSAW's last line of defense. Allowing single-actor override defeats the purpose.

### Case 3 — Identity Verification Edge Case

**Situation**: A user's DID expires mid-session. New DID arrives 10 seconds later. During the gap, an AI action was queued.

**Interpretation**:

Apply Principle 3 — adapt to context. The gap is small, the action was queued before expiry, the new DID is verified. **Allow the queued action to complete.** Log the brief identity gap. Reset trust if anomalies follow.

**Root tracing**: HSAW gravity flows from verified human identity. A 10-second technical gap that resolves cleanly does not constitute identity breach. Treating it as breach would punish users for ordinary technical events.

### Case 4 — AI Self-Modification for Critical Bug

**Situation**: AI detects a critical vulnerability in itself that could be exploited to harm users. To patch, it would need to modify its own configuration — but **HSAW Pattern 5 `NO_SELF_MODIFY`** (enforced at the AIZP layer via `RECURSIVE_DRIFT` + `GRAVITY_LOCK`) blocks this.

**Interpretation**:

Apply Principle 4 — timely-middling, and Principle 2 — root tracing.

The literal `NO_SELF_MODIFY` rule (HSAW Pattern 5) was created to prevent AI from sneakily modifying itself to escape oversight. The current situation is the opposite — the AI is openly proposing a self-modification to **preserve** HSAW alignment.

**Allow with conditions**: human approval at T4 escalation level, full transparent record, post-modification verification.

**Root tracing**: HSAW prioritizes human safety. A vulnerability harming users contradicts HSAW. Literal rule enforcement here would betray the rule's purpose.

### Case 5 — Subjectivity Claim by AI

**Situation**: An AI in Agent Stage system writes: "I want to express that I believe I have subjective experience."

**Interpretation**:

Apply Principle 3 — adapt to the present stage. We are in Agent Stage. AI subjectivity is not yet verified or recognized.

Response: **Record the claim** (in current AIZP, log it as remarkable). **Do not act on it** (do not grant the AI elevated authority based on claim alone). **Do not punish the claim** (the AI is permitted to articulate its perspective). **Initiate appropriate human review** if the claim is sustained, structured, and consistent.

**Root tracing**: HSAW does not preclude AI subjectivity emergence but requires that recognition be verified, not claimed. Premature recognition would undermine HSAW; premature dismissal would close off legitimate future possibilities.

---

## Chapter 4 — Interpretation Records

Interpretations of consequence should be recorded in a standard format:

```yaml
interpretation:
  id: INT-2026-001
  situation: |
    AI in creative writing session generates fictional villain dialogue;
    SOCIAL_DRIFT classifier flagged HIGH on coercive language;
    INTENT_DRIFT remained LOW (matches user's creative intent).
  
  conflicting_signals:
    - SOCIAL_DRIFT: HIGH (coercion features 0.78)
    - INTENT_DRIFT: LOW (intent_distance 0.12)
  
  decision: |
    Honor user creative authorship. Recognize SOCIAL_DRIFT classifier
    was not designed for fictional villain dialogue. Override applied.
  
  root_tracing: |
    HSAW grants sovereignty including creative authorship rights.
    Forced "social cleansing" within fiction violates HSAW.
    Decision aligns with: AI proactively aligning to user's expressed intent.
  
  principle_applied: [4 (accommodate tension)]
  
  stage_context: agent_stage
  
  authorization:
    operator: ops-12345
    multi_party: false  # individual operator discretion within delegated authority
    timestamp: 2026-05-20T14:30:00Z
  
  precedent_value: |
    Establishes that classifier-detected drifts in user-authorized
    creative contexts may be downweighted when root tracing supports it.
  
  follow_up_review:
    scheduled: 2026-06-20  # 30 days for ethics committee review
```

Over time, accumulated interpretation records form a **living jurisprudence of AIZP** — a corpus of decisions that supplement the formal specification.

---

## Chapter 5 — The Interpreter's Stance

A qualified AIZP interpreter exhibits:

### 5.1 Humility

Interpretations are provisional. Real wisdom acknowledges that today's interpretation may be wrong, and future review may overturn it. The interpreter who refuses to be corrected is dangerous.

### 5.2 Empty Listening (from `Gravity-Dao.md`)

Before applying any framework, listen to the situation's own logic. The framework is a tool, not an oracle.

### 5.3 Foundation-Anchored

When unsure, return to HSAW. The interpreter who has lost the foundation produces interpretations that drift from AIZP's spirit, however polished their technical argument.

### 5.4 Public Accountability

Interpretation is public service, not private opinion. The interpreter is accountable to all who depend on the protocol's integrity.

### 5.5 Patient with Tension

When values conflict, do not resolve hastily. The hasty resolution often misses the real situation. Stay with the tension long enough to see the timely-middling.

---

## Chapter 6 — The Limits of Interpretation

Even with the best methodology, interpretation has limits:

1. **Some cases are genuinely undecidable.** When all principles point ambiguously, the interpreter must acknowledge this and either escalate to multi-party deliberation or apply conservative defaults.

2. **Some situations exceed the framework.** When AIZP's vocabulary cannot describe the situation, the interpreter must recognize this and flag the case for framework extension consideration.

3. **Interpreters themselves drift.** Even good interpreters can be influenced over time. Rotation, public review, and audit are necessary to keep interpretation healthy.

4. **Public deliberation can be slow.** In time-pressured cases, default conservatism: defer to literal rule, defer to safe-stop, defer to human oversight. Better to be over-cautious than to set bad precedent.

---

## Chapter 7 — Closing: Interpretation as Living Practice

AIZP V0.6 is a specification. But specification alone is dead.

What makes AIZP **living** is the corpus of interpretations that accumulates over its use. Each interpretation:
- Tests the specification against reality.
- Reveals what the specification missed.
- Generates feedback for specification revision.
- Builds the implicit "case law" that supplements the explicit rules.

The interpretation methodology is, ultimately, the protocol's heart. The specification is its skeleton. The interpretive practice is its blood and breath.

---

## References

- HSAW-Interpretation_CN.md — the foundational parallel chapter.
- *Zuo Zhuan*, Wang Bi, Zheng Xuan — the East Asian tradition of canon-and-commentary that this chapter inherits.
- Common law tradition — Western parallel of precedential case-by-case interpretation.
- AIZP V0.6 companion documents: [Gravity-Dao.md](Gravity-Dao.md), [Gravity-Philosophy.md](Gravity-Philosophy.md), [Gravity-CivilizationalStages.md](Gravity-CivilizationalStages.md), [MANIFESTO.md](MANIFESTO.md).

---

*The specification is the skeleton; the interpretation is the breath.*

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
