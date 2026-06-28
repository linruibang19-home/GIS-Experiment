# 广州市高新技术企业年度时空预测研究方案重构：替代ConvLSTM的可行设计

> 适用背景：2015—2024年年度高新技术企业数据；企业登记信息集中统一在年末；登记月份不具备真实动态意义；不宜构建季度或月度序列。  
> 核心结论：本研究不建议将ConvLSTM作为主模型。更适合采用“年度格网面板 + 企业资格事件流 + 空间滞后/空间随机效应 + 机器学习或贝叶斯预测”的组合框架。

---

## 1. 为什么季度方案不可取

你指出的限制非常关键：企业数据虽然包含登记时间，但实际登记信息集中统一在当年年末，月份不具有真实事件发生意义。因此，不能把年度数据拆成季度或月度序列。

如果强行构建季度数据，会出现以下问题：

1. **伪时序问题**：季度变化不是企业真实进入或退出过程，而是登记制度造成的记录时间。
2. **模型误导问题**：ConvLSTM会把人为制造的季度差异当作真实时间动态学习。
3. **评估偏差问题**：模型可能在伪季度上表现很好，但对真实年度预测没有意义。
4. **机制解释问题**：高新技术企业资格有效期是3年，年度状态转移比季度波动更符合制度逻辑。根据《高新技术企业认定管理办法》，通过认定的高新技术企业资格自颁发证书之日起有效期为3年。[^hitech3y]

因此，本研究应明确写为：

> 本文不对企业登记月份进行季度化处理，而是以年度为最小有效时间单位，基于2015—2024年格网—年份面板数据开展时空预测研究。

---

## 2. 为什么ConvLSTM不适合作为主模型

ConvLSTM原本适合处理连续、密集、规则的时空序列。其原始研究将降水临近预报定义为时空序列预测问题，并通过卷积结构捕捉空间相关和时间依赖。[^convlstm]

你的数据条件不同：

| 维度 | ConvLSTM理想条件 | 本研究数据条件 |
|---|---|---|
| 时间长度 | 较长、连续、密集 | 仅2015—2024共10个年度时间片 |
| 时间粒度 | 小时、日、月、季度等真实序列 | 年度才是真实有效单位 |
| 样本生成 | 可形成大量时序窗口 | 全市矩阵只有少量年度窗口 |
| 变量类型 | 连续场或高频栅格序列 | 零膨胀的格网计数数据 |
| 机制结构 | 主要依赖数据学习 | 高新资格有明确3年制度周期 |
| 解释性 | 较弱 | 论文需要解释影响机制和政策含义 |

如果使用3年输入预测下一年：

```text
2015-2017 → 2018
2016-2018 → 2019
2017-2019 → 2020
2018-2020 → 2021
2019-2021 → 2022
2020-2022 → 2023
2021-2023 → 2024
```

全市矩阵层面只有7个训练窗口。即使切成空间patch，也只是增加空间样本，不能真正增加时间动态样本。

### 2.1 论文中建议的表述

可以这样写：

> 鉴于本文高新技术企业数据的有效时间粒度为年度，且2015—2024年仅包含10个真实时间截面，深度时空序列模型如ConvLSTM存在时间样本不足、过拟合风险高和解释性不足等问题。因此，本文将ConvLSTM作为探索性对照模型或不纳入主实验，转而构建符合高新技术企业资格生命周期的年度事件流状态转移预测模型。

---

## 3. 年度时空预测研究的总体目标

建议把“时空预测性研究”拆成三个层次：

### 3.1 数量预测

预测每个500m格网未来一年：

- 活跃存量；
- 进入代理量；
- 退出代理量；
- 续认代理量。

### 3.2 热点预测

预测未来一年：

- 哪些格网会成为高值热点；
- 哪些格网会持续为热点；
- 哪些格网可能从非热点变为热点；
- 哪些格网可能从热点衰退。

### 3.3 风险预测

识别：

- 续认不足风险区；
- 退出代理量高风险区；
- 高新企业增长停滞区；
- 政策平台未充分转化区。

---

## 4. 推荐主方案：年度事件流状态转移预测模型

### 4.1 核心思想

不要直接把活跃存量当成黑箱序列预测，而是把未来活跃存量拆解为事件流：

\[
\hat A_{g,t+1}=A_{g,t}+\hat I_{g,t+1}-\hat O_{g,t+1}
\]

其中：

- \(A_{g,t}\)：格网 \(g\) 在年份 \(t\) 的活跃存量；
- \(\hat I_{g,t+1}\)：预测的下一年进入代理量；
- \(\hat O_{g,t+1}\)：预测的下一年退出代理量。

也可以写为：

\[
\hat A_{g,t+1}=\hat C_{g,t+1}+\hat I_{g,t+1}
\]

其中：

- \(C\)：持续活跃量；
- \(I\)：进入代理量。

### 4.2 为什么这个方案更适合你的研究

| 优势 | 解释 |
|---|---|
| 符合年度数据 | 不需要虚构季度序列 |
| 符合高新资格制度 | 能利用3年有效期和续认逻辑 |
| 解释性强 | 可分别解释进入、退出、续认机制 |
| 样本量可用 | 使用格网—年份面板，而不是只有10个时间片 |
| 可做预测 | 可预测2025年格网存量、增长区和风险区 |
| 适合GIS论文 | 能输出地图、热点、误差、风险区等空间结果 |

---

## 5. 事件流预测模型结构

### 5.1 子模型一：进入代理量预测

#### 因变量

\[
I_{g,t+1}
\]

即格网 \(g\) 在下一年新进入高新技术企业资格体系的企业数量。

#### 推荐模型

| 模型 | 适用性 |
|---|---|
| 零膨胀负二项回归 ZINB | 适合大量0值和过度离散的格网计数 |
| 负二项回归 NB | 适合计数型、过度离散数据 |
| XGBoost Poisson | 适合非线性和变量交互 |
| 随机森林 | 稳健、解释方便、变量重要性直观 |
| Logistic + Count两阶段模型 | 先预测是否有进入，再预测进入数量 |

#### 解释变量

| 类型 | 变量 |
|---|---|
| 路径依赖 | 上一年活跃存量、近3年增长率、上一年进入量 |
| 邻近效应 | 邻域活跃存量、邻域进入量、热点邻接数量 |
| 创新资源 | 高校距离、科研院所距离、孵化器密度、创新平台密度 |
| 政策平台 | 是否位于高新区、开发区、科学城、知识城、南沙等 |
| 产业基础 | 产业园密度、工业POI、生产性服务业POI、软件信息服务POI |
| 交通可达性 | 地铁站距离、道路密度、到核心区时间成本 |
| 企业结构 | 注册资本均值、企业规模结构、门类多样性 |

#### 模型形式

\[
I_{g,t+1} \sim f(A_{g,t}, WA_{g,t}, I_{g,t}, WI_{g,t}, X_{g,t})
\]

其中 \(W\) 为空间权重矩阵。

---

### 5.2 子模型二：续认代理量预测

续认是你的研究中最有特色的部分，因为高新技术企业资格存在3年周期。

#### 因变量

\[
R_{g,t+1}
\]

即下一年续认企业数量。

#### 到期候选企业

可以先构建：

\[
D_{g,t+1}
\]

表示在 \(t+1\) 年可能面临到期或重新认定的企业数量。

然后预测续认率：

\[
p^{renew}_{g,t+1}=\frac{R_{g,t+1}}{D_{g,t+1}+1}
\]

#### 推荐模型

| 模型 | 适用性 |
|---|---|
| 二项Logit | 因变量为“候选企业中有多少续认” |
| Beta回归 | 因变量为续认率，需处理0和1 |
| XGBoost分类/回归 | 捕捉非线性续认机制 |
| 贝叶斯二项模型 | 可输出续认概率不确定性 |

#### 模型形式

\[
R_{g,t+1} \sim Binomial(D_{g,t+1}, p^{renew}_{g,t+1})
\]

\[
logit(p^{renew}_{g,t+1})=\alpha+\beta X_{g,t}+\rho A_{g,t}+\theta WA_{g,t}
\]

#### 解释重点

续认模型可以回答：

- 哪些区域不仅吸引企业，而且能帮助企业持续维持高新资格？
- 创新平台、孵化器、高校科研资源是否提升续认概率？
- 小微企业集中区是否续认率较低？
- 成熟产业园区是否具有更高资格维持能力？

---

### 5.3 子模型三：退出代理量预测

#### 因变量

\[
O_{g,t+1}
\]

即下一年高新技术企业资格退出代理量。

#### 推荐模型

| 模型 | 适用性 |
|---|---|
| ZINB / NB | 退出数量为计数型且大量0 |
| 二项Logit | 在上一年活跃企业中预测退出概率 |
| XGBoost | 适合非线性风险预测 |
| 生存分析 | 若企业级历史足够完整，可预测资格持续时间 |

#### 模型形式

\[
O_{g,t+1} \sim f(A_{g,t}, D_{g,t+1}, R_{g,t+1}, X_{g,t})
\]

其中 \(D_{g,t+1}\) 是到期候选企业数量，\(R_{g,t+1}\) 是续认预测量。

#### 解释重点

退出模型可以用于识别：

- 资格流失风险区；
- 创新支撑不足区；
- 小微企业脆弱区；
- 政策培育需要加强的区域。

---

### 5.4 子模型四：活跃存量更新

预测得到进入和退出后，用事件平衡式更新活跃存量：

\[
\hat A_{g,t+1}=A_{g,t}+\hat I_{g,t+1}-\hat O_{g,t+1}
\]

为了避免负值：

\[
\hat A_{g,t+1}=max(0,\ A_{g,t}+\hat I_{g,t+1}-\hat O_{g,t+1})
\]

如果采用持续活跃口径：

\[
\hat A_{g,t+1}=\hat C_{g,t+1}+\hat I_{g,t+1}
\]

其中：

\[
\hat C_{g,t+1}=A_{g,t}-\hat O_{g,t+1}
\]

---

## 6. 年度事件流预测的具体实验步骤

### 步骤1：构建格网—年份建模面板

每条样本为：

```text
grid_id + year
```

目标变量是下一年事件：

```text
entry_proxy_next = entry_proxy_{t+1}
exit_proxy_next = exit_proxy_{t+1}
renewal_proxy_next = renewal_proxy_{t+1}
active_stock_next = active_stock_{t+1}
```

特征变量使用当年或滞后变量：

```text
active_stock_t
entry_proxy_t
exit_proxy_t
renewal_proxy_t
active_stock_t_minus_1
growth_rate_3yr
neighbor_active_stock_t
neighbor_entry_proxy_t
policy_intensity
metro_access
innovation_platform_density
category_entropy
registered_capital_structure
```

Python示例：

```python
panel = panel.sort_values(["grid_id", "year"])

for col in ["active_stock", "entry_proxy", "exit_proxy", "renewal_proxy"]:
    panel[f"{col}_next"] = panel.groupby("grid_id")[col].shift(-1)
    panel[f"{col}_lag1"] = panel.groupby("grid_id")[col].shift(1)

panel["growth_rate_3yr"] = (
    panel.groupby("grid_id")["active_stock"]
    .pct_change(periods=3)
    .replace([float("inf"), -float("inf")], 0)
    .fillna(0)
)

model_data = panel.dropna(subset=[
    "active_stock_next",
    "entry_proxy_next",
    "exit_proxy_next",
    "renewal_proxy_next"
])
```

### 步骤2：构建空间滞后特征

```python
from libpysal.weights import Queen

w = Queen.from_dataframe(grid)
w.transform = "r"

def add_spatial_lag(df_year, var):
    values = df_year[var].fillna(0).values
    return w.sparse @ values

out = []
for year, df_year in panel.groupby("year"):
    df_year = df_year.sort_values("grid_id")
    df_year["neighbor_active_stock"] = add_spatial_lag(df_year, "active_stock")
    df_year["neighbor_entry_proxy"] = add_spatial_lag(df_year, "entry_proxy")
    out.append(df_year)

panel = pd.concat(out)
```

### 步骤3：设置滚动验证

```python
splits = [
    {"train_end": 2019, "test_year": 2020},
    {"train_end": 2020, "test_year": 2021},
    {"train_end": 2021, "test_year": 2022},
    {"train_end": 2022, "test_year": 2023},
    {"train_end": 2023, "test_year": 2024},
]
```

### 步骤4：训练进入、退出、续认子模型

以XGBoost为例：

```python
from xgboost import XGBRegressor

features = [
    "active_stock",
    "entry_proxy",
    "exit_proxy",
    "renewal_proxy",
    "active_stock_lag1",
    "neighbor_active_stock",
    "neighbor_entry_proxy",
    "growth_rate_3yr",
    "policy_intensity",
    "metro_access",
    "innovation_platform_density",
    "producer_service_density",
    "category_entropy"
]

targets = {
    "entry_model": "entry_proxy_next",
    "exit_model": "exit_proxy_next",
    "renewal_model": "renewal_proxy_next"
}

models = {}

for name, target in targets.items():
    model = XGBRegressor(
        n_estimators=500,
        max_depth=4,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="count:poisson",
        random_state=42
    )
    model.fit(train[features], train[target])
    models[name] = model
```

### 步骤5：用事件流公式更新活跃存量

```python
entry_hat = models["entry_model"].predict(test[features])
exit_hat = models["exit_model"].predict(test[features])
renewal_hat = models["renewal_model"].predict(test[features])

test["active_hat_event_flow"] = (
    test["active_stock"] + entry_hat - exit_hat
).clip(lower=0)
```

### 步骤6：评价预测效果

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

y_true = test["active_stock_next"]
y_pred = test["active_hat_event_flow"]

mae = mean_absolute_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
spearman = test[["active_stock_next", "active_hat_event_flow"]].corr(method="spearman").iloc[0, 1]

print(mae, rmse, spearman)
```

### 步骤7：热点命中率评价

```python
threshold_true = test["active_stock_next"].quantile(0.9)
threshold_pred = test["active_hat_event_flow"].quantile(0.9)

test["true_hotspot"] = (test["active_stock_next"] >= threshold_true).astype(int)
test["pred_hotspot"] = (test["active_hat_event_flow"] >= threshold_pred).astype(int)

tp = ((test["true_hotspot"] == 1) & (test["pred_hotspot"] == 1)).sum()
fp = ((test["true_hotspot"] == 0) & (test["pred_hotspot"] == 1)).sum()
fn = ((test["true_hotspot"] == 1) & (test["pred_hotspot"] == 0)).sum()

precision = tp / (tp + fp + 1e-9)
recall = tp / (tp + fn + 1e-9)
f1 = 2 * precision * recall / (precision + recall + 1e-9)
```

### 步骤8：输出地图

输出以下地图：

1. 真实2024活跃存量图；
2. 预测2024活跃存量图；
3. 预测误差图；
4. 真实热点与预测热点叠加图；
5. 高估区图；
6. 低估区图；
7. 预测2025潜在增长区图；
8. 预测2025资格退出风险区图。

---

## 7. 备选方案A：零膨胀负二项回归 ZINB

### 7.1 适用原因

你的格网计数数据很可能存在大量零值：

- 很多500m格网没有高新企业；
- 少数格网企业数量很高；
- 方差大于均值。

这类数据适合使用零膨胀负二项模型。`statsmodels`提供ZeroInflatedNegativeBinomialP接口，可设置计数部分和零膨胀部分。[^zinb]

### 7.2 模型结构

\[
Y_{g,t+1} \sim ZINB(\mu_{g,t+1}, \pi_{g,t+1}, \phi)
\]

计数部分：

\[
\log(\mu_{g,t+1})=\alpha+\beta X_{g,t}+\rho A_{g,t}+\theta WA_{g,t}
\]

零膨胀部分：

\[
logit(\pi_{g,t+1})=\gamma Z_{g,t}
\]

其中：

- \(\mu\)：计数均值；
- \(\pi\)：结构性零概率；
- \(\phi\)：过度离散参数；
- \(X\)：影响因素；
- \(Z\)：是否容易长期为0的空间条件，例如非建设用地、远离中心、远离产业平台等。

### 7.3 Python示例

```python
import statsmodels.api as sm
from statsmodels.discrete.count_model import ZeroInflatedNegativeBinomialP

y = train["entry_proxy_next"]

X = train[[
    "active_stock",
    "neighbor_active_stock",
    "policy_intensity",
    "metro_access",
    "innovation_platform_density",
    "producer_service_density"
]]
X = sm.add_constant(X)

Z = train[[
    "valid_mask",
    "construction_land_ratio",
    "distance_to_center",
    "policy_zone_dummy"
]]
Z = sm.add_constant(Z)

model = ZeroInflatedNegativeBinomialP(
    endog=y,
    exog=X,
    exog_infl=Z,
    inflation="logit"
)

result = model.fit(maxiter=500)
print(result.summary())
```

### 7.4 输出解释

ZINB适合输出：

- 哪些因素显著增加进入数量；
- 哪些因素降低结构性零概率；
- 哪些区域更可能从无企业变成有企业；
- 影响方向和显著性。

---

## 8. 备选方案B：XGBoost/随机森林年度格网面板预测

### 8.1 适用原因

年度时间片少，但格网数量多。将数据组织为格网—年份面板后，样本数量为：

\[
N_{sample}=N_{grid} \times 9
\]

虽然时间只有10年，但每年有大量空间单元，机器学习模型可以学习空间差异、路径依赖和非线性因素。

### 8.2 预测任务

| 任务 | 因变量 |
|---|---|
| 活跃存量直接预测 | `active_stock_next` |
| 进入预测 | `entry_proxy_next` |
| 退出预测 | `exit_proxy_next` |
| 续认预测 | `renewal_proxy_next` |
| 热点分类 | `hotspot_next` |

### 8.3 建议特征

| 类别 | 特征 |
|---|---|
| 时间滞后 | `active_stock`, `active_stock_lag1`, `growth_rate_3yr` |
| 空间滞后 | `neighbor_active_stock`, `neighbor_entry_proxy` |
| 空间位置 | `centroid_x`, `centroid_y`, `district_dummy` |
| 政策平台 | `policy_intensity`, `hightech_zone_dummy` |
| 交通 | `metro_access`, `road_density` |
| 创新资源 | `innovation_platform_density`, `university_distance` |
| 企业结构 | `category_entropy`, `avg_registered_capital`, `large_firm_ratio` |

### 8.4 模型评价重点

机器学习模型容易数值表现较好，但论文要避免只报告RMSE。建议同时报告：

- 数值误差；
- 热点命中率；
- 残差空间自相关；
- 特征重要性；
- SHAP解释图；
- 预测误差地图。

---

## 9. 备选方案C：贝叶斯时空层级模型

### 9.1 适用原因

贝叶斯时空模型特别适合：

- 年度面板不长；
- 空间单元很多；
- 数据有空间相关；
- 希望输出不确定性；
- 需要更强的学术表达。

CARBayesST面向多个时期的非重叠面单元时空数据，通过CAR类先验捕捉空间和时空自相关。[^carbayesst]

### 9.2 模型形式

\[
Y_{g,t} \sim NegativeBinomial(\mu_{g,t}, \phi)
\]

\[
\log(\mu_{g,t})=
\alpha+
\beta X_{g,t-1}+
\rho \log(1+A_{g,t-1})+
u_g+
v_t+
\delta_{g,t}
\]

其中：

- \(u_g\)：空间随机效应；
- \(v_t\)：时间随机效应；
- \(\delta_{g,t}\)：时空交互项；
- \(\rho\)：路径依赖项。

### 9.3 工具选择

| 工具 | 优点 | 难点 |
|---|---|---|
| R `CARBayesST` | 专门处理面单元时空模型 | 需要R环境和邻接矩阵 |
| R-INLA | 高效，适合空间贝叶斯 | 学习成本较高 |
| PyMC | Python生态统一 | 需要自己构建CAR先验 |
| Stan | 灵活 | 空间模型实现成本较高 |

### 9.4 R伪代码

```r
library(CARBayesST)

# W为空间邻接矩阵
# data包含grid_id、year、active_stock、lag_active_stock、covariates

model <- ST.CARar(
  formula = active_stock ~ lag_active_stock + policy_intensity +
            metro_access + innovation_platform_density,
  family = "poisson",
  data = data,
  W = W,
  burnin = 20000,
  n.sample = 100000,
  thin = 10
)

summary(model)
```

### 9.5 输出结果

1. 预测均值图；
2. 预测下限图；
3. 预测上限图；
4. 不确定性图；
5. 高增长概率图；
6. 高退出风险概率图。

例如：

\[
P(A_{g,2025} > A_{g,2024})
\]

可以表达为“增长概率”。

---

## 10. 备选方案D：空间Markov / LISA-Markov格局预测

### 10.1 适用原因

空间Markov不追求精确预测企业数量，而是预测空间等级和格局转移。PySAL `giddy`用于纵向空间数据动态分析，其Spatial Markov和LISA-Markov可显式纳入空间条件和局部空间关联。[^giddy][^lisa_markov]

### 10.2 状态划分

将格网活跃存量划分为：

| 状态 | 含义 |
|---|---|
| S0 | 无高新企业 |
| S1 | 低值 |
| S2 | 中值 |
| S3 | 高值 |
| S4 | 极高值 |

划分方式：

```text
S0：active_stock = 0
S1-S4：对非零格网按四分位数划分
```

### 10.3 转移矩阵

计算：

\[
P(S_{t+1}=j|S_t=i)
\]

进一步加入空间条件：

\[
P(S_{t+1}=j|S_t=i,\ SpatialLagState=k)
\]

### 10.4 LISA-Markov

LISA状态可分为：

| 状态 | 含义 |
|---|---|
| HH | 高—高集聚 |
| LL | 低—低集聚 |
| HL | 高值异常 |
| LH | 低值洼地 |

分析：

- HH → HH：持续热点；
- LH → HH：潜在跃升区；
- HH → LL或非显著：衰退风险区；
- LL → LL：长期低活跃区。

### 10.5 Python示例

```python
import numpy as np
from giddy.markov import Markov, LISA_Markov

# y_matrix: n_grid × n_year
# 每一列为一个年份的状态或数值
markov = Markov(y_matrix)
print(markov.transitions)
print(markov.p)

lisa_markov = LISA_Markov(y_matrix, w, permutations=99)
print(lisa_markov.transitions)
print(lisa_markov.p)
```

### 10.6 输出结果

1. 状态转移矩阵；
2. 空间条件转移矩阵；
3. LISA状态转移图；
4. 持续热点图；
5. 潜在跃升区图；
6. 衰退风险区图。

---

## 11. 是否完全放弃ConvLSTM？

不一定。可以将ConvLSTM降级为以下两种角色。

### 11.1 角色一：不纳入正式实验

这是最稳妥方案。论文中说明：

> 由于年度时间片较少且无法有效季度化，本文不采用ConvLSTM作为主要预测模型。

### 11.2 角色二：探索性对照模型

如果导师希望保留深度学习，可将ConvLSTM作为附录或对照实验，但不能作为主模型。

设定：

```text
输入：过去3年格网矩阵
输出：下一年活跃存量矩阵
样本：滚动窗口 + 空间patch
地位：探索性对照，不作为核心结论依据
```

注意事项：

1. 不宣称ConvLSTM是最优模型。
2. 不用季度伪数据。
3. 只和Persistence、Moving Average、XGBoost等做对照。
4. 重点说明其受限于年度时间片较少。
5. 若结果不好，也可以作为“深度学习不适合该数据条件”的方法讨论。

---

## 12. 最推荐的最终预测实验组合

建议最终采用：

| 层次 | 模型 | 作用 |
|---|---|---|
| 基准层 | Persistence、Moving Average | 判断预测是否真正优于简单外推 |
| 格局层 | 空间Markov、LISA-Markov | 解释热点等级转移 |
| 解释层 | ZINB / NB | 解释进入、退出、续认的影响因素 |
| 预测层 | XGBoost / 随机森林 | 提高年度格网预测精度 |
| 机制层 | 事件流状态转移模型 | 主模型，符合高新资格生命周期 |
| 不确定性层 | 贝叶斯时空层级模型 | 输出预测可信区间和风险概率 |
| 深度学习层 | ConvLSTM | 可选探索性对照，不推荐主模型 |

### 12.1 主模型命名建议

你可以把主模型命名为：

**“基于事件流状态转移的年度时空预测模型”**

英文可写为：

**Event-flow State Transition Spatiotemporal Prediction Model**

缩写：

```text
EF-STP
```

论文中可以这样表述：

> 本文构建EF-STP模型，将高新技术企业未来活跃存量分解为进入、退出和持续活跃三个事件过程，并结合空间滞后特征、政策平台变量和创新资源变量，对500m格网尺度下的高新技术企业年度空间分布进行预测。

---

## 13. 年度预测实验设计总表

| 实验编号 | 实验名称 | 输入 | 输出 | 评价指标 |
|---|---|---|---|---|
| P1 | 简单外推基准 | \(A_{t}\) | \(\hat A_{t+1}\) | MAE、RMSE |
| P2 | 三年移动平均 | \(A_{t},A_{t-1},A_{t-2}\) | \(\hat A_{t+1}\) | MAE、RMSE |
| P3 | 空间Markov | 状态等级序列 | 下一年等级 | 状态准确率、转移矩阵 |
| P4 | LISA-Markov | LISA状态序列 | 下一年LISA状态 | HH命中率、跃升区识别 |
| P5 | ZINB进入模型 | 滞后变量+空间变量 | 进入代理量 | MAE、系数显著性 |
| P6 | ZINB退出模型 | 到期候选+空间变量 | 退出代理量 | MAE、风险区识别 |
| P7 | XGBoost直接预测 | 格网面板特征 | 活跃存量 | MAE、RMSE、Top-K |
| P8 | EF-STP事件流模型 | 进入、退出、续认子模型 | 活跃存量 | MAE、RMSE、热点F1 |
| P9 | 贝叶斯时空模型 | 格网面板+邻接矩阵 | 活跃存量分布 | 可信区间覆盖率 |
| P10 | ConvLSTM探索对照 | 3年矩阵窗口 | 下一年矩阵 | 仅对照，不作主结论 |

---

## 14. 预测结果可视化设计

### 14.1 数值预测图

1. 真实活跃存量图；
2. 预测活跃存量图；
3. 预测误差图；
4. 标准化残差图；
5. 高估区图；
6. 低估区图。

### 14.2 热点预测图

1. 真实热点图；
2. 预测热点图；
3. 热点命中图；
4. 漏判热点图；
5. 误判热点图；
6. 新兴热点预测图。

### 14.3 事件流图

1. 预测进入热点图；
2. 预测退出风险图；
3. 预测续认优势图；
4. 预测持续活跃核心区图；
5. 预测增长潜力区图：

\[
GrowthPotential_{g,t+1}=\hat I_{g,t+1}-\hat O_{g,t+1}
\]

### 14.4 不确定性图

贝叶斯模型可以输出：

1. 预测均值图；
2. 95%可信区间宽度图；
3. 增长概率图；
4. 退出风险概率图；
5. 热点概率图。

---

## 15. 预期研究结论

### 15.1 方法结论

在年度高新技术企业数据条件下，事件流状态转移模型比ConvLSTM更适合。原因是该模型利用了高新技术企业资格3年有效期和续认制度，能够将未来活跃存量拆解为进入、退出和持续活跃过程，既符合数据粒度，也具有更强解释性。

### 15.2 空间预测结论

预计成熟高新企业集聚区具有较强路径依赖，未来仍可能保持高活跃存量；新兴增长区更可能位于政策平台、产业园区、交通改善区和创新资源外溢区；退出风险区可能集中在创新支撑不足、企业规模偏小或续认基础较弱的格网。

### 15.3 模型比较结论

预期结果可能为：

1. Persistence模型在成熟热点区表现尚可，但难以预测新兴增长区。
2. Moving Average能平滑波动，但对突增区域不敏感。
3. ZINB解释性较强，但非线性捕捉能力有限。
4. XGBoost/随机森林预测精度较好，但需要结合SHAP或变量重要性解释。
5. EF-STP事件流模型在解释性和预测性之间最平衡。
6. 贝叶斯时空模型能提供不确定性，适合作为高级补充。
7. ConvLSTM受限于年度时间片较少，可能不稳定。

### 15.4 政策结论

1. 对预测进入热点区，应提前布局孵化器、研发服务、金融服务和产业配套。
2. 对预测退出风险区，应加强高新资格续认辅导、研发投入支持和知识产权服务。
3. 对持续热点区，应从招商扩张转向创新质量提升和企业梯度培育。
4. 对政策平台覆盖但预测增长不足的区域，应检查平台政策、空间供给、交通和创新服务是否真正转化为企业集聚。

---

## 16. 推荐写入论文的方法表述

### 16.1 方法选择说明

```text
考虑到本文高新技术企业数据以年度为有效统计单位，且企业认定登记信息集中于年末，月度或季度时间信息不具备真实动态解释意义。因此，本文不采用基于高频时空序列的ConvLSTM作为主预测模型，而是构建年度格网面板数据，并基于高新技术企业资格生命周期设计事件流状态转移预测框架。
```

### 16.2 主模型表述

```text
本文将格网未来活跃存量拆解为进入、退出和持续活跃三个事件过程，分别构建进入代理量预测模型、退出代理量预测模型和续认代理量预测模型，并通过存量—流量平衡关系更新下一年度活跃存量。该方法既能够利用格网尺度的空间邻近效应和影响因素变量，又能够体现高新技术企业资格有效期与续认制度约束。
```

### 16.3 ConvLSTM处理表述

```text
ConvLSTM适用于连续密集时空序列预测，但本文数据仅包含2015—2024年10个真实年度时间截面，无法形成充足的时序训练样本。为避免伪季度序列造成模型偏误，本文未将ConvLSTM作为主模型，仅在扩展实验中作为探索性对照，或不纳入正式模型比较。
```

---

## 17. 最终建议

建议你最终将时空预测章节设计为：

```text
第六章 基于年度事件流状态转移的广州市高新技术企业时空预测

6.1 年度时空预测问题定义
6.2 ConvLSTM适用性讨论与方法调整
6.3 年度格网面板构建
6.4 事件流状态转移预测模型
6.5 对照模型：Persistence、Moving Average、ZINB、XGBoost、空间Markov
6.6 滚动时间验证与评价指标
6.7 预测结果分析
6.8 未来增长区、续认优势区与退出风险区识别
6.9 小结
```

这比直接使用ConvLSTM更稳妥，也更容易形成具有解释性的GIS硕士论文成果。

---

## 18. 参考资料

[^hitech3y]: 国务院公报，《高新技术企业认定管理办法》，第九条规定“通过认定的高新技术企业，其资格自颁发证书之日起有效期为3年”。https://www.gov.cn/gongbao/content/2016/content_5076985.htm

[^convlstm]: Shi et al., *Convolutional LSTM Network: A Machine Learning Approach for Precipitation Nowcasting*. https://proceedings.neurips.cc/paper/5955-convolutional-lstm-network-a-

[^zinb]: Statsmodels Documentation, *ZeroInflatedNegativeBinomialP*. https://www.statsmodels.org/stable/generated/statsmodels.discrete.count_model.ZeroInflatedNegativeBinomialP.html

[^rf]: Scikit-learn Documentation, *RandomForestRegressor*. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

[^xgb]: XGBoost Documentation, *Python API Reference*. https://docs.xgboost.com.cn/en/stable/python/python_api.html

[^carbayesst]: CRAN, *CARBayesST: Spatio-Temporal Areal Unit Modelling in R*. https://cran.r-project.org/web/packages/CARBayesST/vignettes/CARBayesST.pdf

[^giddy]: PySAL, *GeospatIal Distribution DYnamics (GIDDY)*. https://pysal.org/giddy/

[^lisa_markov]: PySAL, *giddy.markov.LISA_Markov*. https://pysal.org/giddy/generated/giddy.markov.LISA_Markov.html
