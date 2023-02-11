# Need For Speed Most Wanted 2012 Vehicle Model Tool 简介/Introduction
## 中文

此教程对应的NFSMWVMT版本：1.1.2

感谢Binko提供的法线算法，Mip贴图算法，多边面导入方法

NFSMW12VMT无Mesh，贴图数量限制，支持更多材质与可调参数，修复了法线平滑的问题

### 需要的额外工具
+ Noesis
+ DGIorio的[NFS Most Wanted Packer and Unpacker for Noesis](https://cdn.discordapp.com/attachments/635520888204165160/663416960587137024/tool_NFSMW2012_Packer_Unpacker.rar)
+ Blender插件blender_export_obj_NFSMW12VMT

### 注意事项
+ 在Blender中同时启用blender_export_obj_NBMC与blender_export_obj_NFSMW12VMT会发生冲突，导致导出的obj格式错误
+ 若转换后出现顶点数量大于60000的错误(不止为何顶点数量大于60000游戏会崩溃)，可以通过平滑着色或者将三角面转为四边面来减少顶点，平滑着色可以减少大量顶点，转换为四边面减少少量顶点
+ 多个Mesh可以共用同一材质
+ 一个不可以使用多个材质

### 教程
+ 1. 将blender_export_obj_NFSMW12VMT插件安装至Blender3.4
+ 2. 将下载到的tool_NFSMW2012_Packer_Unpacker.rar解压至Noesis主目录下的plugins\python文件夹内
+ 3. 使用Need For Speed Most Wanted 2012 Unpacker解包要修改的车辆BNDL文件
+ 4. 使用Blender按照以下方式制作对应模型

为Mesh命名应按照此格式：Mesh名称_材质类型

为物体命名好材质类型后，就可以为Mesh创建材质，材质的名称可以随意填写，着色器应使用原理化BSDF，并调好材质的参数
材质类型 | 可调参数 | 材质类型描述
-- | -- | --
body | 基础色，糙度 | 固定颜色车身
bodypaint | 无 | 变色车身，维修站换色，颜色类型与数量取决于原车
bodypaintlivery | 无 | 贴花车身，贴花透明部分可变色
carbon | 无 | 碳纤维
glass | Alpha | 玻璃
colouriseglass | 基础色，自发光(发射)，自发光强度 | 着色玻璃
glassdoublesided | Alpha | 贴花玻璃
light | 基础色，自发光(发射)，自发光强度 | 车灯
grille | 基础色，糙度 | 格栅
interior | 自发光(发射)，自发光强度 | 内饰
refraction | 基础色，自发光(发射)，自发光强度 | 车灯，比light材质表现更好

参数类型 | 取值范围 | 描述
-- | -- | --
基础色 | 0~1 | 漫反射颜色
糙度 | 0~1 | 表面粗糙程度
自发光(发射) | 0~1 | 发光颜色
自发光强度 | 0~10 | 发光强度，游戏中这个值通常为10
Alpha | 0~1 | 不透明度

导出时应使用Wavefront OBJ format (NFSMW12VMT)选项导出

+ 5. 按以下方式创建对应贴图

创建贴图时，应将贴图命名为：Mesh名称_贴图类型 的形式，并且贴图格式必须为dds，贴图所在的位置应与obj和mtl文件位于同一目录下

建议使用分辨率长宽比为1:1的图片，否则可能会导致游戏崩溃

贴图类型 | 类型代表
-- | --
c | 颜色贴图
d | 漫反射贴图
dp | 置换贴图
e | 自发光贴图
en | 外部法线贴图
in | 内部法线贴图
l | 发光贴图
n | 法线贴图
s | 高光贴图

发光贴图和自发光贴图的作用：贴图alpha通道指示后灯，贴图red通道指示刹车灯，贴图green通道指示头灯，贴图blue通道指示倒车灯

支持的贴图类型的首项为默认贴图，如果无法找到默认贴图会直接报错，如果默认贴图之后的贴图无法找到则会使用默认贴图代替

材质类型 | 支持的贴图类型
-- | -- 
bodypaintlivery | d
glassdoublesided | d
light | l，n，s
grille | d，n
interior | d，n，s
refraction | c，en，e，in，dp

+ 6. 创建完毕obj，mtl文件和贴图后，使用NFSMW12VMT转换模型，需手动填入解包车辆文件夹路径与obj路径
+ 7. 模型转换完毕后，使用Need For Speed Most Wanted 2012 Packer封包车辆文件，此时在解包车辆文件夹里会生成一个Output.BNDL，将其命名为其游戏文件夹中车辆文件的原名即可

## English

The corresponding NFSMWVMT version of this tutorial: 1.1.2

Thanks for the normal algorithm, mipmap algorithm, polyface import method, provided by Binko_ctr

NFSMW12VMT has no mesh and texture number limited, supports more materials and adjustable parameters, and fixes the problem of shade smooth

Thanks for tutorial translated by enthuse

### Required extra tools
+ Noesis
+ [NFS Most Wanted Packer and Unpacker for Noesis](https://cdn.discordapp.com/attachments/635520888204165160/663416960587137024/tool_NFSMW2012_Packer_Unpacker.rar) by DGIorio
+ blender_export_obj_NFSMW12VMT (A blender plugin)

### Side Notes
+ In Blender Enable Blender_export_obj_NBMC and blender_export_obj_NFSMW12VMT at the same time will cause conflict, resulting in the exported obj format error
+ If there are more than 60,000 vertices present after conversion, you can use the "Shade Smooth" or "Tris to Quads" option in blender to decrease the amount of vertices. (Use "Shade Smooth" can decrease a large number of vertices，use "Tris to Quads" can decrease a less number of vertices)
+ You can use the same material on multiple meshes.
+ One object cannot use multiple materials

### Tutorial
+ 1. Install blender_export_obj_NFSMW12VMT for Blender3.4 as a plugin, there should be plenty of tutorials out there.
+ 2. After downloading 'tool_NFSMW2012_Packer_Unpacker.rar', extract the python scripts and put it under <Whatever your noesis directory>\plugins\python 
+ 3. Unpack your desired BNDL using the 'Need For Speed Most Wanted 2012 Unpacker' script in Noesis. It can be found at the toolbar above under "Tools".
+ 4. Prepare the model with Blender as follows.

Mesh should be named in this format: MeshName_MaterialType
An example will be: FrontWindShield_glass.

After done naming the mesh, you can create a material for the mesh. The material name can be filled in at will. The shader should use the principle BSDF and adjust the material parameters

Listed below are the available materials type and the infos.
Material Type | Editable Data | Info
-- | -- | --
body | Base Colour, Roughness | Non-changing body colour
bodypaint | NA | Changable body colour when entering gas-station
bodypaintlivery | NA | Car body with liveries/wraps, transparent area will be car's body paint
carbon | NA | carbon fiber
glass | Alpha | glass
colouriseglass | Base Colour | glass with colour
glassdoublesided | Alpha | glass with texture/livery
light | Base Colour, Emission, Emission Strength | light
grille | Base Colour, Roughness | grille
interior | Emission, Emission Strength  | interior
refraction | Base Colour, Emission, Emission Strength | light, but better than light material

Editable Data | Value Range | Info
-- | -- | --
Base Colour | 0~1 | Diffuse Colour
Roughness | 0~1 | How rough a surface is
Emission | 0~1 | Emission Colour
Emission Strength | 0~10 | How strong the light emitts, this value is usually 10 in the game
Alpha | 0~1 | Opacity

To export, select Wavefront OBJ format (NFSMW12VMT).

+ 5. Creating and naming respective textures as follows

Textures should be named in the format: MeshName_TextureType. Texture must be in dds format, with the same directory with mtl and obj file.

It is recommended to use a picture with a resolution aspect ratio of 1:1, otherwise it may cause the game crash

Texture Type | Info
-- | --
c | Colour texture
d | Diffuse texture
dp | Displacement texture
e | Emissive texture
en | External normal texture
in | Internal normal texture
l | Lightmap lights texture
n | Normal texture
s | Specular texture

emissive texture and lightmap lights texture: the alpha channel of the texture indicates rear lights, the red channel of the texture indicates brake lights, the green channel of the texture indicates headlights, and the blue channel of the texture indicates reversing lights

The supported texture types first item is the default texture, default textures are used if the tool can't find the respective texture for the respective mesh.

Material Type | Supported Textures
-- | -- 
bodypaintlivery | d
glassdoublesided | d
light | l，n，s
grille | d，n
interior | d，n，s
refraction | c，en，e，in，dp

+ 6. After exporting the obj and mtl file, use the tool NFSMW12VMT to convert the model, you need to manually input the respective directories.
+ 7. After conversion using the NFSMW12VMT tool, pack the file with DGI's MW12 Packer, rename the file and put where it belongs, enjoy.
