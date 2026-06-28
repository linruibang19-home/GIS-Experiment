# ArcGIS Pro 具体操作步骤

## 1. 工程准备

建议在现有 `Project_Location/GIS_new_project/GIS_new_project.aprx` 中新建地图：

```text
Map_阶段二_年度分布
Map_阶段二_Moran_LISA_GiStar
Map_阶段二_时空热点
Map_阶段二_论文图件
```

若担心影响原工程，可先另存为阶段二工程副本。

## 2. 年度格网图层准备

### 方案 A：已有年度图层

若阶段一 GDB 中已有年度格网图层，直接复制到阶段二使用。

### 方案 B：从 CSV Join

1. 加载主格网面图层；
2. 添加年度 CSV：`master_grid_panel_YYYY.csv`；
3. 使用 `Add Join`：

```text
目标字段：grid_id
连接字段：grid_id
连接类型：保留所有目标要素
```

4. 使用 `Export Features` 导出永久图层：

```text
grid_panel_2015
...
grid_panel_2024
```

5. 设置定义查询：

```text
valid_mask = 1
```

不要添加：

```text
active_cnt > 0
```

## 3. 年度描述统计

ArcGIS Pro 工具：

```text
Analysis -> Tools -> Summary Statistics
```

字段：

```text
active_cnt、entry_cnt、renew_cnt、exit_next_cnt、capital_sum
```

建议统计：

```text
SUM、MAX、MEAN
```

活跃格网数量和高承载格网数量可用选择统计：

```text
active_cnt > 0
active_cnt >= 10
```

## 4. 年度空间分布图

符号系统建议：

```text
0
1
2-4
5-9
10-19
20-49
50+
```

要求：

1. 代表年份使用同一分级；
2. 使用同一地图范围；
3. 零值格网用浅灰或透明浅灰；
4. 标注重点区时避免遮挡热点。

## 5. 空间权重矩阵

ArcGIS Pro 工具：

```text
Spatial Statistics Tools
-> Modeling Spatial Relationships
-> Generate Spatial Weights Matrix
```

主权重：

```text
Conceptualization: Contiguity edges corners
Row Standardization: Row
Unique ID: grid_id
```

稳健性权重：

```text
KNN 8
Distance Band
```

## 6. Global Moran's I

ArcGIS Pro 工具：

```text
Spatial Statistics Tools
-> Analyzing Patterns
-> Spatial Autocorrelation (Global Moran's I)
```

参数：

```text
Input Feature Class: grid_panel_YYYY
Input Field: active_cnt
Conceptualization: Get spatial weights from file
Weights Matrix File: weights_queen.swm
Row Standardization: Row
```

输出记录：

```text
Moran's I、Expected I、z-score、p-value
```

## 7. LISA

ArcGIS Pro 工具：

```text
Spatial Statistics Tools
-> Mapping Clusters
-> Cluster and Outlier Analysis (Anselin Local Moran's I)
```

输出字段通常包括：

```text
COType、LMIIndex、LMIZScore、LMIPValue
```

解释：

| 类型 | 含义 |
|---|---|
| HH | 高值集聚核心 |
| LL | 低值集聚区 |
| HL | 高值孤岛 |
| LH | 低值洼地 |
| NS | 不显著 |

## 8. Getis-Ord Gi*

ArcGIS Pro 工具：

```text
Spatial Statistics Tools
-> Mapping Clusters
-> Hot Spot Analysis (Getis-Ord Gi*)
```

输出字段：

```text
Gi_Bin、GiZScore、GiPValue
```

解释：

| Gi_Bin | 含义 |
|---:|---|
| 3 | 99% 热点 |
| 2 | 95% 热点 |
| 1 | 90% 热点 |
| 0 | 不显著 |
| -1 | 90% 冷点 |
| -2 | 95% 冷点 |
| -3 | 99% 冷点 |

## 9. 时空热点演化

ArcGIS Pro 工具：

```text
Space Time Pattern Mining Tools
-> Create Space Time Cube From Defined Locations
-> Emerging Hot Spot Analysis
```

建议参数：

```text
Location ID: grid_id
Time Field: year
Analysis Field: active_cnt
Time Step Interval: 1 Year
```

若 ArcGIS Pro 难以直接识别长表，可以先构建年度格网图层或时空立方体输入表。

