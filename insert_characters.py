from database import SessionLocal, Character, engine, Base

# Ensures tables are created if you haven't run your app yet
Base.metadata.create_all(bind=engine)

# Data from your spreadsheet
character_data = [
    {
        "name": "Priestess",
        "trigger_word": "priestess_\\(arknights\\),grey eyes , diamond-shaped_pupils , (white or purple) pupils, brown hair ,long hair, black hairband,bowtie,turtleneck sweater ,long sleeves ,(lab coat:0.9),open clothes,white_capelet,id card,belt,skirt ,pantyhose ,high heels ,",
        "lora_filename": "Robertlu1021_priestess_arknights_v2.0-000010.safetensors",
    },
    {
        "name": "Theresa",
        "trigger_word": "theresa_\\(arknights\\),pink eyes , pink hair, horns , long hair,turtleneck , cleavage cutout , white dress, two-tone dress,torn clothes, long sleeves ,torn sleeves , multiple rings,jewelry, single_pauldron,",
        "lora_filename": "Robertlu1021_theresa_arknights_v3.1-000010.safetensors",
    },
    {
        "name": "Amiya, for Demon King",
        "trigger_word": "amiya_\\(demon_king\\) ,blue_eyes, brown hair, rabbit ears, floating crown,hair_over_one_eye, one_eye_covered, see-through veil, black_bridal_veil, white dress, oripathy lesion (arknights) , torn cloak, single glove, turtleneck, short sleeves, spikes, barefoot, black_cracked_egg, holding, ",
        "lora_filename": "Robertlu1021_amiya_demon_king_v3.3-000012.safetensors",
    },
    {
        "name": "laqeramaline",
        "trigger_word": "laqeramaline_\\(arknights\\) ,red eyes, pointy ears , grey hair, horns,black dress , bridal gauntlets ,bodystocking ,long dress, high_heels,(see-through veil:1.2),",
        "lora_filename": "laqeramaline_arknights_for_IL-000012.safetensors",
    },
    {
        "name": "Jessica the liberated",
        "trigger_word": "jessica_the_liberated_\\(arknights\\),blue hair,green eyes, ponytail,multicolored hair ,streaked hair, headset , high ponytail ,short shorts ,black jacket, black thighhighs, black shirt, id card , black choker,knee pads ,holding gun , rifle , jessica shield, holding shield, ",
        "lora_filename": "jessica_the_liberated_arknights_for_IL.safetensors",
    },
    {
        "name": "Saria",
        "trigger_word": "saria_\\(stronghold\\)_\\(arknights\\),grey hair, dragon horns, orange eyes , dragon tail , black short shirt , black thighhighs , bandaged arm ,single glove,cross earrings ,sleeveless shirt,knee_boots,holding shield, ",
        "lora_filename": "saria_arknights_for_IL.safetensors",
    },
    {
        "name": "Irene",
        "trigger_word": "irene_\\(arknights\\) ,grey eyes,grey hair,head wings ,scar across eye ,long hair,short_bangs, black gloves,earrings ,seamed pantyhose, black jacket, puffy long sleeves, white capelet , ammunition belt, ankle boots ,",
        "lora_filename": "Robertlu1021_irene_arknights_v3.1-000012.safetensors",
    },
]

def seed_database():
    db = SessionLocal()
    try:
        # Check if records already exist to avoid duplicate entries
        existing_count = db.query(Character).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} characters. Skipping insertion.")
            return

        # Turn each dictionary into a Character model instance
        character_objects = [Character(**item) for item in character_data]

        # Stage and save to the database
        db.add_all(character_objects)
        db.commit()
        print(f"Successfully inserted {len(character_objects)} characters!")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()