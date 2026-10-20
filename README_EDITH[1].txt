FANTASY REALMS RPG — BLADE OF THE BROKEN HORIZON

CONTENTS
- Blade_of_the_Broken_Horizon.bbmodel: editable Blockbench project (starter geometry).
- blade_of_broken_horizon_texture.png: 64x64 pixel-art texture.
- blade_of_broken_horizon_item_model_template.json: display/texture template for a Java item model, NOT a complete custom 3D geometry export.

IMPORTANT STATUS
This package was generated programmatically as a starter asset. It has not been opened in Blockbench, exported by Blockbench, or tested in Minecraft/Forge. Edith must validate the .bbmodel in Blockbench and adjust face UVs if needed. The current geometry is a simple cuboid-based stylized sword; it is not yet a production-ready animated model.

BLOCKBENCH
1. Open Blockbench.
2. File > Open Model and select Blade_of_the_Broken_Horizon.bbmodel.
3. Check the sword silhouette, texture and UV mapping. If any face looks wrong, adjust UVs and save.
4. For a vanilla Java item model, use the Java Block/Item format and export the model as JSON if the chosen Blockbench format supports the intended item geometry. Otherwise rebuild/export the item model using the Minecraft Java item workflow.
5. Copy the PNG into src/main/resources/assets/fantasyrealms/textures/item/blade_of_broken_horizon.png.
6. Put the final exported JSON in the resource location expected by the item registration, normally assets/fantasyrealms/models/item/blade_of_broken_horizon.json.
7. Register the item in Fantasy Core and point its item properties/model to fantasyrealms:item/blade_of_broken_horizon.
8. Run the Forge client and verify inventory, GUI, first-person and third-person rendering.

FOR EDITH — INTEGRATION TASKS
- Inspect the existing Forge 1.20.1 project and its mod id; do not assume it is fantasyrealms if the actual mod id differs.
- Validate the .bbmodel by opening it in Blockbench.
- Fix geometry and UV mapping, then export the correct Minecraft Java item model.
- Ensure the exported model references the texture path and namespace actually used by the mod.
- Register the item with the project's DeferredRegister<Item> pattern (or its existing registration architecture).
- Add a translation key and display name “Blade of the Broken Horizon”.
- Test client rendering and compilation; report exact tests run and errors.
- Optional: implement a special parry-charge ability in Java separately. The model/texture does not implement gameplay mechanics.

DESIGN INTENT
Dark steel, cyan arcane rune, silver crossguard, dark grip and a cyan pommel crystal.
