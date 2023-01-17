import uvicorn


if __name__ == "__main__":
    #uvicorn.run("blog.main:app", reload=True)
    uvicorn.run("blog.main:app")