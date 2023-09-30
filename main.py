import functions

# Update this directory as per the location of your dataset folder
input_dir = 'dataset/data'
#output_dir = 'output/ttd'
#locales = ['en-US', 'sw-KE', 'de-DE']
#partitions = ['test', 'train', 'dev']

#generatecreate a file that contains the english translation of the language
#generate a en-xx.xlxs file for all the languages.
generate_excel_files=functions.create_excel_files(input_dir)

#For English (en), Swahili (sw) and German (de), generate separate jsonl files with test, train and dev respectively.
separate_files=functions.generate_partitioned_jsonl(input_dir)

#Generate one large json file showing all the translations from en to xx with id and utt for all the train sets.
train_translations=functions.generate_combined_json(input_dir)

