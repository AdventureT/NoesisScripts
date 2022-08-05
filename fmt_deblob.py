from inc_noesis import *
import noesis
import rapi

class MeshTable():
    def __init__(self, zero, one, unknown1, unknown2, meshNameOffset, meshSubInfoOffset):
        self.zero = zero
        self.one = one
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.meshNameOffset = meshNameOffset
        self.meshSubInfoOffset = meshSubInfoOffset
class MeshSubInfos():
    def __init__(self, vertexCount, normalCount, faceCount, one, normalOffset, vertexOffset, faceOffset):
        self.vertexCount = vertexCount
        self.normalCount = normalCount
        self.faceCount = faceCount
        self.one = one
        self.normalOffset = normalOffset
        self.vertexOffset = vertexOffset
        self.faceOffset = faceOffset

def registerNoesisTypes():
   handle = noesis.register("De Blob (PC)", ".TMDL")
   noesis.setHandlerTypeCheck(handle, noepyCheckType)
   noesis.setHandlerLoadModel(handle, noepyLoadModel)
   #noesis.logPopup()
   return 1

def noepyCheckType(data):
    return 1

def noepyLoadModel(data, mdlList):
    f = NoeBitStream(data)
    ctx = rapi.rpgCreateContext()
    fileHeaderOffset = f.readUInt()
    skeletonHeaderOffset = f.readUInt()
    skeletonOffset = f.readUInt()
    collisionOffset = f.readUInt()
    tmodOffset = f.readUInt()
    tmdl = f.readBytes(4).decode("ASCII")
    zero = f.readUInt()
    unknown = f.readUInt()
    zero = f.readUInt()
    modelNameOffset = f.readUInt()
    f.seek(modelNameOffset + 20, NOESEEK_ABS)
    modelName = f.readString()
    f.seek(0x2C + 20, NOESEEK_ABS)
    boneCount = f.readUInt()
    f.seek(0x30, NOESEEK_REL)
    bonesOffset = f.readUInt()
    f.seek(bonesOffset + 20, NOESEEK_ABS)
    bones = []
    for i in range(0,boneCount):
        f.seek(0x10, NOESEEK_REL)
        Mat44 = NoeMat44.fromBytes(f.readBytes(0x40)).toMat43()
        f.seek(0x40, NOESEEK_REL) # inverse matrix
        boneNameOffset = f.readUInt()
        ret = f.tell()
        f.seek(boneNameOffset + 20, NOESEEK_ABS)
        boneName = f.readString()
        f.seek(ret, NOESEEK_ABS)
        parent = f.readShort()
        f.seek(0x1A, NOESEEK_REL)
        bones.append( NoeBone(i, boneName, Mat44, None, parent) )
    f.seek(tmodOffset + 20, NOESEEK_ABS)
    modelFileNameOffset = f.readUInt()
    print (modelFileNameOffset)
    modelCount = f.readUInt()
    unknown = f.readFloat()
    unknown1 = f.readUInt()
    vertexStride = f.readUInt()
    collisionOffset2 = f.readUInt()
    meshInfoOffsetOffset = f.readUInt()
    f.seek(meshInfoOffsetOffset + 20, NOESEEK_ABS)
    meshInfoOffset = f.readUInt()
    f.seek(meshInfoOffset + 20, NOESEEK_ABS)
    unknown1Digit = f.readUInt()
    meshTableOffsetsOffset = f.readUInt()
    meshCount = f.readUInt()
    f.seek(meshTableOffsetsOffset + 20, NOESEEK_ABS)
    meshTableOffsets = []
    for i in range(0,meshCount):
        meshTableOffsets.append(f.readUInt())
    meshTables = []
    meshNames = []
    for i in range(0,meshCount):
        f.seek(meshTableOffsets[i] + 20, NOESEEK_ABS)
        meshTables.append(MeshTable(f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt()))
        f.seek(meshTables[i].meshNameOffset + 20, NOESEEK_ABS)
        meshNames.append(f.readString())
        print (meshNames[i])
    meshSubInfos = []
    for i in range(0,meshCount):
        f.seek(meshTables[i].meshSubInfoOffset + 20, NOESEEK_ABS)
        meshSubInfos.append(MeshSubInfos(f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt(), f.readUInt()))
        print (meshSubInfos[i].faceOffset)
    meshes = []
    for i in range(0,meshCount):
        posList = []
        idxList = []
        idxList2 = []
        normals = []
        uvs = []
        bidx = []
        bwgt = []
        weights = []
        colors = []
        bidx = []
        bwgt = []
        f.seek(meshSubInfos[i].faceOffset + 20, NOESEEK_ABS)
        for j in range(0,meshSubInfos[i].faceCount):
            idxList.append(f.readUShort())
        f.seek(meshSubInfos[i].normalOffset + 20, NOESEEK_ABS)
        for j in range(0,meshSubInfos[i].one):
            idxList2.append(f.readUInt())
        f.seek(meshSubInfos[i].vertexOffset + 20, NOESEEK_ABS)
        for j in range(0,meshSubInfos[i].vertexCount):
            posList.append(NoeVec3.fromBytes(f.readBytes(12)))
            normals.append(NoeVec3.fromBytes(f.readBytes(12)))
            bwgt = [f.readUByte() / 255 for j in range(4)]
            bidx = [idxList2[int((f.readUByte() / 3) % len(idxList2))] for j in range(4)]
            uvs.append(NoeVec3((f.readFloat(), f.readFloat(), 0)))
            weights.append(NoeVertWeight(bidx, bwgt))
            colors.append(NoeVec4((f.readUByte() / 255, f.readUByte() / 255, f.readUByte() / 255, f.readUByte() / 255)))
        mesh = NoeMesh(idxList, posList, meshNames[i])
        mesh.weights = weights
        mesh.normals = normals
        mesh.colors = colors
        mesh.uvs = uvs
        meshes.append(mesh)
    rapi.processCommands("-rotate 180 0 0")
    mdl = NoeModel()
    mdl.setMeshes(meshes)
    mdl.setBones(bones)
    mdlList.append(mdl)
    return 1
