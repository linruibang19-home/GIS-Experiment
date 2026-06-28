# 最终格网标准数据说明

## 一、目录定位

本目录是本研究后续全部分析任务的唯一标准数据目录。

从本目录开始，所有研究统一采用“主格网”体系，不再以旧的 clip 格网随机 `grid_id` 作为正式分析底板。

主格网体系的核心原则如下：

- 统一使用完整规则 500m 格网作为唯一主格网。
- 统一使用主格网标准标识：`grid_id`、`row_id`、`col_id`、`centroid_x`、`centroid_y`。
- 边界裁剪问题通过 `cover_ratio` 和 `boundary_mask` 表达。
- 市外格网通过 `valid_mask=0` 表达。
- 后续空间统计、影响因素分析、深度学习实验全部以本目录中的文件为准。

## 二、目录结构

```text
7、最终格网标准数据/
├─ 1、基础元数据/
├─ 2、面板数据/
├─ 3、年度csv/
├─ 4、空间图层/
└─ README_最终格网标准数据.md
```

## 三、各目录与文件说明

### 1、基础元数据

该目录存放主格网体系的基础元信息和旧新格网映射关系，是后续全部数据解释与追溯的基础。

#### 1. `master_grid_metadata.csv`

作用：

- 存放完整主格网的标准元数据。
- 是整个主格网体系的基础底表。
- 适用于构建完整规则矩阵、校验格网坐标、深度学习张量索引、空间可视化对照等任务。

核心字段：

- `grid_id`：主格网标准ID，格式为 `RxxxCxxx`。
- `row_id`：主格网行号。
- `col_id`：主格网列号。
- `centroid_x`：主格网标准质心 X 坐标。
- `centroid_y`：主格网标准质心 Y 坐标。
- `master_area`：完整主格网面积，理论上为 250000 平方米。

说明：

- 该文件包含全部完整主格网，不仅包含广州市内格网，也包含市外补齐格网。
- 该文件主要用于主格网定义与索引，不直接承载年度业务变量。

#### 2. `clip_to_master_grid_mapping.csv`

作用：

- 存放旧 clip 格网随机 `grid_id` 到主格网标准 `grid_id` 的映射关系。
- 用于把历史成果从 clip 格网体系平滑切换到主格网体系。
- 是历史结果追溯和方法论说明的重要桥梁文件。

核心字段：

- `old_grid_id`：旧 clip 格网ID，如 `G000001`。
- `new_grid_id`：新主格网ID，如 `R079C109`。
- `row_id`：对应主格网行号。
- `col_id`：对应主格网列号。
- `old_centroid_x`、`old_centroid_y`：旧 clip 格网质心坐标。
- `centroid_x`、`centroid_y`：新主格网标准质心坐标。
- `clip_area`：clip 格网实际面积。
- `master_area`：主格网标准面积。
- `cover_ratio`：`clip_area / master_area`。
- `boundary_mask`：边界格网标记，边界格网为 1，非边界格网为 0。
- `valid_mask`：广州市内有效格网标记，映射到的 clip 格网均为 1。
- `offset_m`：旧 clip 质心与主格网质心的偏移距离。
- `join_count`：空间映射时的匹配数量。

说明：

- 本文件是旧体系与新体系之间的唯一正式映射表。
- 如需追溯旧图层、旧统计结果、旧随机格网编号，统一以此文件为准。

#### 3. `clip_to_master_grid_mapping_report.txt`

作用：

- 存放 clip 格网到主格网映射的质量报告。
- 用于检查映射是否存在漏配、多配、边界异常等问题。

主要内容：

- clip 格网总数。
- 未匹配数量。
- `Join_Count != 1` 的数量。
- 边界格网数量。
- 最大质心偏移距离。

说明：

- 本次结果中，映射已通过结构校验，可作为正式主格网切换依据。
- 本文件建议长期保留，供论文方法章节、附录和结果解释使用。

---

### 2、面板数据

该目录存放后续实证分析和深度学习建模的核心表格数据。

#### 1. `master_grid_year_panel.csv`

作用：

- 主格网标准年度面板。
- 用于空间统计分析与影响因素分析。
- 是广州市内有效格网的正式研究面板。

数据结构：

- 行数约为 `297550`，即 `29755 个有效格网 × 10 年`。
- 覆盖年份为 `2015-2024`。

核心字段：

- `grid_id`：主格网标准ID。
- `year`：年份。
- `row_id`、`col_id`：主格网行列号。
- `centroid_x`、`centroid_y`：主格网标准质心坐标。
- `cover_ratio`：格网被广州市范围覆盖的比例。
- `boundary_mask`：边界格网标记。
- `valid_mask`：有效格网标记。
- 业务字段：
  - `active_cnt`
  - `entry_cnt`
  - `persist_cnt`
  - `renew_cnt`
  - `exit_next_cnt`
  - `capital_mean`
  - `capital_median`
  - `capital_sum`
  - `n_size_*`
  - `n_cat_*`

推荐用途：

- 全局 Moran's I
- 局部空间自相关分析
- 热点分析
- 空间计量或格网层面的影响因素分析
- 面板回归或描述性统计分析

使用建议：

- 默认保留 `valid_mask=1` 的记录使用。
- 若需要稳健性检验，可进一步考虑是否排除 `boundary_mask=1` 的边界格网。

#### 2. `master_full_grid_year_panel.csv`

作用：

- 完整规则主格网年度面板。
- 用于 ConvLSTM 和其他需要规则矩阵输入的深度学习任务。

数据结构：

- 行数约为 `689300`，即 `68930 个完整主格网 × 10 年`。
- 包含广州市内格网和市外补齐格网。

核心字段：

- `grid_id`
- `year`
- `row_id`
- `col_id`
- `centroid_x`
- `centroid_y`
- `cover_ratio`
- `boundary_mask`
- `valid_mask`
- 全部业务字段

说明：

- 该文件中市外格网保留，但其业务字段通常为 0，且 `valid_mask=0`。
- 深度学习任务应以本文件作为唯一标准输入底板。
- 构造张量时应结合 `row_id`、`col_id` 恢复规则二维矩阵。

#### 3. `master_grid_mapping_qc.csv`

作用：

- 主格网映射质检表。
- 用于抽样核对旧格网和新格网的替换关系。

内容特点：

- 包含旧 `grid_id`、新 `grid_id`、新旧质心坐标、覆盖率、边界标记、偏移距离等信息。
- 适合人工检查若干典型格网，验证替换结果是否符合空间直觉。

说明：

- 本文件主要用于质检与审查，不建议作为正式分析输入。

---

### 3、年度csv

该目录存放按年份拆分后的主格网标准 CSV，是 ArcGIS 制图与逐年空间分析的直接输入层。

包含文件：

- `grid_panel_2015.csv`
- `grid_panel_2016.csv`
- `grid_panel_2017.csv`
- `grid_panel_2018.csv`
- `grid_panel_2019.csv`
- `grid_panel_2020.csv`
- `grid_panel_2021.csv`
- `grid_panel_2022.csv`
- `grid_panel_2023.csv`
- `grid_panel_2024.csv`

共同特点：

- 每个文件对应一个年份。
- 每个文件约 `29755` 行，对应当年全部有效主格网。
- 文件中不再单独保留 `year` 字段，年份由文件名表达。
- 适合在 ArcGIS 中按年 Join 到主格网底图。

字段结构：

- `grid_id`
- `row_id`
- `col_id`
- `centroid_x`
- `centroid_y`
- `cover_ratio`
- `boundary_mask`
- `valid_mask`
- 各类年度业务统计字段

推荐用途：

- 按年专题制图
- 每年单独空间分析
- 与 ArcGIS 主格网底图进行 1:1 Join

---

### 4、空间图层

该目录存放 ArcGIS 最终空间图层成果。

#### `主格网年度面板.gdb`

作用：

- 存放最终统一主格网体系下的年度空间图层。
- 是 ArcGIS 中正式使用的标准年度格网图层库。

包含要素类：

- `master_grid_panel_2015`
- `master_grid_panel_2016`
- `master_grid_panel_2017`
- `master_grid_panel_2018`
- `master_grid_panel_2019`
- `master_grid_panel_2020`
- `master_grid_panel_2021`
- `master_grid_panel_2022`
- `master_grid_panel_2023`
- `master_grid_panel_2024`

每个要素类的特点：

- 以完整规则主格网作为几何底图。
- 仅保留当年有效格网记录。
- 已挂接当年的业务统计字段。
- 已统一到主格网标准 ID 体系。

推荐用途：

- ArcGIS 空间统计分析
- 年度专题制图
- 出图展示
- 后续空间变量 Join
- 论文配图与附图制作

---

## 四、后续研究的正式使用规范

### 1. 空间统计分析

正式输入优先级：

- 首选：`2、面板数据/master_grid_year_panel.csv`
- ArcGIS 制图或按年分析时：`4、空间图层/主格网年度面板.gdb/master_grid_panel_YYYY`

### 2. 影响因素分析

正式输入优先级：

- 首选：`2、面板数据/master_grid_year_panel.csv`

说明：

- 该文件已经统一了主格网ID和标准坐标，可直接作为后续变量拼接和回归分析底表。

### 3. 深度学习预测（如 ConvLSTM）

正式输入优先级：

- 唯一标准输入：`2、面板数据/master_full_grid_year_panel.csv`

说明：

- 该文件保留完整规则矩形格网，适合构造规则二维矩阵和时空张量。
- 应配合 `valid_mask` 使用，以区分广州市内有效格网和市外补齐格网。

### 4. 历史结果追溯与旧ID对照

正式输入优先级：

- 首选：`1、基础元数据/clip_to_master_grid_mapping.csv`
- 质量核验：`1、基础元数据/clip_to_master_grid_mapping_report.txt`

---

## 五、不再作为正式分析底板的旧文件

以下旧文件或旧体系成果建议仅保留用于归档、追溯与核对，不再作为后续正式研究输入：

- 旧 clip 格网随机 `grid_id` 体系
- 旧 `grid_year_panel_final.csv`
- 旧 `格网年度面板.gdb`
- 旧 `grid_base_clip` 直接分析体系

说明：

- 后续全部研究统一以主格网标准数据为准。
- 如确需追溯旧结果，应通过映射表进行对照，不应直接混用旧新体系。

---

## 六、建议长期保留的核心文件

若后续需要做归档、论文提交、成果备份，建议至少长期保留以下文件：

- `1、基础元数据/master_grid_metadata.csv`
- `1、基础元数据/clip_to_master_grid_mapping.csv`
- `1、基础元数据/clip_to_master_grid_mapping_report.txt`
- `2、面板数据/master_grid_year_panel.csv`
- `2、面板数据/master_full_grid_year_panel.csv`
- `4、空间图层/主格网年度面板.gdb`

---

## 七、最终结论

本目录已经完成从旧 clip 格网随机编号体系到主格网标准体系的全面切换。

从本目录开始：

- 空间统计分析
- 影响因素分析
- 深度学习预测

均应只基于主格网标准数据开展，不再混用旧 clip 格网体系。
