# SDanimation_backend

fastapi(web framework) 
uvicorn(server engine)
Sqlalchemy(sql library)
httpx(send http request)
python-multipart(parse the http request body as FormData object)
comfy-sdk

source venv/Scripts/activate
uvicorn main:app --reload

# aws structure
i can recall i upload the docker image to ECR, and define task in the ECS, make service(task manager) with the task defination, and ALB so that i don't have to connect to the task with the public id; but the dns(i don't know what is dns) of ALB is under http protolcal, which make image generation failed, (the query to RDS somehow works, i don't know why, i can't make it to this far with our this work), you provided some instruction on cloud front or something, i don't really recall, we managed to get a https url map to that http alb dns, which make the things works(solved mixed content error?), the last problem we encounter is that generation take some time, around 2 minutes, and both alb dns and cloud front url consider the connection failed after 1 minutes, we made a quick fix extend that time to 2 minutes, which isn't the best practice, you say the best practice is return a header and have a polling? i haven't start implement that part yet 

# todo:
the data base is on my laptop rightnow right now, even the container can't transplant that, i haven't figure out how to solve it yet
my api key is exposed to public, it's like wearing no pants while walking on the street, i'm fond of it
update API_BASE_URL after host the backend on the aws
data base(use sqllite now, better use postgreSQL)
replace the character name achronym in the character select modal with character preview picture
docker(modern production environments)
infrastructure(AWS/GCP)
modern front end framework?
user experience enhaunce, it could take more then five minutes for a generation work to finish, it would me nice if there's a anxious reliver
should clean up the inputs directory and outputs directory every a few days


# current exist problem:
i need to implement the asynchronized job and polling
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