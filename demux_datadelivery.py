import os, sys, re

'''
    AUTHOR:    Shwetha Hara Sridhar, Ying Chih Wang
    VERSION:   19.07.19

    ICAHN SCHOOL OF MEDICINE AT MOUNT SINAI

    Department of Genetics and Genomic Sciences (DevTech)
'''

def remove_fastqdirs(numb_path):

    # Input:
    #        Takes the path to the numbered fastq directories created after demux
    # Method:
    #        Moves the fastq files from their respective numbered directories into the outer parent directory
    #        Deletes the older numbered directories
    #        Returns the outer directory path which contains the fastq files

    os.chdir(numb_path)
    # setting working directory to the path to numbered directories with fastq files
    list_num_dir = os.listdir(numb_path)
    # lists out the files in the current directory assigns it to "list_num_dir" variable

    fastq_dirs = {}
    # empty dictionary to keep note of which numbered directory has which fastq files

    # Now, we use module "os' to list the fastq files and save them as values to fastq_dirs dictionary
    # The try block used below gives us information on if there were fastq files found or not.
    # It also prints the directory/folder in which the fastq file was found or not.

    for subdir in list_num_dir:
        try:
            fastq_dirs[subdir] = os.listdir(subdir)
        except OSError:
            print("No Fastqs found in ")
        else:
            print("FASTQ Files Found in!\n", str(subdir))
            for reads in fastq_dirs[subdir]:
                try:
                    os.rename(numb_path + "/" + subdir + "/" + reads, numb_path + "/" + reads)
                except OSError:
                    print("Failed" % reads)
                else:
                    print("FASTQ Files moved!")

            os.removedirs(numb_path + "/" + subdir)

    # Using the fastq_dirs dictionary to fetch the fastq files and move them to the parent directory
    # Removes the empty directories, in this case, the numbered directories which had the fastq files before moving
    # Finally, returns the path to where the fastq files are accumulated

    return


def rename_fastqs(path, samplesheet):

    present_names = os.listdir(path)
    sample_sheet = open(samplesheet, "r")
    sample_sheet = sample_sheet.readlines()[14:]
    header = sample_sheet[0].split(",")
    parsed_info = {}
    new_names = {}

    for line in sample_sheet[1:]:

        line = line.split(",")

        for idx, col_names in enumerate(header):

            sample_idx = 0

            if col_names == "Lane":

                lane = line[idx]

                while len(idx) > 3:
                    lane = "0"+line[idx]

                if col_names == "Sample_ID":
                    sample_idx = idx
                    parsed_info["S"+line[sample_idx]+"_L"+lane] = ""

                elif col_names == 'I7_Index_ID':
                    parsed_info["S"+line[sample_idx]+"_L"+lane] += line[idx+1]

                elif col_names == 'I5_Index_ID':

                    if line[sample_idx] != "":
                        parsed_info["S"+line[sample_idx]+"_L"+lane] += "_"+line[idx+1]
                    else:
                        pass

                else:
                    pass

            else:

                if col_names == "Sample_ID":
                    sample_idx = idx
                    parsed_info["S"+line[sample_idx]] = ""

                elif col_names == 'I7_Index_ID':
                    parsed_info["S"+line[sample_idx]] += line[idx+1]

                elif col_names == 'I5_Index_ID':

                    if line[sample_idx] != "":
                        parsed_info["S"+line[sample_idx]] += "_"+line[idx+1]
                    else:
                        pass

                else:
                    pass

    for k, v in parsed_info.items():

        for names in present_names:

            if k in names:
                new_names[names] = v.join(names.split(k))

            else:
                pass

    return new_names


def rename_move(fastq_path, dict_newname):
    # Input:
    #       The path to fastq files after running remove_fastqdirs() method
    #       newname_dict after running indices_from_samplesheet() method
    #
    # Method:
    #       Uses regular expressions to fetch sample names from fastq file name.
    #       renames the fastq files with the indices compilation from dict_newname. makes a new dict called new_paths,
    #       which uses sample names (new_dir_names) as keys and a tuple of the fastq file's old name and the new name
    #       as the values.

    os.chdir(fastq_path)
    file_name = os.listdir(fastq_path)
    for files in file_name:
        if files.endswith(".fastq.gz"):
            found = files.split("_S")[0]

            # Makes new directories with sample name as their names.
            # moves the fastq files into their respective sample names.

            try:
                os.mkdir(found)
                os.rename(fastq_path + "/" + files, fastq_path + "/" + found + "/" + dict_newname[files])
                print("\nmoved:", fastq_path + "/" + files, "\nto:", fastq_path + "/" + found + "/" + dict_newname[files])
            except:
                os.rename(fastq_path + "/" + files, fastq_path + "/" + found + "/" + dict_newname[files])
                print("\nmoved:", fastq_path + "/" + files, "\nto:", fastq_path + "/" + found + "/" + dict_newname[files])

    return print("Done!")


if __name__ == "__main__":
    sample_sheet = str(sys.argv[1])
    src_path = str(sys.argv[2])

    # running two methods within one method:
    # remove fastqs to move fastqs into the parent directory
    # Indices from samplesheet for index information
    # Finally, runs the output of the above two methods into rename_move method
    # to move the fastqs into their respective sample names after renaming them

    remove_fastqdirs(src_path)
    print("removed fastqs")
    dict_deets = rename_fastqs(src_path, sample_sheet)
    print("Found fastqs, renaming them!")
    rename_move(src_path, dict_deets)


