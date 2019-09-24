# Minecraft Randomizer

A tool that lets you randomize loot tables and other data in Minecraft.

## Requirements

The tool requires python to be installed in order to run.   
The 1.14 data pack is included in the repository.

## Usage

The script can be used in two ways:

* **User Interface:**
  Simply execute `randomizer.py`. You will be able to configure the build with a simple UI.
* **Arguments:**
  Run the command  `python randomizer.py <seed> [loot_tables] [advancements] [recipes]`.   
  The argument `<seed>` can either be a seed as an integer or `r` for a random seed.
  All other arguments are optional. Providing no optional arguments will result in an empty datapack.

The script will build a datapack that can be added to map.   
**PLEASE NOTE:** Using the advancement and recipe randomizer is not recommended.
These features are still experimental, using them might have unexpected results.

## Credit

This tool is based on SethBling's loot table randomizer.   
Download the original [here](https://www.youtube.com/redirect?q=https%3A%2F%2Fsethbling.s3-us-west-2.amazonaws.com%2FDownloads%2FDataPacks%2FMinecraftLootRandomizer.zip&v=3JEXAZOrykQ&event=video_description&redir_token=68Tu3k2uCG3jhQftUuV5ANeZnQp8MTU2OTE4NzgyOUAxNTY5MTAxNDI5) and watch his showcase video [here](https://www.youtube.com/watch?v=3JEXAZOrykQ).
