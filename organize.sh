#!/bin/bash

# "ISC License"
# 
# "Copyright (c) 2021 Serafeim Karaiskos"
# 
# "Permission to use, copy, modify, and/or distribute this software for any"
# "purpose with or without fee is hereby granted, provided that the above"
# "copyright notice and this permission notice appear in all copies."
# 
# "THE SOFTWARE IS PROVIDED \"AS IS\" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH"
# "REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY"
# "AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,"
# "INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM"
# "LOSS OF USE, DATA OR  To refere to help.PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR"
# "OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR"
# "PERFORMANCE OF THIS SOFTWARE."
# 
#  ##  ##  ##
#
# A helping script to download and organize in an convinient way the lobbard grid corpuse
# Video files with isues
# silent:
#  s28_l_gik8a_WRONG_#sil.mov
#  s27_l_bah2s_WRONG_#sil.mov
# corrupted:
#  s32_l_pwip9p.mov
#  s32_p_bwwj2n.mov
#  s33_l_pwajza.mov
#  s33_p_sgwq2s.mov
# 
# audio duration seconds max: 4.08, min: 1.41
# video frames           max: 100 , min: 35
# 
#  ##  ##  ##

###################
# Help            #
###################
Help()
{
   # Display Help
   echo "Download & Organize the lombard grid corpus as:"
   echo
   echo "lombardgrid"
   echo "├── audio"
   echo "│   ├── s10"
   echo "│   │   ├── s10_l_bbat9p.wav"
   echo "│   │   ├── s10_l_bbay5n.wav"
   echo "│   │   ..."
   echo "│   ├── s11"
   echo "│   │   ├── s11_l_bbab2n.wav"
   echo "│   │   ├── s11_l_bbbg8p.wav"
   echo "│   │   ..."
   echo "│   ..."
   echo "|"
   echo "└── front"
   echo "    ├── s10"
   echo "    │   ├── s10_l_bbat9p.mov"
   echo "    │   ├── s10_l_bbay5n.mov"
   echo "    │   ..."
   echo "    ├── s11"
   echo "    │   ├── s11_l_bbab2n.mov"
   echo "    │   ├── s11_l_bbbg8p.mov"
   echo "    │   ..."
   echo "    ..."
   echo
   echo "If download (-D) option is not active make sure to extract"
   echo "the audio and the front zip files to the specified directory"
   echo "using the -d option if nessesary."
   echo
   echo "If a sentence is spoken incorrectly then the filename will"
   echo "be \"_WRONG.wav\" e.g. s8_2_38_8_r_lrwizp_WRONG_lrbizp.wav"
   echo "There is the option to rename the file to the spoken sentence,"
   echo "delete them, or (default) do nothing\keep."
   echo
   echo "Syntax: organize.sh [-h|D|q|i|R|r] [-d DIR]"
   echo "options:"
   echo "h     Print this Help."
   echo "d     Set directory, default to current directory."
   echo "D     Download lombard grid corpus dataset."
   echo "q     Quiet mode."
   echo "R     Incorrectly spoken sentences are removed/deleted."
   echo "r     Incorrectly spoken sentences are renamed."
   echo "i     Print the ISC License notification."
   echo
   echo "If -d is set then user asked to create a soft link is created."
   echo "Do not use both R and r options at the same time"
   echo
}


###################
# License         #
###################
License()
{
   echo "ISC License"
   echo 
   echo "Copyright (c) 2021 Serafeim Karaiskos"
   echo 
   echo "Permission to use, copy, modify, and/or distribute this software for any"
   echo "purpose with or without fee is hereby granted, provided that the above"
   echo "copyright notice and this permission notice appear in all copies."
   echo 
   echo "THE SOFTWARE IS PROVIDED \"AS IS\" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH"
   echo "REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY"
   echo "AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,"
   echo "INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM"
   echo "LOSS OF USE, DATA OR  To refere to help.PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR"
   echo "OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR"
   echo "PERFORMANCE OF THIS SOFTWARE."
   echo 
}


###################
# Download        #
###################
Download()
{  
   # download,unpack, and delete .zip files
   [ $_Q -eq 0 ] && echo "Download dataset."   
   url='https://zenodo.org/record/3736465/files/lombardgrid_front.zip'
   if [ $_Q -eq 0 ]
   then
      wget $url
      unzip ${url##*/} #removes everything up to last '/' (including '/'), or "lombardgrid_front.zip"
   else
      wget -nv $url
      unzip -q ${url##*/}
   fi
   
   local url='https://zenodo.org/record/3736465/files/lombardgrid_audio.zip'
   if [ $_Q -eq 0 ]
   then
      wget $url
      unzip ${url##*/}  
   else
      wget -nv $url
      unzip -q ${url##*/} 
   fi
   
   if [ $_Q -eq 0 ]
   then
      rm -v *.zip
   else
      rm *.zip
   fi
}


###################
# Rename          #
###################
Rename()
{  
   # file is to be renamed
   local newname=${file%_WRONG*} # chop everything after _WRONG with it included
   newname=${newname%_*}         # chop the intented sentence
   newname+="_${file##*_}"        # concat the spoken sentence

   [ $_Q -eq 0 ] && mv -v "${file}" "${newname}" || mv "${file}" "${newname}"
   file=$newname
}


###################
# Move file       #
###################
Move_file()
{
   # move file to the corespoding folder
   local speaker=$(cut -d'_' -f1<<<${file})
   # make apropriate folder if not exist
   if [ ! -d "./${speaker}" ] 
   then
      [ $_Q -eq 0 ] && mkdir -v ${speaker} || mkdir ${speaker}
   fi
   [ $_Q -eq 0 ] && mv -v "${file}" "${speaker}" || mv "${file}" "${speaker}"
}


###################
###################
# Main program    #
###################
###################

_Q=0
_DL=0
_DIR=$(pwd)
_RDIR=$(pwd)
_ACT=0
# Get the options
while getopts ":hDrRqid:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      q) # activate verbose
         _Q=1;;
      d) # change directory
         _DIR=$OPTARG
         if [ ! -d "${_DIR}" ] 
         then
            echo "Directory does not exist."
            exit
         fi
         cd "${_DIR}"
         _DIR=$(pwd);;

      D) # enable to download
         _DL=1;;
      R) # Remove incorrectly spoken sentence
         _ACT=1;;
      r) # rename incorrectly spoken sentence
         _ACT=2;;
      i) # print license notification
         License
         exit;;
     \?) # Invalid option
         echo "Error: Invalid option."
         echo "To refere to help run \"source ${0} -h\""
         exit;;
   esac
done


# download if -D is set
[ $_DL -eq 1 ] && Download # Download and unpack the lombard grid corpus

[ $_Q -eq 0 ] && echo "Organize files to speaker directories."

cd lombardgrid/front
for file in *.mov; do
   #[ -f "$fname" ] || continue
   if [ ! -f "$file" ]
   then
      echo "No .mov files in directory $(pwd)/"
      continue
   fi
   # do the specified action to the _WRONG labeled files
   if [ $file = *"_WRONG"* ]
   then
      if [ $_ACT -eq 1 ] # file is to be removed
      then
         [ $_Q -eq 0 ] && rm -v ${file} || rm ${file}
         # file is removed so go to next file
         continue
      fi
      [ $_ACT -eq 2 ] && Rename
   fi
   # move file to coresponting folder 
   Move_file
done

cd ../audio
for file in *.wav; do
   if [ ! -f "$file" ]
   then
      echo "No .wav files in directory $(pwd)/"
      continue
   fi
   # do the specified action to the _WRONG labeled files
   if [ $file = *"_WRONG"* ]
   then
      if [ $_ACT -eq 1 ] # file is to be removed
      then
         [ $_Q -eq 0 ] && rm -v ${file} || rm ${file}
         # file is removed so go to next file
         continue
      fi
      [ $_ACT -eq 2 ] && Rename
   fi
   # move file to coresponting folder 
   Move_file
done

while [ $_ACT -ne 0 ]
do
   read -p "Do you wish to create a soft link?[y/n]" yn
   case $yn in
      [Yy]* ) 
         cd ${_RDIR}
         ln -s ${_DIR}/lombardgrid/  
         
         break;;
      [Nn]* ) 
         break;;
      *) 
         echo "Please answer yes or no.";;
    esac
done
