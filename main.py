import geopandas as gpd
import matplotlib.pyplot as plt

# 读取 shapefile
gdf = gpd.read_file('2020/vegetation.shp', encoding='GBK')

# 打印 CRS 信息
print(f"Original CRS: {gdf.crs}")

# 检查并转换坐标系（如果需要）
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs(epsg=4326)  # 转换为 WGS84 地理坐标系

print(f"Transformed CRS: {gdf.crs}")

# 筛选特定的植被类型
vegetation_types = [
    '禾草、薹草及杂类草沼泽化草甸',
    '禾草、杂类草草甸',
    '温带禾草、杂类草草甸草原',
    '温带丛生禾草草原',
    '亚高山草原',
    '高寒草原',
    '草原化灌木荒漠'
]

# 提取特定植被类型的 GeoDataFrame
specific_vegetation = gdf[gdf['植被类型'].isin(vegetation_types)]

# 打印几何对象的一些信息，检查是否有 NaN 或无效数据
print(specific_vegetation.geometry.is_valid().value_counts())
print(specific_vegetation.geometry.isna().sum())

# 修复无效几何对象（如果存在）
if not specific_vegetation.geometry.is_valid().all():
    specific_vegetation['geometry'] = specific_vegetation.buffer(0)

# 删除包含 NaN 的行
specific_vegetation = specific_vegetation.dropna()

# 创建绘图
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('auto')

# 绘制特定植被类型的多边形
specific_vegetation.plot(column='植被类型', ax=ax, legend=True,
                        legend_kwds={'bbox_to_anchor': (1, 1), 'title': '植被类型'},
                        cmap='Set3')  # 使用 Set3 调色板显示不同类型的颜色

# 设置标题和标签
ax.set_title('指定植被类型的分布', fontsize=15)
ax.set_xlabel('经度')
ax.set_ylabel('纬度')

# 确保坐标轴比例正确
ax.set_aspect('equal')

# 显示图形
plt.show()
