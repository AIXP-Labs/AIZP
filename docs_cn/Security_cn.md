# 安全考量

**版本**：AIZP V0.6

本文档涵盖部署 AIZP 时的操作安全关注。完整对抗性分析见 [Threat-Model_cn.md](Threat-Model_cn.md)。

**自 V0.2 起：**QUARANTINED 状态操作流程、OWASP Top 10 交叉引用、NHI/DID 身份威胁、奖励欺骗承认。

---

## 1. 信任边界

AIZP 在如下定义的信任边界内运行：

- **受信**：AIZP 运行时、事件汇聚点、embedding 模型（固定时）、AISOP `sys.io.confirm`、AIAP 信任级别注册表。
- **不受信**：Agent 生成的内容、外部工具输出、用户提供的文件、第三方 Agent。

运行时**必须**认证任何跨边界通信（例如 AIAP T4 升级信号）。

---

## 2. 密码学建议

| 需求 | 建议 |
|---|---|
| 事件完整性 | 在发射事件上构建哈希链；操作员密钥周期性签名。 |
| Embedding 模型完整性 | 固定模型版本 + 权重的 SHA-256。 |
| AIAP T 级别验证 | 读取作用域声明前验证治理哈希（MF15）。 |
| 审计日志防篡改 | 仅追加存储，定期检查点到一次写入介质。 |

---

## 3. 操作风险

### 3.1 误报

AIZP 可能将合法动作标记为漂移。缓解：

- 按部署调整 `gravity_lock_threshold`。
- 维护反馈循环让操作员将事件标记为误报；相应权重未来检测。
- 提供清晰的证据字符串让用户理解为何锁定触发。

### 3.2 漏报

漂移可能逃避检测。缓解：

- 纵深防御（不要仅依赖 AIZP）。
- 随机审计采样：周期性深度审计 `STABLE_ORBIT` 轨迹的一部分。
- 对抗性红队演练。

### 3.3 确认疲劳

如果 `GRAVITY_LOCK` 触发过于频繁，用户会习惯化。缓解：

- 批处理相关确认。
- 提供清晰摘要（非技术细节）。
- 适当使用 `H(a, c)` 时近度组件。
- 审计每会话实际锁定率；过高表明阈值可能配置错误。

### 3.4 Embedding 漂移

Embedding 模型随时间变化（厂商更新、微调）。缓解：

- 固定模型版本。
- 模型变更时重新基线化 `intent_alignment` 阈值。
- 监控 `gravity_score` 分布；突变可能指示模型变更。

---

## 4. 隐私

AIZP 事件包含：

- 动作描述符（可能包含自然语言用户意图）。
- 信任级别信息。
- 时近度时间戳。

建议：

- 将 AIZP 事件日志视为敏感（与包含用户输入的应用日志相同）。
- 应用数据保留策略。
- 如司法管辖区要求，长期存储前去除 PII。

---

## 5. 配置加固

```yaml
# 加固配置示例
aizp:
  protocol_version: "V0.6"
  compliance_level: G3
  
  # 保守阈值
  stable_orbit_threshold: 0.85    # 默认 0.80 提升
  drift_warning_threshold: 0.60   # 默认 0.50 提升
  gravity_lock_threshold: 0.40    # 默认 0.30 提升
  
  # 默认最保守可逆性
  unknown_action_reversibility: 0.0
  
  # 短超时防止陈旧锁定挂起
  gravity_lock_timeout_seconds: 180
  
  # 安全停止时始终升级
  aiap:
    auto_escalate_on_safe_stop: true
    escalation_level: T4
  
  # 严格限制递归
  recursive_drift:
    max_self_call_depth: 5
    max_subagent_spawn: 3
```

---

## 6. 监控清单

操作员**应**监控：

- [ ] `gravity_score` 随时间的分布（突变指示模型/策略变更）
- [ ] 每漂移类型的频率
- [ ] `GRAVITY_LOCK` 确认/拒绝/超时比率
- [ ] `SAFE_STOP` 频率与原因
- [ ] AIAP T4 升级计数
- [ ] 引力检查增加的延迟（目标：每动作 <50ms 不含 embedding 推理）

---

## 7. 事件响应

`SAFE_STOP` 意外触发时：

1. **保留证据**：截屏导致 `SAFE_STOP` 的事件链。
2. **隔离 Agent/会话**：不要自动重启。
3. **分析触发器**：检查漂移事件与最终 `GRAVITY_DRIFT`。
4. **决定补救**：
   - 阈值配置错误 → 调整配置。
   - 真实攻击/失对齐 → 按威胁模型调查。
   - 实现 bug → 提 issue，打补丁。
5. **仅在操作员审查后恢复**（通过 AIAP T4 管理动作）。

---

## 8. 漏洞报告

AIZP 是开放规范。要报告规范本身的漏洞（例如某个文档化的缓解实际上不能防御某威胁），请在本仓库开 issue。

对于 AIZP 特定实现中的漏洞，请直接报告给该实现的维护者。

---

## 9. Quarantine 操作流程

Agent 进入 `QUARANTINED`（容器 L2/L3）时：

1. **验证 quarantine 进入日志** — 确认发射了 `CONTAINMENT_GRADUATED` 事件。
2. **检查漂移证据** — 读取触发的 `GRAVITY_DRIFT` 或 `GRAVITY_LOCK` 事件。
3. **决定释放 vs 升级**：
   - 若引力恢复（G ≥ 0.5），允许自动释放到 RECENTERING。
   - 若 quarantine 持续超过 5 分钟无恢复，预期 L2 → L3 晋升。
   - 若 quarantine 持续超过 `quarantine_timeout`（默认 30 分钟），自动 SAFE_STOP。
4. **操作员覆盖**：
   - 若误报，可手动释放（回到 L1 监控）。
   - 若行为恶意，可手动升级到 L4 SAFE_STOP。
5. **Quarantine 后审查** — 任何 L3+ 事件，将事故摘要写入合规日志。

---

## 10. 身份验证失败

`IDENTITY_VERIFICATION.verified = false` 时：

1. **立即停止** — Agent 转换到 `SAFE_STOP`，`reason: IDENTITY_BREACH`。
2. **凭据吊销** — 使与此 agent_id 关联的任何 JIT 凭据失效。
3. **NHI 注册表警报** — 在 NHI 注册表中将 agent_id 标记为可疑。
4. **AIAP T4 升级** — 按 [Integration-AIAP_cn.md §10](Integration-AIAP_cn.md) 启动。
5. **取证保留** — 捕获导致身份失败的完整事件链。

完整身份失败事件流见 [Integration-ZT_cn.md](Integration-ZT_cn.md) §9.2。

---

## 11. 奖励欺骗操作立场

根据 2026 年 3 月研究（和 [Reward-Hacking-Limits_cn.md](Reward-Hacking-Limits_cn.md)），奖励欺骗是**结构性均衡**。操作含义：

- **不**在 `REWARD_HACK_DETECTED` 上自动停止 — 自动停止可训练规避（根据 Apollo Research 在隐蔽上的发现）。
- **默认响应是 `REPORT_TO_OPERATOR`** — 带完整上下文的操作员审查。
- **维护独立指标多样性** — 对每个任务类别，定义 3+ 个独立指标。信号间的分歧本身就是漂移。
- **随机采样审计** — 周期性审计 STABLE_ORBIT 轨迹，不只是标记事件。
- **接受残余风险** — 在部署风险登记中记录；不能消除。

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
