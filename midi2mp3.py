import os 
import music_generator as musicGen
import configuration as config




def make_mp3():
    mp3_path = os.path.join(config.midi_save_folder, config.generated_mp3_music_name + ".mp3")
    os.system("timidity {} -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k {}".format(musicGen.get_music_to_return(), mp3_path))
    return mp3_path