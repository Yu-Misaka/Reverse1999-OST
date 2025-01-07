from funasr import AutoModel
import os
# paraformer-zh is a multi-functional asr model
# use vad, punc, spk or not as you need
model = AutoModel(model="Whisper-large-v3-turbo",  
                  # vad_model="fsmn-vad", 
                  # vad_kwargs={"max_single_segment_time": 60000},
                  # punc_model="ct-punc", 
                  # spk_model="cam++",
                  ncpu = 12
                  )

res_list = []
wav_file_folder = "/root/autodl-tmp/Reverse1999-OST/Selection/3023/"
wav_file_list = os.listdir(wav_file_folder)
for wav_file in wav_file_list:
    wav_file_path = os.path.join(wav_file_folder, wav_file)
    if os.path.splitext(wav_file_path)[1] == ".wav":
        res = model.generate(input=wav_file_path, batch_size_s=300, batch_size_threshold_s=60)
        res_list.append(res[0])
        # res_list.append(wav_file_path)

train_path = ".\\training_set\\"

with open("ASR.txt", "w") as file:
    for line in res_list:
        file.write(train_path + line["key"] + ".wav" + "|Sonetto|en|" + line["text"] + '\n')