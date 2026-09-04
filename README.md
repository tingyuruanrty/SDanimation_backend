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
need to save the character reference picture and motion reference gif/video on the disk, i'm thinking achieve it use some data base
need to alter node 3, 22, 57, 12, 60 based on the five parameter that's been took apart from the request body(paused)

# current exist problem:
comfy cloud api don't take lora as standard upload file(?)