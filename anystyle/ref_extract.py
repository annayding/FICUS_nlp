import os

folder_title = "REFERENCES_FOLDER"

dir = os.path.dirname(os.path.realpath(__file__))
dir = dir + folder_title
report_dir = dir + "/OCR_pdfs/"
ref_dir = dir + "/Refs_Unedited/"
ref_edited_dir = dir + "/Refs_Edited/"
parsed_dir = dir + "/Parsed/"

# make sure the file neames are correct
# for report in os.listdir(report_dir):
#     os.rename(report_dir + report, report_dir + report.replace(" ", "_"))

# for report in os.listdir(report_dir):
#     print(report)
#     os.system("anystyle -f ref find --no-layout " + report_dir + report + " " + ref_dir)

# for ref in os.listdir(ref_edited_dir):
#     os.system("anystyle -f xml parse " + ref_edited_dir + ref + " " + parsed_dir )