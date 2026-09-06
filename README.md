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
data base
need to alter node 3, 22, 57, 12, 60 based on the five parameter that's been took apart from the request body(paused)
manage the asynchronize keyword to inplement concurrency

# current exist problem:
comfy cloud api don't take lora as standard upload file(?)
i need a data base, to keep track of the trigger word for each lora
i want a user system, keep track of generation history for each user