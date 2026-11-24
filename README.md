# Gazai's Cobblemon Utility+ Resource Pack

Resource pack that retextures and renames the items from the
**[Cobblemon Utility+](https://modrinth.com/mod/cobblemon-utility+)** mod
(modid `cobblemon_utility`) — MC 1.21.1. Requires the mod.

## What it changes

Version 2.0.0 follows the new names and sprites of Cobblemon Utility Items:

- **Mystery Candy** (Wooden Candy), **Moldy Nutrient** (Void Vial), **Outdated Rare Candy** (Common Candy), **Moldy Poke Snack** (Stale Poke Snack).
- **Apricorn Energy Drink** and **Outdated Apricorn Energy Drink** (Apricorn Energy Max and Min), **Master Aprijuice** (Golden Aprijuice).
- **Moldy** stat candies (Obsidian candies) and **Rotten** stat candies (Void candies).
- A new **Ball Synchronizer** sprite.

The other items keep their stat candy, Shiny Powder, Transmutation Orb, Master Candy and Devolution Wand looks.

Languages: English, French, Spanish, German, Italian.

## Structure
- `assets/cobblemon_utility/textures/item/*.png` — item textures (16×16).
- `assets/cobblemon_utility/lang/*.json` — item display names per language.
- `pack.mcmeta` — pack_format 34 (MC 1.21.1).
- `pack.png` — pack icon.

## Usage
Drop the folder (or a zip of it) into `.minecraft/resourcepacks/` and enable it in
Video Settings → Resource Packs, above other packs so its textures win.

## Releasing
Push a tag `vX.Y.Z` — the CI (`.github/workflows/release.yml`) zips the pack and
publishes it to Modrinth (and CurseForge if `CURSEFORGE_ID` / `CURSEFORGE_TOKEN` are set).
