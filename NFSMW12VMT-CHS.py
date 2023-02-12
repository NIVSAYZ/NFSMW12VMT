import os
import math
import struct
from timeit import default_timer as timer

def check_path():
    Location = os.path.abspath('') + "\\"
    LibraryBasePath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template"
    LibraryBasePathItemGroup = ["Material", "Renderable", "SamplerState", "Texture", "IDs.BIN"]
    Missing = "No"
    MissingItemGroup = []
    for Item in LibraryBasePathItemGroup:
        if not os.path.exists(LibraryBasePath + "\\" + Item):
            Missing = "Yes"
            MissingItemGroup.append(Item)
    if Missing == "Yes":
        input("错误: Library不完整, 缺少的项目: {}".format(MissingItemGroup))
        exit()

    LibraryMaterialPath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template\Material"
    LibraryMaterialPathItemGroup = ["Body.dat", "BodyPaint.dat", "BodyPaintLivery.dat", "Carbon.dat", "ColouriseGlass.dat", "Glass.dat", "GlassDoublesided.dat", "Grille.dat", "Interior.dat", "Light.dat", "Refraction.dat", "Tyre.dat", "Hub.dat", "Rim.dat"]
    Missing = "No"
    MissingItemGroup = []
    for Item in LibraryMaterialPathItemGroup:
        if not os.path.exists(LibraryMaterialPath + "\\" + Item):
            Missing = "Yes"
            MissingItemGroup.append(Item)
    if Missing == "Yes":
        input("错误: Library材质不完整, 缺少的项目: {}".format(MissingItemGroup))
        exit()

    LibraryRenderablePath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template\Renderable"
    LibraryRenderablePathItemGroup = ["Block.dat", "Header.dat"]
    Missing = "No"
    MissingItemGroup = []
    for Item in LibraryRenderablePathItemGroup:
        if not os.path.exists(LibraryRenderablePath + "\\" + Item):
            Missing = "Yes"
            MissingItemGroup.append(Item)
    if Missing == "Yes":
        input("错误: Library Renderable不完整, 缺少的项目: {}".format(MissingItemGroup))
        exit()

    LibrarySamplerPath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template\SamplerState"
    LibrarySamplerPathItemGroup = ["7F_77_6A_0A.dat", "8A_7A_30_2B.dat", "60_7D_0D_2E.dat", "74_2A_D8_6D.dat", "89_B6_8C_9A.dat", "D5_4F_91_2F.dat"]
    Missing = "No"
    MissingItemGroup = []
    for Item in LibrarySamplerPathItemGroup:
        if not os.path.exists(LibrarySamplerPath + "\\" + Item):
            Missing = "Yes"
            MissingItemGroup.append(Item)
    if Missing == "Yes":
        input("错误: Library SamplerState不完整, 缺少的项目: {}".format(MissingItemGroup))
        exit()

    LibraryTexturePath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template\Texture"
    LibraryTexturePathItemGroup = ["Header.dat"]
    Missing = "No"
    MissingItemGroup = []
    for Item in LibraryTexturePathItemGroup:
        if not os.path.exists(LibraryTexturePath + "\\" + Item):
            Missing = "Yes"
            MissingItemGroup.append(Item)
    if Missing == "Yes":
        input("错误: Library纹理不完整, 缺少的项目: {}".format(MissingItemGroup))
        exit()

    LibraryIDsPath = Location + r"NFSMW_Library_PC_NIVSAYZ\Template\IDs.BIN"
    return LibraryBasePath, LibraryIDsPath, LibraryMaterialPath, LibraryRenderablePath, LibrarySamplerPath, LibraryTexturePath

def read_obj():
    with open(ObjPath, encoding="utf-8") as f:
        ObjLines = f.readlines()
    LineCount = ObjectCount = int()
    ObjectNameGroup = list(); ObjectLineRangeGroup = list(); UsemtlGroup = list(); MaterialGroup = list()
    MtlFile = None
    for Line in ObjLines:
        SplitLine = Line.strip().split(" ")
        if SplitLine[0] == "mtllib":
            MtlFile = SplitLine[1]  # mtl文件名
            MtlPath = os.path.dirname(ObjPath) + "\\" + MtlFile  # mtl文件路径
        elif SplitLine[0] == "usemtl":
            UsemtlGroup.append(SplitLine[1])
        elif SplitLine[0] == "o":
            if len(SplitLine[1].split("_")) < 2:
                input("错误：物体：{} 的命名不正确！".format(SplitLine[1].split("_")[0]))
                exit()
            ObjectCount += 1  # object计数
            MaterialGroup.append(SplitLine[1].split("_")[1])
            ObjectNameGroup.append(SplitLine[1].split("_")[0])
            ObjectLineRangeGroup.append(LineCount)  # object行范围开始
        LineCount += 1  # 行计数
    if MtlFile == None:
        input("错误：没有与obj关联的mtl!")
        exit()
    ObjectLineRangeGroup.append(LineCount)  # object行范围结束
    vCount = vtCount = vnCount = int()
    vGroup = list(); vtGroup = list(); vnGroup = list(); vCountGroup = [0]; vtCountGroup = [0]; vnCountGroup = [0]; VertexCountGroup = list(); ObjDataGroup = list(); vVertexIndexGroup = list(); vtVertexIndexGroup = list(); vnVertexIndexGroup = list(); VertexIndexGroup = list()
    for ObjectNum in range(ObjectCount):  # object总数循环
        VertexCount = int()
        vGroupCache = list(); vtGroupCache = list(); vnGroupCache = list(); VertexGroup = list(); FaceEdgeGroup = list(); vVertexIndexCache = list(); vtVertexIndexCache = list(); vnVertexIndexCache = list(); VertexNumGroup = list()
        RemoveRepeatVertexDict = RemoveRepeatSequentialVertexDict = dict()
        ObjDataGroup.append([ObjectNameGroup[ObjectNum], MaterialGroup[ObjectNum], UsemtlGroup[ObjectNum]])  # 收集object名称与object关联材质
        for LineNum in range(ObjectLineRangeGroup[ObjectNum] + 1, ObjectLineRangeGroup[ObjectNum + 1]):  # object行范围循环
            SplitLine = ObjLines[LineNum].strip().split()
            if SplitLine[0] == 'v':
                vGroupCache.append([float(SplitLine[1]), float(SplitLine[2]), float(SplitLine[3])])
                vCount += 1
            elif SplitLine[0] == 'vt':
                vtGroupCache.append([float(SplitLine[1]), float(SplitLine[2])])
                vtCount += 1
            elif SplitLine[0] == 'vn':
                vnGroupCache.append([float(SplitLine[1]), float(SplitLine[2]), float(SplitLine[3])])
                vnCount += 1
            elif SplitLine[0] == "f":
                for EdgeNum in range(1, len(SplitLine)):  # 面边数循环
                    VertexCount += 1
                    RemoveRepeatVertexDict[SplitLine[EdgeNum]] = VertexCount  # 生成去重字典
                    VertexGroup.append(SplitLine[EdgeNum])  # 顶点组
                FaceEdgeGroup.append(EdgeNum)  # 每面边数组
        if len(RemoveRepeatVertexDict) > 60000:
            input("错误: 物体{}转换后的顶点将超过60000，这会导致游戏崩溃，请减少此物体的顶点!".format(ObjDataGroup[ObjectNum][0]))
            exit()
        RemoveRepeatVertexGroup = list(RemoveRepeatVertexDict.keys())  # 去重顶点组
        vCountGroup.append(vCount)  # v计数组
        vtCountGroup.append(vtCount)  # vt计数组
        vnCountGroup.append(vnCount)  # vn计数组
        vGroup.append(vGroupCache)
        vtGroup.append(vtGroupCache)
        vnGroup.append(vnGroupCache)
        for VertexNum in range(len(RemoveRepeatVertexDict)):  # 去重字典键值总数循环
            RemoveRepeatSequentialVertexDict[RemoveRepeatVertexGroup[VertexNum]] = VertexNum  # 生成去重，重生成顶点序号字典
        VertexCountGroup.append(len(RemoveRepeatVertexDict))  # 收集去重顶点数量
        for RemoveRepeatVertex in RemoveRepeatVertexGroup:  # 去重顶点循环
            RemoveRepeatVertex = RemoveRepeatVertex.split("/")  # 分割去重顶点v/vt/vn
            vVertexIndexCache.append(int(RemoveRepeatVertex[0]) - vCountGroup[ObjectNum] - 1)  # v
            if RemoveRepeatVertex[1] == "":
                vtVertexIndexCache.append(0)
            else:
                vtVertexIndexCache.append(int(RemoveRepeatVertex[1]) - vtCountGroup[ObjectNum] - 1)  # vt
            vnVertexIndexCache.append(int(RemoveRepeatVertex[2]) - vnCountGroup[ObjectNum] - 1)  # vn
        vVertexIndexGroup.append(vVertexIndexCache)
        vtVertexIndexGroup.append(vtVertexIndexCache)
        vnVertexIndexGroup.append(vnVertexIndexCache)
        for Vertex in VertexGroup:  # 顶点循环
            VertexNumGroup.append(RemoveRepeatSequentialVertexDict[Vertex])  # 查找去重字典生成顶点序号组
        EdgeCount = int()
        VertexIndexCache = list()
        for FaceEdge in FaceEdgeGroup:  # 每面边数组循环
            Cache = list()
            for EdgeNum in range(FaceEdge):  # 面边数循环
                Cache.append(VertexNumGroup[EdgeNum + EdgeCount])  # 每面顶点序号组
            VertexIndexCache.append(Cache[0])  # 取每面顶点序号组首项
            Count1 = 0
            Count2 = 0
            for i3 in range(1, FaceEdge):
                if i3 % 2 != 0:
                    Count1 += 1
                    VertexIndexCache.append(Cache[Count1])
                elif i3 % 2 == 0:
                    Count2 -= 1
                    VertexIndexCache.append(Cache[Count2])
            VertexIndexCache.append("FFFF")  # 每面顶点序号组转换
            EdgeCount += EdgeNum + 1  # 面边数计数
        VertexIndexGroup.append(VertexIndexCache)
    return MtlPath, ObjectCount, ObjDataGroup, vGroup, vtGroup, vnGroup, vVertexIndexGroup, vtVertexIndexGroup, vnVertexIndexGroup, VertexIndexGroup, VertexCountGroup

def read_mtl():
    if not os.path.exists(MtlPath):
        input("错误：mtl文件路径无效！")
        exit()
    with open(MtlPath, encoding="utf-8") as f:
        MtlLines = f.readlines()
    LineCount = NewmtlCount = int()
    MaterialLineRangeGroup = list()
    NewmtlDict = dict()
    for Line in MtlLines:
        SplitLine = Line.strip().split(" ")
        if SplitLine[0] == "newmtl":
            MaterialLineRangeGroup.append(LineCount)  # 材质行范围开始
            NewmtlDict[SplitLine[1]] = NewmtlCount  # 建立材质字典
            NewmtlCount += 1
        LineCount += 1  # 行计数
    MaterialLineRangeGroup.append(LineCount)  # 材质行范围结束
    MaterialCount = int()
    MaterialParameterGroup = list()
    for ObjectNum in range(ObjectCount):
        MaterialCount += 1
        Material = ObjDataGroup[ObjectNum][1]
        Num = NewmtlDict[ObjDataGroup[ObjectNum][2]]
        if Material == "body":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
                elif SplitLine[0] == "Ks":
                    Specular_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Specular_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Specular_B = struct.pack("<f", float(SplitLine[3])).hex()
                    SpecularColor = Specular_R + Specular_G + Specular_B
                elif SplitLine[0] == "roughness":
                    Roughness = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, DiffuseColor, Roughness, SpecularColor])
        elif Material == "bodypaint":
            MaterialParameterGroup.append([Material])
        elif Material == "bodypaintlivery":
            MaterialParameterGroup.append([Material])
        elif Material == "carbon":
            MaterialParameterGroup.append([Material])
        elif Material == "glass":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "d":
                    Opacity = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, Opacity])
        elif Material == "colouriseglass":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
            MaterialParameterGroup.append([Material, DiffuseColor])
        elif Material == "glassdoublesided":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "d":
                    Opacity = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, Opacity])
        elif Material == "light":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
                elif SplitLine[0] == "Ke":
                    Emmission_R = struct.pack("<f", float(SplitLine[1]) / 10).hex()
                    Emmission_G = struct.pack("<f", float(SplitLine[2]) / 10).hex()
                    Emmission_B = struct.pack("<f", float(SplitLine[3]) / 10).hex()
                    EmmissionColor = Emmission_R + Emmission_G + Emmission_B
                elif SplitLine[0] == "Kes":
                    EmmissionStrength = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, EmmissionColor, DiffuseColor, EmmissionStrength])
        elif Material == "grille":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
                elif SplitLine[0] == "roughness":
                    Roughness = struct.pack("<f", float(SplitLine[1])).hex()
                elif SplitLine[0] == "Ks":
                    Specular_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Specular_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Specular_B = struct.pack("<f", float(SplitLine[3])).hex()
                    SpecularColor = Specular_R + Specular_G + Specular_B
            MaterialParameterGroup.append([Material, DiffuseColor, Roughness, SpecularColor])
        elif Material == "interior":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Ke":
                    Emmission_R = struct.pack("<f", float(SplitLine[1]) / 10).hex()
                    Emmission_G = struct.pack("<f", float(SplitLine[2]) / 10).hex()
                    Emmission_B = struct.pack("<f", float(SplitLine[3]) / 10).hex()
                    EmmissionColor = Emmission_R + Emmission_G + Emmission_B
                elif SplitLine[0] == "Kes":
                    EmmissionStrength = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, EmmissionColor, EmmissionStrength])
        elif Material == "refraction":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # 材质行循环
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
                elif SplitLine[0] == "Ke":
                    Emmission_R = struct.pack("<f", float(SplitLine[1]) / 10).hex()
                    Emmission_G = struct.pack("<f", float(SplitLine[2]) / 10).hex()
                    Emmission_B = struct.pack("<f", float(SplitLine[3]) / 10).hex()
                    EmmissionColor = Emmission_R + Emmission_G + Emmission_B
                elif SplitLine[0] == "Kes":
                    EmmissionStrength = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, EmmissionColor, EmmissionStrength, DiffuseColor])
        elif Material == "tyre":
            MaterialParameterGroup.append([Material])
        elif Material == "hub":
            MaterialParameterGroup.append([Material])
        elif Material == "rim":
            MaterialParameterGroup.append([Material])
        else:
            input("错误：材质：{} 为不支持的材质类型！".format(Material))
            exit()
    return MaterialCount, MaterialParameterGroup

def create_mesh():
    def get_normal():
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # 法向坐标组
        Normal = struct.pack("<f", vnCoord[0]).hex() + struct.pack("<f", vnCoord[1]).hex() + struct.pack("<f", vnCoord[2]).hex()
        return Normal

    def get_tangent():
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # 法向坐标组
        if vnCoord[0] == 0 and vnCoord[1] == 0 and vnCoord[2] == 1:
            Tangent_x = 0
            Tangent_y = 1
            Tangent_z = 0
        elif vnCoord[0] == 1 and vnCoord[1] == 0 and vnCoord[2] == 0:
            Tangent_x = 0
            Tangent_y = 1
            Tangent_z = 0
        else:
            Tangent_x = vnCoord[1] * 1 - 0 * vnCoord[2]
            Tangent_y = 0 * vnCoord[2] - vnCoord[0] * 1
            Tangent_z = 0
            if Tangent_x == 0 and Tangent_y == 0 and Tangent_z == 0:
                Tangent_x = 0
                Tangent_y = 1 * vnCoord[2] - vnCoord[0] * 0
                Tangent_z = vnCoord[0] * 0 - 1 * vnCoord[1]
        Tangent = struct.pack("<f", Tangent_x).hex() + struct.pack("<f", Tangent_y).hex() + struct.pack("<f", Tangent_z).hex()
        return Tangent

    def get_binnormal():
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # 法向坐标组
        if vnCoord[0] == 0 and vnCoord[1] == 0 and vnCoord[2] == 1:
            Tangent_x = 0
            Tangent_y = 1
            Tangent_z = 0
        elif vnCoord[0] == 1 and vnCoord[1] == 0 and vnCoord[2] == 0:
            Tangent_x = 0
            Tangent_y = 1
            Tangent_z = 0
        else:
            Tangent_x = vnCoord[1] * 1 - 0 * vnCoord[2]
            Tangent_y = 0 * vnCoord[2] - vnCoord[0] * 1
            Tangent_z = 0
            if Tangent_x == 0 and Tangent_y == 0 and Tangent_z == 0:
                Tangent_x = 0
                Tangent_y = 1 * vnCoord[2] - vnCoord[0] * 0
                Tangent_z = vnCoord[0] * 0 - 1 * vnCoord[1]
        Binnormal_x = vnCoord[1] * Tangent_z - Tangent_y * vnCoord[2]
        Binnormal_y = Tangent_x * vnCoord[2] - vnCoord[0] * Tangent_z
        Binnormal_z = vnCoord[0] * Tangent_y - Tangent_x * vnCoord[1]
        Binnormal = struct.pack("<f", Binnormal_x).hex() + struct.pack("<f", Binnormal_y).hex() + struct.pack("<f", Binnormal_z).hex()
        return Binnormal

    def get_normal_packed():  # 法线坐标数据转换函数(Binko_ctr)
        def ab_to_tanhalf_ab(a, b):
            cot_a_b = b / a
            cot_a_b_2 = cot_a_b * cot_a_b
            csc_a_b = math.sqrt(1 + cot_a_b_2) if a > 0 else - math.sqrt(1 + cot_a_b_2)
            return 1 / (cot_a_b + csc_a_b)

        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # 法向坐标组

        # 转换法线坐标数据
        NormalPackedCache_z = 1
        # nfs format
        if vnCoord[0] == 0 and vnCoord[1] == 0:
            if vnCoord[2] < 0:
                NormalPackedCache_x = 1
                NormalPackedCache_y = NormalPackedCache_z = 0
            else:
                NormalPackedCache_x = NormalPackedCache_y = 0
        elif vnCoord[0] == 0:
            tanhalf_z_y = ab_to_tanhalf_ab(vnCoord[1], vnCoord[2])
            NormalPackedCache_y = tanhalf_z_y * NormalPackedCache_z
            NormalPackedCache_x = 0
        elif vnCoord[1] == 0:
            tanhalf_x_y = ab_to_tanhalf_ab(vnCoord[0], vnCoord[2])
            NormalPackedCache_x = tanhalf_x_y * NormalPackedCache_z
            NormalPackedCache_y = 0
        else:
            xz_length = math.sqrt(vnCoord[0] * vnCoord[0] + vnCoord[1] * vnCoord[1])
            tanhalf_xz_y = ab_to_tanhalf_ab(xz_length, vnCoord[2])
            NormalPackedCache_x = (tanhalf_xz_y / xz_length) * vnCoord[0] * NormalPackedCache_z
            NormalPackedCache_y = (tanhalf_xz_y / xz_length) * vnCoord[1] * NormalPackedCache_z
        # 归一化 + 法线映射
        Norm = math.sqrt(NormalPackedCache_x ** 2 + NormalPackedCache_y ** 2 + NormalPackedCache_z ** 2)
        NormalPacked_x = struct.pack("<h", round(NormalPackedCache_x / Norm * 32767)).hex()
        NormalPacked_y = struct.pack("<h", round(NormalPackedCache_y / Norm * 32767)).hex()
        NormalPacked_z = struct.pack("<h", round(NormalPackedCache_z / Norm * 32767)).hex()
        NormalPacked_w = struct.pack("<h", round(0.03 * 32767)).hex()
        NormalPacked = NormalPacked_x + NormalPacked_y + NormalPacked_z + NormalPacked_w
        return NormalPacked

    # 面转换
    VertexIndexHexGroup = list(); VertexIndexHexLengthGroup = list()
    for ObjectNum in range(ObjectCount):  # object总数循环
        VertexIndexHex = str()
        for VertexIndex in VertexIndexGroup[ObjectNum]:  # Mesh顶点总数循环
            if VertexIndex == "FFFF":
                VertexIndexHex += "FFFF"
            else:
                VertexIndexHex += struct.pack("<H", VertexIndex).hex()
        VertexIndexHexGroup.append(VertexIndexHex)  # 收集Mesh顶点数据
        VertexIndexHexLengthGroup.append(int(len(VertexIndexHex) / 4))  # 收集面字节长度
    # 顶点转换
    VertexHexGroup = list()
    BlendIndices = "00000000"
    BlendWeight = "FF000000"
    for ObjectNum in range(ObjectCount):  # object数量循环
        VertexHex = str()
        Usemtl = ObjDataGroup[ObjectNum][1]  # 材质
        for VertexNum in range(VertexCountGroup[ObjectNum]):  # 顶点总数循环
            vCoord = vGroup[ObjectNum][vVertexIndexGroup[ObjectNum][VertexNum]]  # 顶点坐标组
            Position = struct.pack("<h", int(round(vCoord[0] * 32767 / 11))).hex() + struct.pack("<h", int(round(vCoord[1] * 32767 / 11))).hex() + struct.pack("<h", int(round(vCoord[2] * 32767 / 11))).hex() + "FF7F"  # 合并一组顶点坐标数据
            if vtVertexIndexGroup[ObjectNum][VertexNum] == 0:
                vtCoord = [0, 1]
            else:
                vtCoord = vtGroup[ObjectNum][vtVertexIndexGroup[ObjectNum][VertexNum]]  # 纹理坐标组
            Texcoord = struct.pack("<e", vtCoord[0]).hex() + struct.pack("<e", 1 - vtCoord[1]).hex()
            if Usemtl == "body" or Usemtl == "bodypaint" or Usemtl == "bodypaintlivery":
                Color = "FF000000"
                Texcoord1 = Texcoord2 = Texcoord3 = Texcoord4 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                VertexHex += Position + BlendIndices + BlendWeight + Color + Texcoord1 + Texcoord2 + Texcoord3 + Texcoord4 + NormalPacked
            elif Usemtl == "carbon":
                Color = "FF000000"
                Texcoord1 = Texcoord3 = Texcoord4 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                VertexHex += Position + BlendIndices + BlendWeight + Color + Texcoord1 + Texcoord3 + Texcoord4 + NormalPacked
            elif Usemtl == "light":
                Color = "FF000000"
                Texcoord1 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                VertexHex += Position + BlendIndices + BlendWeight + Color + Texcoord1 + NormalPacked
            elif Usemtl == "glass":
                (Normal) = get_normal()  # normal[12byte:3f]
                (Tangent) = get_tangent()
                Color = "FF000000"
                Texcoord2 = Texcoord3 = Texcoord
                VertexHex += Position + Normal + Tangent + BlendIndices + BlendWeight + Color + Texcoord2 + Texcoord3
            elif Usemtl == "colouriseglass":
                (Normal) = get_normal()  # normal[12byte:3f]
                (Tangent) = get_tangent()
                Color = "FF000000"
                Texcoord2 = Texcoord
                VertexHex += Position + Normal + Tangent + BlendIndices + BlendWeight + Color + Texcoord2
            elif Usemtl == "glassdoublesided":
                (Normal) = get_normal()  # normal[12byte:3f]
                (Tangent) = get_tangent()
                Color = "00000000"
                Texcoord1 = Texcoord2 = Texcoord3 = Texcoord
                VertexHex += Position + Normal + Tangent + BlendIndices + BlendWeight + Color + Texcoord1 + Texcoord2 + Texcoord3
            elif Usemtl == "grille":
                Color = "FF000000"
                Texcoord1 = Texcoord2 = Texcoord3 = Texcoord4 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                VertexHex += Position + BlendIndices + BlendWeight + Color + Texcoord1 + Texcoord2 + Texcoord3 + Texcoord4 + NormalPacked
            elif Usemtl == "interior":
                Color = "FF000000"
                Texcoord1 = Texcoord4 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                VertexHex += Position + BlendIndices + BlendWeight + Color + Texcoord1 + Texcoord4 + NormalPacked
            elif Usemtl == "refraction":
                (Normal) = get_normal()  # normal[12byte:3f]
                (Tangent) = get_tangent()
                (Binnormal) = get_binnormal
                Color = "FF000000"
                Texcoord1 = Texcoord
                VertexHex += Position + Normal + Tangent + Binnormal + BlendIndices + BlendWeight + Color + Texcoord1
            elif Usemtl == "tyre":
                Color = "FF000000"
                Texcoord1 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                Unknow_0xA = NormalPacked
                VertexHex += Position + Color + Texcoord1 + NormalPacked + Unknow_0xA
            elif Usemtl == "hub" or Usemtl == "rim":
                Color = "FF000000"
                Texcoord1 = Texcoord
                (NormalPacked) = get_normal_packed()  # normal_packed[8byte:4hnorm]
                Unknow_0xA = NormalPacked
                VertexHex += Position + Color + Texcoord1 + NormalPacked + Unknow_0xA
        VertexHexGroup.append(VertexHex)
    return VertexIndexHexLengthGroup, VertexIndexHexGroup, VertexHexGroup

def read_graphicsspec():
    ModelHexIDDict = dict()
    if os.path.exists(UnpackPath + r"\GraphicsSpec"):
        GraphicsSpecHex = open(UnpackPath + r"\GraphicsSpec" + "\\" + os.listdir(UnpackPath + r"\GraphicsSpec")[0], "rb+").read().hex()
    elif os.path.exists(UnpackPath + r"\06_01_00_00"):
        GraphicsSpecHex = open(UnpackPath + r"\06_01_00_00" + "\\" + os.listdir(UnpackPath + r"\06_01_00_00")[0], "rb+").read().hex()
    else:
        input("错误: 无效的GraphicsSpec[06_01_00_00]路径!")
        exit()
    Wheel1BlockPointer = struct.unpack("<I", bytes.fromhex(GraphicsSpecHex[24:32]))[0] * 2
    AuxFilePointer = (struct.unpack("<I", bytes.fromhex(GraphicsSpecHex[Wheel1BlockPointer + 240:Wheel1BlockPointer + 248]))[0] + 64) * 2
    for LineNum in range(int((len(GraphicsSpecHex) - AuxFilePointer) / 32)):  # AuxFile行数循环
        Line = GraphicsSpecHex[AuxFilePointer + LineNum * 32:AuxFilePointer + (LineNum + 1) * 32]
        if Line[8:16] == "60000001":
            PolygonSoupListID = struct.unpack("<L", bytes.fromhex(Line[:8]))[0]
        elif Line[8:16] == "00000000":
            ModelHexIDDict[Line[:8].upper()] = LineNum
    ModelHexIDList = list(ModelHexIDDict.keys())
    VehicleModelFileName = '_'.join([ModelHexIDList[0][x:x + 2] for x in range(0, len(ModelHexIDList[0]), 2)])
    FrontWheelModelFileNameGroup = list(); RearWheelModelFileNameGroup = list()
    for ModelHexIDNum in range(1, 5):
        FrontWheelModelFileNameGroup.append('_'.join([ModelHexIDList[ModelHexIDNum][x:x + 2] for x in range(0, len(ModelHexIDList[ModelHexIDNum]), 2)]))  # [轮胎, 钢圈, 轮毂样式, 卡钳]
    for ModelHexIDNum in range(5, 9):
        RearWheelModelFileNameGroup.append('_'.join([ModelHexIDList[ModelHexIDNum][x:x + 2] for x in range(0, len(ModelHexIDList[ModelHexIDNum]), 2)]))  # [轮胎, 钢圈, 轮毂样式, 卡钳]
    return PolygonSoupListID, VehicleModelFileName, FrontWheelModelFileNameGroup, RearWheelModelFileNameGroup

def read_model_vehicle():
    if os.path.exists(UnpackPath + r"\Model" + "\\" + VehicleModelFileName + ".dat"):
        VehicleModelHex = open(UnpackPath + r"\Model" + "\\" + VehicleModelFileName + ".dat", "rb+").read().hex()
    elif os.path.exists(UnpackPath + r"\51_00_00_00" + "\\" + VehicleModelFileName + ".dat"):
        VehicleModelHex = open(UnpackPath + r"\51_00_00_00" + "\\" + VehicleModelFileName + ".dat", "rb+").read().hex()
    else:
        input("错误: 无效的Model[51_00_00_00]路径!")
        exit()
    VehicleRenderableFileCount = struct.unpack("<H", bytes.fromhex(VehicleModelHex[40:44]))[0]
    VehicleRenderableFilePointer = len(VehicleModelHex) - (VehicleRenderableFileCount + struct.unpack("<L", bytes.fromhex(VehicleModelHex[32:40]))[0]) * 32
    VehicleRenderableFileNameGroup = list()
    for VehicleLodFilenNum in range(VehicleRenderableFileCount):
        VehicleRenderableFileName = VehicleModelHex[VehicleRenderableFilePointer + VehicleLodFilenNum * 32:VehicleRenderableFilePointer + (VehicleLodFilenNum + 1) * 32][:8].upper()
        VehicleRenderableFileNameGroup.append('_'.join([VehicleRenderableFileName[x:x + 2] for x in range(0, len(VehicleRenderableFileName), 2)]))
    return VehicleRenderableFileNameGroup

def create_id():
    Count = int()
    Count += 1
    MaterialHexIDGroup = list(); TextureHexIDGroup = list()
    for ObjData in ObjDataGroup:  # object计数循环
        Usemtl = ObjData[1]
        MaterialID = PolygonSoupListID + Count
        if Usemtl == "body" or Usemtl == "bodypaint" or Usemtl == "carbon" or Usemtl == "glass" or Usemtl == "mirrorglass" or Usemtl == "colouriseglass" or Usemtl == "tyre":
            Count += 1  # 材质+贴图
        elif Usemtl == "bodypaintlivery":
            Count += 2  # 材质+贴图
            for i in range(1, 2):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "light":
            Count += 4  # 材质+贴图
            for i in range(1, 4):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "glassdoublesided":
            Count += 2  # 材质+贴图
            for i in range(1, 2):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "grille":
            Count += 3  # 材质+贴图
            for i in range(1, 3):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "interior":
            Count += 4  # 材质+贴图
            for i in range(1, 4):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "refraction":
            Count += 6  # 材质+贴图
            for i in range(1, 6):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "hub" or Usemtl == "rim":
            Count += 4  # 材质+贴图
            for i in range(1, 4):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        MaterialHexIDGroup.append(struct.pack("<L", MaterialID).hex().upper())
    return MaterialHexIDGroup, TextureHexIDGroup

def create_texture():
    def MipMapping(input):  # (Binko_ctr)
        input = struct.unpack("<H", bytes.fromhex(input))[0]
        output = 0
        while input != 0:
            input >>= 1
            output += 1
        output = struct.pack("<b", output).hex()
        return output

    TextureHeaderTemplateHex = open(LibraryTexturePath + r"\Header.dat", "rb+").read().hex()  #模板纹理header数据
    ImageNum = TextureNum = int()
    for ObjData in ObjDataGroup:  # object计数循环
        Usemtl = ObjData[1]  # 材质
        ImageNum += 1
        if Usemtl == "bodypaintlivery":
            TextureTypeGroup = ["d"]
        elif Usemtl == "glasstextured":
            TextureTypeGroup = ["d"]
        elif Usemtl == "light":
            TextureTypeGroup = ["l", "n", "s"]
        elif Usemtl == "grille":
            TextureTypeGroup = ["d", "n"]
        elif Usemtl == "interior":
            TextureTypeGroup = ["d", "n", "s"]
        elif Usemtl == "refraction":
            TextureTypeGroup = ["c", "en", "e", "in", "dp"]
        elif Usemtl == "hub" or Usemtl == "rim":
            TextureTypeGroup = ["d", "n", "s"]
        else:
            continue
        ImageName = ObjData[0]  # 图片名称
        ImageBasePath = os.path.dirname(ObjPath) + "\\" + ImageName  # 图片位置
        DefaultImagePath = ImageBasePath + "_" + TextureTypeGroup[0] + ".dds"
        if not os.path.exists(DefaultImagePath):
            input("错误: 未找到默认贴图: {}".format(os.path.basename(DefaultImagePath)))
            exit()
        for TextureType in TextureTypeGroup:
            ImagePath = ImageBasePath + "_" + TextureType + ".dds"
            if not os.path.exists(ImagePath):
                print("警告: 未找到贴图: {}, 将使用贴图: {}替代".format(os.path.basename(ImagePath), os.path.basename(DefaultImagePath)))
                ImagePath = DefaultImagePath
            ImageHex = open(ImagePath, "rb+").read().hex()
            TransverseResolution = ImageHex[24:28]
            VerticalResolution = ImageHex[32:36]
            DXTType = ImageHex[174:176]
            if DXTType == "35":
                DXTTypeHex = "4D000000"
            elif DXTType == "31":
                DXTTypeHex = "47000000"
            else:
                input("错误: 不支持的DXT格式!")
                exit()
            TextureHeaderHex = TextureHeaderTemplateHex[:56] + DXTTypeHex + TextureHeaderTemplateHex[64:72] + VerticalResolution + TransverseResolution + TextureHeaderTemplateHex[80:90] + MipMapping(TransverseResolution) + TextureHeaderTemplateHex[92:96]
            if os.path.exists(UnpackPath + r"\Texture"):
                TextureHeaderOutputPath = UnpackPath + r"\Texture" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + ".dat"
                TextureOutputPath = UnpackPath + r"\Texture" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + "_texture.dat"
            elif os.path.exists(UnpackPath + r"\01_00_00_00"):
                TextureHeaderOutputPath = UnpackPath + r"\01_00_00_00" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + ".dat"
                TextureOutputPath = UnpackPath + r"\01_00_00_00" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + "_texture.dat"
            else:
                input("错误: 无效的Texture[01_00_00_00]路径!")
                exit()
            TextureHeaderOutputPathOpen = open(TextureHeaderOutputPath, "wb+")
            TextureHeaderOutputPathOpen.write(bytes.fromhex(TextureHeaderHex))
            TextureHeaderOutputPathOpen.close()
            ImageCodeHex = ImageHex[256:]
            TextureOutputPathOpen = open(TextureOutputPath, "wb+")
            TextureOutputPathOpen.write(bytes.fromhex(ImageCodeHex))
            TextureOutputPathOpen.close()
            TextureNum += 1

def create_material():
    MaterialCount = TextureCount = int()
    MaterialHex = str()
    MaterialHexGroup = list()
    for MaterialParameter in MaterialParameterGroup:
        MaterialHexID = MaterialHexIDGroup[MaterialCount]
        Usemtl = MaterialParameter[0]
        MaterialCount += 1
        if Usemtl == "body":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Body.dat", "+rb").read().hex()
            DiffuseColor = MaterialParameter[1]
            Roughness = MaterialParameter[2]
            SpecularColor = MaterialParameter[3]
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:256] + DiffuseColor + MaterialTemplateHex[280:288] + Roughness + MaterialTemplateHex[296:384] + SpecularColor + MaterialTemplateHex[408:]
        elif Usemtl == "bodypaint":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\BodyPaint.dat", "+rb").read().hex()
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:]
        elif Usemtl == "bodypaintlivery":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\BodyPaintLivery.dat", "+rb").read().hex()
            DiffuseTextureID = TextureHexIDGroup[TextureCount]
            TextureCount += 1
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:192] + DiffuseTextureID + MaterialTemplateHex[200:]
        elif Usemtl == "carbon":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Carbon.dat", "+rb").read().hex()
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:]
        elif Usemtl == "glass":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Glass.dat", "+rb").read().hex()
            opacity = MaterialParameter[1]
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:320] + opacity + MaterialTemplateHex[328:]
        elif Usemtl == "colouriseglass":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\ColouriseGlass.dat", "+rb").read().hex()
            DiffuseColor = MaterialParameter[1]
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:128] + DiffuseColor + MaterialTemplateHex[152:]
        elif Usemtl == "glassdoublesided":  # [material, opacity]
            MaterialTemplateHex = open(LibraryMaterialPath + r"\GlassDoublesided.dat", "+rb").read().hex()
            Opacity = MaterialParameter[1]
            DiffuseTextureID = TextureHexIDGroup[TextureCount]
            TextureCount += 1
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:352] + Opacity + MaterialTemplateHex[360:768] + DiffuseTextureID + MaterialTemplateHex[776:]
        elif Usemtl == "light":  # [usemtl, emmission_color, emmission_strength]
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Light.dat", "+rb").read().hex()
            EmmissionColor = MaterialParameter[1]
            DiffuseColor = MaterialParameter[2]
            EmmissionStrength = MaterialParameter[3]
            LightTextureID = TextureHexIDGroup[TextureCount]
            NormalTextureID = TextureHexIDGroup[TextureCount + 1]
            SpecularTextureID = TextureHexIDGroup[TextureCount + 2]
            TextureCount += 3
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:192] + EmmissionColor + MaterialTemplateHex[216:224] + EmmissionColor + MaterialTemplateHex[248:256] + EmmissionColor + MaterialTemplateHex[280:288] + EmmissionColor + MaterialTemplateHex[312:384] + DiffuseColor + MaterialTemplateHex[408:416] + EmmissionStrength + MaterialTemplateHex[424:544] + NormalTextureID + MaterialTemplateHex[552:576] + SpecularTextureID + MaterialTemplateHex[584:608] + LightTextureID + MaterialTemplateHex[616:]
        elif Usemtl == "grille":  # [usemtl, diffuse_color, roughness, specular_color]
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Grille.dat", "+rb").read().hex()
            DiffuseColor = MaterialParameter[1]
            Roughness = MaterialParameter[2]
            SpecularColor = MaterialParameter[3]
            DiffuseTextureID = TextureHexIDGroup[TextureCount]
            NormalTextureID = TextureHexIDGroup[TextureCount + 1]
            TextureCount += 2
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:256] + DiffuseColor + MaterialTemplateHex[280:288] + Roughness + MaterialTemplateHex[296:384] + SpecularColor + MaterialTemplateHex[408:512] + NormalTextureID + MaterialTemplateHex[520:544] + DiffuseTextureID + MaterialTemplateHex[552:]
        elif Usemtl == "interior":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Interior.dat", "+rb").read().hex()
            EmmissionColor = MaterialParameter[1]
            EmmissionStrength = MaterialParameter[2]
            DiffuseTextureID = TextureHexIDGroup[TextureCount]
            NormalTextureID = TextureHexIDGroup[TextureCount + 1]
            SpecularTextureID = TextureHexIDGroup[TextureCount + 2]
            TextureCount += 3
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:160] + EmmissionColor + MaterialTemplateHex[184:256] + EmmissionStrength + MaterialTemplateHex[264:416] + NormalTextureID + MaterialTemplateHex[424:448] + DiffuseTextureID + MaterialTemplateHex[456:480] + SpecularTextureID + MaterialTemplateHex[488:]
        elif Usemtl == "refraction":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Refraction.dat", "+rb").read().hex()
            EmmissionColor = MaterialParameter[1]
            EmmissionStrength = MaterialParameter[2]
            DiffuseColor = MaterialParameter[3]
            ColorTextureID = TextureHexIDGroup[TextureCount]
            ExternalNormalTextureID = TextureHexIDGroup[TextureCount + 1]
            EmissiveTextureID = TextureHexIDGroup[TextureCount + 2]
            InternalNormalTextureID = TextureHexIDGroup[TextureCount + 3]
            DisplacementTextureID = TextureHexIDGroup[TextureCount + 4]
            TextureCount += 5
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:224] + EmmissionColor + MaterialTemplateHex[248:256] + EmmissionStrength + MaterialTemplateHex[264:288] + EmmissionColor + MaterialTemplateHex[312:384] + DiffuseColor + MaterialTemplateHex[408:448] + EmmissionColor + MaterialTemplateHex[472:480] + EmmissionColor + MaterialTemplateHex[504:704] + ColorTextureID + MaterialTemplateHex[712:736] + ExternalNormalTextureID + MaterialTemplateHex[744:768] + EmissiveTextureID + MaterialTemplateHex[776:800] + InternalNormalTextureID + MaterialTemplateHex[808:832] + DisplacementTextureID + MaterialTemplateHex[840:]
        elif Usemtl == "tyre":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Tyre.dat", "+rb").read().hex()
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:]
        elif Usemtl == "hub" or Usemtl == "rim":
            MaterialTemplateHex = open(LibraryMaterialPath + r"\Hub.dat", "+rb").read().hex()
            NormalTexture = TextureHexIDGroup[TextureCount + 1]
            DiffuseTexture = TextureHexIDGroup[TextureCount]
            SpecularTexture = TextureHexIDGroup[TextureCount + 2]
            TextureCount += 3
            MaterialHex = MaterialHexID + MaterialTemplateHex[8:448] + NormalTexture + MaterialTemplateHex[456:480] + DiffuseTexture + MaterialTemplateHex[488:544] + SpecularTexture + MaterialTemplateHex[552:]
        MaterialHexGroup.append(MaterialHex)
    for MaterialNum in range(MaterialCount):
        if os.path.exists(UnpackPath + r"\Material"):
            MaterialOutputPath = UnpackPath + r"\Material" + "\\" + '_'.join([(MaterialHexIDGroup[MaterialNum])[x:x + 2] for x in range(0, len((MaterialHexIDGroup[MaterialNum])), 2)]) + ".dat"
        elif os.path.exists(UnpackPath + r"\02_00_00_00"):
            MaterialOutputPath = UnpackPath + r"\02_00_00_00" + "\\" + '_'.join([(MaterialHexIDGroup[MaterialNum])[x:x + 2] for x in range(0, len((MaterialHexIDGroup[MaterialNum])), 2)]) + ".dat"
        else:
            input("error: Invalid Material[02_00_00_00] path!")
        MaterialOutputPathOpen = open(MaterialOutputPath, "wb+")
        MaterialOutputPathOpen.write(bytes.fromhex(MaterialHexGroup[MaterialNum]))
        MaterialOutputPathOpen.close()

def create_renderable():
    RenderableHeaderTemplateHex  = open(LibraryRenderablePath + r"\Header.dat", "rb+").read().hex()
    RenderableHeaderHex = RenderableHeaderTemplateHex[:36] + struct.pack("<H", ObjectCount).hex() + RenderableHeaderTemplateHex[40:]
    MeshHeaderPointerLength = ObjectCount * 4 + (16 - (ObjectCount * 4) % 16)  # 计算Block指针组的总长度
    MeshHeaderPointerPlaceholder = "00" * (16 - (ObjectCount * 4) % 16)  # 计算Block指针组占位符
    for ObjectNum in range(ObjectCount):  # object总数循环
        MeshHeaderPointer = struct.pack("<I", MeshHeaderPointerLength + ObjectNum * 96 + 32).hex()  # 计算Block指针[UInt32]
        RenderableHeaderHex += MeshHeaderPointer  # 合并Block指针至Header数据
    RenderableHeaderHex += MeshHeaderPointerPlaceholder  # 合并Block指针组占位符至Header数据
    MeshHexLengthCount = int()
    RenderableHexGroup = list()
    RenderableBlockTemplateHex = open(LibraryRenderablePath + r"\Block.dat", "rb+").read().hex()
    for ObjectNum in range(ObjectCount):
        MeshVertexIndexCountHex = struct.pack("<L", VertexIndexHexLengthGroup[ObjectNum]).hex()  # 顶点索引字节长度
        MeshVertexIndexInfoBlockPointer = struct.pack("<L", int(len(RenderableHeaderHex) / 2) + 48 + 96 * ObjectNum).hex()
        MeshVertexInfoBlockPointer = struct.pack("<L", int(len(RenderableHeaderHex) / 2) + 72 + 96 * ObjectNum).hex()
        MeshVertexIndexLengthHex = struct.pack("<L", VertexIndexHexLengthGroup[ObjectNum] * 2).hex()
        MeshVertexLengthHex = struct.pack("<L", int(len(VertexHexGroup[ObjectNum]) / 2)).hex()
        if ObjectNum == 0:
            MeshVertexIndexPointerHex = "00000000"
            MeshVertexPointerHex = MeshVertexIndexLengthHex
            MeshHexLengthCount += int(len(VertexIndexHexGroup[ObjectNum]) / 2) + int(len(VertexHexGroup[ObjectNum]) / 2)
        else:
            MeshVertexIndexPointerHex = struct.pack("<L", MeshHexLengthCount).hex()
            MeshVertexPointerHex = struct.pack("<L", MeshHexLengthCount + VertexIndexHexLengthGroup[ObjectNum] * 2).hex()
            MeshHexLengthCount += int(len(VertexIndexHexGroup[ObjectNum]) / 2) + int(len(VertexHexGroup[ObjectNum]) / 2)
        RenderableHexGroup.append(RenderableBlockTemplateHex[:56] + MeshVertexIndexCountHex + RenderableBlockTemplateHex[64:80] + MeshVertexIndexInfoBlockPointer + MeshVertexInfoBlockPointer + RenderableBlockTemplateHex[96:120] + MeshVertexIndexPointerHex + MeshVertexIndexLengthHex + RenderableBlockTemplateHex[136:168] + MeshVertexPointerHex + MeshVertexLengthHex + RenderableBlockTemplateHex[184:])
    AuxFileHexGroup = list()
    for MaterialHexIDNum in range(len(MaterialHexIDGroup)):
        AuxFilePointerHex = struct.pack("<L", int(len(RenderableHeaderHex) / 2) + 32 + 96 * MaterialHexIDNum).hex()
        AuxFileHex = MaterialHexIDGroup[MaterialHexIDNum] + "00000001" + AuxFilePointerHex + "00000000"
        AuxFileHexGroup.append(AuxFileHex)
    if os.path.exists(UnpackPath + r"\Renderable"):
        VehicleRenderableFilePath = UnpackPath + r"\Renderable" + "\\" + VehicleRenderableFileNameGroup[0] + ".dat"  # 取LOD0
        VehicleRenderableMainFilePath = UnpackPath + r"\Renderable" + "\\" + VehicleRenderableFileNameGroup[0] + "_model.dat"
    elif os.path.exists(UnpackPath + r"\05_00_00_00"):
        VehicleRenderableFilePath = UnpackPath + r"\05_00_00_00" + "\\" + VehicleRenderableFileNameGroup[0] + ".dat"  # 取LOD0
        VehicleRenderableMainFilePath = UnpackPath + r"\05_00_00_00" + "\\" + VehicleRenderableFileNameGroup[0] + "_model.dat"
    else:
        print("error: 无效的Renderable[05_00_00_00]路径!")
    RenderableHex = str()
    for RenderableHexCache in RenderableHexGroup:
        RenderableHex += RenderableHexCache
    AuxFileHex = str()
    for AuxFileHexCache in AuxFileHexGroup:
        AuxFileHex += AuxFileHexCache
    NewRenderableHex = bytes.fromhex(RenderableHeaderHex + RenderableHex + AuxFileHex)
    VehicleRenderableFilePathOpen = open(VehicleRenderableFilePath, "wb+")
    VehicleRenderableFilePathOpen.write(NewRenderableHex)
    VehicleRenderableFilePathOpen.close()
    NewRenderableMainHex = str()
    for ObjectNum in range(ObjectCount):
        NewRenderableMainHex += VertexIndexHexGroup[ObjectNum] + VertexHexGroup[ObjectNum]
    NewRenderableMainHex = bytes.fromhex(NewRenderableMainHex)
    VehicleRenderableMainFilePathOpen = open(VehicleRenderableMainFilePath, "wb+")
    VehicleRenderableMainFilePathOpen.write(NewRenderableMainHex)
    VehicleRenderableMainFilePathOpen.close()

def create_samplerstate():
    id_samplerstate_hex_list = []
    for data_object in ObjDataGroup:
        name_object = data_object[1]
        if name_object == "bodypaintlivery":
            id_samplerstate_hex_list = ["8A7A302B"]
    for id_samplerstate_hex in id_samplerstate_hex_list:
        data_template_samplerstate = open(LibrarySamplerPath + "\\" + '_'.join([id_samplerstate_hex[x:x + 2] for x in range(0, len(id_samplerstate_hex), 2)]) + ".dat", "rb+").read()
        if os.path.exists(UnpackPath + r"\SamplerState"):
            path_samplerstate_open = open(UnpackPath + r"\SamplerState" + "\\" + '_'.join([id_samplerstate_hex[x:x + 2] for x in range(0, len(id_samplerstate_hex), 2)]) + ".dat", "wb+")
        elif os.path.exists(UnpackPath + r"\07_00_00_00"):
            path_samplerstate_open = open(UnpackPath + r"\07_00_00_00" + "\\" + '_'.join([id_samplerstate_hex[x:x + 2] for x in range(0, len(id_samplerstate_hex), 2)]) + ".dat", "wb+")
        else:
            input("错误: 无效的SamplerState[07_00_00_00]路径!")
        path_samplerstate_open.write(data_template_samplerstate)
        path_samplerstate_open.close()
    return id_samplerstate_hex_list

def write_ids():
    data_new_ids = str()
    data_template_ids = open(LibraryIDsPath, "rb+").read().hex()
    data_ids = open(UnpackPath + "\IDs.BIN", "rb+").read().hex()
    data_header_ids = data_ids[:224]
    data_blocks_ids = data_ids[224:]
    for id_texture_hex in TextureHexIDGroup:
        data_new_ids += id_texture_hex + data_template_ids[8:144]
    for id_material_hex in MaterialHexIDGroup:
        data_new_ids += id_material_hex + data_template_ids[152:288]
    for id_samplerstate_hex in id_samplerstate_hex_list:
        data_new_ids += id_samplerstate_hex + data_template_ids[296:432]
    data_new_ids = bytes.fromhex(data_header_ids + data_new_ids + data_blocks_ids)
    path_ids_open = open(UnpackPath + "\IDs.BIN", "wb+")
    path_ids_open.write(data_new_ids)
    path_ids_open.close()

(LibraryPath, LibraryIDsPath, LibraryMaterialPath, LibraryRenderablePath, LibrarySamplerPath, LibraryTexturePath) = check_path()
print("Library检查完成!")
print("Need For Speed Most Wanted(2012) Vehicle Model Tool by NIVSAYZ")
print("版本: 1.1.3 - Release")
ObjPath = input("obj文件路径:")
if not os.path.exists(ObjPath):
    input("错误: obj文件路径无效!")
    exit()
UnpackPath = input("解包车辆文件路径:")
if not os.path.exists(UnpackPath):
    input("错误: 解包车辆文件路径无效!")
    exit()
os.system("CLS")
print("开始转换!")
start = timer()  # 记录起始时间
print("获取obj文件数据(1/11)")
(MtlPath, ObjectCount, ObjDataGroup, vGroup, vtGroup, vnGroup, vVertexIndexGroup, vtVertexIndexGroup, vnVertexIndexGroup, VertexIndexGroup, VertexCountGroup) = read_obj()
print("获取mtl文件数据(2/11)")
(MaterialCount, MaterialParameterGroup) = read_mtl()
print("生成Mesh(3/11)")
(VertexIndexHexLengthGroup, VertexIndexHexGroup, VertexHexGroup) = create_mesh()
print("获取GraphicsSpec数据(4/11)")
(PolygonSoupListID, VehicleModelFileName, FrontWheelModelFileNameGroup, RearWheelModelFileNameGroup) = read_graphicsspec()
print("获取车辆模型数据(5/11)")
(VehicleRenderableFileNameGroup) = read_model_vehicle()
print("生成ID(6/11)")
(MaterialHexIDGroup, TextureHexIDGroup) = create_id()
print("生成纹理(7/11)")
create_texture()
print("生成材质(8/11)")
create_material()
print("生成Renderable(9/11)")
create_renderable()
print("写入Sampler(10/11)")
(id_samplerstate_hex_list) = create_samplerstate()
print("写入IDs(11/11)")
write_ids()
end = timer()  # 记录结束时间
print("转换完成!")
print("总耗时: {}s".format(end - start))
input("按任意键退出")
