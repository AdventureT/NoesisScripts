from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
    handle = noesis.register("Ed Edd Eddy mis Ed-ventures (PC) Texture", ".a2mtexture")
    noesis.setHandlerTypeCheck(handle, A2MCheckType)
    noesis.setHandlerLoadRGBA(handle, A2MLoadTexture)
    noesis.logPopup()
    return 1

def A2MCheckType(data):
    return 1

def A2MLoadTexture(data, texList):
    bs = NoeBitStream(data)
    ctx = rapi.rpgCreateContext()
    textureName = bs.readString()
    print(textureName)
    bs.seek(0x20)
    bs.seek(0x64) # unknown stuff
    unk = bs.readUInt()
    width = bs.readUInt()
    height = bs.readUInt()
    type = bs.readUInt()
    textureType = noesis.NOESISTEX_RGBA32
    bs.seek(0x84)
    
    pixeldata = bs.readBytes(width * height * 4)
    texList.append(NoeTexture(textureName ,width, height, pixeldata))
    return 1