# Island Living - Tanning Fix 

A mod for Custom Tan Lines

This mod allows to apply custom tan lines for an outfit.
* It does not fix broken skin tones.
* It does not create a proper diffuse map (uv_0) for an existing, broken outfit.

If tanning works fine for your sims with all outfits this tool is likely not needed. I came across multiple UGC creators who UV unwrap their outfit mesh to random places on the diffuse map. While this may be good for layered outfits the effects on tanning are random. After tanning the sims have tan lines which don't match the outfit at all.

The same way to fix the broken outfits can be used to create tan-through outfits. Creating such outfits using good items is even more easy as one only needs to modify the opacity/transparency or remove some parts completely.

Creating custom tan lines
This part is quite long as it describes how to add custom tan lines. It does not describe how to use

Needful things
* An item to create the diffuse map for.
* The diffuse map to get an idea which parts to tan.
* Vanilla diffuse maps of various swimwear and similar outfits as a reference can be helpful.
* Gimp, Photoshop or any other image editor to create a new diffuse map.
* Sims4Studio, S4PE or any other tool to create a package file
* GUIDs
* Optionally Python to verify the 'data' *1)
* Optionally an XML editor to create the XML snippet *2

*1) Online: https://www.tutorialspoint.com/onli...n_formatter.htm - add 'a=' before the data. 'Beautify' checks the syntax and uglifies the code.
*2) Online: https://www.tutorialspoint.com/online_xml_editor.htm

The package file needs to contain:
* Diffuse map with the desired tan lines
* CAS Part Item referencing to the diffuse map.
* XML Snippet Tuning referencing the CAS Part Item and which CAS Part Items should be replaced.

Diffuse Map
The most easy way is to use a good diffuse map of an existing item and modify it. Make some areas transparent or increase the size of the opaque area.
Or merge 2-3 diffuse maps.

Naming and Instance ID
Select a name for your creation. I picked 'o19_yfBody_EF01SwimsuitOnePiece_TanThrough' as I modified a 'yfBody_EF01SwimsuitOnePiece_...' diffuse map.
I also named my diffuse map 'o19_yfBody_EF01SwimsuitOnePiece_TanThrough.png'

Use the hash generator to generate the fnv64 IDs (with High-Bit) in hex and dec:
Eg: 'o19_yfBody_EF01SwimsuitOnePiece_TanThrough' = (0x) ECA26728CACFC809 = 17051304564077086729
Write the name, hex and dec ID down as it is needed later.

One may either add this to the current package (for UGC) or create a new one for EA CAS Parts:
* Start S4S
* S4S > Tools > Create Empty Package

1) Image
* Add > RLE 2 Image > Group: 0, Instance: ECA26728CACFC809 (the written down hex ID)
* Select the image entry
* Import > File 'o19_yfBody_EF01SwimsuitOnePiece_TanThrough.png'

2) CAS Part
* Import or modify the CAS Part with the completely different instance key.
* Modify:
* Key.Instance to ECA26728CACFC809 [REF.hex]
* PartFlags.Allow*: Uncheck
* PartFlags.Default*: Uncheck
* PartFlags.Show*: Uncheck

3) Snippet Tuning
* Add > Snippet Tuning > Group: 0, Instance: ECA26728CACFC809 (matches the selected item) [REF]
* Select the Snippet Tuning entry
* Insert (n~[REF.name], s=[REF.dec]:
Code:
```xml
<>?xml version="1.0" encoding="utf-8"?>
<I c="TanningFix" i="snippet" m="tanning.snippet" n="o19_yfBody_EF01SwimsuitOnePiece_TanThrough" s="17051304564077086729">
  <;!-- ECA26728CACFC809 -->
  <T n="version"></T>
  <T n="data">
        {
            'BodyType.FULL_BODY': {
                0xECA26728CACFC809: [ 0x10927, 0x10928, 0x10929, 0x1092A, 0x1092B, 0x1092C, 0x1092D, 0x1092E, 0x1092F,
                    0x11929, 0x1192A, 0x1192B, 0x1192C, ],  # New swatches
                # Add the name behind the IDs, if it can be parsed it'll replace the line above
                'o19_yfBody_EF01SwimsuitOnePiece_TanThrough': ['yfBody_EF01SwimsuitOnePiece_*', ],
            },
        }
    </T>
</I>
```


Obviously obtaining the name and using a wildcard for the EA CAS parts is more easy than using the numbers. You may really want to start like this and check the log file. This mod searches all matching items and lists their IDs (as dec, these numbers match the hex numbers from above):
_get_int_cas_part_ids(o19_yfBody_EF01SwimsuitOnePiece_TanThrough) -> '{17051304564077086729}'
_get_int_cas_part_ids(yfBody_EF01SwimsuitOnePiece_*) -> '{67879, 67880, 67881, 67882, 67883, 67884, 67885, 67886, 67887, 71977, 71978, 71979, 71980}'


Save the package file.

Some more information
Instead of `'BodyType.FULL_BODY'` the number `5` may be used. The most commonly used types are:
Code:
```sh
HAT = 1
HAIR = 2
HEAD = 3
FULL_BODY = 5
UPPER_BODY = 6
LOWER_BODY = 7
SHOES = 8
NECKLACE = 12
GLOVES = 13
SOCKS = 36
TIGHTS = 42
```


Multiple settings can be joined, sections are separated with ','.
Another example of a dict which will obviously not work:
Code:
```json
{
    1: {
        12: [34, 56, ],
        11: [22, 33, ],
    },
    'BodyType.SOCKS ': {
        'foo': ['bar*', ],
        'kk': ['nik*', 'adi*', ],
    },
}
```


# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.97.62 (2023-05) and S4CL v2.6 (2023-04).
It is expected to work with many older and upcoming releases of TS4 and S4CL.

## Dependencies
* S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest
* TS4Lib https://github.com/Oops19/TS4-Library/releases/latest

If not installed download and install these mods.

## Installation
* Locate the `The Sims 4` folder which contains the 'Mods' folder.
* Extract the ZIP file into the `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/*.ts4script`, `mod_data/$mod_name/*`
* 'mod_logs' will be created as soon as data is logged.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this. 
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
Sources: https://github.com/Oops19/
Support: https://discord.gg/d8X9aQ3jbm
Donations: https://www.patreon.com/o19

## Copyright and License
© 2023 https://github.com/Oops19
Unless specified differently: https://creativecommons.org/licenses/by/4.0/ unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 is not endorsed by or affiliated with Electronic Arts, or its licensors.
Trademarks are the property of their respective owners.
Game content and materials copyright Electronic Arts Inc. and its licensors.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use Patch-XML https://github.com/Oops19/TS4-PatchXML or LiveXML https://github.com/Oops19/TS4-LiveXML.
* To check custom tunings use https://github.com/Oops19/TS4-VanillaLogs.
