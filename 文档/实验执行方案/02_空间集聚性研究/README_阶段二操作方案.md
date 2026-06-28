# 阶段二：空间集聚性研究 ArcGIS Pro 操作方案

## 1. 阶段定位

阶段二是论文的第一个实证分析模块，承接阶段一已经完成的企业动态变量与 500m 格网数据底板，目标是回答三个问题：

1. 广州市高新技术企业在 2015-2024 年是否存在显著空间集聚；
2. 企业活跃存量、新增进入、续认能力和退出代理的空间格局是否不同；
3. 企业集聚热点是否存在扩展、强化、转移或衰退过程。

本阶段所有空间统计和地图表达均建议在 ArcGIS Pro 中完成。Python 只作为必要的数据核对或表格整理辅助，不作为主要空间分析平台。

## 2. 本阶段核心结论目标

完成阶段二后，论文应能形成以下结论链条：

```text
年度分布格局
  -> 企业数量增长和空间覆盖扩展
  -> 全局空间自相关检验是否集聚
  -> LISA 识别局部高值集聚和异常格网
  -> Gi* 识别热点、冷点和热点演化
  -> 比较活跃、新增、续认、退出代理及企业结构差异
  -> 为阶段三影响因素研究提供被解释对象
```

正文中不要只展示“企业越来越多”，而要明确回答：

```text
是否集聚？
在哪里集聚？
哪些区域持续集聚？
哪些区域新兴增长？
哪些动态变量的空间格局不同？
```

## 3. 推荐输出目录

在实际执行阶段二时，建议建立以下目录：

```text
阶段二：空间集聚性研究/
├─ 0、输入数据副本/
├─ 1、ArcGIS工程/
│  ├─ stage2_spatial_agglomeration.aprx
│  └─ stage2_spatial_agglomeration.gdb
├─ 2、年度格网图层/
├─ 3、描述性统计/
├─ 4、年度空间分布图/
├─ 5、全局空间自相关/
├─ 6、局部空间自相关_LISA/
├─ 7、热点分析_GiStar/
├─ 8、时空热点演化/
├─ 9、企业结构分类比较/
├─ 10、稳健性检验/
├─ 11、论文图件/
├─ 12、质检报告/
└─ 13、结果说明文档/
```

其中，`11、论文图件` 用于保存最终可放入论文或答辩 PPT 的地图；其他目录用于保存中间结果、ArcGIS Pro 输出图层和统计表。

## 4. 输入数据

### 4.1 首选输入数据

当前阶段一已经形成可用数据底板，阶段二优先使用以下文件：

```text
阶段一：企业动态变量研究/
├─ 7、最终格网标准数据/
│  ├─ 1、基础元数据/master_grid_metadata.csv
│  ├─ 2、面板数据/master_grid_year_panel.csv
│  ├─ 3、年度csv/master_grid_panel_2015.csv
│  ├─ ...
│  ├─ 3、年度csv/master_grid_panel_2024.csv
│  └─ 4、空间图层/主格网年度面板.gdb
└─ 8、最终点位数据/
   └─ 1、主格网对齐点位表/firm_year_points_2015_2024.csv
```

核心格网面板字段包括：

```text
grid_id, year, row_id, col_id, centroid_x, centroid_y,
cover_ratio, boundary_mask, valid_mask,
active_cnt, entry_cnt, persist_cnt, renew_cnt, exit_next_cnt,
capital_mean, capital_median, capital_sum,
n_size_微型, n_size_小型, n_size_中型, n_size_大型, n_size_未知,
n_cat_电子信息, n_cat_高技术服务, n_cat_先进制造与自动化技术,
n_cat_新材料技术, n_cat_生物与新医药技术, n_cat_资源与环境技术,
n_cat_新能源与节能技术, n_cat_航空航天技术
```

### 4.2 使用原则

1. 阶段二只读使用阶段一成果，不回改阶段一原始数据。
2. 主分析使用 `master_grid_year_panel.csv` 或年度 CSV。
3. 若 `主格网年度面板.gdb` 中已经有年度格网图层，可直接复制到阶段二工程库使用。
4. 若年度图层未整理好，则使用阶段一主格网空间图层作为几何底图，再按 `grid_id + year` 或按年度 CSV 连接属性。
5. 空间统计应保留所有 `valid_mask = 1` 的有效格网，零值格网不能随意删除，否则会夸大集聚程度。

## 5. 变量选择

### 5.1 主变量

| 变量 | 研究含义 | 阶段二用途 |
|---|---|---|
| `active_cnt` | 年度活跃高新技术企业数量 | 主线变量，用于年度分布、Moran、LISA、Gi*、热点演化 |
| `entry_cnt` | 新进入高新资格体系的企业数量代理 | 分析新增增长空间 |
| `renew_cnt` | 续认企业数量代理 | 分析高新资格稳定性和持续创新能力 |
| `exit_next_cnt` | 下一年退出代理 | 分析潜在资格退出风险 |

### 5.2 企业结构变量

| 变量 | 研究含义 | 建议用途 |
|---|---|---|
| `capital_sum` | 格网注册资本总量 | 资本强度集聚分析 |
| `capital_mean` | 格网平均注册资本 | 企业质量或资本基础辅助分析 |
| `n_size_微型`、`n_size_小型` | 小微企业数量 | 孵化型、成长型企业空间格局 |
| `n_size_中型`、`n_size_大型` | 中大型企业数量 | 成熟企业空间格局 |
| `n_cat_*` | 不同高新技术门类数量 | 技术门类差异分析 |

### 5.3 年份使用限制

1. `2015` 年是面板起始年份，`entry_cnt` 不宜完全解释为真实新增企业。
2. `2024` 年缺少下一年观测，`exit_next_cnt` 存在右删失，不宜作为真实退出零值解释。
3. `active_cnt` 可用于 2015-2024 全部年份。
4. `entry_cnt`、`renew_cnt`、`exit_next_cnt` 可用于空间格局比较，但正文解释要标注代理变量属性。

## 6. ArcGIS Pro 工程准备

### 步骤 1：新建阶段二工程

在 ArcGIS Pro 中新建工程：

```text
工程名称：stage2_spatial_agglomeration
工程位置：阶段二：空间集聚性研究/1、ArcGIS工程/
默认数据库：stage2_spatial_agglomeration.gdb
```

建议在工程中建立以下地图：

```text
Map_年度分布
Map_GlobalMoran
Map_LISA
Map_GiStar
Map_热点演化
Map_企业结构比较
Map_论文图件
```

### 步骤 2：导入阶段一图层

在 ArcGIS Pro 中执行：

```text
Catalog
-> Folders
-> Add Folder Connection
-> 连接项目根目录
-> 找到 阶段一：企业动态变量研究/7、最终格网标准数据/4、空间图层/主格网年度面板.gdb
```

将其中可用的主格网或年度面板图层复制到：

```text
阶段二：空间集聚性研究/1、ArcGIS工程/stage2_spatial_agglomeration.gdb
```

如果 GDB 中已有年度格网图层，建议统一命名：

```text
grid_panel_2015
grid_panel_2016
...
grid_panel_2024
```

如果 GDB 中只有主格网底图，则按下一步从年度 CSV 连接属性。

### 步骤 3：从年度 CSV 生成年度格网图层

如果需要手动构建年度图层，按以下方式执行：

1. 将主格网空间图层复制为 `grid_panel_YYYY`。
2. 添加对应年度 CSV：

```text
阶段一：企业动态变量研究/7、最终格网标准数据/3、年度csv/master_grid_panel_YYYY.csv
```

3. 使用 `Add Join`：

```text
目标图层字段：grid_id
连接表字段：grid_id
连接类型：保留所有目标要素
```

4. 使用 `Export Features` 导出为永久图层：

```text
2、年度格网图层/grid_panel_YYYY
```

5. 每个年度图层设置定义查询：

```text
valid_mask = 1
```

注意：不要设置 `active_cnt > 0` 作为空间统计分析条件。零值有效格网是空间分布的重要组成部分。

## 7. 描述性统计

### 7.1 年度统计表

在 ArcGIS Pro 中可使用：

```text
Analysis
-> Tools
-> Summary Statistics
```

或在属性表中右键字段查看统计。

每年统计以下指标：

| 指标 | 字段 |
|---|---|
| 年度活跃企业总量 | `SUM(active_cnt)` |
| 年度新增进入量 | `SUM(entry_cnt)` |
| 年度续认量 | `SUM(renew_cnt)` |
| 年度退出代理量 | `SUM(exit_next_cnt)` |
| 活跃格网数量 | `active_cnt > 0` 的格网数 |
| 高承载格网数量 | `active_cnt >= 10` 的格网数 |
| 单格网最大值 | `MAX(active_cnt)` |
| 零值比例 | `active_cnt = 0` 的格网比例 |
| 资本总量 | `SUM(capital_sum)` |

建议输出：

```text
3、描述性统计/yearly_summary.csv
3、描述性统计/grid_load_summary.csv
```

### 7.2 已知阶段一基准值

这些数值可作为 ArcGIS Pro 统计结果的核对基准：

| 指标 | 2015 | 2024 |
|---|---:|---:|
| 活跃企业记录 | 1,865 | 13,523 |
| 活跃格网数量 | 944 | 3,269 |
| `active_cnt >= 10` 高承载格网 | 18 | 290 |
| 单格网最大企业数 | 32 | 117 |
| Gini 系数 | 约 0.981 | 约 0.953 |
| 前 1% 格网承载比例 | 约 63.70% | 约 45.52% |

如果 ArcGIS Pro 统计结果与上述数值差距较大，优先检查是否错误删除了零值格网、是否重复连接 CSV、是否只选择了部分行政区或是否未筛选 `valid_mask = 1`。

## 8. 年度空间分布图

### 8.1 制图年份

正文建议展示四个代表年份：

```text
2015、2018、2021、2024
```

完整 2015-2024 十年图可放入附录或阶段成果文件夹。

### 8.2 制图变量

主图：

```text
active_cnt
```

补充图：

```text
entry_cnt
renew_cnt
exit_next_cnt
capital_sum
```

### 8.3 符号系统建议

`active_cnt` 建议使用固定分级，保证跨年可比：

```text
0
1
2-4
5-9
10-19
20-49
50及以上
```

ArcGIS Pro 操作：

```text
Layer Properties
-> Symbology
-> Graduated Colors
-> Field: active_cnt
-> Method: Manual Interval
-> Classes: 固定断点
```

建议色带：

```text
浅黄 -> 橙色 -> 深红
```

注意：

1. 10 年图必须使用同一色带、同一分级、同一地图范围。
2. 零值格网可设置为极浅灰或透明浅灰。
3. 地图中建议标注天河、黄埔、番禺、南沙等重点区域，但不要让标注遮挡热点区。

输出：

```text
4、年度空间分布图/map_active_cnt_2015.png
4、年度空间分布图/map_active_cnt_2018.png
4、年度空间分布图/map_active_cnt_2021.png
4、年度空间分布图/map_active_cnt_2024.png
```

论文图件建议：

```text
11、论文图件/图4-1_高新技术企业活跃存量年度空间分布.png
```

## 9. 空间权重设置

空间统计前必须统一空间关系概念。建议主分析使用 Queen 邻接，稳健性使用 KNN 或距离权重。

### 9.1 主分析权重

ArcGIS Pro 工具：

```text
Spatial Statistics Tools
-> Modeling Spatial Relationships
-> Generate Spatial Weights Matrix
```

推荐参数：

| 参数 | 设置 |
|---|---|
| Input Feature Class | `grid_panel_YYYY` 或统一有效格网 |
| Unique ID Field | `grid_id` |
| Conceptualization of Spatial Relationships | Contiguity edges corners |
| Row Standardization | Row |
| Output Spatial Weights Matrix File | `weights_queen.swm` |

`Contiguity edges corners` 对应 Queen 邻接，适合 500m 规则格网。

### 9.2 稳健性权重

补充生成：

```text
weights_knn8.swm
weights_distance.swm
```

建议：

1. KNN 使用 `Number of Neighbors = 8`；
2. 距离权重阈值可先用 `Calculate Distance Band from Neighbor Count` 获取建议距离；
3. 所有权重矩阵均记录参数，写入质检报告。

输出：

```text
5、全局空间自相关/weights_queen.swm
10、稳健性检验/weights_knn8.swm
10、稳健性检验/weights_distance.swm
12、质检报告/qc_spatial_weights.md
```

## 10. 全局空间自相关 Moran's I

### 10.1 研究目的

全局 Moran's I 用于判断企业格网分布是否整体存在空间集聚。论文中需要报告：

```text
Moran's I 值
Z-score
p-value
显著性水平
空间关系设置
```

### 10.2 ArcGIS Pro 操作

工具路径：

```text
Spatial Statistics Tools
-> Analyzing Patterns
-> Spatial Autocorrelation (Global Moran's I)
```

主分析变量：

```text
active_cnt
```

补充变量：

```text
entry_cnt
renew_cnt
exit_next_cnt
capital_sum
n_cat_电子信息
n_cat_高技术服务
n_cat_先进制造与自动化技术
```

参数建议：

| 参数 | 设置 |
|---|---|
| Input Feature Class | `grid_panel_YYYY` |
| Input Field | 对应变量 |
| Conceptualization | Get spatial weights from file |
| Weights Matrix File | `weights_queen.swm` |
| Row Standardization | Row |

### 10.3 执行顺序

建议先做：

```text
active_cnt: 2015-2024 全部年份
```

再做：

```text
entry_cnt: 2016、2018、2021、2024
renew_cnt: 2018、2021、2024
exit_next_cnt: 2016、2019、2022、2023
```

注意：`exit_next_cnt` 不建议使用 2024 年解释退出。

### 10.4 输出表

整理成：

```text
5、全局空间自相关/global_moran_active_yearly.csv
5、全局空间自相关/global_moran_dynamic_variables.csv
11、论文图件/图4-2_Global_Moran_I年度变化.png
```

结果表字段建议：

| 字段 | 含义 |
|---|---|
| `year` | 年份 |
| `variable` | 变量 |
| `moran_i` | Moran's I |
| `expected_i` | 随机期望值 |
| `z_score` | 标准化统计量 |
| `p_value` | 显著性 |
| `weight_type` | 权重矩阵 |

## 11. 局部空间自相关 LISA

### 11.1 研究目的

LISA 用于识别局部空间集聚类型：

| 类型 | 解释 | 论文含义 |
|---|---|---|
| HH | 高值-高值 | 企业高值集聚区 |
| LL | 低值-低值 | 低值集聚区或外围低密区域 |
| HL | 高值-低值 | 局部高值异常点 |
| LH | 低值-高值 | 被高值区包围的低值洼地 |
| NS | 不显著 | 无显著局部空间关联 |

### 11.2 ArcGIS Pro 操作

工具路径：

```text
Spatial Statistics Tools
-> Mapping Clusters
-> Cluster and Outlier Analysis (Anselin Local Moran's I)
```

主变量：

```text
active_cnt
```

建议年份：

```text
2015、2018、2021、2024
```

参数建议：

| 参数 | 设置 |
|---|---|
| Input Feature Class | `grid_panel_YYYY` |
| Input Field | `active_cnt` |
| Conceptualization | Get spatial weights from file |
| Weights Matrix File | `weights_queen.swm` |
| Row Standardization | Row |
| Apply False Discovery Rate Correction | 可勾选，论文中说明 |

### 11.3 输出图层

工具会生成字段，如：

```text
COType
LMIIndex
LMIZScore
LMIPValue
```

建议导出：

```text
6、局部空间自相关_LISA/lisa_active_2015
6、局部空间自相关_LISA/lisa_active_2018
6、局部空间自相关_LISA/lisa_active_2021
6、局部空间自相关_LISA/lisa_active_2024
```

### 11.4 制图规则

LISA 图建议颜色：

| 类型 | 建议颜色 |
|---|---|
| HH | 深红 |
| LL | 深蓝 |
| HL | 橙色 |
| LH | 浅蓝 |
| NS | 浅灰或透明 |

论文图件：

```text
11、论文图件/图4-3_代表年份LISA聚类图.png
```

## 12. Getis-Ord Gi* 热点分析

### 12.1 研究目的

Gi* 热点分析用于识别高值热点和低值冷点，比 LISA 更适合表达连续热点区。论文中建议将其作为阶段二的核心地图成果。

### 12.2 ArcGIS Pro 操作

工具路径：

```text
Spatial Statistics Tools
-> Mapping Clusters
-> Hot Spot Analysis (Getis-Ord Gi*)
```

主变量：

```text
active_cnt
```

补充变量：

```text
entry_cnt
renew_cnt
exit_next_cnt
```

参数建议：

| 参数 | 设置 |
|---|---|
| Input Feature Class | `grid_panel_YYYY` |
| Input Field | 对应变量 |
| Conceptualization | Get spatial weights from file |
| Weights Matrix File | `weights_queen.swm` |
| Row Standardization | Row |
| Apply False Discovery Rate Correction | 建议勾选 |

### 12.3 热点等级解释

输出字段通常包括：

```text
Gi_Bin
GiZScore
GiPValue
```

`Gi_Bin` 解释：

| 值 | 含义 |
|---:|---|
| 3 | 99% 置信度热点 |
| 2 | 95% 置信度热点 |
| 1 | 90% 置信度热点 |
| 0 | 不显著 |
| -1 | 90% 置信度冷点 |
| -2 | 95% 置信度冷点 |
| -3 | 99% 置信度冷点 |

### 12.4 输出

```text
7、热点分析_GiStar/hotspot_active_2015
7、热点分析_GiStar/hotspot_active_2018
7、热点分析_GiStar/hotspot_active_2021
7、热点分析_GiStar/hotspot_active_2024
11、论文图件/图4-4_代表年份GiStar热点图.png
```

动态变量可输出：

```text
7、热点分析_GiStar/hotspot_entry_YYYY
7、热点分析_GiStar/hotspot_renew_YYYY
7、热点分析_GiStar/hotspot_exit_YYYY
```

## 13. 时空热点演化

### 13.1 研究目的

时空热点演化用于判断热点是否是新出现、连续存在、增强、减弱或振荡。该部分是阶段二从“静态热点图”提升到“时空演化研究”的关键。

### 13.2 ArcGIS Pro 工具

使用：

```text
Space Time Pattern Mining Tools
-> Create Space Time Cube From Defined Locations
-> Emerging Hot Spot Analysis
```

### 13.3 数据组织

推荐使用固定 500m 格网位置和 2015-2024 年度值：

| 参数 | 设置 |
|---|---|
| Location ID | `grid_id` |
| Time Field | `year` |
| Analysis Field | `active_cnt` |
| Time Step Interval | 1 Years |
| Aggregation | Defined Locations |
| Fill Missing Values | 使用固定面板补零结果 |

如果 ArcGIS Pro 无法直接从面板表创建时空立方体，建议先使用阶段一完整年度面板或在 ArcGIS Pro 中构建长表图层，保证每个 `grid_id` 均有 2015-2024 年记录。

### 13.4 输出类型

Emerging Hot Spot Analysis 会输出：

```text
New Hot Spot
Consecutive Hot Spot
Intensifying Hot Spot
Persistent Hot Spot
Diminishing Hot Spot
Sporadic Hot Spot
Oscillating Hot Spot
Historical Hot Spot
No Pattern Detected
```

论文中重点解释：

| 类型 | 论文解释 |
|---|---|
| New Hot Spot | 新兴增长区域 |
| Intensifying Hot Spot | 集聚强度增强区域 |
| Persistent Hot Spot | 稳定核心集聚区域 |
| Diminishing Hot Spot | 热点减弱区域 |
| Historical Hot Spot | 曾经集聚但后期减弱区域 |

输出：

```text
8、时空热点演化/active_space_time_cube.nc
8、时空热点演化/emerging_hotspot_active
11、论文图件/图4-5_高新技术企业时空热点演化类型图.png
```

## 14. 企业结构分类比较

### 14.1 比较内容

不要把所有技术门类和企业规模都放入正文。建议正文选择三类比较：

1. 企业规模：小微企业与中大型企业；
2. 技术门类：电子信息、高技术服务、先进制造与自动化技术；
3. 注册资本：企业数量集聚与资本强度集聚。

### 14.2 建议构建字段

如果 ArcGIS Pro 中还没有这些字段，可使用 `Calculate Field` 构建：

```text
small_micro_cnt = n_size_微型 + n_size_小型
medium_large_cnt = n_size_中型 + n_size_大型
capital_log = Log10(capital_sum + 1)
cat_main_einfo = n_cat_电子信息
cat_main_service = n_cat_高技术服务
cat_main_manu = n_cat_先进制造与自动化技术
```

### 14.3 分析方式

对上述变量可执行：

1. 年度分布图；
2. Gi* 热点分析；
3. 与 `active_cnt` 热点结果叠加比较。

输出：

```text
9、企业结构分类比较/map_size_comparison_2024.png
9、企业结构分类比较/map_category_comparison_2024.png
9、企业结构分类比较/map_capital_hotspot_2024.png
```

## 15. 稳健性检验

阶段二至少完成以下稳健性检查：

| 检查 | 目的 |
|---|---|
| Queen 邻接 vs KNN8 | 检查空间权重选择是否影响结果 |
| Queen 邻接 vs 距离权重 | 检查距离阈值设定影响 |
| 保留边界格网 vs 剔除 `boundary_mask = 1` | 检查边界格网影响 |
| `active_cnt` vs `capital_sum` | 检查数量集聚与资本强度集聚是否一致 |
| 2015、2018、2021、2024 代表年份对比 | 检查时序演化结论是否稳定 |

稳健性结果不一定全部放入正文，但应在阶段成果中保存。

输出：

```text
10、稳健性检验/robustness_weights_comparison.csv
10、稳健性检验/robustness_boundary_grid.md
10、稳健性检验/robustness_active_vs_capital.md
```

## 16. 论文图表建议

| 编号 | 图表 |
|---|---|
| 图 4-1 | 2015、2018、2021、2024 年高新技术企业活跃存量空间分布图 |
| 图 4-2 | 2015-2024 年活跃企业数量、活跃格网和高承载格网变化图 |
| 图 4-3 | Global Moran's I 年度变化图 |
| 图 4-4 | 代表年份 LISA 局部空间聚类图 |
| 图 4-5 | 代表年份 Getis-Ord Gi* 热点图 |
| 图 4-6 | 高新技术企业时空热点演化类型图 |
| 图 4-7 | 不同企业结构类型热点比较图 |
| 表 4-1 | 年度描述性统计表 |
| 表 4-2 | Global Moran's I 结果表 |
| 表 4-3 | 热点区数量和面积变化表 |

## 17. 阶段二结果解释模板

### 17.1 全局 Moran's I

可按以下逻辑解释：

```text
Global Moran's I 结果显示，2015-2024 年广州市高新技术企业活跃存量在 500m 格网尺度下整体呈现显著正向空间自相关，说明企业分布并非随机分布，而是存在明显空间集聚。随着研究期内企业数量增长和活跃格网扩展，Moran's I 的变化反映了企业集聚强度和空间扩散过程之间的关系。
```

### 17.2 LISA

```text
LISA 结果进一步表明，高值-高值集聚区主要分布于创新资源、产业平台和城市功能条件较强的区域，低值-低值集聚区主要位于企业分布较稀疏的外围区域。不同年份 LISA 类型变化揭示了高新技术企业集聚核心区的强化、扩展和局部转移过程。
```

### 17.3 Gi* 热点

```text
Gi* 热点分析显示，高新技术企业热点区具有较强的连续性和扩展性。活跃企业热点主要反映既有产业基础和创新资源集聚，新进入企业热点更能反映新兴增长空间，续认企业热点则体现企业持续创新能力和高新资格稳定性。
```

### 17.4 时空热点演化

```text
时空热点演化结果可进一步区分持续热点、新兴热点、增强热点和减弱热点。持续热点可视为高新技术企业稳定核心承载区，新兴热点反映未来增长空间，减弱或历史热点则提示部分区域企业集聚优势可能下降。
```

## 18. 质检清单

执行阶段二后，逐项检查：

1. 年度图层是否均为 `valid_mask = 1` 的有效格网；
2. 是否保留零值有效格网；
3. `active_cnt` 年度汇总是否与阶段一统计一致；
4. 年度地图是否使用统一范围、统一色带和统一分级；
5. Moran、LISA、Gi* 是否使用同一主权重矩阵；
6. 权重矩阵参数是否记录；
7. 2024 年 `exit_next_cnt` 是否避免解释为真实零退出；
8. 2015 年 `entry_cnt` 是否避免解释为真实新增起点；
9. 论文图件是否包含比例尺、指北针、图例、数据来源和年份；
10. 结果表和图件命名是否能对应论文图表编号。

## 19. 完成标准

阶段二完成时，应至少形成：

1. 2015-2024 年度格网图层；
2. 年度描述性统计表；
3. `active_cnt` 年度空间分布图；
4. Global Moran's I 年度结果表和趋势图；
5. 代表年份 LISA 图；
6. 代表年份 Gi* 热点图；
7. 时空热点演化图；
8. 企业规模、技术门类和注册资本结构比较图；
9. 空间权重和数据口径质检报告；
10. 可写入论文第四章的阶段二文字结论。
