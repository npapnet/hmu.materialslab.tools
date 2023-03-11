Welcome to the tension test with imada


# Workflow

1. Crop images
2. Create the "meta-info.txt" file
3. DIC Process 
4. extract the data from the "result.dic" file
5. merge DIC and Testing Machine data. 


## additional 

to prepare a video from the sequences it is possible to use Openshot. 
- import file into the project (as an image sequence)
- add the image sequence onto a track
- Export the video. 


```mermaid
---
title: Current DIC Analysis procedure
---
flowchart TD 
    camImages[("Labview Output<br> Camera Images")]
    resultDIC[("result.dic")]
    LABVIEW_OUTPUT[("Labview Output<br> _image_times.txt")]
    meta_file[("_meta-data.txt")]
    INFILE_DIC[("myexcel.xlsx")]
    UTFILE[("IMADA.csv")]
    RESULT_XLSX_FNAME[("total_data.xlsx")]

    DICAnalysis --> Part1
    Part1 -->Part2


    LABVIEW_OUTPUT --> convert_to_meta -->meta_file
    camImages --> pydic.init
    pydic.init --> resultDIC
    resultDIC --> pydic.read_dic_file 
    meta_file-->df_img_meta

    df_dic_tot-->INFILE_DIC
    INFILE_DIC-->df_dico
    UTFILE -->read_imada_csv

    df_fin --> RESULT_XLSX_FNAME
    subgraph DICAnalysis ["main_imada.py"]
        pydic.init 
        convert_to_meta["Convert to Meta"]
    end

    subgraph Part1 ["post_1_obtain_dic_strain.py"]
        pydic.read_dic_file -->gridlist
        gridlist[("grid_listres")] --> obtainStrainCurve-->df_dic[("df_dic")] -->df_dic_tot[("df_dic_tot")]
        df_img_meta[("df_img_meta")] -->df_dic_tot
    end


    subgraph Part2 ["post_2_merge_dic_ut.py"]
        read_imada_csv["read_imada_csv()"] -->df_decimated[("df_decimated")]
        df_dico[("df_dico")]
        df_dico --> plotsyncedgraph["plot_synced_graph()<br>sync time vectors"]
        df_decimated --> plotsyncedgraph
        plotsyncedgraph --> df_dicrs[("DIC df with common time")]
        plotsyncedgraph --> df_utrs[("Imada df with common time")]
        df_dicrs-->df_fin[("DIC and UT <br> merged df <br> with common time")]
        df_utrs-->df_fin
    end

``` 