# Reverse 1999 Game resources unpack

## Working procedure

### Audio unpack

Every time the game updates,
1. copy `C:\Program Files (x86)\reverse1999_global\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\audios\Windows` to `Origin`, override all existing files if any.
2. copy `C:\Program Files (x86)\reverse1999_global\Reverse1999en\reverse1999_Data\StreamingAssets\Windows\audios\Windows` to `Origin`, override all existing files if any.
3. delete everything in `Decoded` except `pull_out.nb`.

Next, use "WwiseExtractorConsole" or "foobar2000" + "vgmstream" to decode all `.wem` and `.bnk` files, place the result under `Decoded` folder, override all existing files if any.

"WwiseExtractorConsole" extracts each `.wem` and `.bnk` file into separate subfolders, `pull_out.nb` can flatten the directory structure via pulling those audios in all subfolders out by one layer.

I don't know how to control the export bitrate of "foobar2000" + "vgmstream" yet, directly export into `.wav` seems to produce excessively large files.

`select.nb` is for selecting proper audio for AI training. One can utilize `selectedFiles` to select all audio files of one particular character via inserting corresponding character ID.

### Live2D

Decrypting Live2D involves handling huge amount of bundle files so I omit them in this repository. 

In short, setup a new directory, create a subfolder named `bundles`, and copy all files from `C:\Program Files (x86)\reverse1999_global\Reverse1999en\reverse1999_Data\StreamingAssets\PersistentRoot\bundles` and `C:\Program Files (x86)\reverse1999_global\Reverse1999en\reverse1999_Data\StreamingAssets\Windows\bundles` to `bundles`.

Then copy `test.py` in `Decryption` to `bundles` - **`test.py` is written by [@66hh](https://github.com/66hh) in [1999decrypt](https://github.com/66hh/1999decrypt), go check the great work!**

Run `test.py`, it should yield a new folder `bundles-decrypt` along with ~25000 decrypted files. Opening those files via "AssetStudio.net6.v0.16.47" requires around 48G of ram according to my observation. You can use `partition.nb` in `Decryption` to split them into 5 subfolders and unpack them folder by folder.

[this issue](https://github.com/66hh/1999decrypt/issues/6) provides clear guidance towards finally extract live2d models.

Take Sonetto for example, search "shisi" (Chinese for Sonetto) using the filter in AssetStudio, select all with container looks like "Assets\ZResourcesLib\live2d\roles\", export them normally and in raw.

Among the resulted subfolders, we'll use `302301_shisihangshi.dat` (around 1 MB) in `MonoBehaviour` and the two largest image in `Texture2D`. First open `302301_shisihangshi.dat` with hex editor, delete everything before `MOC3`, then rename it into `302301_shisihangshi.moc3`.

Next, create a file `index.json` that looks like
```
{
  "Version": 3,
  "Type": 0,
  "FileReferences": {
    "Moc": "MonoBehaviour/302301_shisihangshi.moc3",
    "Textures": [
      "Texture2D/302301_shisihangshi_00.png",
      "Texture2D/302301_shisihangshi_01.png"
    ],
    "PhysicsV2": {}
}
```
Finally open this json with "Live2DViewerEX".

The model in `v2t` follows a different modality as it's a spine project. One can reconstruct it by starting a spine project in Live2DViewerEX with spine file `560501_vertin.skel.prefab` (rename to `560501_vertin.skel`), texture file `560501_vertin.atlas.prefab` (rename it to `560501_vertin.atlas`) and `560501_vertin.png` and `560501_vertin.skel.prefab` (rename to `560501_vertin.skel`).

## TO-DO

- [ ] Text extraction: Training the audio requires corresponding dialog script, which I don't konw where to find.
- [ ] Live2D motion: I didn't manage to make the model move as in the game - expressions and breath seem working though.
