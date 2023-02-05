Need For Speed Most Wanted(2012) Vehicle Model Tool (By NIVSAYZ)
Version: 1.1.3 - Release
Thanks for the normal algorithm, mipmap algorithm, polyface import method, provided by Binko_ctr
This tutorial translated by enthuse

Required extra tools:
1. NFS Most Wanted Packer and Unpacker for Noesis by DGIorio (https://cdn.discordapp.com/attachments/635520888204165160/663416960587137024/tool_NFSMW2012_Packer_Unpacker.rar)
2. Noesis
3. blender_export_obj_NFSMW12VMT (A blender plugin)

Tutorial:
1. Install blender_export_obj_NFSMW12VMT for Blender3.4 as a plugin, there should be plenty of tutorials out there.
2. After downloading 'tool_NFSMW2012_Packer_Unpacker.rar', extract the python scripts and put it under <Whatever your noesis directory>\plugins\python 
3. Unpack your desired BNDL using the 'Need For Speed Most Wanted 2012 Unpacker' script in Noesis. It can be found at the toolbar above under "Tools".
4. Prepare your model with Blender.

Side Notes:
1. If there are more than 60,000 vertices present after conversion, you can use the "Shade Smooth" or "Triangulate Face" option in blender to decrease the amount of vertices. (Shade Smooth is recommended)
2. You can use the same material on multiple meshes.
3. One object cannot use multiple materials

Naming's in Blender

The format should be "MeshName_MaterialType". 
An example will be: FrontWindShield_glass.

Listed below are the available materials and the infos.

MaterialType		  | Info

body			        | Non-changing body colour
bodypaint			    | Changable body colour when entering gas-station
bodypaintlivery	  | Car body with liveries/wraps, transparent area will be car's body paint
carbon			      | carbon fiber
glass			        | glass
colouriseglass	  | glass with colour
glassdoublesided	| glass with texture/livery
light			        | light
grille			      | grille
interior			    | interior
refraction			  | light, but better than light material


After done naming your materials and meshes, you can assign values for your desired settings using Blender's "Principled BSDF" surface found under the materials tab. Values will be exported to an extra mtl file for conversion later.


Material			    | Editable Data

body			        | Base Colour, Roughness
bodypaint			    | NA
bodypaintlivery	  | NA
carbon			      | NA
glass			        | Alpha
colouriseglass	  | Base Colour
glassdoublesided	| Alpha
light			        | Base Colour, Emission, Emission Strength
grille			      | Base Colour, Roughness
interior			    | Emission, Emission Strength 
refraction			  | Base Colour, Emission, Emission Strength

Type (Description) 				                      | Value Range

Base Colour (Diffuse Colour) 			              | 0 ~ 1
Roughness (How rough a surface is) 	            | 0 ~ 1
Emission (Emission Colour) 			                | 0 ~ 1
Emission Strength (How strong the light emitts)	| 0 ~ 10
Alpha (Opacity)				                          | 0 ~ 1

To export, select Wavefront OBJ format (NFSMW12VMT).

4. Creating and naming respective textures

Textures should be named in the format: MeshName_TextureType. Texture must be in dds format, with the same directory with mtl and obj file.
Default textures are used if the tool can't find the respective texture for the respective mesh.
Texture Type: c (colour texture) , d (diffuse texture) , dp (displacement texture) , e (emissive texture) , en (external normal texture) , in (internal normal texture) , l (lightmap lights texture) , n (normal texture) , s (specular texture)
emissive texture and lightmap lights texture: the alpha channel of the texture indicates rear lights, the red channel of the texture indicates brake lights, the green channel of the texture indicates headlights, and the blue channel of the texture indicates reversing lights
It is recommended to use a picture with a resolution aspect ratio of 1:1, otherwise it may cause the game crash

Material		      | Supported Textures

bodypaintlivery	  | d
glassdoublesided 	| d
light 		        | l , n , s 
grille		        | d , n
interior		      | d , n , s 
refraction		    | c , en , e , in , dp

5. After exporting the obj and mtl file, use the tool NFSMW12VMT to convert the model, you need to manually input the respective directories.
6. After conversion using the NFSMW12VMT tool, pack the file with DGI's MW12 Packer, rename the file and put where it belongs, enjoy.

Update Log:
---1.1.3---
1.Fix errors caused by not unwrapped UV
