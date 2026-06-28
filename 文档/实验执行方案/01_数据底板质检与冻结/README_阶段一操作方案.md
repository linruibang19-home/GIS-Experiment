# 阶段一：数据底板质检与冻结

## 1. 阶段目标

在进入正式分析前，对现有企业动态数据、格网数据和空间映射结果进行最终核验，并冻结正式输入版本。

本阶段不重新推翻已有处理成果。重点是补齐质检报告、修正分析口径、派生预测所需变量，并明确后续只读底板。

## 2. 正式输入

```text
阶段一：企业动态变量研究/
├─ 0、企业核心数据表/
│  ├─ 02_认定事件表/firm_cert_event.csv
│  ├─ 03_企业主表/firm_master.csv
│  ├─ 04_企业年份活跃表/firm_year_presence_2015_2024.csv
│  └─ 05_退出代理表/firm_exit_proxy_2015_2024.csv
├─ 7、最终格网标准数据/
│  ├─ 1、基础元数据/master_grid_metadata.csv
│  ├─ 1、基础元数据/clip_to_master_grid_mapping.csv
│  └─ 2、面板数据/master_grid_year_panel.csv
├─ 8、最终点位数据/
│  └─ 1、主格网对齐点位表/firm_year_points_2015_2024.csv
└─ 9、最终DL格网标准数据/
   ├─ 1、基础元数据/master_full_grid_metadata.csv
   └─ 2、面板数据/master_full_grid_year_panel.csv
```

## 3. 建议输出目录

```text
阶段一：企业动态变量研究/
└─ 10、正式底板冻结/
   ├─ 0、输入版本清单/
   ├─ 1、质检报告/
   ├─ 2、补充变量/
   ├─ 3、正式底板/
   └─ 4、脚本/
```

## 4. 操作步骤

### 步骤 1：建立输入版本清单

对正式输入文件记录：

- 文件相对路径；
- SHA256 哈希值；
- 文件大小；
- 数据行数；
- 字段名；
- 生成时间；
- 用途说明。

输出：

```text
0、输入版本清单/input_manifest.csv
0、输入版本清单/input_manifest.md
```

### 步骤 2：企业基础表质检

检查：

1. `firm_id` 是否为空；
2. `firm_id` 是否唯一；
3. 统一社会信用代码格式是否异常；
4. 经纬度是否为空或超出合理范围；
5. `cert_valid_from <= cert_valid_to`；
6. `cert_year` 是否与证书有效期起始年份一致；
7. 同一企业多次认定事件是否存在时间重叠或明显异常。

输出：

```text
1、质检报告/qc_firm_master.csv
1、质检报告/qc_cert_event.csv
1、质检报告/qc_cert_episode_overlap.csv
```

### 步骤 3：企业年度状态质检

检查：

1. 每行必须满足 `present ∈ {0,1}`；
2. 每行必须满足 `entry_proxy ∈ {0,1}`；
3. 每行必须满足 `persist ∈ {0,1}`；
4. 每行必须满足 `renew_proxy ∈ {0,1}`；
5. 每行必须满足 `exit_proxy_next_yr ∈ {0,1}`；
6. 不应存在 `present=0` 但 `entry_proxy=1` 或 `persist=1`；
7. 同一企业同一年最多一条记录；
8. 2015 年为左截断年份，单独标记；
9. 2024 年为右删失年份，单独标记。

增加字段：

| 字段 | 说明 |
|---|---|
| `left_censored` | 2015 年记录标记为 1 |
| `right_censored` | 2024 年记录标记为 1 |
| `usable_for_exit_model` | 仅保留具有下一年观测值的记录 |

### 步骤 4：重新生成标准区县字段

现有企业点位表中存在少量广州市外区县文本标签。应以企业点位与广州市县级行政区面进行空间连接，生成：

| 字段 | 说明 |
|---|---|
| `district_raw` | 原始企业属性中的区县 |
| `district_spatial` | 企业点位空间连接得到的标准区县 |
| `district_mismatch` | 两者是否一致 |

人工核验：

- `district_spatial` 为空的企业；
- `district_raw != district_spatial` 的企业；
- 位于广州边界外的企业点；
- 位于边界附近的企业点。

输出：

```text
1、质检报告/qc_firm_district_mismatch.csv
2、补充变量/firm_year_points_with_spatial_district.csv
```

### 步骤 5：派生企业迁移变量

当前格网层面的跨年平衡式并非完全成立，原因是部分企业年度位置发生变化。必须派生迁移事件。

企业级迁移规则：

```text
若同一 firm_id 在年份 t 和 t+1 均活跃，
且 grid_id(t) != grid_id(t+1)，
则记录一次迁移。
```

派生企业级迁移表：

| 字段 | 说明 |
|---|---|
| `firm_id` | 企业 ID |
| `year_from` | 迁移前年份 |
| `year_to` | 迁移后年份 |
| `grid_id_from` | 迁出格网 |
| `grid_id_to` | 迁入格网 |
| `district_from` | 迁出区县 |
| `district_to` | 迁入区县 |
| `move_distance_m` | 迁移距离 |
| `cross_district_move` | 是否跨区县迁移 |

聚合到格网年度：

| 字段 | 说明 |
|---|---|
| `move_in_cnt` | 下一年迁入数量 |
| `move_out_cnt` | 下一年迁出数量 |
| `net_move_cnt` | `move_in_cnt - move_out_cnt` |

修订后的格网存量平衡式：

\[
A_{g,t+1}=A_{g,t}+I_{g,t+1}-O_{g,t+1}+M^{in}_{g,t+1}-M^{out}_{g,t+1}
\]

输出：

```text
2、补充变量/firm_move_event_2015_2024.csv
2、补充变量/grid_year_move_event.csv
```

### 步骤 6：格网面板一致性检查

检查：

1. 每年必须有 29,755 条有效格网记录；
2. 每行必须满足 `active_cnt = entry_cnt + persist_cnt`；
3. `active_cnt` 必须等于规模分类数量之和；
4. `active_cnt` 必须等于技术门类数量之和；
5. 迁移变量加入后，跨年平衡式应成立；
6. 每个格网每年最多一条记录；
7. `valid_mask=1`；
8. `cover_ratio` 范围应为 `[0,1]`；
9. 对 `cover_ratio` 极小的边界格网单独列出。

输出：

```text
1、质检报告/qc_grid_year_panel_summary.md
1、质检报告/qc_grid_year_panel_bad_rows.csv
1、质检报告/qc_boundary_grid.csv
```

### 步骤 7：冻结正式分析底板

建议生成：

```text
3、正式底板/
├─ grid_metadata_analysis.csv
├─ grid_year_event_analysis.csv
├─ grid_year_event_prediction.csv
├─ firm_year_points_analysis.csv
├─ firm_move_event_2015_2024.csv
└─ master_full_grid_year_panel_prediction.csv
```

其中：

| 文件 | 用途 |
|---|---|
| `grid_year_event_analysis.csv` | 空间集聚和影响因素分析 |
| `grid_year_event_prediction.csv` | 增加迁移、删失标记和预测目标变量 |
| `master_full_grid_year_panel_prediction.csv` | 完整规则矩阵预测 |

## 5. 已知基准值

现有数据应至少满足：

| 指标 | 基准值 |
|---|---:|
| 唯一企业数 | 22,657 |
| 企业年度记录数 | 99,498 |
| 有效主格网数 | 29,755 |
| 完整矩形格网数 | 68,930 |
| 边界格网数 | 1,815 |
| 旧新格网未匹配数 | 0 |
| `active_cnt != entry_cnt + persist_cnt` 行数 | 0 |
| 多格网企业数 | 777 |
| 最少格网变化次数 | 780 |

## 6. 完成标准

满足以下条件后进入阶段二：

1. 质检报告已输出；
2. 标准区县字段已生成；
3. 迁入、迁出变量已加入预测面板；
4. 左截断和右删失字段已加入；
5. 正式底板已生成哈希清单；
6. 后续阶段不再直接修改阶段一归档文件。

