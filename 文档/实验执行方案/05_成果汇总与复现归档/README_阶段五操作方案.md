# 阶段五：成果汇总、论文图表与复现归档

## 1. 阶段目标

将阶段一至阶段四的正式成果整理为论文可直接使用、可复核、可复现的归档包。

## 2. 建议输出目录

```text
论文成果汇总/
├─ 0、版本说明/
├─ 1、论文表格/
├─ 2、论文图件/
├─ 3、空间图层/
├─ 4、模型结果/
├─ 5、脚本/
├─ 6、环境说明/
├─ 7、日志与质检/
└─ 8、附录材料/
```

## 3. 操作步骤

### 步骤 1：冻结最终版本

记录：

- 每个正式输入文件的 SHA256；
- 每个最终输出文件的 SHA256；
- 文件生成时间；
- 对应脚本；
- 软件和包版本；
- 关键参数；
- 操作人员；
- 备注。

输出：

```text
0、版本说明/final_manifest.csv
0、版本说明/release_notes.md
```

### 步骤 2：整理论文表格

建议：

```text
1、论文表格/
├─ table_3_1_data_source.xlsx
├─ table_3_2_variable_definition.xlsx
├─ table_4_1_yearly_summary.xlsx
├─ table_4_2_global_moran.xlsx
├─ table_5_1_covariate_summary.xlsx
├─ table_5_2_geodetector.xlsx
├─ table_5_3_count_regression.xlsx
├─ table_5_4_multiscale_robustness.xlsx
├─ table_6_1_model_setting.xlsx
└─ table_6_2_prediction_metrics.xlsx
```

### 步骤 3：整理论文图件

建议：

```text
2、论文图件/
├─ chapter03/
├─ chapter04/
├─ chapter05/
├─ chapter06/
└─ appendix/
```

图件规范：

1. 正文图统一尺寸；
2. 地图统一投影和研究区范围；
3. 字体、字号、图例、比例尺和指北针统一；
4. 输出 PNG 和 PDF 两种格式；
5. 文件名使用章节号；
6. 图件必须可以追溯到脚本和源数据。

### 步骤 4：整理空间图层

空间图层建议使用 GeoPackage 或 File Geodatabase 归档：

```text
3、空间图层/
├─ thesis_grid_results.gpkg
├─ thesis_point_results.gpkg
└─ thesis_arcgis_results.gdb
```

每个图层至少包含：

- 图层用途；
- 主键；
- 坐标系；
- 字段说明；
- 数据年份；
- 生成脚本；
- 是否正式成果。

### 步骤 5：保存脚本

建议按阶段整理：

```text
5、脚本/
├─ 01_qc_and_freeze/
├─ 02_spatial_pattern/
├─ 03_covariates_and_models/
├─ 04_prediction/
└─ 05_figures_and_tables/
```

要求：

1. 禁止只在 ArcGIS Pro Python 窗口中运行而不保存；
2. 每个脚本写明输入、输出和依赖；
3. 使用相对路径或集中配置文件；
4. 保存日志；
5. 固定随机种子。

### 步骤 6：保存环境说明

输出：

```text
6、环境说明/
├─ README_environment.md
├─ requirements.txt
├─ environment.yml
└─ r_packages.md
```

记录：

- Python 版本；
- ArcGIS Pro 版本；
- R 版本；
- PySAL、GeoPandas、statsmodels、scikit-learn、XGBoost、mgwr 等包版本；
- R 包版本；
- 操作系统；
- 字符编码和坐标系。

### 步骤 7：整理质检报告

汇总：

```text
7、日志与质检/
├─ qc_stage01_data.md
├─ qc_stage02_spatial_weights.md
├─ qc_stage03_covariates.md
├─ qc_stage04_prediction.md
└─ known_limitations.md
```

`known_limitations.md` 至少说明：

1. 企业认定数据的制度口径；
2. 2015 年左截断；
3. 2024 年右删失；
4. 企业迁移处理方式；
5. 单一年份 POI 的时间局限；
6. 静态人口数据的局限；
7. 预测模型的适用边界；
8. ConvLSTM 未作为主模型的原因。

## 4. 论文写作映射

| 论文章节 | 主要来源 |
|---|---|
| 第三章 数据与指标 | 阶段一、阶段三 |
| 第四章 空间集聚格局 | 阶段二 |
| 第五章 多尺度影响因素 | 阶段三 |
| 第六章 年度时空预测 | 阶段四 |
| 第七章 讨论与展望 | 各阶段质检报告和局限说明 |

## 5. 完成标准

1. 正式成果文件有统一版本清单；
2. 每个论文图表均能追溯到数据和脚本；
3. 空间图层字段说明完整；
4. 软件环境可复现；
5. 已知局限已明确记录；
6. 项目归档结构清晰，可用于论文送审和后续答辩。

