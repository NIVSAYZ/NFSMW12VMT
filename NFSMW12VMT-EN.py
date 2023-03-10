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
        input("error: Library is incomplete, missing item: {}".format(MissingItemGroup))
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
        input("error: Library material is incomplete, missing item: {}".format(MissingItemGroup))
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
        input("error: Library renderable is incomplete, missing item: {}".format(MissingItemGroup))
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
        input("error: Library sampler is incomplete, missing item: {}".format(MissingItemGroup))
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
        input("error: Library texture is incomplete, missing item: {}".format(MissingItemGroup))
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
            MtlFile = SplitLine[1]  # mtl?????????
            MtlPath = os.path.dirname(ObjPath) + "\\" + MtlFile  # mtl????????????
        elif SplitLine[0] == "usemtl":
            UsemtlGroup.append(SplitLine[1])
        elif SplitLine[0] == "o":
            if len(SplitLine[1].split("_")) < 2:
                input("error: The naming format of object: {} is incorrect!".format(SplitLine[1].split("_")[0]))
                exit()
            ObjectCount += 1  # object??????
            MaterialGroup.append(SplitLine[1].split("_")[1])
            ObjectNameGroup.append(SplitLine[1].split("_")[0])
            ObjectLineRangeGroup.append(LineCount)  # object???????????????
        LineCount += 1  # ?????????
    if MtlFile == None:
        input("error: The obj file has no associated mtl file!")
        exit()
    ObjectLineRangeGroup.append(LineCount)  # object???????????????
    vCount = vtCount = vnCount = int()
    vGroup = list(); vtGroup = list(); vnGroup = list(); vCountGroup = [0]; vtCountGroup = [0]; vnCountGroup = [0]; VertexCountGroup = list(); ObjDataGroup = list(); vVertexIndexGroup = list(); vtVertexIndexGroup = list(); vnVertexIndexGroup = list(); VertexIndexGroup = list()
    for ObjectNum in range(ObjectCount):  # object????????????
        VertexCount = int()
        vGroupCache = list(); vtGroupCache = list(); vnGroupCache = list(); VertexGroup = list(); FaceEdgeGroup = list(); vVertexIndexCache = list(); vtVertexIndexCache = list(); vnVertexIndexCache = list(); VertexNumGroup = list()
        RemoveRepeatVertexDict = RemoveRepeatSequentialVertexDict = dict()
        ObjDataGroup.append([ObjectNameGroup[ObjectNum], MaterialGroup[ObjectNum], UsemtlGroup[ObjectNum]])  # ??????object?????????object????????????
        for LineNum in range(ObjectLineRangeGroup[ObjectNum] + 1, ObjectLineRangeGroup[ObjectNum + 1]):  # object???????????????
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
                for EdgeNum in range(1, len(SplitLine)):  # ???????????????
                    VertexCount += 1
                    RemoveRepeatVertexDict[SplitLine[EdgeNum]] = VertexCount  # ??????????????????
                    VertexGroup.append(SplitLine[EdgeNum])  # ?????????
                FaceEdgeGroup.append(EdgeNum)  # ???????????????
        if len(RemoveRepeatVertexDict) > 60000:
            input("error: The transformed vertex of object {} will exceed 60000, it will cause the game to crash, please reduce the vertex of this object!".format(ObjDataGroup[ObjectNum][0]))
            exit()
        RemoveRepeatVertexGroup = list(RemoveRepeatVertexDict.keys())  # ???????????????
        vCountGroup.append(vCount)  # v?????????
        vtCountGroup.append(vtCount)  # vt?????????
        vnCountGroup.append(vnCount)  # vn?????????
        vGroup.append(vGroupCache)
        vtGroup.append(vtGroupCache)
        vnGroup.append(vnGroupCache)
        for VertexNum in range(len(RemoveRepeatVertexDict)):  # ??????????????????????????????
            RemoveRepeatSequentialVertexDict[RemoveRepeatVertexGroup[VertexNum]] = VertexNum  # ??????????????????????????????????????????
        VertexCountGroup.append(len(RemoveRepeatVertexDict))  # ????????????????????????
        for RemoveRepeatVertex in RemoveRepeatVertexGroup:  # ??????????????????
            RemoveRepeatVertex = RemoveRepeatVertex.split("/")  # ??????????????????v/vt/vn
            vVertexIndexCache.append(int(RemoveRepeatVertex[0]) - vCountGroup[ObjectNum] - 1)  # v
            if RemoveRepeatVertex[1] == "":
                vtVertexIndexCache.append(0)
            else:
                vtVertexIndexCache.append(int(RemoveRepeatVertex[1]) - vtCountGroup[ObjectNum] - 1)  # vt
            vnVertexIndexCache.append(int(RemoveRepeatVertex[2]) - vnCountGroup[ObjectNum] - 1)  # vn
        vVertexIndexGroup.append(vVertexIndexCache)
        vtVertexIndexGroup.append(vtVertexIndexCache)
        vnVertexIndexGroup.append(vnVertexIndexCache)
        for Vertex in VertexGroup:  # ????????????
            VertexNumGroup.append(RemoveRepeatSequentialVertexDict[Vertex])  # ???????????????????????????????????????
        EdgeCount = int()
        VertexIndexCache = list()
        for FaceEdge in FaceEdgeGroup:  # ?????????????????????
            Cache = list()
            for EdgeNum in range(FaceEdge):  # ???????????????
                Cache.append(VertexNumGroup[EdgeNum + EdgeCount])  # ?????????????????????
            VertexIndexCache.append(Cache[0])  # ??????????????????????????????
            Count1 = 0
            Count2 = 0
            for i3 in range(1, FaceEdge):
                if i3 % 2 != 0:
                    Count1 += 1
                    VertexIndexCache.append(Cache[Count1])
                elif i3 % 2 == 0:
                    Count2 -= 1
                    VertexIndexCache.append(Cache[Count2])
            VertexIndexCache.append("FFFF")  # ???????????????????????????
            EdgeCount += EdgeNum + 1  # ???????????????
        VertexIndexGroup.append(VertexIndexCache)
    return MtlPath, ObjectCount, ObjDataGroup, vGroup, vtGroup, vnGroup, vVertexIndexGroup, vtVertexIndexGroup, vnVertexIndexGroup, VertexIndexGroup, VertexCountGroup

def read_mtl():
    if not os.path.exists(MtlPath):
        input("error: Invalid mtl file path???")
        exit()
    with open(MtlPath, encoding="utf-8") as f:
        MtlLines = f.readlines()
    LineCount = NewmtlCount = int()
    MaterialLineRangeGroup = list()
    NewmtlDict = dict()
    for Line in MtlLines:
        SplitLine = Line.strip().split(" ")
        if SplitLine[0] == "newmtl":
            MaterialLineRangeGroup.append(LineCount)  # ?????????????????????
            NewmtlDict[SplitLine[1]] = NewmtlCount  # ??????????????????
            NewmtlCount += 1
        LineCount += 1  # ?????????
    MaterialLineRangeGroup.append(LineCount)  # ?????????????????????
    MaterialCount = int()
    MaterialParameterGroup = list()
    for ObjectNum in range(ObjectCount):
        MaterialCount += 1
        Material = ObjDataGroup[ObjectNum][1]
        Num = NewmtlDict[ObjDataGroup[ObjectNum][2]]
        if Material == "body":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
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
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "d":
                    Opacity = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, Opacity])
        elif Material == "colouriseglass":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "Kd":
                    Diffuse_R = struct.pack("<f", float(SplitLine[1])).hex()
                    Diffuse_G = struct.pack("<f", float(SplitLine[2])).hex()
                    Diffuse_B = struct.pack("<f", float(SplitLine[3])).hex()
                    DiffuseColor = Diffuse_R + Diffuse_G + Diffuse_B
            MaterialParameterGroup.append([Material, DiffuseColor])
        elif Material == "glassdoublesided":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
                SplitLine = MtlLines[LineNum].strip().split(" ")
                if SplitLine[0] == "d":
                    Opacity = struct.pack("<f", float(SplitLine[1])).hex()
            MaterialParameterGroup.append([Material, Opacity])
        elif Material == "light":
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
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
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
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
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
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
            for LineNum in range(MaterialLineRangeGroup[Num], MaterialLineRangeGroup[Num + 1]):  # ???????????????
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
            input("error: The material type: {} is an unsupported material type!".format(Material))
            exit()
    return MaterialCount, MaterialParameterGroup

def create_mesh():
    def get_normal():
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????
        Normal = struct.pack("<f", vnCoord[0]).hex() + struct.pack("<f", vnCoord[1]).hex() + struct.pack("<f", vnCoord[2]).hex()
        return Normal

    def get_tangent():
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????
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
        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????
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

    def get_normal_packed():  # ??????????????????????????????(Binko_ctr)
        def ab_to_tanhalf_ab(a, b):
            cot_a_b = b / a
            cot_a_b_2 = cot_a_b * cot_a_b
            csc_a_b = math.sqrt(1 + cot_a_b_2) if a > 0 else - math.sqrt(1 + cot_a_b_2)
            return 1 / (cot_a_b + csc_a_b)

        vnCoord = vnGroup[ObjectNum][vnVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????

        # ????????????????????????
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
        # ????????? + ????????????
        Norm = math.sqrt(NormalPackedCache_x ** 2 + NormalPackedCache_y ** 2 + NormalPackedCache_z ** 2)
        NormalPacked_x = struct.pack("<h", round(NormalPackedCache_x / Norm * 32767)).hex()
        NormalPacked_y = struct.pack("<h", round(NormalPackedCache_y / Norm * 32767)).hex()
        NormalPacked_z = struct.pack("<h", round(NormalPackedCache_z / Norm * 32767)).hex()
        NormalPacked_w = struct.pack("<h", round(0.03 * 32767)).hex()
        NormalPacked = NormalPacked_x + NormalPacked_y + NormalPacked_z + NormalPacked_w
        return NormalPacked

    # ?????????
    VertexIndexHexGroup = list(); VertexIndexHexLengthGroup = list()
    for ObjectNum in range(ObjectCount):  # object????????????
        VertexIndexHex = str()
        for VertexIndex in VertexIndexGroup[ObjectNum]:  # Mesh??????????????????
            if VertexIndex == "FFFF":
                VertexIndexHex += "FFFF"
            else:
                VertexIndexHex += struct.pack("<H", VertexIndex).hex()
        VertexIndexHexGroup.append(VertexIndexHex)  # ??????Mesh????????????
        VertexIndexHexLengthGroup.append(int(len(VertexIndexHex) / 4))  # ?????????????????????
    # ????????????
    VertexHexGroup = list()
    BlendIndices = "00000000"
    BlendWeight = "FF000000"
    for ObjectNum in range(ObjectCount):  # object????????????
        VertexHex = str()
        Usemtl = ObjDataGroup[ObjectNum][1]  # ??????
        for VertexNum in range(VertexCountGroup[ObjectNum]):  # ??????????????????
            vCoord = vGroup[ObjectNum][vVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????
            Position = struct.pack("<h", int(round(vCoord[0] * 32767 / 11))).hex() + struct.pack("<h", int(round(vCoord[1] * 32767 / 11))).hex() + struct.pack("<h", int(round(vCoord[2] * 32767 / 11))).hex() + "FF7F"  # ??????????????????????????????
            if vtVertexIndexGroup[ObjectNum][VertexNum] == 0:
                vtCoord = [0, 1]
            else:
                vtCoord = vtGroup[ObjectNum][vtVertexIndexGroup[ObjectNum][VertexNum]]  # ???????????????
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
        input("error: Invalid GraphicsSpec[06_01_00_00] path!")
        exit()
    Wheel1BlockPointer = struct.unpack("<I", bytes.fromhex(GraphicsSpecHex[24:32]))[0] * 2
    AuxFilePointer = (struct.unpack("<I", bytes.fromhex(GraphicsSpecHex[Wheel1BlockPointer + 240:Wheel1BlockPointer + 248]))[0] + 64) * 2
    for LineNum in range(int((len(GraphicsSpecHex) - AuxFilePointer) / 32)):  # AuxFile????????????
        Line = GraphicsSpecHex[AuxFilePointer + LineNum * 32:AuxFilePointer + (LineNum + 1) * 32]
        if Line[8:16] == "60000001":
            PolygonSoupListID = struct.unpack("<L", bytes.fromhex(Line[:8]))[0]
        elif Line[8:16] == "00000000":
            ModelHexIDDict[Line[:8].upper()] = LineNum
    ModelHexIDList = list(ModelHexIDDict.keys())
    VehicleModelFileName = '_'.join([ModelHexIDList[0][x:x + 2] for x in range(0, len(ModelHexIDList[0]), 2)])
    FrontWheelModelFileNameGroup = list(); RearWheelModelFileNameGroup = list()
    for ModelHexIDNum in range(1, 5):
        FrontWheelModelFileNameGroup.append('_'.join([ModelHexIDList[ModelHexIDNum][x:x + 2] for x in range(0, len(ModelHexIDList[ModelHexIDNum]), 2)]))  # [??????, ??????, ????????????, ??????]
    for ModelHexIDNum in range(5, 9):
        RearWheelModelFileNameGroup.append('_'.join([ModelHexIDList[ModelHexIDNum][x:x + 2] for x in range(0, len(ModelHexIDList[ModelHexIDNum]), 2)]))  # [??????, ??????, ????????????, ??????]
    return PolygonSoupListID, VehicleModelFileName, FrontWheelModelFileNameGroup, RearWheelModelFileNameGroup

def read_model_vehicle():
    if os.path.exists(UnpackPath + r"\Model"):
        VehicleModelHex = open(UnpackPath + r"\Model" + "\\" + VehicleModelFileName + ".dat", "rb+").read().hex()
    elif os.path.exists(UnpackPath + r"\51_00_00_00"):
        VehicleModelHex = open(UnpackPath + r"\51_00_00_00" + "\\" + VehicleModelFileName + ".dat", "rb+").read().hex()
    else:
        input("error: Invalid Model[51_00_00_00] path!")
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
    Count += 1024
    MaterialHexIDGroup = list(); TextureHexIDGroup = list()
    for ObjData in ObjDataGroup:  # object????????????
        Usemtl = ObjData[1]
        MaterialID = PolygonSoupListID * 256 + Count
        if Usemtl == "body" or Usemtl == "bodypaint" or Usemtl == "carbon" or Usemtl == "glass" or Usemtl == "mirrorglass" or Usemtl == "colouriseglass" or Usemtl == "tyre":
            Count += 1  # ??????+??????
        elif Usemtl == "bodypaintlivery":
            Count += 2  # ??????+??????
            for i in range(1, 2):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "light":
            Count += 4  # ??????+??????
            for i in range(1, 4):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "glassdoublesided":
            Count += 2  # ??????+??????
            for i in range(1, 2):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "grille":
            Count += 3  # ??????+??????
            for i in range(1, 3):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "interior":
            Count += 4  # ??????+??????
            for i in range(1, 4):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "refraction":
            Count += 6
            for i in range(1, 6):
                TextureID = MaterialID + i
                TextureHexIDGroup.append(struct.pack("<L", TextureID).hex().upper())
        elif Usemtl == "hub" or Usemtl == "rim":
            Count += 4  # ??????+??????
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

    TextureHeaderTemplateHex = open(LibraryTexturePath + r"\Header.dat", "rb+").read().hex()  #????????????header??????
    ImageNum = TextureNum = int()
    for ObjData in ObjDataGroup:  # object????????????
        Usemtl = ObjData[1]  # ??????
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
        ImageName = ObjData[0]  # ????????????
        ImageBasePath = os.path.dirname(ObjPath) + "\\" + ImageName  # ????????????
        DefaultImagePath = ImageBasePath + "_" + TextureTypeGroup[0] + ".dds"
        if not os.path.exists(DefaultImagePath):
            input("error: Default texture: {} not found!".format(os.path.basename(DefaultImagePath)))
            exit()
        for TextureType in TextureTypeGroup:
            ImagePath = ImageBasePath + "_" + TextureType + ".dds"
            if not os.path.exists(ImagePath):
                print("warning: Not found texture: {}, texture: {} will be used instead".format(os.path.basename(ImagePath), os.path.basename(DefaultImagePath)))
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
                input("error: Unsupported DXT format!")
                exit()
            TextureHeaderHex = TextureHeaderTemplateHex[:56] + DXTTypeHex + TextureHeaderTemplateHex[64:72] + VerticalResolution + TransverseResolution + TextureHeaderTemplateHex[80:90] + MipMapping(TransverseResolution) + TextureHeaderTemplateHex[92:96]
            if os.path.exists(UnpackPath + r"\Texture"):
                TextureHeaderOutputPath = UnpackPath + r"\Texture" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + ".dat"
                TextureOutputPath = UnpackPath + r"\Texture" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + "_texture.dat"
            elif os.path.exists(UnpackPath + r"\01_00_00_00"):
                TextureHeaderOutputPath = UnpackPath + r"\01_00_00_00" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + ".dat"
                TextureOutputPath = UnpackPath + r"\01_00_00_00" + "\\" + '_'.join([TextureHexIDGroup[TextureNum][x:x + 2] for x in range(0, len(TextureHexIDGroup[TextureNum]), 2)]) + "_texture.dat"
            else:
                input("error: Invalid Texture[01_00_00_00] path!")
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
    MeshHeaderPointerLength = ObjectCount * 4 + (16 - (ObjectCount * 4) % 16)  # ??????Block?????????????????????
    MeshHeaderPointerPlaceholder = "00" * (16 - (ObjectCount * 4) % 16)  # ??????Block??????????????????
    for ObjectNum in range(ObjectCount):  # object????????????
        MeshHeaderPointer = struct.pack("<I", MeshHeaderPointerLength + ObjectNum * 96 + 32).hex()  # ??????Block??????[UInt32]
        RenderableHeaderHex += MeshHeaderPointer  # ??????Block?????????Header??????
    RenderableHeaderHex += MeshHeaderPointerPlaceholder  # ??????Block?????????????????????Header??????
    MeshHexLengthCount = int()
    RenderableHexGroup = list()
    RenderableBlockTemplateHex = open(LibraryRenderablePath + r"\Block.dat", "rb+").read().hex()
    for ObjectNum in range(ObjectCount):
        MeshVertexIndexCountHex = struct.pack("<L", VertexIndexHexLengthGroup[ObjectNum]).hex()  # ????????????????????????
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
        VehicleRenderableFilePath = UnpackPath + r"\Renderable" + "\\" + VehicleRenderableFileNameGroup[0] + ".dat"  # ???LOD0
        VehicleRenderableMainFilePath = UnpackPath + r"\Renderable" + "\\" + VehicleRenderableFileNameGroup[0] + "_model.dat"
    elif os.path.exists(UnpackPath + r"\05_00_00_00"):
        VehicleRenderableFilePath = UnpackPath + r"\05_00_00_00" + "\\" + VehicleRenderableFileNameGroup[0] + ".dat"  # ???LOD0
        VehicleRenderableMainFilePath = UnpackPath + r"\05_00_00_00" + "\\" + VehicleRenderableFileNameGroup[0] + "_model.dat"
    else:
        print("error: Invalid Renderable[05_00_00_00] path!")
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
            input("error: Invalid SamplerState[07_00_00_00] path!")
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
print("Library check completed!")
print("Need For Speed Most Wanted(2012) Vehicle Model Tool by NIVSAYZ")
print("Version: 1.1.3 - Release")
ObjPath = input("obj file path:")
if not os.path.exists(ObjPath):
    input("error: Invalid obj file path!")
    exit()
UnpackPath = input("Unpack vehicle folder path:")
if not os.path.exists(UnpackPath):
    input("error: Invalid unpack vehicle folder path!")
    exit()
os.system("CLS")
print("Start conversion!")
start = timer()  # ??????????????????
print("Get obj data(1/11)")
(MtlPath, ObjectCount, ObjDataGroup, vGroup, vtGroup, vnGroup, vVertexIndexGroup, vtVertexIndexGroup, vnVertexIndexGroup, VertexIndexGroup, VertexCountGroup) = read_obj()
print("Get mtl data(2/11)")
(MaterialCount, MaterialParameterGroup) = read_mtl()
print("Create Mesh(3/11)")
(VertexIndexHexLengthGroup, VertexIndexHexGroup, VertexHexGroup) = create_mesh()
print("Get graphicsSpec data(4/11)")
(PolygonSoupListID, VehicleModelFileName, FrontWheelModelFileNameGroup, RearWheelModelFileNameGroup) = read_graphicsspec()
print("Get vehicle model data(5/11)")
(VehicleRenderableFileNameGroup) = read_model_vehicle()
print("Create ID(6/11)")
(MaterialHexIDGroup, TextureHexIDGroup) = create_id()
print("Create texture(7/11)")
create_texture()
print("Create material(8/11)")
create_material()
print("Create renderable(9/11)")
create_renderable()
print("Add sampler(10/11)")
(id_samplerstate_hex_list) = create_samplerstate()
print("Write to IDs(11/11)")
write_ids()
end = timer()  # ??????????????????
print("Conversion complete!")
print("Time used: {}s".format(end - start))
input("Press any key to exit")
