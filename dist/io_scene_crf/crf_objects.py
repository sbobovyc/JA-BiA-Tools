from __future__ import print_function
from __future__ import division
    
import math
import struct

# Footer constants
CRF_ROOT_NODE = 0x0
CRF_MESHFILE = 0x1b4f7cc7
CRF_JOINTMAP = 0xb8fa7643
CRF_SKELETON = 0xbd9d53a3

CRF_FOOTER_ENTRY_CONSTANTS = {CRF_ROOT_NODE:"CRF_ROOT_NODE", CRF_MESHFILE:"CRF_MESHFILE", CRF_JOINTMAP:"CRF_JOINTMAP", CRF_SKELETON:"CRF_SKELETON"}

# unsupported constants
CRF_SKININFO = None
CRF_GEOMESH = None
CRF_COLLISION_SHAPE = None
CRF_OCCLUSION_SHAPE = None

# vertex layout constants
CRF_VERTEX_DECLRATION_TYPE0 = 0xc018021 # vertex positions, colors, uv, normals, specular, blendweight
CRF_VERTEX_DECLRATION_TYPE1 = 0xc # blendindices and blendweight
CRF_VERTEX_DECLRATION_TYPE2 = 0x80000 # unknown stream type
CRF_VERTEX_DECLRATION_TYPE3 = 0x8 # blendindices only

# Supported texture formats
CRF_TexFormats = ["bmp", "tga", "jpg", "dds"]

# Materials constants
CRF_Diffuse = b"sffd"
CRF_Normals = b"smrn"
CRF_Specular = b"lcps"
CRF_Custom1 = b"1tsc"
CRF_Custom2 = b"2tsc"
CRF_Custom3 = b"3tcs"
CRF_Custom4 = b"4tcs"
CRF_Custom5 = b"5tcs"
CRF_Custom6 = b"6tcs"
CRF_Custom7 = b"7tcs"
CRF_Custom8 = b"8tcs"
CRF_Custom9 = b"9tcs"
CRF_Custom10 = b"01tcs"
CRF_Custom11 = b"11cs"
CRF_Custom12 = b"21cs"

CRF_NormalLayered = "smrn1tsclcps" # MoG TangentNormalLayered
CRF_NormalLayeredMagick = 0x10004000
"""
.rdata:00507E8C aMogTangentnorm db 'MoG TangentNormalLayered',0 ; DATA XREF: sub_2B0220+7o
.rdata:00507EA5                 align 4
.rdata:00507EA8 dword_507EA8    dd 64666673h            ; DATA XREF: sub_2B0B50:loc_2B0C11r
.rdata:00507EAC                 db  73h ; s
.rdata:00507EAD                 db  6Dh ; m
.rdata:00507EAE                 db  72h ; r
.rdata:00507EAF                 db  6Eh ; n
.rdata:00507EB0                 db  31h ; 1
.rdata:00507EB1                 db  74h ; t
.rdata:00507EB2                 db  73h ; s
.rdata:00507EB3                 db  63h ; c
.rdata:00507EB4                 db  6Ch ; l
.rdata:00507EB5                 db  63h ; c
.rdata:00507EB6                 db  70h ; p
.rdata:00507EB7                 db  73h ; s
.rdata:00507EB8 dword_507EB8    dd 0                    ; DATA XREF: sub_2B0B50:loc_2B0C01r
.rdata:00507EBC                 align 10h
.rdata:00507EC0                 db    1
.rdata:00507EC1                 db    0
.rdata:00507EC2                 db    0
.rdata:00507EC3                 db    0
.rdata:00507EC4                 db    4
.rdata:00507EC5                 db    0
.rdata:00507EC6                 db    0
.rdata:00507EC7                 db    0
"""

"""
.rdata:00507EC8 aMpNormallayere db 'MP+ NormalLayered',0 ; DATA XREF: sub_2B0F60+Do
.rdata:00507EDA                 align 4
.rdata:00507EDC aSpecularRgb    db 'Specular(RGB)',0    ; DATA XREF: sub_2B0F60+19o
.rdata:00507EDC                                         ; sub_3FA770+73o
.rdata:00507EEA                 align 4
.rdata:00507EEC aSpecularA      db 'Specular(A)',0      ; DATA XREF: sub_2B0F60+40o
.rdata:00507EF8 aSelfIlluminati db 'Self-Illumination',0 ; DATA XREF: sub_2B0F60+AEo
.rdata:00507F0A                 align 4
.rdata:00507F0C aDiffuseRgbMask db 'Diffuse(RGB)Mask(A)',0 ; DATA XREF: sub_2B0F60+EAo
.rdata:00507F0C                                         ; sub_2B1F10+18o ...
.rdata:00507F20 aNormalRg       db 'Normal(RG)',0       ; DATA XREF: sub_2B0F60+13Co
.rdata:00507F20                                         ; sub_2B1F10+B9o ...
.rdata:00507F2B                 align 4
.rdata:00507F2C aOverlayRgbAlph db 'Overlay(RGB)Alpha(A)',0 ; DATA XREF: sub_2B0F60+18Bo
.rdata:00507F2C                                         ; sub_3F5DA0+99o
.rdata:00507F41                 align 4
.rdata:00507F44 aSpecularRgbAlp db 'Specular(RGB)Alpha(A)',0 ; DATA XREF: sub_2B0F60+1D6o
.rdata:00507F5A                 align 4
.rdata:00507F5C aUseOverlayLaye db 'Use overlay layer',0 ; DATA XREF: sub_2B0F60+225o
.rdata:00507F6E                 align 10h
.rdata:00507F70 aSupportsLightm db 'Supports lightmap',0 ; DATA XREF: sub_2B0F60+27Fo
.rdata:00507F70                                         ; sub_3FBF80+842o ...
.rdata:00507F82                 align 4
.rdata:00507F84 aUseSpecularMap db 'Use specular map',0 ; DATA XREF: sub_2B0F60+2D4o
.rdata:00507F95                 align 4
.rdata:00507F98 aNormalUWrap    db 'Normal U Wrap',0    ; DATA XREF: sub_2B0F60+328o
.rdata:00507F98                                         ; sub_3FED20+1B6o
.rdata:00507FA6                 align 4
.rdata:00507FA8 aX2             db 'x 2',0              ; DATA XREF: sub_2B0F60+34Ao
.rdata:00507FA8                                         ; sub_2B0F60+467o ...
.rdata:00507FAC aX4             db 'x 4',0              ; DATA XREF: sub_2B0F60+36Do
.rdata:00507FAC                                         ; sub_2B0F60+48Ao ...
.rdata:00507FB0 aX6             db 'x 6',0              ; DATA XREF: sub_2B0F60+391o
.rdata:00507FB0                                         ; sub_2B0F60+4AEo ...
.rdata:00507FB4 aX8             db 'x 8',0              ; DATA XREF: sub_2B0F60+3B5o
.rdata:00507FB4                                         ; sub_2B0F60+4D2o ...
.rdata:00507FB8 aX12            db 'x 12',0             ; DATA XREF: sub_2B0F60+3D9o
.rdata:00507FB8                                         ; sub_2B0F60+4F6o ...
.rdata:00507FBD                 align 10h
.rdata:00507FC0 aX20            db 'x 20',0             ; DATA XREF: sub_2B0F60+3FDo
.rdata:00507FC0                                         ; sub_2B0F60+51Ao ...
.rdata:00507FC5                 align 4
.rdata:00507FC8 aClamp          db 'Clamp',0            ; DATA XREF: sub_2B0F60+421o
.rdata:00507FC8                                         ; sub_2B0F60+53Eo ...
.rdata:00507FCE                 align 10h
.rdata:00507FD0 aNormalVWrap    db 'Normal V Wrap',0    ; DATA XREF: sub_2B0F60+445o
.rdata:00507FD0                                         ; sub_3FED20+2D4o
.rdata:00507FDE                 align 10h
.rdata:00507FE0 aNormalsRgAreIn db '[Normals](RG) are in tangent space.',0Ah,0
.rdata:00507FE0                                         ; DATA XREF: sub_2B0F60+56Ao
.rdata:00507FE0                                         ; sub_2B1F10+35Bo ...
.rdata:00508005                 align 4
.rdata:00508008 aTheOverlayIsBl db 'The [Overlay] is blended over with the factor of its alpha channe'
.rdata:00508008                                         ; DATA XREF: sub_2B0F60+578o
.rdata:00508008                 db 'l (optional).',0Ah,0
.rdata:00508058 aSpecularAHolds db 'Specular(A) holds self-illumination scale which multiplies with s'
.rdata:00508058                                         ; DATA XREF: sub_2B0F60+589o
.rdata:00508058                 db 'elf-illumination color (which is multiplied with diffuse color).',0Ah
.rdata:00508058                 db 0
.rdata:005080DB                 align 4
.rdata:005080DC aProvideA3rdUvS db 'Provide a 3rd UV Set to support lightmaps (optional).',0Ah,0
.rdata:005080DC                                         ; DATA XREF: sub_2B0F60+597o
.rdata:005080DC                                         ; sub_3FED20+424o
"""
CRF_TransperentEnvM = "smrnlcps" # M+ Transparent Env
CRF_TransperentEnvMMagick = 0x0000000
"""
.rdata:00518A48 aMTransparentEn db 'M+ Transparent Env',0 ; DATA XREF: sub_3FE3B0+7o
.rdata:00518A5B                 align 4
.rdata:00518A5C dword_518A5C    dd 64666673h            ; DATA XREF: sub_3FEAC0:loc_3FEB2Fr
.rdata:00518A60                 db  73h ; s
.rdata:00518A61                 db  6Dh ; m
.rdata:00518A62                 db  72h ; r
.rdata:00518A63                 db  6Eh ; n
.rdata:00518A64                 db  6Ch ; l
.rdata:00518A65                 db  63h ; c
.rdata:00518A66                 db  70h ; p
.rdata:00518A67                 db  73h ; s
.rdata:00518A68 dword_518A68    dd 0                    ; DATA XREF: sub_3FEAC0:loc_3FEB20r
.rdata:00518A6C                 db    0
.rdata:00518A6D                 db    0
.rdata:00518A6E                 db    0
.rdata:00518A6F                 db    0
.rdata:00518A70                 db    0
.rdata:00518A71                 db    0
.rdata:00518A72                 db    0
.rdata:00518A73                 db    0
"""

"""
.rdata:00518A74 aMpTransparente db 'MP+ TransparentEnv',0 ; DATA XREF: sub_3FED20+Co
.rdata:00518A87                 align 4
.rdata:00518A88 aSpecularRgbEnv db 'Specular(RGB)Env(A)',0 ; DATA XREF: sub_3FED20+B9o
.rdata:00518A9C aSupportsReflec db 'Supports reflection',0 ; DATA XREF: sub_3FED20+162o
.rdata:00518AB0 aUseDiffuseAlph db 'Use Diffuse Alpha channel to set the opacity strength.',0Ah,0
.rdata:00518AB0                                         ; DATA XREF: sub_3FED20+408o
.rdata:00518AE8 aUseSpecularAlp db 'Use Specular Alpha channel to determinate the reflection strength'
.rdata:00518AE8                                         ; DATA XREF: sub_3FED20+416o
.rdata:00518AE8                 db '.',0Ah,0
"""


# unsupported materials
CRF_Relection = "clfr"
CRF_Brightness = "snrb"
CRF_Environment = "tvne"
CRF_Emissive = "vsme"

CRF_MultiFunctional = "1tsc2tscsffd" # MoG MultiFunctional
"""
MP+ MultiFunctional
SelfIllumination
Tint Dark
Tint Bright
Tint(R)SelfIllu(G)Spec(B)
Animation(A)
Use animated illumination
Multifunctional character/item shader.
"""
"""
.rdata:00517694 aGhostly        db 'Ghostly',0          ; DATA XREF: sub_3E6100+7o
.rdata:0051769C dword_51769C    dd 63737431h            ; DATA XREF: sub_3E6A20:loc_3E6ACCr
.rdata:005176A0                 db  73h ; s
.rdata:005176A1                 db  66h ; f
.rdata:005176A2                 db  66h ; f
.rdata:005176A3                 db  64h ; d
.rdata:005176A4                 db  6Ch ; l
.rdata:005176A5                 db  63h ; c
.rdata:005176A6                 db  70h ; p
.rdata:005176A7                 db  73h ; s
.rdata:005176A8                 db  32h ; 2
.rdata:005176A9                 db  74h ; t
.rdata:005176AA                 db  73h ; s
.rdata:005176AB                 db  63h ; c
.rdata:005176AC dword_5176AC    dd 0                    ; DATA XREF: sub_3E6A20:loc_3E6ABDr
.rdata:005176B0                 db    0
.rdata:005176B1                 db    0
.rdata:005176B2                 db    0
.rdata:005176B3                 db    0
.rdata:005176B4                 db    1
.rdata:005176B5                 db    0
.rdata:005176B6                 db    0
.rdata:005176B7                 db    0
.rdata:005176B8                 db    0
.rdata:005176B9                 db    0
.rdata:005176BA                 db    0
.rdata:005176BB                 db    0
.rdata:005176BC dword_5176BC    dd 64666673h            ; DATA XREF: sub_3E6A20:loc_3E6B50r
.rdata:005176BC                                         ; sub_3FDEE0:loc_3FDF40r
.rdata:005176C0                 db  6Ch ; l
.rdata:005176C1                 db  63h ; c
.rdata:005176C2                 db  70h ; p
.rdata:005176C3                 db  73h ; s
.rdata:005176C4                 db  31h ; 1
.rdata:005176C5                 db  74h ; t
.rdata:005176C6                 db  73h ; s
.rdata:005176C7                 db  63h ; c
.rdata:005176C8 aMpGhostly      db 'MP+ Ghostly',0      ; DATA XREF: sub_3E6EB0+Do
.rdata:005176D4 aLayeraRgba     db 'LayerA(RGBA)',0     ; DATA XREF: sub_3E6EB0+19o
.rdata:005176E1                 align 4
.rdata:005176E4 aLayerbRgba     db 'LayerB(RGBA)',0     ; DATA XREF: sub_3E6EB0+7Ao
.rdata:005176F1                 align 4
.rdata:005176F4 aDepthgradientR db 'DepthGradient(RGBA)',0 ; DATA XREF: sub_3E6EB0+C8o
.rdata:00517708 aVelvetgradient db 'VelvetGradient(RGBA)',0 ; DATA XREF: sub_3E6EB0+116o
.rdata:0051771D                 align 10h
.rdata:00517720 aDepthColor     db 'Depth Color',0      ; DATA XREF: sub_3E6EB0+164o
.rdata:0051772C aLayerColor     db 'Layer Color',0      ; DATA XREF: sub_3E6EB0+18Bo
.rdata:00517738 aVelvetColor    db 'Velvet Color',0     ; DATA XREF: sub_3E6EB0+1B2o
.rdata:00517745                 align 4
.rdata:00517748 aDepthStrength  db 'Depth Strength',0   ; DATA XREF: sub_3E6EB0+1D9o
.rdata:00517757                 align 4
.rdata:00517758 aDepthRange     db 'Depth Range',0      ; DATA XREF: sub_3E6EB0+247o
.rdata:00517764 aLayerStrength  db 'Layer Strength',0   ; DATA XREF: sub_3E6EB0+2BAo
.rdata:00517773                 align 4
.rdata:00517774 aVelvetStrength db 'Velvet Strength',0  ; DATA XREF: sub_3E6EB0+325o
.rdata:00517784 aLayeraUvScale  db 'LayerA UV Scale',0  ; DATA XREF: sub_3E6EB0+390o
.rdata:00517794 aLayerbUvScale  db 'LayerB UV Scale',0  ; DATA XREF: sub_3E6EB0+403o
.rdata:005177A4 aBlendMode      db 'Blend Mode',0       ; DATA XREF: sub_3E6EB0+476o
.rdata:005177A4                                         ; sub_3F65E0+F7o
.rdata:005177AF                 align 10h
.rdata:005177B0 aAdd            db 'Add',0              ; DATA XREF: sub_3E6EB0+498o
.rdata:005177B0                                         ; sub_3F65E0+13Ao
.rdata:005177B4 aSubtract       db 'Subtract',0         ; DATA XREF: sub_3E6EB0+4BBo
.rdata:005177BD                 align 10h
.rdata:005177C0 aBlend          db 'Blend',0            ; DATA XREF: sub_3E6EB0+4DFo
.rdata:005177C0                                         ; sub_3FF7D0+77o ...
.rdata:005177C6                 align 4
.rdata:005177C8 aSolid          db 'Solid',0            ; DATA XREF: sub_3E6EB0+503o
.rdata:005177CE                 align 10h
.rdata:005177D0 aUseLayerb      db 'Use LayerB',0       ; DATA XREF: sub_3E6EB0+527o
.rdata:005177DB                 align 4
.rdata:005177DC aScaleLayeraToS db 'Scale LayerA to Screen',0 ; DATA XREF: sub_3E6EB0+57Fo
.rdata:005177F3                 align 4
.rdata:005177F4 aScaleLayerbToS db 'Scale LayerB to Screen',0 ; DATA XREF: sub_3E6EB0+5D1o
.rdata:0051780B                 align 4
.rdata:0051780C aCompareZEqual  db 'Compare Z Equal',0  ; DATA XREF: sub_3E6EB0+623o
.rdata:0051781C aLayerbIsOption db '[LayerB] is optional. All colors are optional.',0Ah,0
"""

CRF_SkinLayeredM = "lcpssmrn1tsc2tsc" #M+ SkinLayered
CRF_SkinLayeredMMagick = 0x10002000
"""
.rdata:00508150 aMSkinlayered   db 'M+ SkinLayered',0   ; DATA XREF: sub_2B1610+7o
.rdata:0050815F                 align 10h
.rdata:00508160 ; int dword_508160[]
.rdata:00508160 dword_508160    dd 64666673h            ; DATA XREF: sub_2B1B10:loc_2B1B7Fr
.rdata:00508164                 db  6Ch ; l
.rdata:00508165                 db  63h ; c
.rdata:00508166                 db  70h ; p
.rdata:00508167                 db  73h ; s
.rdata:00508168                 db  73h ; s
.rdata:00508169                 db  6Dh ; m
.rdata:0050816A                 db  72h ; r
.rdata:0050816B                 db  6Eh ; n
.rdata:0050816C                 db  31h ; 1
.rdata:0050816D                 db  74h ; t
.rdata:0050816E                 db  73h ; s
.rdata:0050816F                 db  63h ; c
.rdata:00508170                 db  32h ; 2
.rdata:00508171                 db  74h ; t
.rdata:00508172                 db  73h ; s
.rdata:00508173                 db  63h ; c
.rdata:00508174 ; int dword_508174[]
.rdata:00508174 dword_508174    dd 0                    ; DATA XREF: sub_2B1B10:loc_2B1B70r
.rdata:00508178                 align 10h
.rdata:00508180                 db    1
.rdata:00508181                 db    0
.rdata:00508182                 db    0
.rdata:00508183                 db    0
.rdata:00508184                 db    2
.rdata:00508185                 db    0
.rdata:00508186                 db    0
.rdata:00508187                 db    0
"""
CRF_SkinLayeredMP = "6tsc5tsc" #MP+ SkinLayered
"""
.rdata:00508188 dword_508188    dd 63737437h            ; DATA XREF: sub_2B1B10:loc_2B1C05r
.rdata:0050818C                 db  36h ; 6
.rdata:0050818D                 db  74h ; t
.rdata:0050818E                 db  73h ; s
.rdata:0050818F                 db  63h ; c
.rdata:00508190                 db  35h ; 5
.rdata:00508191                 db  74h ; t
.rdata:00508192                 db  73h ; s
.rdata:00508193                 db  63h ; c
.rdata:00508194 aMpSkinlayered  db 'MP+ SkinLayered',0  ; DATA XREF: sub_2B1F10+Co
.rdata:005081A4 aTranslucencyRS db 'Translucency(R)Spec(G)',0 ; DATA XREF: sub_2B1F10+6Ao
.rdata:005081BB                 align 4
.rdata:005081BC aOverlayaRgba   db 'OverlayA(RGBA)',0   ; DATA XREF: sub_2B1F10+108o
.rdata:005081CB                 align 4
.rdata:005081CC aOverlaybRgba   db 'OverlayB(RGBA)',0   ; DATA XREF: sub_2B1F10+157o
.rdata:005081DB                 align 4
.rdata:005081DC aTranslucencyNe db 'Translucency Neutral',0 ; DATA XREF: sub_2B1F10+1A6o
.rdata:005081F1                 align 4
.rdata:005081F4 aTranslucencyMe db 'Translucency Melanin',0 ; DATA XREF: sub_2B1F10+1FBo
.rdata:00508209                 align 4
.rdata:0050820C aTranslucencyHe db 'Translucency Hemoglobin',0 ; DATA XREF: sub_2B1F10+250o
.rdata:00508224 aUseOverlayA    db 'Use overlay A',0    ; DATA XREF: sub_2B1F10+2A5o
.rdata:00508232                 align 4
.rdata:00508234 aUseOverlayB    db 'Use overlay B',0    ; DATA XREF: sub_2B1F10+2FFo
.rdata:00508242                 align 8
.rdata:00508248 aOverlayaOverla db 'OverlayA + OverlayB use the UV Channel ',27h,'overlay',27h,' (map#2).',0Ah
.rdata:00508248                                         ; DATA XREF: sub_2B1F10+369o
.rdata:00508248                 db 'Both overlays are blended over with the factor of its alpha chann'
.rdata:00508248                 db 'el.',0Ah,0
"""

def float2uint32(number):
    return int(number * 4294967295)    # 2^32 - 1

def uint2float(uint_number):
    return uint_number / 4294967295.

def ubyte2float(ubyte_number):
    return ubyte_number / 255.0

def byte2float(int_number, old_way=False):
    if old_way:
        if int_number > 128:
            return float(int_number / 128.0) - 1
        elif int_number < 128:
            return float(-(128.0 - int_number) / 128.0)
        else:
            return 0.0
    else:    
        return (int_number/127.5) - 1.0
    
def float2uint(f_number, old_way=False):
    if old_way:
        if f_number <= 0:
            return int((f_number+1.0)/2.0 * 255.0 + 1)
        else:
            return int((f_number+1.0)/2.0 * 256.0 - 1)
    else:
        return int(math.floor((f_number + 1.0)*127.5))

class CRF_object(object):
    def __init__(self):
        self.header = CRF_header()
        self.footer = CRF_footer()
        self.meshfile = CRF_meshfile()
        self.jointmap = None
        self.skeleton = None
        
    def parse_bin(self, file, verbose=False):        
        self.header.parse_bin(file)        
        self.footer.parse_bin(file, self.header.footer_offset1, self.header.footer_offset2, self.header.footer_entries)        
        self.meshfile.parse_bin(file, self.footer.get_meshfile().file_offset, verbose=verbose)
        
        if(self.footer.get_jointmap() != None):
            self.jointmap = CRF_jointmap(file, self.footer.get_jointmap().file_offset)

        if(self.footer.get_skeleton() != None):
            self.skeleton = CRF_skeleton(file, self.footer.get_skeleton().file_offset)
            
    def get_bin(self):
        data = b""
        #TODO update all data structures, then write them out
        mesh_data = self.meshfile.get_bin()
        joint_data = None
        if self.jointmap != None:
            joint_data = self.jointmap.get_bin()
        
        meshfile_size = len(mesh_data)
        footer1_size = len(self.footer.entries * 32)
        self.footer.update_meshfile(meshfile_size)
        self.header.footer_offset1 = 0x14 + meshfile_size 
        self.header.footer_offset2 = 0x14 + meshfile_size + footer1_size
        data += self.header.get_bin()
        data += mesh_data
        if joint_data != None:
            data += joint_data
        data += self.footer.get_bin()
        return data
    
class CRF_header(object):
    def __init__(self):
        self.crf_magick = b"fknc"
        self.version = 1
        self.footer_offset1 = 0
        self.footer_offset2 = 0
        self.footer_entries = 2 #TODO This only supports static objects. For animated objects, more complex footer has to be supported.
		
    def parse_bin(self,file):
        print("===Parsing header===")
        self.crf_magick, self.version = struct.unpack("<4sI", file.read(8))    
        if self.crf_magick != b"fknc":
            print("Not a CRF file!")
            return 
        self.footer_offset1,self.footer_offset2 = struct.unpack("<II", file.read(8))
        self.footer_entries, = struct.unpack("<I", file.read(4))
        print("Footer offset 1: %s, footer offset 2: %s" % (hex(self.footer_offset1).strip('L'), hex(self.footer_offset2).strip('L')))
        print("Footer entries", self.footer_entries)
        print("===End of parsing header===")
        
    def get_bin(self):
        data = b""
        data += self.crf_magick
        data += struct.pack("<I", self.version)
        # footer offsets are blank and will get filled in later
        data += struct.pack("<I", self.footer_offset1)
        data += struct.pack("<I", self.footer_offset2)
        data += struct.pack("<I", self.footer_entries)     
        return data
        
class CRF_footer(object):
    def __init__(self):
        self.entries = []
        self.entry_descriptors = []

    def parse_bin(self, file, footer_offset1, footer_offset2, footer_entries): 
        print("===Parsing footer===")
        file.seek(footer_offset1)
        for i in range(0, footer_entries):
            entry = CRF_entry()            
            entry.parse_bin(file)
            self.entries.append(entry)
                
        for entry in self.entries:
            entry_description = CRF_entry_descriptor()
            entry_description.parse_bin(file, entry.type)
            self.entry_descriptors.append(entry_description)
        print("===End of parsing footer===")

    def get_meshfile(self):
        for entry in self.entries:
            if entry.type == CRF_MESHFILE:
                return entry
        return None

    def get_jointmap(self):
        for entry in self.entries:
            if entry.type == CRF_JOINTMAP:
                return entry
        return None

    def get_skeleton(self):
        for entry in self.entries:
            if entry.type == CRF_SKELETON:
                return entry
        return None
    
    def update_meshfile(self, new_size):
        for i in range(0, len(self.entries)):
            entry = self.entries[i]
            if entry.type == CRF_MESHFILE:
                self.entries[i].size = new_size 

    def get_bin(self):
        data = b""
        for entry in self.entries:
            data += entry.get_bin()
        for entry in self.entry_descriptors:
            data += entry.get_bin()
        return data
        
class CRF_entry(object):
    def __init__(self):
        self.type = None
        self.entry_id = None
        self.file_offset = None
        self.size = None
        self.const = None #(a, b, c, d) unknown
        
    def parse_bin(self, file):
        self.type, self.entry_id, self.file_offset, self.size = struct.unpack("<IIII", file.read(16))
        print("Type: %s (%s) \n Entry: %s \n File offset: %s \n Size: %s" % (CRF_FOOTER_ENTRY_CONSTANTS[self.type], hex(self.type), self.entry_id, hex(self.file_offset), self.size) )
        self.const = struct.unpack("<IIII", file.read(16))
        print(" Unknown constants:", self.const)
        
    def create_rootnode(self):        
        self.type = CRF_ROOT_NODE
        self.entry_id = 0
        self.file_offset = 0
        self.size = 0
        self.const = (0xFFFFFFFF, 1, 1, 0)

    def create_meshfile(self, size):        
        self.type = CRF_MESHFILE
        self.entry_id = 1
        self.file_offset = 0x14
        self.size = size
        self.const = (0, 0, 0, 0)
        
    def get_bin(self):
        data = b""
        data = struct.pack("<IIIIIIII", self.type, self.entry_id, self.file_offset, self.size, *self.const)
        return data
        
class CRF_entry_descriptor(object):        
    def __init__(self):
        self.type = None
        self.entry_id = None
        self.name_length = None
        self.name = None

    def create_rootnode(self):
        self.type = CRF_ROOT_NODE
        self.entry_id = 0
        self.name_length = 9
        self.name = b"root node"
        
    def create_meshfile(self):
        self.type = CRF_MESHFILE
        self.entry_id = 1
        self.name_length = 8
        self.name = b"meshfile"
        
    def parse_bin(self, file, CRF_TYPE):
        self.type = CRF_TYPE
        if(self.type == CRF_ROOT_NODE):
            file.read(4)
            self.entry_id, = struct.unpack("<I", file.read(4))            
            self.name_length, = struct.unpack("<I", file.read(4))
            self.name, = struct.unpack("%ss" % self.name_length, file.read(self.name_length))
        if(self.type == CRF_MESHFILE or self.type == CRF_JOINTMAP or self.type == CRF_SKELETON):             
            self.entry_id, = struct.unpack("<I", file.read(4))            
            self.name_length, = struct.unpack("<I", file.read(4))
            self.name, = struct.unpack("%ss" % self.name_length, file.read(self.name_length))
            file.read(4)
        print("Entry id: %i, entry name: %s, entry type: %s" %(self.entry_id, self.name, CRF_FOOTER_ENTRY_CONSTANTS[self.type]))

    def get_bin(self):
        if(self.type == CRF_ROOT_NODE):
            data = struct.pack("<xxxxII%ss" % self.name_length, self.entry_id, self.name_length, self.name)
        if(self.type == CRF_MESHFILE or self.type == CRF_JOINTMAP or self.type == CRF_SKELETON):
            data = struct.pack("<II%ssxxxx" % self.name_length, self.entry_id, self.name_length, self.name)
        return data

class CRF_meshfile(object):
    def __init__(self):
        self.num_meshes = None
        self.model_bounding_box = None # ((LoX, LoY, LoZ), (HiX, HiY, HZ))
        self.meshes = []

    def parse_bin(self, file, file_offset, verbose=False):
        print("===Parsing meshfile===")
        file.seek(file_offset)
        magick, self.num_meshes = struct.unpack("<II", file.read(8))
        LoX, LoY, LoZ = struct.unpack("<fff", file.read(12)) #bounding box       
        HiX, HiY, HiZ = struct.unpack("<fff", file.read(12)) #bounding box
        self.model_bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))
        print("Number of meshes:", self.num_meshes)        
        print("Bounding box of entire model: ", self.model_bounding_box)

        for i in range(0, self.num_meshes):
            mesh = CRF_mesh()
            mesh.parse_bin(file, file.tell(), i, verbose)
            self.meshes.append(mesh)

        print("===End of parsing meshfile===")

    def scale(self, scale_factor):
        #TODO need to scale the bounding box
        for mesh in self.meshes:
            for i in range(0, len(mesh.vertices0)):
                mesh.vertices0[i].x = mesh.vertices0[i].x*scale_factor
                mesh.vertices0[i].y = mesh.vertices0[i].y*scale_factor
                mesh.vertices0[i].z = mesh.vertices0[i].z*scale_factor                

    def translate(self, translation):
        x_offset, y_offset, z_offset = translation
        #TODO need to translate the bounding box
        for mesh in self.meshes:
            for i in range(0, len(mesh.vertices0)):
                mesh.vertices0[i].x = mesh.vertices0[i].x+x_offset
                mesh.vertices0[i].y = mesh.vertices0[i].y+y_offset
                mesh.vertices0[i].z = mesh.vertices0[i].z+z_offset

    def __str__(self):
        string = ""
        string += "Number of meshes: %s\n" % self.num_meshes
        string += "Model bounding box: (%s, %s)\n" % (self.model_bounding_box[0], self.model_bounding_box[1])
        for mesh in self.meshes:
            string += mesh.__str__()
        return string

        
    def get_bin(self):
        data = b""
        # some unknown magick number
        data += struct.pack("<I", 0xFFFF0006)        
        data += struct.pack("<I", self.num_meshes)
        LoXYZ = self.model_bounding_box[0]
        HiXYZ = self.model_bounding_box[1]
        data += struct.pack("<fff", *list(LoXYZ))
        data += struct.pack("<fff", *list(HiXYZ))
        # loop through all meshes
        for mesh in self.meshes:
            data += mesh.get_bin()
            print("Writing mesh", mesh.mesh_number)
            # write separator, unknown format
            if self.num_meshes > 1:
                data += struct.pack("<I%sx" % 0x10, 2)
        return data

class CRF_mesh(object):
    def __init__(self):
        self.mesh_number = 0
        self.number_of_vertices = None
        self.number_of_faces = None
        self.face_list = []
        self.stream_count = 0
        self.vertex_stream0_layout = [] # [layout, stride]
        self.vertices0 = [] # vertex positions, colors, uv, normals, specular, blendweight
        self.vertex_stream1_layout = [] # [layout, stride]        
        self.vertices1 = [] # blendindices and blendweight
        self.vertex_stream2_layout = [] # [layout, stride]             
        self.vertices2 = [] # unknown stream, used on animated meshes
        self.vertex_blendindices_only = []
        self.bounding_box = None # ((LoX, LoY, LoZ), (HiX, HiY, HZ))
        self.materials = None

    def parse_bin(self, file, file_offset, mesh_number, verbose=False):
        self.mesh_number = mesh_number
        print("Mesh %i, face/vertex list at %s" % (self.mesh_number, hex(file.tell()).strip('L')))
        self.number_of_vertices, = struct.unpack("<I", file.read(4))
        self.number_of_faces, = struct.unpack("<I", file.read(4))
        print("Model vertices: %i, faces: %i" % (self.number_of_vertices, self.number_of_faces))
        
        # read in face/vertex index list
        for i in range(0, self.number_of_faces):
                v1, v2, v3 = struct.unpack("<HHH", file.read(6))
                face_vert_loc_indices = [v1, v2, v3]
                face_vert_tex_indices = [v1, v2, v3]
                self.face_list.append((v1, v2, v3))
                if verbose:
                    print("face index %s, verts (%s, %s, %s)" % (i, v1, v2, v3))

        print("Vertex information starts at", hex(file.tell()).strip('L'))                
        self.stream_count, = struct.unpack("<B", file.read(1))
        print("Number of streams:", self.stream_count)
        for stream in range(0, self.stream_count):
        # then the vertex declaration
            layout, stride = struct.unpack("<II", file.read(8))
            print("Stream%i declaration: %s, stride: %i bytes" % (stream, hex(layout).strip('L'), stride))
            if layout == CRF_VERTEX_DECLRATION_TYPE0:
                print("Vertex stream at", hex(file.tell()).strip('L'))
                # read in vertices, vertex normals, ks, and UVs
                for i in range(0, self.number_of_vertices):
                    vertex = CRF_vertex()
                    vertex.bin2raw(file, file.tell(), i)
                    vertex.raw2blend()
                    self.vertices0.append(vertex)
                    if verbose:
                        print(vertex)
                self.vertex_stream0_layout = [layout, stride]
            
            elif layout == CRF_VERTEX_DECLRATION_TYPE1:
                print("Blendweight/blendindex stream at", hex(file.tell()).strip('L'))
                for i in range(0, self.number_of_vertices):
                    vertex_blend = CRF_vertex_blend()
                    vertex_blend.bin2raw(file, file.tell(), i, verbose=verbose)
                    self.vertices1.append(vertex_blend)
                self.vertex_stream1_layout = [layout, stride]
            elif layout == CRF_VERTEX_DECLRATION_TYPE2:
                print("Unknown stream at", hex(file.tell()).strip('L'))
                for i in range(0, self.number_of_vertices):
                    vertex_blend = CRF_vertex_unknown()
                    vertex_blend.bin2raw(file, file.tell(), i, verbose=verbose)
                    self.vertices2.append(vertex_blend)
                self.vertex_stream2_layout = [layout, stride]
            elif layout == CRF_VERTEX_DECLRATION_TYPE3:
                print("Blendindices stream at", hex(file.tell()).strip('L'))
                for i in range(0, self.number_of_vertices):
                    vertex_blend = CRF_vertex_blend_indices_only()
                    vertex_blend.bin2raw(file, file.tell(), i, verbose=verbose)
                    self.vertex_blendindices_only.append(vertex_blend)                               
        print("End of vertex data at", hex(file.tell()).strip('L'))

        #read in mesh bounding box
        LoX, LoY, LoZ = struct.unpack("<fff", file.read(12)) #bounding box       
        HiX, HiY, HiZ = struct.unpack("<fff", file.read(12)) #bounding box
        self.bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))        
        print("Bounding box of model %i: %s" % (self.mesh_number, self.bounding_box))

        #material info comes next
        print("==Parsing meshfile materials==")
        self.materials = CRF_materials()
        self.materials.parse_bin(file, file.tell(), verbose)
        print("==End of parsing meshfile materials==")

    def __str__(self):
        string = ""
        string += "Mesh number: %s, vertices = %s, faces = %s\n" % (self.mesh_number, self.number_of_vertices, self.number_of_faces)
        return string
        
    def get_bin(self):
        data = b""
        data += struct.pack("<I", self.number_of_vertices)
        data += struct.pack("<I", self.number_of_faces)
        for face in self.face_list:
            data += struct.pack("<HHH", *list(face))
        data += struct.pack("<B", self.stream_count)
        
        # write first stream
        if len(self.vertex_stream0_layout) != 0:
            data += struct.pack("<II", *self.vertex_stream0_layout)
            for vertex in self.vertices0:
                #TODO should convert blender to raw here
                data += vertex.get_bin()
            
        # write second stream
        if len(self.vertex_stream1_layout) != 0:
            data += struct.pack("<II", *self.vertex_stream1_layout)
            for vertex in self.vertices1:
                #TODO should convert blender to raw here
                data += vertex.get_bin()

        # write third stream
        if len(self.vertex_stream2_layout) != 0:        
            data += struct.pack("<II", *self.vertex_stream2_layout)
            for vertex in self.vertices2:
                #TODO should convert blender to raw here
                data += vertex.get_bin()

        # write mesh's bounding box
        LoXYZ = self.bounding_box[0]
        HiXYZ = self.bounding_box[1]
        data += struct.pack("<fff", *list(LoXYZ))
        data += struct.pack("<fff", *list(HiXYZ))

        # write materials
        if self.materials != None:
            data += self.materials.get_bin()
        
        return data
    
class CRF_materials(object):
    def __init__(self):
        self.material_type = b''
        self.material_subtype = b''
        self.diffuse_texture = b''
        self.normal_texture = b''
        self.specular_texture = b''
        self.specular_constant = (0.0, 0.0, 0.0) # (R, G, B)
        self.specular_constant_alpha = 0.0 #TODO not sure if this is right
        self.overlay_texture = b''
        self.unknown_texture = b''        
        self.custom_data_count = 0
        self.custom1_1 = (0, 0, 0)
        self.custom1_2 = 0
        self.custom_array = [(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0)] #TODO change into a map or an object

    def parse_bin(self, file, file_offset, verbose=False):
        print("Materials at:", hex(file.tell()).strip('L'))
        self.material_type, = struct.unpack("2s", file.read(2))
        print("Material type:", self.material_type)
        self.material_subtype, = struct.unpack(">Q", file.read(8))
        print("Material subtype:", hex(self.material_subtype))

        reading_materials = True
        current_state = "start"

        if self.material_type == b"nm" or self.material_type == b"tm" or self.material_type == b"ts":
            while(reading_materials):
                # state transition logic
                if current_state == "start":
                    current_state = "read_diffuse"
                elif current_state == "read_diffuse":
                    if self.material_type == b"ts":
                        current_state = "read_specular"
                    else:
                        current_state = "read_normal"                    
                elif current_state == "read_normal":
                    if self.material_type == b"tm":
                        current_state = "read_specular"
                    else:
                        current_state = "read_overlay"
                elif current_state == "read_overlay":
                    if self.material_subtype == 0x100000003000000 or self.material_type == b"ts":
                        if self.material_type == b"ts":
                            current_state = "read_unknown_texture"
                        else:
                            self.custom_data_count, = struct.unpack("<I", file.read(4))
                            print("Custom data count", self.custom_data_count)                            
                            current_state = "read_specular_const"
                    elif self.material_subtype == 0x100000004000000:
                        current_state = "read_specular"
                elif current_state == "read_specular":
                    if self.material_type == b"tm":
                        # read in unknown
                        file.read(0x1C)
                        current_state = "done"
                    elif self.material_type == b"ts":
                        current_state = "read_normal"
                    else:
                        self.custom_data_count, = struct.unpack("<I", file.read(4))
                        print("Custom data count", self.custom_data_count)
                        current_state = "read_specular_const"
                elif current_state == "read_specular_const":
                    if self.material_subtype == 0x100000003000000:
                        # read in unknown
                        file.read(0x14)
                        current_state = "done"
                    elif self.material_subtype == 0x100000004000000:                        
                        current_state = "read_custom"
                elif current_state == "read_unknown_texture":
                    self.custom_data_count, = struct.unpack("<I", file.read(4))
                    print("Custom data count", self.custom_data_count)
                    current_state = "read_custom"
                elif current_state == "read_custom":
                    import binascii                    
                    # read in unknown                    
                    if self.material_type == b"ts":
                        trailer = file.read(0x10)
                        print(binascii.hexlify(trailer))
                    else:
                        trailer = file.read(0x14)
                        print(binascii.hexlify(trailer))
                    current_state = "done"
                elif current_state == "done":
                    reading_materials = False

                        
                print("Current state =", current_state)
                # state logic
                if current_state == "read_diffuse":
                    # read diffuse texture
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    if(data_type == CRF_Diffuse):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print("Texture:", texture)
                        self.diffuse_texture = texture
                        # read in some 0s
                        file.read(4)
                    else:
                        print("Error reading diffuse texture")
                        reading_materials = False                    
                elif current_state == "read_normal":
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    if(data_type == CRF_Normals):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print("Texture:", texture)
                        self.normal_texture = texture
                        # read in some 0s
                        file.read(4)
                    else:
                        print("Error reading normal texture")
                        reading_materials = False
                elif current_state == "read_overlay":
                    # read overlay
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    if(data_type == CRF_Custom1):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print("Texture:", texture)
                        self.overlay_texture = texture
                        # read in some 0s
                        file.read(4)
                    else:
                        print("Error reading overlay reference")
                        reading_materials = False
                elif current_state == "read_specular":
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    if(data_type == CRF_Specular):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print("Texture:", texture)
                        self.specular_texture = texture
                        # read in some 0s
                        file.read(4)
                    else:
                        print("Error reading specular texture")
                        reading_materials = False                    
                elif current_state == "read_specular_const":
                    # read specular constant
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    R,G,B = struct.unpack("<fff", file.read(12))                    
                    print(R,G,B)
                    self.specular_constant = (R, G, B)                    
                    if self.custom_data_count == 1:
                        A, = struct.unpack("f", file.read(4))
                        print(A)
                        self.specular_constant_alpha = A
                elif current_state == "read_unknown_texture":
                    data_type, = struct.unpack("4s", file.read(4))
                    print("Type:", data_type)
                    if(data_type == CRF_Custom2):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print("Texture:", texture)
                        self.unknown_texture = texture
                        # read in some 0s
                        file.read(4)
                    else:
                        print("Error reading unknown texture")
                        reading_materials = False                    
                elif current_state == "read_custom":
                    if self.material_type == b"ts":
                        for i in range(0, self.custom_data_count):
                            data_type, = struct.unpack("4s", file.read(4))
                            print("Type:", data_type)                            
                            unknown = struct.unpack("<III", file.read(12))
                            print(unknown)
                            self.custom_array.append(unknown)                         
                    elif self.custom_data_count == 2:
                        data_type, = struct.unpack("4s", file.read(4))
                        print("Type:", data_type)
                        self.custom1_1 = struct.unpack("<IIII", file.read(16))
                        print("custom1_1 =",self.custom1_1)
                        data_type, = struct.unpack("4s", file.read(4))
                        print("Type:", data_type)
                        self.custom1_2, = struct.unpack("<I", file.read(4))
                        print("custom1_2 =",self.custom1_2)                        
        else:
            print("Material type is not supported")
        print("Materials end at:", hex(file.tell()).strip('L'))

    def get_bin(self):
        data = b""
        writing_materials = True
        current_state = "start"

        while(writing_materials):
            if self.material_type == b"nm":
                if current_state == "start":
                    data += struct.pack("2s", self.material_type)
                    data += struct.pack(">Q", self.material_subtype)
                    current_state = "write_diffuse"
                elif current_state == "write_diffuse":
                    current_state = "write_normal"
                elif current_state == "write_normal":
                        current_state = "write_overlay"
                elif current_state == "write_overlay":
                    if self.material_subtype == 0x100000003000000:
                        current_state = "write_specular_constant"
                    else:                    
                        current_state = "write_specular"
                elif current_state == "write_specular":
                    current_state = "write_specular_constant"
                elif current_state == "write_specular_constant":
                    if self.material_subtype == 0x100000003000000:
                        current_state = "done"
                    else:
                        current_state = "write_custom"
                elif current_state == "write_custom":
                    current_state = "done"
                elif current_state == "done":
                    writing_materials = False
                    
                print(current_state)
                if current_state == "write_diffuse":                
                    data += struct.pack("4s", b"sffd")
                    data += struct.pack("<I", len(self.diffuse_texture))            
                    data += struct.pack("%ss" % len(self.diffuse_texture), self.diffuse_texture)
                    data += struct.pack("xxxx")
                elif current_state == "write_normal":            
                    data += struct.pack("4s", b"smrn")
                    data += struct.pack("<I", len(self.normal_texture))            
                    data += struct.pack("%ss" % len(self.normal_texture), self.normal_texture)
                    data += struct.pack("xxxx")
                elif current_state == "write_overlay":
                    data += struct.pack("4s", b"1tsc")
                    data += struct.pack("<I", len(self.overlay_texture))            
                    data += struct.pack("%ss" % len(self.overlay_texture), self.overlay_texture)
                    data += struct.pack("xxxx")
                elif current_state == "write_specular":
                    data += struct.pack("4s", b"lcps")
                    data += struct.pack("<I", len(self.specular_texture))            
                    data += struct.pack("%ss" % len(self.specular_texture), self.specular_texture)
                    data += struct.pack("xxxx")                    
                elif current_state == "write_specular_constant":
                    if self.custom_data_count == 1:
                        data += struct.pack("<I", 0x1)
                        data += struct.pack("4s", b"lcps")
                        data += struct.pack("<fff", *list(self.specular_constant))
                        data += struct.pack("<f", self.specular_constant_alpha)
                    elif self.custom_data_count == 2:
                        data += struct.pack("<I", 0x2)
                        data += struct.pack("4s", b"lcps")
                        data += struct.pack("<fff", *list(self.specular_constant))
                elif current_state == "write_custom":
                    if self.custom_data_count == 2:
                        data += struct.pack("4s", b"1tsc")
                        data += struct.pack("<IIII", *list(self.custom1_1))
                        data += struct.pack("4s", b"1tsc")
                        data += struct.pack("<I", self.custom1_2)                                                                    
        return data
        
class CRF_vertex_blend(object):
    def __init__(self):
        self.index = 0
        self.blendweights = (0, 0, 0, 0)
        self.blendindices = (0, 0, 0, 0) # This refers to index in CRF_skeleton.skeleton_list, not the bone directly      
        self.blendweights_blend = (0, 0, 0, 0)
        
    def raw2blend(self):
        self.blendweights_blend = (ubyte2float(self.blendweights[0]), ubyte2float(self.blendweights[1]), ubyte2float(self.blendweights[2]), ubyte2float(self.blendweights[3]))
        
    def bin2raw(self, file, file_offset, index, verbose=False):
        self.index = index
        self.blendweights = struct.unpack("<BBBB", file.read(4))
        self.blendindices = struct.unpack("<BBBB", file.read(4))
        if verbose:
            print("vert index=%s, blendweights: %s, blendindices: %s" % (self.index, self.blendweights, self.blendindices))

    def get_bin(self):
        data = b""
        data += struct.pack("<BBBB", *self.blendweights)
        data += struct.pack("<BBBB", *self.blendindices)
        return data
                                
class CRF_vertex_blend_indices_only(object):
    def bin2raw(self, file, file_offset, index, verbose=False):
        self.index = index
        self.blendindices = struct.unpack("<bbbb", file.read(4))
        if verbose:
            print("vert index=%s, blendindices: %s" % (self.index, self.blendindices))
            
    def get_bin(self):
        data = b""
        data += struct.pack("<bbbb", *self.blendindices)
        return data

class CRF_vertex_unknown(object):
    def __init__(self):
        self.index = 0
        self.unknown = (0, 0)
            
    def bin2raw(self, file, file_offset, index, verbose=False):
        self.index = index
        self.unknown = struct.unpack("<ff", file.read(8))
        if verbose:
            print("vert index=%s, unknown: %s" % (self.index, self.unknown))

    def get_bin(self):
        data = b""
        data += struct.pack("<ff", *self.unknown)
        return data    
    
class CRF_vertex(object):
    def __init__(self):
        self.index = 0
        
        # Raw CRF variables:
        self.x = 0
        self.y = 0
        self.z = 0
        self.normal_x = 0
        self.normal_y = 0
        self.normal_z = 0
        self.normal_w = 0
        self.tangent_x = 0
        self.tangent_y = 0
        self.tangent_z = 0
        self.tangent_w = 0
        self.u0 = 0
        self.v0 = 0
        self.u1 = 0
        self.v1 = 0
        self.blendweights1_x = 0
        self.blendweights1_y = 0
        self.blendweights1_z = 0
        self.blendweights1_w = 0

        # Blender variables
        self.x_blend = 0
        self.y_blend = 0
        self.z_blend = 0
        self.normal_x_blend = 0
        self.normal_y_blend = 0
        self.normal_z_blend = 0
        self.normal_w_blend = 0
        self.tangent_x_blend = 0
        self.tangent_y_blend = 0
        self.tangent_z_blend = 0
        self.tangent_w_blend = 0 #Not iplemented      
        self.u0_blend = 0
        self.v0_blend = 0
        self.u1_blend = 0
        self.v1_blend = 0
        self.blendweights1_blend = 0
        self.blendweights1_x_blend = 0
        self.blendweights1_y_blend = 0
        self.blendweights1_z_blend = 0
        self.blendweights1_w_blend = 0

            
    
    def __str__(self):
        string = "Vertex index = %s\n" % (self.index)
        string += "Blender values:\n"
        string += "xyz = %f %f %f\n" % (self.x_blend, self.y_blend, self.z_blend)
        string += "\tvertex normal XYZW  = %f %f %f %f\n" % (self.normal_x_blend, self.normal_y_blend, self.normal_z_blend, self.normal_w_blend)
        #string += "\tvertex normal length = %s\n" % (math.sqrt(self.normal_x_blend*self.normal_x_blend + self.normal_y_blend*self.normal_y_blend + self.normal_z_blend*self.normal_z_blend))
        string += "\tvertex tangent XYZW  = %f %f %f %f\n" % (self.tangent_x_blend, self.tangent_y_blend, self.tangent_z_blend, self.tangent_w_blend)                                                 
        string += "\tuv0 = %f %f\n" % (self.u0_blend, self.v0_blend)
        string += "\tuv1 = %f %f\n" % (self.u1_blend, self.v1_blend)
        string += "\tblendeweight = %f %f %f %f\n" % (self.blendweights1_x_blend, self.blendweights1_y_blend, self.blendweights1_z_blend, self.blendweights1_w_blend)     

        string += "CRF values:\n"
        string += "xyz = %f %f %f\n" % (self.x, self.y, self.z)        
        string += "\tvertex normal XYZW  = %i %i %i %i, %s %s %s %s\n" % (self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                                     hex(self.normal_x), hex(self.normal_y), hex(self.normal_z), hex(self.normal_w))        
        string += "\tvertex tangent XYZW  = %i %i %i %i, %s %s %s %s\n" % (self.tangent_x, self.tangent_y, self.tangent_z, self.tangent_w,
                                                                     hex(self.tangent_x), hex(self.tangent_y), hex(self.tangent_z), hex(self.tangent_w))
        string += "\tuv0 = %i %i, %s %s\n" % (self.u0, self.v0, hex(self.u0 & 0xffff), hex(self.v0 & 0xffff))
        string += "\tuv1 = %i %i, %s %s\n" % (self.u1, self.v1, hex(self.u1 & 0xffff), hex(self.v1 & 0xffff))        
        string += "\tblendweight = 0x%x 0x%x 0x%x 0x%x\n" % (self.blendweights1_x & 0xff, self.blendweights1_y & 0xff, self.blendweights1_z & 0xff, self.blendweights1_w & 0xff)       
        return string   

    def raw2blend(self):
        """ Convert raw values to blender values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x_blend = self.x
        self.x_blend = -self.x_blend # mirror vertex across x axis        
        self.y_blend = self.y
        self.z_blend = self.z        

        self.normal_x_blend = byte2float(self.normal_x)
        self.normal_y_blend = byte2float(self.normal_y) 
        self.normal_z_blend = byte2float(self.normal_z) 
        self.normal_w_blend = byte2float(self.normal_w)

        self.tangent_x_blend = byte2float(self.tangent_x)
        self.tangent_y_blend = byte2float(self.tangent_y)
        self.tangent_z_blend = byte2float(self.tangent_z)
        self.tangent_w_blend = byte2float(self.tangent_w)
        
        self.u0_blend = 0.5+(self.u0 / 32768.)/2.0
        self.v0_blend = 0.5-(self.v0 / 32768.)/2.0
        self.u1_blend = 0.5+(self.u1 / 32768.)/2.0
        self.v1_blend = 0.5-(self.v1 / 32768.)/2.0
        
        self.blendweights1_x_blend = byte2float(self.blendweights1_x)
        self.blendweights1_y_blend = byte2float(self.blendweights1_y)
        self.blendweights1_z_blend = byte2float(self.blendweights1_z)
        self.blendweights1_w_blend = byte2float(self.blendweights1_w)   
        
        
    def blend2raw(self):
        """ Convert blender values to raw values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x = self.x_blend
        self.y = self.z_blend
        self.z = self.y_blend
        self.x = -self.x # mirror vertex across x axis
        self.z = -self.z # mirror vertex across z axis

        print("Blender normal %i: %f, %f, %f" % (self.index, self.normal_x_blend, self.normal_y_blend, self.normal_z_blend))
        self.normal_x = float2uint(-1*self.normal_x_blend)
        self.normal_y = float2uint(self.normal_y_blend) 
        self.normal_z = float2uint(self.normal_z_blend) 
        self.normal_w = 0#float2uint(self.normal_w_blend)
        print("Raw normal %i: %f, %f, %f" % (self.index, self.normal_x, self.normal_y, self.normal_z))        
        
        self.tangent_x = float2uint(self.tangent_x_blend)
        self.tangent_y = float2uint(self.tangent_y_blend)
        self.tangent_z = float2uint(self.tangent_z_blend)
        self.tangent_w = 0xff # matches what's in the orignal binary files
        
        self.u0 = int(((self.u0_blend - 0.5) * 2) * 32768)
        self.v0 = int(((self.v0_blend - 0.5) * -2) * 32768)
        self.u1 = int(((self.u1_blend - 0.5) * 2) * 32768)
        self.v1 = int(((self.v1_blend - 0.5) * -2) * 32768)

        self.blendweights1_x = float2uint(self.blendweights1_x_blend)
        self.blendweights1_y = float2uint(self.blendweights1_y_blend)
        self.blendweights1_z = float2uint(self.blendweights1_z_blend)
        self.blendweights1_w = float2uint(self.blendweights1_w_blend)

        # clamp uv values to be <= 32768 and >=-32768
        if self.u0 >= 32768:
            self.u0 = 32767
        if self.v0 >= 32767:
            self.v0 = 32767
        if self.u1 >= 32768:
            self.u1 = 32767
        if self.v1 >= 32768:
            self.v1 = 32767
        if self.u0 <= -32768:
            self.u0 = -32767
        if self.v0 <= -32768:
            self.v0 = -32767
        if self.u1 <= -32768:
            self.u1 = -32767
        if self.v1 <= -32768:
            self.v1 = -32767               

    def bin2raw(self, file, file_offset, index):
            self.index = index
            self.x, self.y, self.z, \
                self.normal_x, self.normal_y, self.normal_z, self.normal_w, \
                self.tangent_x, self.tangent_y, self.tangent_z, self.tangent_w, \
                self.u0, self.v0, self.u1, self.v1, \
                self.blendweights1_x, self.blendweights1_y, \
                self.blendweights1_z, self.blendweights1_w = struct.unpack("<fffBBBBBBBBhhhhBBBB", file.read(32))
            
        
    def get_bin(self):        
        data = struct.pack("<fffBBBBBBBBhhhhBBBB", self.x, self.y, self.z,
                                                        self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                        self.tangent_x, self.tangent_y, self.tangent_z, self.tangent_w,
                                                        self.u0, self.v0, self.u1, self.v1,
                                                        self.blendweights1_x, self.blendweights1_y,
                                                        self.blendweights1_z, self.blendweights1_w)                          
        return data
    

class CRF_joint(object):
    def __init__(self):
        self.joint_id = 0
        self.matrix = [ (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,1) ]
        self.parent_id = 0xFFFFFFFF
        self.skeleton_index = 0
        self.i1 = 0 # unknown
        self.i2 = 0 # unknown

    def get_bin(self):
        print("Getting joint in binary form")
        data = b""
        return data        

    def __str__(self):
        string = ""
        string += "Joint id: %s\n" % self.joint_id
        string += "Matrix: \n%s\n%s\n%s\n%s\n" % (self.matrix[0],self.matrix[1],self.matrix[2],self.matrix[3])
        string += "Parent: %s\n" % self.parent_id
        string += "Skeleton index: %s\n" % self.skeleton_index        
        string += "Unknown: %s, %s\n" % (self.i1, self.i2)
        return string
    
class CRF_bone(object): #TODO better name since CRF does not use bones
    def __init__(self):
        self.bone_id = 0
        self.bone_name = b""
        self.child_list = []
        self.i1 = 0
        self.i2 = 0
        self.i3 = 0
        self.i4 = 0

    def get_bin(self):
        print("Getting bone in binary form")
        data = b""
        data += struct.pack("<II", self.bone_id, len(self.bone_name))
        data += struct.pack("%is" % len(self.bone_name), self.bone_name)
        data += struct.pack("<I", len(self.child_list))
        return data
    
    def __str__(self):
        string = ""
        string += "ID: %s, Name: %s, Children: %s, Unknown (as ubyte): %s, %s, %s, %s" % (self.bone_id, self.bone_name, self.child_list, self.i1, self.i2, self.i3, self.i4)
        byte = struct.pack("BBBB", self.i4, self.i3, self.i2, self.i1)        
        string += " Unknown (as float): %s" % struct.unpack("<f", byte)
        return string
    
class CRF_jointmap(object):
    def __init__(self, file=None, file_offset=0):
        self.magick = 0x1
        self.joint_count = 0
        self.joint_list = []
        self.bone_count = 0
        self.i1 = 0 # unknown
        self.bone_dict = {}  # map bone id to CRF_bone object
        self.bone_name_id_dict = {} # map bone name to bone id, helper for Blender
        
        if file != None:
            file.seek(file_offset)
            self.parse(file)
        
    def parse(self, file):
        self.magick, = struct.unpack("<I", file.read(4)) #TODO can there be multiple jointmaps?
        self.joint_count, = struct.unpack("<I", file.read(4))
        print("Joint count", self.joint_count)

        for i in range(0, self.joint_count):
            joint = CRF_joint()
            joint.joint_id = i
            print(hex(file.tell()))            
            f11, f12, f13 = struct.unpack("<fff", file.read(12))
            joint.parent_id, = struct.unpack("<I", file.read(4))                
            f21, f22, f23 = struct.unpack("<fff", file.read(12))
            joint.skeleton_index, = struct.unpack("<I", file.read(4))                
            f31, f32, f33 = struct.unpack("<fff", file.read(12))
            joint.i1, = struct.unpack("<I", file.read(4))
            f41, f42, f43 = struct.unpack("<fff", file.read(12))
            joint.i2, = struct.unpack("<I", file.read(4))

            joint.matrix = []
            joint.matrix.append( (f11, f12, f13, 0) )
            joint.matrix.append( (f21, f22, f23, 0) )
            joint.matrix.append( (f31, f32, f33, 0) )
            joint.matrix.append( (f41, f42, f43, 1) )

            print("Bone id:", i)
            print(joint)
            self.joint_list.append(joint)

        self.bone_count, = struct.unpack("<I", file.read(4))
        print("Bone count", self.joint_count)        
        self.i1, = struct.unpack("<I", file.read(4))
        
        for i in range(0, self.bone_count):
            bone = CRF_bone()
            bone_id,bone_name_length = struct.unpack("<II", file.read(8))
            bone_name, = struct.unpack("%is" % bone_name_length, file.read(bone_name_length))
            bone.bone_id = bone_id
            bone.bone_name = bone_name
            
            num_children, = struct.unpack("<I", file.read(4))            
            
            for i in range(0, num_children):
                child, = struct.unpack("<I", file.read(4))
                bone.child_list.append(child)
            bone.i1, bone.i2, bone.i3, bone.i4 = struct.unpack("BBBB", file.read(4))
    
            self.bone_dict[bone.bone_id] = bone
            self.bone_name_id_dict[bone.bone_name] = bone.bone_id
            print(bone)
        #TODO followd by 61 bytes of unknown
            
    def get_bin(self):
        print("Getting joint in binary form")
        data = b""
        data = struct.pack("<I", self.magick)
        data += struct.pack("<I", self.joint_count)
        
        for joint in self.joint_list:
            data += joint.get_bin()

        data += struct.pack("<I", self.bone_count)
        data += struct.pack("<I", self.i1)

        for bone in self.bone_dict:
            data += self.bone_dict[bone].get_bin()
        
            
    def __str__(self):
        string = ""
        string += "Jointmap (Bone name: bone id):\n"
        for key in self.bone_name_id_dict:
            string += "\t%s: %s\n" % (key,self.bone_name_id_dict[key])
        string += "\nBone relationships (parent: [children])\n"
        for key in self.bone_dict:
            parent = self.bone_dict[key].bone_name
            child_ids = self.bone_dict[key].child_list
            children = map(lambda x: self.bone_dict[x].bone_name, child_ids)
            string += "\t%s: %s\n" % (parent, children)
            
        return string
    
class CRF_skeleton(object):
    def __init__(self, file=None, file_offset=0):
        self.skeleton_count = 0
        self.skeleton_list = [] # [ (bone, bone bone), (bone, bone) ... ] with each tuple representing one sub model
        
        if file != None:
            file.seek(file_offset)
            self.parse(file)

    def parse(self, file):
        self.skeleton_count, = struct.unpack("<I", file.read(4))
        print("===Parsing skeleton===")
        for i in range(0, self.skeleton_count):
            bone_count, = struct.unpack("<I", file.read(4))
            bones = struct.unpack("<%sH" % bone_count, file.read(bone_count*2))
            self.skeleton_list.append(bones)
        print("===End parsing skeleton===")

    def __str__(self):
        string = "Skeleton:\n"
        idx = 0
        for bones in self.skeleton_list:            
            string += "\tMesh: %s, map of blendindices to bones %s\n" % (idx, bones)
            idx += 1
        return string


