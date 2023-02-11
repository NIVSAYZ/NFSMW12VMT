# Need For Speed Most Wanted 2012 Vehicle Model Tool
## 中文
感谢Binko提供的法线算法，Mip贴图算法，多边面导入方法

NFSMW12VMT无限制Mesh，贴图数量，支持更多材质，修复法线平滑
### 需要的额外工具
+ Noesis
+ DGIorio的[NFS Most Wanted Packer and Unpacker for Noesis](https://cdn.discordapp.com/attachments/635520888204165160/663416960587137024/tool_NFSMW2012_Packer_Unpacker.rar)
+ Blender插件blender_export_obj_NFSMW12VMT
### 注意事项
+ 若转换后出现顶点数量大于60000的错误(不止为何顶点数量大于60000游戏会崩溃)，可以通过平滑着色或者将三角面转为四边面来减少顶点，平滑着色可以减少大量顶点，转换为四边面减少少量顶点
+ 多个Mesh可以共用同一材质
+ 一个不可以使用多个材质

为Mesh命名应按照此格式：Mesh名称_材质类型，为物体命名好材质类型后，就可以为Mesh创建材质，材质的名称可以随意填写，着色器应使用原理化BSDF，并调好材质的参数
材质类型 | 可调参数 | 描述
-- | --
body | 基础色，糙度 | 固定颜色车身
bodypaint | 无 | 变色车身，维修站换色，颜色类型与数量取决于原车
bodypaintlivery | 无 | 贴花车身，贴花透明部分可变色
carbon | 无 | 碳纤维
glass | Alpha | 玻璃
colouriseglass | 基础色，自发光(发射)，自发光强度 | 着色玻璃
glassdoublesided | 贴花玻璃
light | 车灯
grille | 格栅
interior | 内饰
refraction | 车灯，比light材质表现更好
