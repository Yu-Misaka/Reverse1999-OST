# Reverse: 1999 resources unpack

![image](https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Image/sundry/bg_denglubeijing.png)

> [!WARNING]
> Large repository. Use shallow clone to reduce size: `git clone --depth=1 https://github.com/Yu-Misaka/Reverse1999-OST.git`.

> [!CAUTION]
> Only for personal use. Bluepoch Co.,Ltd. All Rights Reserved.

## Status

| Resources | Character | Version | Remark |
| :--------- | :------- | :---------- | :-------- |
| Audio | * | 2.6 | |
| Image | * | 1.9 | |
| Text | * | 1.9 | |
| Live2D | Vertin | 1.9 | |
| Live2D | Sonetto | 1.9 | no motion |
| Live2D | Matilda | 1.9 | no motion |

## TO-DO

- [ ] Text extraction: Training the audio requires corresponding dialog script. I placed in `Text` some json files extracted from "Assets\ZResourcesLib\configs\story\", for sure they contain audio scripts, but I don't know how to link the scripts with the audio.
- [ ] Live2D motion: I didn't manage to make the model move as in the game - expressions and breath seem working though.
- [ ] Main hall Live2D: Haven't found the file.

## Working procedure

In the following context, the default assets path `C:\Program Files (x86)\reverse1999_global\Reverse1999en\reverse1999_Data\StreamingAssets\` will be omitted.

### Audio unpack

Every time the game updates,
1. copy `PersistentRoot\audios\Windows` to `Origin`, override all existing files if any.
2. copy `StreamingAssets\Windows\audios\Windows` to `Origin`, override all existing files if any.
3. delete everything in `Decoded` except `pull_out.nb`.
4. use "foobar2000" + "vgmstream" to decode all `.wem` and `.bnk` files, place the result under `Decoded` folder, override all existing files if any.

My export settings of foobar2000 is as follows:
| Option | Settings |
| :--------- | :------- |
| Output format | Format: MP3 (LAME), V6. |
| Destination | File name pattern: %filename%_%STREAM_INDEX% |

LAME requires additional encoder. Please refer to [lame_win32-build](https://github.com/Chocobo1/lame_win32-build) for Windows builds.

`select.nb` is for selecting proper audio for AI training. One can utilize `selectedFiles` to select all audio files with duration > 10s of one particular character via inserting corresponding character ID.

### Bundles Decryption

Decrypting Live2D involves handling huge amount of bundle files whic I omit in this repository. 

In short, setup a new directory named `bundles` under `Decryption`, and copy all files from `PersistentRoot\bundles` and `Windows\bundles` to `bundles`.

Then run `decrypt.nb`, this should leave you ~25000 decrypted files under `Decryption`. Opening those files via "AssetStudio.net6.v0.16.47" requires around 48G of ram according to my observation. `partition.nb` can split them into 5 subfolders so that you can unpack them folder by folder (though I don't think this is a proper method...)

The decryption algorithm follows **[1999decrypt](https://github.com/66hh/1999decrypt)**, go check that out!

#### Image

 - `Assets/ZResourcesLib/singlebg/storybg/story_bg/`: Background images in stories
 - `Assets/ZResourcesLib/singlebg/storybg/story_atcg`: ↑
 - `Assets/ZResourcesLib/singlebg/storybg/bg/`: ↑
 - `Assets/ZResourcesLib/singlebg/headicon_{img, large, middle}`: Character illustrations
 - `Assets/ZResourcesLib/singlebg/headskinicon`: ↑
 - `Assets/ZResourcesLib/singlebg/signature`: Character signatures
 - `Assets/ZResourcesLib/singlebg/seasoncelebritycard`: Cards etc.
 - `Assets/ZResourcesLib/singlebg/handbook/equip`: ↑
 - `Assets/ZResourcesLib/singlebg/equipment/suit`: ↑
 - `Assets/ZResourcesLib/singlebg/loading`: Background of opening page
 - `Assets/ZResourcesLib/bootres/textures/`: ↑

#### Live2D (MOC3)

[This issue](https://github.com/66hh/1999decrypt/issues/6) provides clear guidance towards finally extract live2d models.

Take Sonetto for example, search "shisi" (Chinese for Sonetto) using the filter in AssetStudio, select all with container looks like "Assets\ZResourcesLib\live2d\roles\", export them normally and in raw.

Among the resulted subfolders, we'll use `302301_shisihangshi.dat` (around 1 MB) in `MonoBehaviour` and the two largest image in `Texture2D`. First open `302301_shisihangshi.dat` with a hex editor, delete everything before "MOC3", then rename it into `302301_shisihangshi.moc3`.

<p align="center">
<img src="https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Screenshot/20241204142908.png" width=50%>
</p>

Next, create a file `index.json` following the pattern in [this file](https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Live2D/Sonetto-302301/index.json). Finally open this json with "Live2DViewerEX".

#### Live2D (Spine)

The model in `v2t-560501` follows a different modality as it's a spine project. We shall need a spine file `560501_vertin.skel.prefab`, texture file `560501_vertin.atlas.prefab` and `560501_vertin.png`.

Rename `560501_vertin.skel.prefab` to `560501_vertin.skel`, open with hex editor and delete bytes before `1C`.

<p align="center">
<img src="https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Screenshot/20241204101934.png" width=50%>
</p>

Next, rename `560501_vertin.atlas.prefab` to `560501_vertin.atlas`, open with hex editor and delete bytes before the texture image name.

<p align="center">
<img src="https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Screenshot/20241204102104.png" width=50%>
</p>

One can then reconstruct the project in Live2DViewerEX after creating a json file following the pattern [here](https://github.com/Yu-Misaka/Reverse1999-OST/blob/main/Live2D/v2t-560501/index.config.json).
