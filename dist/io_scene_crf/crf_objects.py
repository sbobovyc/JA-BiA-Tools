from __future__ import print_function    
    
import math
import struct

# Footer constants
CRF_ROOT_NODE = 0x0
CRF_MESHFILE = 0x1b4f7cc7
CRF_JOINTMAP = 0xb8fa7643
CRF_SKELETON = 0xbd9d53a3

# unsupported constants
CRF_SKININFO = None
CRF_GEOMESH = None
CRF_COLLISION_SHAPE = None
CRF_OCCLUSION_SHAPE = None

# Supported texture formats
CRF_TexFormats = ["bmp", "tga", "jpg", "dds"]

# Materials constants
CRF_Diffuse = b"sffd"
CRF_Normals = b"smrn"
CRF_Specular = b"lcps"
CRF_Custom1 = b"1tsc"
CRF_Custom2 = b"2cst"
CRF_Custom3 = b"3cst"
CRF_Custom4 = b"4cst"
CRF_Custom5 = b"5cst"
CRF_Custom6 = b"6cst"
CRF_Custom7 = b"7cst"
CRF_Custom8 = b"8cst"
CRF_Custom9 = b"9cst"
CRF_Custom10 = b"01cs"
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

class CRF_header(object):
    def __init__(self, file):
        crf_magick, = struct.unpack("<Q", file.read(8))    
        if crf_magick != 0x1636E6B66:
            print("Not a CRF file!")
            return 
        self.footer_offset1,self.footer_offset2 = struct.unpack("<II", file.read(8))
        self.footer_entries, magick4, mesh_count = struct.unpack("<III", file.read(12))

        
class CRF_footer(object):
    def __init__(self, file, footer_offset1, footer_offset2, footer_entries):
        self.entries = []
        self.entry_descriptors = []

        file.seek(footer_offset1)
        for i in range(0, footer_entries):
            self.entries.append(CRF_entry(file))
                
        for entry in self.entries:
            self.entry_descriptors.append(CRF_entry_descriptor(file, entry.magick))

    def get_meshfile(self):
        for entry in self.entries:
            if entry.magick == CRF_MESHFILE:
                return entry
        return None

    def get_bin(self):
        data = b""
        for entry in self.entries:
            data += entry.get_bin()
        for entry in self.entry_descriptors:
            data += entry.get_bin()
        return data
        
class CRF_entry(object):
    def __init__(self, file):
        self.magick = None
        self.entry_id = None
        self.file_offset = None
        self.size = None
        self.const = None #(a, b, c, d) unknown
        self.magick, self.entry_id, self.file_offset, self.size = struct.unpack("<IIII", file.read(16))
        print("Magick: %s \n Entry: %s \n File offset: %s \n Size: %s" % (hex(self.magick), self.entry_id, hex(self.file_offset), self.size) )
        self.const = struct.unpack("<IIII", file.read(16))
        print(self.const)

    def get_bin(self):
        data = b""
        data = struct.pack("<IIIIIIII", self.magick, self.entry_id, self.file_offset, self.size, *self.const)
        return data
        
class CRF_entry_descriptor(object):        
    def __init__(self, file, CRF_TYPE):
        self.type = CRF_TYPE
        self.entry_id = None
        self.name_length = None
        self.name = None

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
        print(self.entry_id, self.name)


    def get_bin(self):
        if(self.type == CRF_ROOT_NODE):
            data = struct.pack("<xxxxII%ss" % self.name_length, self.entry_id, self.name_length, self.name)
        if(self.type == CRF_MESHFILE or self.type == CRF_JOINTMAP or self.type == CRF_SKELETON):
            data = struct.pack("<II%ssxxxx" % self.name_length, self.entry_id, self.name_length, self.name)
        return data

class CRF_meshfile(object):
    def __init__(self, file, file_offset, verbose=False):
        self.num_meshes = None
        self.model_bounding_box = None # ((LoX, LoY, LoZ), (HiX, HiY, HZ))
        self.meshes = []

        file.seek(file_offset)
        magick, self.num_meshes = struct.unpack("<II", file.read(8))
        LoX, LoY, LoZ = struct.unpack("<fff", file.read(12)) #bounding box       
        HiX, HiY, HiZ = struct.unpack("<fff", file.read(12)) #bounding box
        self.model_bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))
        print("Number of meshes", self.num_meshes)        
        print("Bounding box of entire model: ", self.model_bounding_box)

        #TODO add support for multiple meshes
        for i in range(0, self.num_meshes):
            self.meshes.append(CRF_mesh(file, file.tell(), i, verbose))

class CRF_mesh(object):
    def __init__(self, file, file_offset, mesh_number, verbose=False):
        self.mesh_number = mesh_number
        self.number_of_verteces = None
        self.number_of_faces = None
        self.face_list = []
        self.verteces1 = [] # 3d data, colors, uv, normals, specular, blendweight
        self.verteces2 = [] # blendindeces and blendweight
        self.bounding_box = [] # ((LoX, LoY, LoZ), (HiX, HiY, HZ))
        self.materials = None

        # parse
        self.number_of_verteces, = struct.unpack("<I", file.read(4))
        self.number_of_faces, = struct.unpack("<I", file.read(4))
        print("Model verteces: %i, faces: %i" % (self.number_of_verteces, self.number_of_faces))
        
        # read in face/vertex index list
        for i in range(0, self.number_of_faces):
                v1, v2, v3 = struct.unpack("<HHH", file.read(6))
                face_vert_loc_indices = [v1, v2, v3]
                face_vert_tex_indices = [v1, v2, v3]
                self.face_list.append((v1, v2, v3))
                if verbose:
                    print("face index %s, verts (%s, %s, %s)" % (i, v1, v2, v3))
                
        #read start token     #0x0000200c01802102, 0x00
        start_token, = struct.unpack("<Qx", file.read(9))
        print("Vertex information starts at ", hex(file.tell()))
        
        # read in verteces, vertex normals, ks, and UVs
        for i in range(0, self.number_of_verteces):
            vertex = CRF_vertex()
            vertex.bin2raw(file, file.tell(), i)
            vertex.raw2blend()
            self.verteces1.append(vertex)
            if verbose:
                print(vertex)

        #read in separator 0x000000080008000000
        #TODO not all files have this separator
        print("Separator 0x000000080008000000 at", hex(file.tell()))
        separator = struct.unpack("<8B", file.read(8))
        #print(map(print, separator))

        print("First blendweight and blendindex stream at", hex(file.tell()))
        for i in range(0, self.number_of_verteces):
            vertex_blend = CRF_vertex_blend()
            vertex_blend.bin2raw(file, file.tell(), i, verbose)
            self.verteces2.append(vertex_blend)
        print("End of vertex data", hex(file.tell()))

        #read in mesh bounding box
        LoX, LoY, LoZ = struct.unpack("<fff", file.read(12)) #bounding box       
        HiX, HiY, HiZ = struct.unpack("<fff", file.read(12)) #bounding box
        self.bounding_box = ((LoX, LoY, LoZ), (HiX, HiY, HiZ))        
        print("Bounding box of model %i: %s" % (self.mesh_number, self.bounding_box))

        #TODO material info comes next
        self.materials = CRF_materials(file, file.tell(), verbose)
        
class CRF_materials(object):
    def __init__(self, file, file_offset, verbose=False):
        self.diffuse_texture = b''
        self.normal_texture = b''
        self.specular_texture = b''
        self.specular_constant = None # (R, G, B)
        self.specular_constant_alpha = None #TODO not sure if this is right
        self.custom1 = None
        
        print("Materials at: ", hex(file.tell()))
        magick, = struct.unpack("2s", file.read(2))
        print(magick)
        material_type, = struct.unpack(">Q", file.read(8))
        print(hex(material_type))

        reading_materials = True
        state = "read_diffuse"
        if magick == b"nm":
            while(reading_materials):
                if state == "read_diffuse":
                    data_type, = struct.unpack("4s", file.read(4))
                    print(data_type)
                    if(data_type == CRF_Diffuse):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print(texture)
                        self.diffuse_texture = texture
                        file.read(4)
                        state = "read_normals"
                    else:
                        print("Error reading diffuse")
                        reading_materials = False

                if state == "read_normals":
                    data_type, = struct.unpack("4s", file.read(4))
                    print(data_type)
                    if(data_type == CRF_Normals):
                        length, = struct.unpack("<I", file.read(4))
                        texture, = struct.unpack("%ss" % length, file.read(length))
                        print(texture)
                        self.normal_texture = texture
                        file.read(4)
                        state = "read_specular"
                    else:
                        print("Error reading normals")                              
                        reading_materials = False
                        
                if state == "read_specular":
                    data_type, = struct.unpack("4s", file.read(4))
                    print(data_type)
                    if(data_type == CRF_Custom1):
                        file.read(8)
                        data_type, = struct.unpack("4s", file.read(4))
                        print(data_type)
                        if(data_type == CRF_Specular):
                            length, = struct.unpack("<I", file.read(4))
                            if(length > 0):
                                texture, = struct.unpack("%ss" % length, file.read(length))
                                print(texture)
                                self.specular_texture = texture
                                file.read(8)
                                data_type, = struct.unpack("4s", file.read(4))
                                print(data_type)
                                R,G,B = struct.unpack("<III", file.read(12))
                                print(hex(R),hex(G),hex(B))
                                #TODO I have no idea if this is right
                                # convert int32 to scaled float
                                #TODO is it uint32 or int32?
                                R = R / 4294967295
                                G = G / 4294967295
                                B = B / 4294967295
                                self.specular_constant = (R, G, B)                                
                                data_type, = struct.unpack("4s", file.read(4))
                                print(data_type)
                                R,G,B = struct.unpack("<III", file.read(12))
                                print(hex(R),hex(G),hex(B))                                
                                file.read(4)
                                data_type, = struct.unpack("4s", file.read(4))
                                print(data_type)
                                file.read(0x18)
                                
                            else:
                                file.read(4)
                                specular_type, = struct.unpack("<I", file.read(4))
                                print(specular_type)
                                if(specular_type == 0x1):
                                    data_type, = struct.unpack("4s", file.read(4))
                                    print(data_type)
                                    R,G,B,A = struct.unpack("<IIII", file.read(16))
                                    #TODO I have no idea if this is right
                                    # convert int32 to scaled float
                                    #TODO is it uint32 or int32?
                                    R = R / 4294967295
                                    G = G / 4294967295
                                    B = B / 4294967295                                    
                                    self.specular_constant = (R,G,B)
                                    print(self.specular_constant)
                                if(specular_type == 0x2):
                                    data_type, = struct.unpack("4s", file.read(4))
                                    print(data_type)
                                    R,G,B = struct.unpack("<III", file.read(12))
                                    data_type, = struct.unpack("4s", file.read(4))
                                    print(data_type)
                                    if(data_type == CRF_Custom1):
                                        A = struct.unpack("<IIII", file.read(16))
                                        # convert int32 to scaled float
                                        #TODO is it uint32 or int32?
                                        R = R / 4294967295
                                        G = G / 4294967295
                                        B = B / 4294967295
                                        self.specular_constant = (R, G, B)
                                        print("Specular constant ", self.specular_constant)
                                    data_type, = struct.unpack("4s", file.read(4))
                                    print(data_type)
                                    unknown, = struct.unpack("<I", file.read(4))
                                    print("Unknown", hex(unknown))
                                file.read(0x14)
                    reading_materials = False
                else:
                    print("Materials %s are not supported", magick)
                print("Materials end at: ", hex(file.tell()))
                    
    
class CRF_vertex_blend(object):
    def bin2raw(self, file, file_offset, index, verbose=False):
        self.index = index
        self.blendweight = None
        self.blendindeces = None
        self.blendweight = struct.unpack("<bbbb", file.read(4))
        self.blendindeces = struct.unpack("<bbbb", file.read(4))
        if verbose:
            print("vert index=%s, blendweights: %s, blendindeces: %s" % (self.index, self.blendweight, self.blendindeces))
        
class CRF_vertex(object):
    """
        Common variables:
        CRF_vertex.index
        
        Raw CRF variables:
        CRF_vertex.x, vert.y, vert.z 
        CRF_vertex.normal_x 
        CRF_vertex.normal_y 
        CRF_vertex.normal_z 
        CRF_vertex.normal_w 
        CRF_vertex.specular_blue 
        CRF_vertex.specular_green
        CRF_vertex.specular_red 
        CRF_vertex.specular_alpha      
        CRF_vertex.u0 
        CRF_vertex.v0 
        CRF_vertex.u1 
        CRF_vertex.v1 
        CRF_vertex.blendweights1_x
        CRF_vertex.blendweights1_y
        CRF_vertex.blendweights1_z
        CRF_vertex.blendweights1_w

        Blender variables
        CRF_vertex.x_blend, vert.y_blend, vert.z_blend 
        CRF_vertex.normal_x_blend 
        CRF_vertex.normal_y_blend 
        CRF_vertex.normal_z_blend 
        CRF_vertex.normal_w_blend 
        CRF_vertex.specular_blue_blend 
        CRF_vertex.specular_green_blend
        CRF_vertex.specular_red_blend 
        CRF_vertex.specular_alpha_blend #Not iplemented      
        CRF_vertex.u0_blend 
        CRF_vertex.v0_blend 
        CRF_vertex.u1_blend 
        CRF_vertex.v1_blend 
        CRF_vertex.blendweights1_blend
        CRF_vertex.blendweights1_x_blend
        CRF_vertex.blendweights1_y_blend
        CRF_vertex.blendweights1_z_blend
        CRF_vertex.blendweights1_w_blend  

            
    """
    def __str__(self):
        string = "Vertex index = %s\n" % (self.index)
        string += "Blender values:\n"
        string += "xyz = %f %f %f\n" % (self.x_blend, self.y_blend, self.z_blend)
        string += "\tvertex normal XYZW  = %f %f %f %f\n" % (self.normal_x_blend, self.normal_y_blend, self.normal_z_blend, self.normal_w_blend)                                                                    
        string += "\tspecular BGRA  = %f %f %f %f\n" % (self.normal_x_blend, self.normal_y_blend, self.normal_z_blend, self.normal_w_blend)                                                 
        string += "\tuv0 = %f %f\n" % (self.u0_blend, self.v0_blend)
        string += "\tuv1 = %f %f\n" % (self.u1_blend, self.v1_blend)
        string += "\tblendeweight = %f %f %f %f\n" % (self.blendweights1_x_blend, self.blendweights1_y_blend, self.blendweights1_z_blend, self.blendweights1_w_blend)     

        string += "CRF values:\n"
        string += "xyz = %f %f %f\n" % (self.x, self.y, self.z)        
        string += "\tvertex normal XYZW  = %i %i %i %i, %s %s %s %s\n" % (self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                                     hex(self.normal_x), hex(self.normal_y), hex(self.normal_z), hex(self.normal_w))
        string += "\tspecular BGRA  = %i %i %i %i, %s %s %s %s\n" % (self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                                     hex(self.specular_blue), hex(self.specular_green), hex(self.specular_red), hex(self.specular_alpha))
        string += "\tuv0 = %i %i, 0x%x 0x%x\n" % (self.u0, self.v0, self.u0, self.v0)
        string += "\tuv1 = %i %i, 0x%x 0x%x\n" % (self.u1, self.v1, self.u1, self.v1)        
        string += "\tblendeweight = 0x%x 0x%x 0x%x 0x%x\n" % (self.blendweights1_x & 0xff, self.blendweights1_y & 0xff, self.blendweights1_z & 0xff, self.blendweights1_w & 0xff)       
        return string

    def float2uint(self, f_number):
        if f_number > 0.0:
            return int(128 + f_number * 127)
        elif f_number < 0.0:
            return int(128 - math.fabs(f_number) * 128)
        else:
            return 128
        
    def uint2float(self, uint_number):
        if uint_number > 128:
            return float(uint_number / 127.0)
        elif uint_number < 128:
            return float(-uint_number / 128.0)
        else:
            return 0.0

    def raw2blend(self):
        """ Convert raw values to blender values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x_blend = self.x
        self.y_blend = self.y
        self.z_blend = self.z
        self.x_blend = -self.x_blend # mirror vertex across x axis

        self.normal_x_blend = self.uint2float(self.normal_x)
        self.normal_y_blend = self.uint2float(self.normal_y) 
        self.normal_z_blend = self.uint2float(self.normal_z) 
        self.normal_w_blend = self.uint2float(self.normal_w)

        self.specular_blue_blend = self.specular_blue / 255
        self.specular_green_blend = self.specular_green / 255
        self.specular_red_blend = self.specular_red / 255
        self.specular_alpha_blend = self.specular_alpha / 255

        self.u0_blend = 0.5+(self.u0 / 32768)/2.0
        self.v0_blend = 0.5-(self.v0 / 32768)/2.0
        self.u1_blend = 0.5+(self.u1 / 32768)/2.0
        self.v1_blend = 0.5-(self.v1 / 32768)/2.0
        
        self.blendweights1_x_blend = self.blendweights1_x / 255
        self.blendweights1_y_blend = self.blendweights1_y / 255
        self.blendweights1_z_blend = self.blendweights1_z / 255
        self.blendweights1_w_blend = self.blendweights1_w / 255        
        
        
    def blend2raw(self):
        """ Convert blender values to raw values """
        #TODO find out how CRF object coordinates work (global or local)
        self.x = self.x_blend
        self.y = self.z_blend
        self.z = self.y_blend
        self.x = -self.x # mirror vertex across x axis
        self.z = -self.z # mirror vertex across z axis
        
        self.normal_x = self.float2uint(self.normal_x_blend)
        self.normal_y = self.float2uint(-self.normal_y_blend) # flip y direction
        self.normal_z = self.float2uint(-self.normal_z_blend) # flip z direction
        self.normal_w = self.float2uint(self.normal_w_blend)
        
        self.specular_blue = int(self.specular_blue_blend * 255)
        self.specular_green = int(self.specular_green_blend * 255)
        self.specular_red = int(self.specular_red_blend * 255)
        self.specular_alpha = int(self.specular_alpha_blend * 255)
        
        self.u0 = int(((self.u0_blend - 0.5) * 2) * 32768)
        self.v0 = int(((self.v0_blend - 0.5) * -2) * 32768)
        self.u1 = int(((self.u1_blend - 0.5) * 2) * 32768)
        self.v1 = int(((self.v1_blend - 0.5) * -2) * 32768)

        self.blendweights1_x = int(self.blendweights1_x_blend * 255)
        self.blendweights1_y = int(self.blendweights1_y_blend * 255)
        self.blendweights1_z = int(self.blendweights1_z_blend * 255)
        self.blendweights1_w = int(self.blendweights1_w_blend * 255)

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
                self.specular_blue, self.specular_green, self.specular_red, self.specular_alpha, \
                self.u0, self.v0, self.u1, self.v1, \
                self.blendweights1_x, self.blendweights1_y, \
                self.blendweights1_z, self.blendweights1_w = struct.unpack("<fffBBBBBBBBhhhhBBBB", file.read(32))
            
        
    def convert2bin(self):        
        binstring = struct.pack("<fffBBBBBBBBhhhhBBBB", self.x, self.y, self.z,
                                                         self.normal_x, self.normal_y, self.normal_z, self.normal_w,
                                                         self.specular_blue, self.specular_green, self.specular_red, self.specular_alpha,
                                                         self.u0, self.v0, self.u1, self.v1,
                                                         self.blendweights1_x, self.blendweights1_y,
                                                        self.blendweights1_z, self.blendweights1_w)                                                
        return binstring
    
if __name__ == "__main__":

    import sys
    import os
    path = os.path.abspath(sys.argv[1])
    print(path)
    file = open(path, "rb")
    
    header = CRF_header(file)
    footer = CRF_footer(file, header.footer_offset1, header.footer_offset2, header.footer_entries)
    meshfile = CRF_meshfile(file, footer.get_meshfile().file_offset)
    file.close()

    # now write back data
    file = open("dump.bin", "wb")
    file.write(footer.get_bin())
