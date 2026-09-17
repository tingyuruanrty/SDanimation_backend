# SDanimation_backend

fastapi(web framework) 
uvicorn(server engine)
Sqlalchemy(sql library)
httpx(send http request)
python-multipart(parse the http request body as FormData object)
comfy-sdk

source venv/Scripts/activate
uvicorn main:app --reload

# todo:
fix the download button
data base(use sqllite now, better use postgreSQL)
replace the character name achronym in the character select modal with character preview picture
docker(modern production environments)
infrastructure(AWS/GCP)
modern front end framework?
user experience enhaunce, it could take more then five minutes for a generation work to finish, it would me nice if there's a anxious reliver


# current exist problem:
comfy cloud api don't take lora as standard upload file(?)
i need a data base, to keep track of the trigger word for each lora
i want a user system, keep track of generation history for each user

# lora library
https://civitai.com/models/1161646/priestess-arknights?modelVersionId=1306676
https://civitai.com/models/923364/lappland-the-decadenza-arknights-noobai?modelVersionId=1033563
https://civitai.com/models/585582/skadi-the-corrupting-heart-arknightsoror-3-outfits?modelVersionId=1394408
https://civitai.com/models/1178340/ascalon-arknights?modelVersionId=1325959
https://civitai.com/models/1179533/laqeramalinearknights?modelVersionId=1327350
https://civitai.com/models/1160846/shu-4-outfitsarknights?modelVersionId=1358524
https://civitai.com/models/1209557/jessica-the-liberated-arknights?modelVersionId=1362286
https://civitai.com/models/1169131/horn-2-outfitsarknights
https://civitai.com/models/1236201/nian-5-outfits-arknights?modelVersionId=1393158
https://civitai.com/models/1201762/saria-3-outfits-arknights?modelVersionId=1353208
https://civitai.com/models/1200892/gummy-2-outfits-arknights?modelVersionId=1352221
https://civitai.com/models/1153182/amiya-for-medic-arknights
https://civitai.com/models/1236181/ling-3-outfits-arknights?modelVersionId=1393135
https://civitai.com/models/1153354/amiya-for-defaultarknights
https://civitai.com/models/1153067/theresa-arknights?modelVersionId=2048873
https://civitai.com/models/1154012/kaltsit-or-or-5-outfits-arknights
https://civitai.com/models/1155909/vulpisfoglia-2-outfitsarknights
https://civitai.com/models/1229040/ines-5-outfits-arknights?modelVersionId=1384866
https://civitai.com/models/1212225/bagpipe-3-outfits-arknights?modelVersionId=1365430
https://civitai.com/models/1183228/wisadelarknights?modelVersionId=1331682
https://civitai.red/models/1239093/kroos-the-keen-glintarknights