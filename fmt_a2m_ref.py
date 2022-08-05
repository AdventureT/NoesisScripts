from ctypes.wintypes import SHORT
from inc_noesis import *
import noesis
import rapi

HEADER_SIZE = 0x40

class Header:

    sectionCount = 0
    modelCount = 0
    unk2 = 0
    unk3 = 0
    floats = []
    sectionOffset = 0
    matricesOffset = 0
    infoSectionOffset1 = 0
    infoSectionOffset2 = 0
    subInfoSectionOffsetCount = 0  #seems incorrect
    subInfoSectionOffset = 0
    unk41 = 0
    subInfoSectionOffset2Count = 0
    subInfoSectionOffset2 = 0

    def __init__(self, sectionCount, modelCount, unk2, unk3, floats, sectionOffset, matricesOffset, 
    infoSectionOffset1, infoSectionOffset2, subInfoSectionOffsetCount, subInfoSectionOffset, 
    unk41, subInfoSectionOffset2Count, subInfoSectionOffset2):
        self.sectionCount = sectionCount
        self.modelCount = modelCount
        self.unk2 = unk2
        self.unk3 = unk3
        self.floats = floats
        self.sectionOffset = sectionOffset
        self.matricesOffset = matricesOffset
        self.infoSectionOffset1 = infoSectionOffset1
        self.infoSectionOffset2 = infoSectionOffset2
        self.subInfoSectionOffsetCount = subInfoSectionOffsetCount
        self.subInfoSectionOffset = subInfoSectionOffset
        self.unk41 = unk41
        self.subInfoSectionOffset2Count = subInfoSectionOffset2Count
        self.subInfoSectionOffset2 = subInfoSectionOffset2

class A2MeshHeader:
    unk11 = 0
    meshInfoCount = 0
    meshInfosOffset = 0
    unk14 = 0
    unk15 = 0
    unk16 = 0
    unk17 = 0
    meshFootersCount = 0
    meshFootersOffset = 0
    unk20 = 0
    unk21 = 0
    unk22 = 0
    unk23 = 0
    unk24 = 0

    def __init__(self, unk11, meshInfoCount, meshInfosOffset, unk14, unk15, unk16, unk17, 
    meshFootersCount, meshFootersOffset, unk20, unk21, 
    unk22, unk23, unk24):
        self.unk11 = unk11
        self.meshInfoCount = meshInfoCount
        self.meshInfosOffset = meshInfosOffset
        self.unk14 = unk14
        self.unk15 = unk15
        self.unk16 = unk16
        self.unk17 = unk17
        self.meshFootersCount = meshFootersCount
        self.meshFootersOffset = meshFootersOffset
        self.unk20 = unk20
        self.unk21 = unk21
        self.unk22 = unk22
        self.unk23 = unk23
        self.unk24 = unk24

class A2MeshInfo:
    meshFooterOffset = 0
    vertexCount = 0
    indicesCount = 0
    idkCount = 0
    unk11 = 0
    unk12 = 0
    unk17 = 0
    unk18 = 0
    intCount = 0
    intsOffset = 0
    unk21 = 0
    unk22 = 0
    unk23 = 0
    unk24 = 0
    indicesOffset = 0
    verticesOffset = 0

    def __init__(self, meshFooterOffset, vertexCount, indicesCount, idkCount, unk11, unk12, unk17, 
    unk18, intCount, intsOffset, unk21, 
    unk22, unk23, unk24, indicesOffset, verticesOffset):
        self.meshFooterOffset = meshFooterOffset
        self.vertexCount = vertexCount
        self.indicesCount = indicesCount
        self.idkCount = idkCount
        self.unk11 = unk11
        self.unk12 = unk12
        self.unk17 = unk17
        self.unk18 = unk18
        self.intCount = intCount
        self.intsOffset = intsOffset
        self.unk21 = unk21
        self.unk22 = unk22
        self.unk23 = unk23
        self.unk24 = unk24
        self.indicesOffset = indicesOffset
        self.verticesOffset = verticesOffset

class A2MeshFooter:
    unk11 = 0
    unk12 = 0
    unk13 = 0.0
    unk14 = 0
    unk15 = 0
    vertexStride = 0
    unk17 = 0
    unk18 = 0
    unk19 = 0
    unk20 = 0
    unk21 = 0
    unk22 = 0
    unk23 = 0
    unk24 = 0
    unk25 = 0
    unk26 = 0
    unk27 = 0
    unk28 = 0

    def __init__(self, unk11, unk12, unk13, unk14, unk15, vertexStride, unk17, 
    unk18, unk19, unk20, unk21, 
    unk22, unk23, unk24, unk25, unk26, unk27, unk28):
        self.unk11 = unk11
        self.unk12 = unk12
        self.unk13 = unk13
        self.unk14 = unk14
        self.unk15 = unk15
        self.vertexStride = vertexStride
        self.unk17 = unk17
        self.unk18 = unk18
        self.unk19 = unk19
        self.unk20 = unk20
        self.unk21 = unk21
        self.unk22 = unk22
        self.unk23 = unk23
        self.unk24 = unk24
        self.unk25 = unk25
        self.unk26 = unk26
        self.unk27 = unk27
        self.unk28 = unk28

class A2Mesh:
    
    meshInfos = []
    meshFooters = []


    def __init__(self, meshHeader, meshInfos, meshFooters):
        self.meshHeader = meshHeader
        self.meshInfos = meshInfos
        self.meshFooters = meshFooters


def registerNoesisTypes():
    handle = noesis.register("Ed Edd Eddy mis Ed-ventures (PC)", ".ref")
    noesis.setHandlerTypeCheck(handle, A2MCheckType)
    noesis.setHandlerLoadModel(handle, A2MLoadModel)
    #noesis.setTypeSharedModelFlags(handle, noesis.NMSHAREDFL_FLATWEIGHTS)
    noesis.logPopup()
    return 1

def A2MCheckType(data):
    return 1

def A2MLoadModel(data, mdlList):
    bs = NoeBitStream(data)
    ctx = rapi.rpgCreateContext()
    header = Header(bs.readUShort(),bs.readUShort(),bs.readInt(),bs.readInt(),
    [bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat()],
    bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
    bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(), bs.readInt())
    
    bs.seek(header.infoSectionOffset2 - HEADER_SIZE)
    offsets = []
    A2meshes = []
    for i in range(header.modelCount):
        offsets.append(bs.readInt())
    
    for offset in offsets:
        bs.seek(offset - HEADER_SIZE)
        count = bs.readInt()
        offset2 = bs.readInt()
        bs.seek(offset2 - HEADER_SIZE)
        offset2 = bs.readInt()
        bs.seek(offset2 - HEADER_SIZE)
        count = bs.readInt()
        count2 = bs.readInt()
        offset2 = bs.readInt()
        offset3 = bs.readInt()
        bs.seek(offset3 - HEADER_SIZE)

        meshHeader = A2MeshHeader(bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
            bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
            bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt())

        meshInfos = []
        bs.seek(meshHeader.meshInfosOffset - HEADER_SIZE)
        for i in range(meshHeader.meshInfoCount):
            mesh = A2MeshInfo(bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
                bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
                bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt())
            meshInfos.append(mesh)
        
        meshFooters = []
        for i in range(meshHeader.meshFootersCount):
            meshFooters.append(A2MeshFooter(bs.readInt(),bs.readInt(),bs.readFloat(),bs.readInt(),
                bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),
                bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt(),bs.readInt()))

        A2meshes.append(A2Mesh(meshHeader, meshInfos, meshFooters))
    x = 0
    for mesh in A2meshes:
        for meshInfo in mesh.meshInfos:
            #rapi.rpgSetName(str(x))
            x += 1
            bs.seek((meshInfo.meshFooterOffset - HEADER_SIZE) + 5*4, NOESEEK_ABS)
            vertexStride = bs.readInt()
            bs.seek(meshInfo.verticesOffset - HEADER_SIZE, NOESEEK_ABS)
            vertexBuffer = bs.readBytes(vertexStride * meshInfo.vertexCount)
            #print(vertexStride)
            if (vertexStride == 52):
                rapi.rpgBindPositionBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, vertexStride, 0)
                rapi.rpgBindNormalBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 28)
                rapi.rpgBindBoneIndexBufferOfs(vertexBuffer, noesis.RPGEODATA_UBYTE, vertexStride, 24, 3)
                rapi.rpgBindBoneWeightBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, vertexStride, 12, 3)
                rapi.rpgBindUV1BufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 44)
                #rapi.rpgBindColorBufferOfs(vertexBuffer, noesis.RPGEODATA_BYTE, vertexStride, 40, 4)
            elif (vertexStride == 36):
                rapi.rpgBindPositionBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, vertexStride, 0)
                rapi.rpgBindNormalBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 12)
                rapi.rpgBindColorBufferOfs(vertexBuffer, noesis.RPGEODATA_BYTE, vertexStride, 24, 4)
                rapi.rpgBindUV1BufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 28)
            #elif (vertexStride == 28):
                #rapi.rpgBindPositionBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, vertexStride, 0)
                #rapi.rpgBindNormalBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 12)
                #rapi.rpgBindColorBufferOfs(vertexBuffer, noesis.RPGEODATA_BYTE, vertexStride, 24, 4)
                #rapi.rpgBindUV1BufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT,vertexStride, 28)
            bs.seek(meshInfo.indicesOffset - HEADER_SIZE, NOESEEK_ABS)
            indexBuffer = bs.readBytes(vertexStride * meshInfo.vertexCount)
            rapi.rpgCommitTriangles(indexBuffer, noesis.RPGEODATA_USHORT, meshInfo.indicesCount, noesis.RPGEO_TRIANGLE_STRIP, 1)

        model = rapi.rpgConstructModel()
        bs.seek(header.sectionOffset - HEADER_SIZE)
        #print(header.sectionOffset)
        bones = []
        for i in range(header.sectionCount):
            boneMat = NoeMat44.fromBytes(bs.readBytes(64))
            parentIdx = bs.readShort()
            unk = bs.readShort()
            unk2 = bs.readShort()
            unk3 = bs.readShort()
            idx = bs.readInt()
            bones.append(NoeBone(i, str(i), boneMat.toMat43(), None, parentIdx))
            bs.seek(20, NOESEEK_REL)
        # Converting local matrix to world space
        for i in range(0, header.sectionCount):
            j = bones[i].parentIndex
            if j != -1:
                bones[i].setMatrix( bones[i].getMatrix() * bones[j].getMatrix() )
        model.setBones(bones)
        mdlList.append(model)
        rapi.rpgClearBufferBinds() #reset in case a subsequent mesh doesn't have the same components
        
    return 1
        
